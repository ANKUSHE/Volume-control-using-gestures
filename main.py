# from unittest import result
import cv2 
import mediapipe as mp
import math
import numpy as np
from sklearn import utils

mphands = mp.solutions.hands
hands = mphands.Hands()
mpDraw = mp.solutions.drawing_utils
lmlist = []



from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volumeRANGE = volume.GetVolumeRange()
print(volumeRANGE)
minVol = volumeRANGE[0]
maxVol = volumeRANGE[1]
volume.SetMasterVolumeLevel(-65.25, None)


camera = cv2.VideoCapture(0)

while True:
    ret, img = camera.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:

            for id, lm in enumerate(handlms.landmark):
                # print(id, lm)
                h,w,c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id,cx,cy)

                if id == 4:
                    x1, y1 = cx,cy
                    cv2.circle(img,(x1,y1),15,[255,0,0],cv2.FILLED)
                    
                    
                if id == 8:
                    x2, y2 = cx,cy
                    cv2.circle(img,(x2,y2),15,[255,0,0],cv2.FILLED)

            distance  = math.hypot(x2-x1,y2-y1)
            print(distance)
            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),3)
            vol = np.interp(distance, [10,250] ,[minVol,maxVol])
            per = np.interp(distance, [10,250],[0,100])
            print(per)

            volume.SetMasterVolumeLevel(vol,None)



                
                    


            mpDraw.draw_landmarks(img, handlms, mphands.HAND_CONNECTIONS)

    # print(result)

    cv2.imshow("Camera",img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()
camera.release()