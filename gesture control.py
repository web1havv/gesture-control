import cv2
import mediapipe as mp
import time
import math
import numpy as np
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
print("You have to enter the value of x as 8 to start")
ptime=0
import handtrackingmodule as htm
tracker=htm.handTracker()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()

minVol=volRange[0]
maxVol=volRange[1]







cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    img=tracker.handsFinder(img)
    lmlist=tracker.positionFinder(img)
    if len(lmlist)!=0:

        #print(lmlist[4],lmlist[8])
        x1,y1=lmlist[4][1],lmlist[4][2]
        x2,y2=lmlist[8][1],lmlist[8][2]
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255, 0, 255),3)
        cx,cy=(x1+x2)//2,(y1+y2)//2
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        length=math.hypot(x2-x1,y2-y1)
        if length<=30:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
        #length from 30 to 200
        # vol range from -65 to zero
        vol=np.interp(length,[20,260],[minVol,maxVol])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)



    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    cv2.putText(img, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255, 0, 255), 3)
    cv2.imshow("Image", img)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break