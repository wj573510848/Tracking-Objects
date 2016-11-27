# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 21:34:52 2016

@author: Administrator
"""
'''
'''
import cv2
import numpy as np

#创建窗口。
frame=np.zeros((800,800,3),np.uint8)
#初始化最初点。
last_measurement=current_measurement=np.array((2,1),np.float32)
last_prediction=current_prediction=np.zeros((2,1),np.float32)
#定义各个参数。
def mousemove(event,x,y,s,p):
    global frame,current_measurement,measurement,last_measurement,current_prediction,last_prediction
    last_prediction=current_prediction
    last_measurement=current_measurement
    current_measurement=np.array([[np.float32(x)],[np.float32(y)]])
    kalman.correct(current_measurement)
    current_prediction=kalman.predict()
    lmx,lmy=last_measurement[0],last_measurement[1]
    cmx,cmy=current_measurement[0],current_measurement[1]
    lpx,lpy=last_prediction[0],last_prediction[1]    
    cpx,cpy=current_prediction[0],current_prediction[1]
    
    cv2.line(frame,(lmx,lmy),(cmx,cmy),(200,0,0))
    cv2.line(frame,(lpx,lpy),(cpx,cpy),(0,100,0))
    print cpx,cpy
    print cmx,cmy

cv2.namedWindow('kalman_tracker')
cv2.setMouseCallback('kalman_tracker',mousemove)
#初始化kalman。
kalman=cv2.KalmanFilter(4,2)
kalman.measurementMatrix=np.array([[1,0,0,0],[0,1,0,0]],np.float32)
kalman.transitionMatrix=np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]],np.float32)
kalman.processNoiseCov=np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],np.float32)

while True:
    cv2.imshow('kalman_tracker',frame)
    if cv2.waitKey(30) & 0xff ==27:
        break
cv2.destroyAllWindows()
