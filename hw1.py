# Visual Interfaces Spring 2015 Assignment 1
# Roberto Amorim - rja2139

import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)
counter = 10
while( cap.isOpened() ) :
    ret,img = cap.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    ret,thresh1 = cv2.threshold(blur,127,255,0)

    contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    drawing = np.zeros(img.shape,np.uint8)
    counter = counter + 1
    cv2.putText(drawing,str(counter/10),(15,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(0,255,0))
    if counter == 100: counter = 10

    max_area=0
    for i in range(len(contours)):
        cnt=contours[i]
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            ci = i
    cnt = contours[ci]
    hull = cv2.convexHull(cnt)

    # Detecting the gravity center of the contour
    moments = cv2.moments(cnt)
    if moments['m00']!=0:
        cx = int(moments['m10']/moments['m00']) # cx = M10/M00
        cy = int(moments['m01']/moments['m00']) # cy = M01/M00

    centr=(cx,cy)
    cv2.circle(img,centr,5,[0,0,255],2)
    cv2.drawContours(drawing,[cnt],0,(0,255,0),2)
    cv2.drawContours(drawing,[hull],0,(0,0,255),2)

    cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    hull = cv2.convexHull(cnt,returnPoints = False)

    if True:
        defects = cv2.convexityDefects(cnt,hull)
        try:
            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                dist = cv2.pointPolygonTest(cnt, centr, True)
                # Here drawing the lines of the contour
                cv2.line(drawing,start,end,[0,255,0],2)
                # And here drawing the convexity defects
                cv2.circle(drawing,far,5,[0,0,255],-1)
            print(i)
            i=0
        except AttributeError:
            print "No shape detected"

    cv2.imshow('output',drawing)
    cv2.imshow('input',img)

    k = cv2.waitKey(10)
    if k == 27:
        break