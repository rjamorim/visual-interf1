# Visual Interfaces Spring 2015 Assignment 1
# Roberto Amorim - rja2139

import cv2
import numpy
from copy import copy, deepcopy

counter = 9
seq = 12
pos = 0
k = 0

pattern = [[2, 3],     # 2nd quadrant, five fingers
           [3, 1],     # 3rd quadrant, closed fist
           [4, 2]]     # 4th quadrant, three fingers

cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    ret, thresh1 = cv2.threshold(blur, 127, 255, 0)

    # This method finds the contours in the image being analyzed
    contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    drawing = numpy.zeros(img.shape, numpy.uint8)
    counter += 1
    cv2.putText(drawing, str(counter/10), (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    if counter == 109:
        counter = 9

    # Here I find the max area of the contour
    max_area = 0
    ci = 0
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            ci = i
    try:
        cnt = contours[ci]
    except IndexError:
        print "No contour found!"

    # The max area is used to calculate the hull
    hull = cv2.convexHull(cnt)

    # Detecting the center of the contour
    moments = cv2.moments(cnt)
    if moments['m00'] != 0:
        cx = int(moments['m10']/moments['m00']) # cx = M10/M00
        cy = int(moments['m01']/moments['m00']) # cy = M01/M00
    cv2.putText(drawing, "CoG X:" + str(cx) + " Y:" + str(cy), (15, 445), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    center=(cx, cy)
    cv2.circle(img, center, 5, [0, 0, 255], 2)
    cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 2)
    cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 2)

    cnt = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
    hull = cv2.convexHull(cnt, returnPoints=False)

    defects = cv2.convexityDefects(cnt,hull)
    try:
        for point in range(defects.shape[0]):
            s, e, f, d = defects[point,0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])
            dist = cv2.pointPolygonTest(cnt, center, True)
            # Here drawing the lines of the contour
            cv2.line(drawing, start, end, [0,255,0], 2)
            # And here drawing the convexity defects
            cv2.circle(drawing, far, 5, [0,0,255], -1)

        point += 1
        cv2.putText(drawing, "Points found: " + str(point), (15,465), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

        # Here I'll start working on the password stuff
        # Whenever the display counter reaches 10, the image is analyzed to see if it matches a certain pattern
        # Each pattern is encoded as (x,y), where x is the quadrant in the image (1 is top left, 2 is top right,
        # 3 is bottom left and 4 is bottom right. y is the hand gesture: 1 is fist, 2 is three fingers - thumb,
        # index and middle -, 3 is five fingers.

        flag = 0

        if counter == 100 and k != 114:
            # These are very ugly nested IFs but they do work so...
            if pattern[pos][0] == 1:
                if cx < 230 and cy < 180:
                    if pattern[pos][1] == 1:
                        if point <= 2:
                            pos += 1
                        else:
                            pos = 0
                    elif pattern[pos][1] == 2:
                        if point >= 3 or point <= 4:
                            pos += 1
                        else:
                            pos = 0
                    elif pattern[pos][1] == 3:
                        if point >= 5:
                            pos += 1
                        else:
                            pos = 0
                else:
                    pos = 0
            elif pattern[pos][0] == 2:
                if cx > 400 and cy < 180:
                    if pattern[pos][1] == 1:
                        if point <= 2:
                            pos += 1
                        else:
                            pos = 0
                    elif pattern[pos][1] == 2:
                        if point >= 3 or point <= 4:
                            pos += 1
                        else:
                            pos = 0
                    elif pattern[pos][1] == 3:
                        if point >= 5:
                            pos += 1
                        else:
                            pos = 0
                else:
                    pos = 0
            elif pattern[pos][0] == 3:
                if cx < 230 and cy > 300:
                    if pattern[pos][1] == 1:
                        if point <= 2:
                            pos += 1
                        else:
                            pos = 0
                    elif pattern[pos][1] == 2:
                        if point >= 3 or point <= 4:
                            pos += 1
                        else:
                            pos = 0
                    elif pattern[pos][1] == 3:
                        if point >= 5:
                            pos += 1
                        else:
                            pos = 0
                else:
                    pos = 0
            elif pattern[pos][0] == 4:
                if cx > 400 and cy > 300:
                    if pattern[pos][1] == 1:
                        if point <= 2:
                            pos += 1
                        else:
                            pos = 0
                    elif pattern[pos][1] == 2:
                        if point >= 3 or point <= 4:
                            pos += 1
                        else:
                            pos = 0
                    elif pattern[pos][1] == 3:
                        if point >= 5:
                            pos += 1
                        else:
                            pos = 0
                else:
                    pos = 0

            print pos

            if pos == 3:
                cv2.putText(drawing, "Pattern Matched!", (60,250), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0,0,255), 3)
                pos = 0

            # I'll capture some images for report purposes
            cv2.imwrite("drawing" + str(seq) + ".jpg", drawing)
            cv2.imwrite("capture" + str(seq) + ".jpg", img)
            seq += 1
        elif counter == 100 and k == 114:
            # Here we create another password pattern. When the counter reaches 10, it captures the hand position and
            # gesture and records it in a sequence.
            pattern2 = [[0, 0],
                        [0, 0],
                        [0, 0]]

            if cx < 230 and cy < 180:
                pattern2[pos][0] == 1
            elif cx > 400 and cy < 180:
                pattern2[pos][0] == 2
            elif cx < 230 and cy > 300:
                pattern2[pos][0] == 3
            elif cx > 400 and cy > 300:
                pattern2[pos][0] == 4
            else:
                print "I coult not understand your hand position for sure. Please restart the gesture sequence"
                pos = 0
                continue

            if point <= 2:
                pattern2[pos][1] == 1
            elif point >= 3 or point <= 4:
                pattern2[pos][1] == 2
            elif point >= 5:
                pattern2[pos][1] == 3

            pos += 1
            if pos == 3:
                k = 0
                # We only copy the new pattern over the older one if it was successfully recorded
                pattern = deepcopy(pattern2)
                print "New password pattern recorded!"

        point = 0
    except AttributeError:
        print "No points detected"

    cv2.imshow('output', drawing)
    cv2.imshow('input', img)

    k = cv2.waitKey(10)
    if k == 27: # Once you hit ESC, the program stops running
        break
    if k == 114: # If you hit the "r" key, you can record a new password
        print "Recording new password sequence"
        pos = 0