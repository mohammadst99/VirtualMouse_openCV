import time
import cv2 as cv
import numpy as np
import mediapipe as mp
import math


class HandDetector :
    def __init__(self ,mode=False , maxHand=2 , detectCon=0.5 ,trackCon=0.5):
        self.mode = mode
        self.maxHand = maxHand
        self.detectCon = detectCon
        self.trackCon = trackCon

        #############################
        self.mpHand = mp.solutions.hands
        self.Hands = self.mpHand.Hands(self.mode,self.maxHand,1,self.detectCon,self.trackCon)  # it has detection mode and Tracking mode when we dont have any thing to trackn in goes to detection mode
                                                                                             # Hands = mpHand.Hands(False,2,min_tracking_confidence=0.5) it can be like that but these are already set as defult so we can leave them
                                                                                             # please note thet this library (hand) just take RGB img
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        #############################


    def findhands(self, img, draw = True):
        imgRGB = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.processHand = self.Hands.process(imgRGB)
        # print(processHand.multi_hand_landmarks)
        if self.processHand.multi_hand_landmarks:  # you can use processHand.multi_hand_landmarks[0] or [1] this hand.no
            for handLMS in self.processHand.multi_hand_landmarks:
                if draw :
                    self.mpDraw.draw_landmarks(img, handLMS, self.mpHand.HAND_CONNECTIONS)

    def findPosition(self ,img ,handsNo=0 ):
        self.lmlist=[]
        xList=[]
        ylist=[]
        bbox=[]
        if self.processHand.multi_hand_landmarks:  # you can use processHand.multi_hand_landmarks[0] or [1] this hand.no
            try:
                myHand = self.processHand.multi_hand_landmarks[handsNo]
                for id, lm in enumerate(myHand.landmark):
                    # print(id, lm)  # the hands has 21 points [0 to 20] each point indicate some part of hand
                    # the problem is that the lm is in decimal and we need pixel ex:(200 w,300 h)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)  # now we have the (id,cx,cy) so we can do anything
                    self.lmlist.append([id,cx,cy])
                    xList.append(cx)
                    ylist.append(cy)
                xmin,xmax = min(xList),max(xList)
                ymin,ymax = min(ylist),max(ylist)
                bbox=xmin,ymin,xmax,ymax
            except:
                pass

        return self.lmlist,bbox

    def fingersUp(self):
        fingers = []
        # Thumb
        if self.lmlist[self.tipIds[0]][1] > self.lmlist[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):

            if self.lmlist[self.tipIds[id]][2] < self.lmlist[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # totalFingers = fingers.count(1)

        return fingers

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lmlist[p1][1:]
        x2, y2 = self.lmlist[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv.circle(img, (x1, y1), r, (255, 0, 255), cv.FILLED)
            cv.circle(img, (x2, y2), r, (255, 0, 255), cv.FILLED)
            cv.circle(img, (cx, cy), r, (0, 0, 255), cv.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length,[x1, y1, x2, y2, cx, cy]


def main():
    cap = cv.VideoCapture(0)
    detector=HandDetector()
    while True:
        sucess, img = cap.read()
        detector.findhands(img)
        lmLIST,bbox = detector.findPosition(img)

        if len(lmLIST)!=0:
            fingers = detector.fingersUp()
            length,bbox = detector.findDistance(8,12,img)
            print(length)
            print(fingers)

        cv.imshow("result", img)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ =='__main__':
    main()