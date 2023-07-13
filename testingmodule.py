import cv2
import mediapipe as mp
import handtrackingmodule as htm



cap = cv2.VideoCapture(0)
tracker = htm.handTracker()

while True:
        success, image = cap.read()
        image = tracker.handsFinder(image)
        lmList = tracker.positionFinder(image)
        if len(lmList) != 0:
            print(lmList[12])  # Print the position of the middle finger

        cv2.imshow("Video", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break