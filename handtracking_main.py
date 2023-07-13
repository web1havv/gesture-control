import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

if not cap.isOpened():
    print("Failed to open the webcam.")
    exit(1)

ptime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            for id,lm in enumerate(handLms.landmark):
                #print(id,lm)
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                print(id,cx,cy)
                if id==0:
                    cv2.circle(img,(cx,cy),15,(45, 255, 255),cv2.FILLED)

    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    cv2.putText(img, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255, 0, 255), 3)
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
