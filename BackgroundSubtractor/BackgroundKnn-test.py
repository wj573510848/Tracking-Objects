# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 20:54:43 2016

@author: Administrator
"""
'''
流程：
1.创建BackgroundSubtractorKNN
2.用前10帧作为背景
3.将BackgroundSubtractorKNN得到的转换为二值图。阈值设置高一点。
腐蚀算法、膨胀算法，使边界更清晰。
4.寻找轮廓并画在每一帧上。
traffic.flv：.\opencv\sources\samples\data
'''
import cv2
import numpy as np
path=r'768x576.avi'
camera=cv2.VideoCapture(path)
history=10
bs=cv2.createBackgroundSubtractorKNN(detectShadows=True) 
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
#调整阈值，使其得到最佳的detect结果。
    th=cv2.threshold(fgmask.copy(),244,255,cv2.THRESH_BINARY)[1]
#调整getStructuringElement（kernel值）。
    th=cv2.erode(th,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)),iterations=2)
    dilated=cv2.dilate(th,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(8,3)),iterations=2)
    image,contours,hier=cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        #调整侦测到的图像大小，过滤掉较小的部分。
        if cv2.contourArea(c)>400:
            (x,y,w,h)=cv2.boundingRect(c)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)
        
    cv2.imshow('mog',fgmask)
    cv2.imshow('thresh',th)
    cv2.imshow('detection',frame)
    if cv2.waitKey(30) & 0xff ==27:
        break

camera.release()
cv2.destroyAllWindows()
