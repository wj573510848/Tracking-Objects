# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 20:54:43 2016

@author: Administrator
"""

import cv2
import numpy as np
path=r'768x576.avi'
camera=cv2.VideoCapture(path)
history=5
bs=cv2.createBackgroundSubtractorMOG2(detectShadows=True) cv2.createB
bs.setHistory(history)
counts=0
while True:
    ret,frame=camera.read()
    if ret is not True:
        break
    fgmask=bs.apply(frame)
    if counts<10:
        counts+=1
        continue
    #th=cv2.threshold(fgmask.copy(),10,255,cv2.THRESH_BINARY)[1]
    #th=cv2.erode(th,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)),iterations=2)
    #dilated=cv2.dilate(th,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,3)),iterations=2)
    image,contours,hier=cv2.findContours(fgmask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if cv2.contourArea(c)>100:
            (x,y,w,h)=cv2.boundingRect(c)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)
        
    cv2.imshow('mog',fgmask)
    #cv2.imshow('thresh',th)
    cv2.imshow('detection',frame)
    if cv2.waitKey(30) & 0xff ==27:
        break

camera.release()
cv2.destroyAllWindows()
