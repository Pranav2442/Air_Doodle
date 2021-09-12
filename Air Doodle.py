import numpy as np
import cv2 as cv
from collections import deque

 
def func(x):
   print(x)







# def col(x):
#     print(x)



cv.namedWindow("COLOR_RANGE_FINDER")
cv.createTrackbar("U_H", "COLOR_RANGE_FINDER", 153, 180,func)
cv.createTrackbar("U_S", "COLOR_RANGE_FINDER", 255, 255,func)
cv.createTrackbar("U_V", "COLOR_RANGE_FINDER", 255, 255,func)
cv.createTrackbar("L_H", "COLOR_RANGE_FINDER", 64, 180,func)
cv.createTrackbar("L_S", "COLOR_RANGE_FINDER", 72, 255,func)
cv.createTrackbar("L_V", "COLOR_RANGE_FINDER", 49, 255,func)
# cv.createTrackbar("B","Paint",0,255,col)
# cv.createTrackbar("G","Paint",0,255,col)
# cv.createTrackbar("R","Paint",0,255,col)


Blue_p = [deque(maxlen=1024)]
Green_p = [deque(maxlen=1024)]
Red_p = [deque(maxlen=1024)]
Yellow_p = [deque(maxlen=1024)]
Cyan_p=[deque(maxlen=1024)]

index_of_blue_col = 0
index_of_red_col = 0
index_of_yellow_col = 0
index_of_cyan_col=0
index_of_green_col = 0
 
kernel = np.ones((5,5),np.uint8)

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255),(255,165,0)]
colorin = 0


window = np.zeros((512,800,3))
window = cv.rectangle(window, (20,1), (110,65), (0,0,0), 2)
window = cv.rectangle(window, (120,1), (200,65), colors[0], -1)
window = cv.rectangle(window, (210,1), (310,65), colors[1], -1)
window = cv.rectangle(window, (320,1), (420,65), colors[2], -1)
window = cv.rectangle(window, (430,1), (530,65), colors[3], -1)
window = cv.rectangle(window, (540,1), (630,65), colors[4], -1)


cv.putText(window, "CLEAR", (30, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv.LINE_AA)
cv.putText(window, "BLUE", (140, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)
cv.putText(window, "GREEN", (240, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)
cv.putText(window, "RED", (350, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)
cv.putText(window, "YELLOW", (450, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv.LINE_AA)
cv.putText(window, "CYAN", (550, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv.LINE_AA)
cv.namedWindow('Paint', cv.WINDOW_AUTOSIZE)



cap = cv.VideoCapture(0)
cap.set(3,400)
cap.set(4,400)
while cap.isOpened():
    
    
    ret, frame = cap.read()
    if ret:    
        frame = cv.flip(frame, 1)
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)


        upper_hue = cv.getTrackbarPos("U_H", "COLOR_RANGE_FINDER")
        upper_saturation = cv.getTrackbarPos("U_S", "COLOR_RANGE_FINDER")
        upper_value = cv.getTrackbarPos("U_V", "COLOR_RANGE_FINDER")
        Lower_hue = cv.getTrackbarPos("L_H", "COLOR_RANGE_FINDER")
        Lower_saturation = cv.getTrackbarPos("L_S", "COLOR_RANGE_FINDER")
        Lower_value = cv.getTrackbarPos("L_V", "COLOR_RANGE_FINDER")
        Upper_hsv = np.array([upper_hue,upper_saturation,upper_value])
        Lower_hsv = np.array([Lower_hue,Lower_saturation,Lower_value])
    # r=cv.getTrackbarPos("B","Paint")
    # g=cv.getTrackbarPos("G","Paint")
    # b=cv.getTrackbarPos("R","Paint")

    
        Mask = cv.inRange(hsv, Lower_hsv, Upper_hsv)
        Mask = cv.erode(Mask, kernel, iterations=1)
        Mask = cv.morphologyEx(Mask, cv.MORPH_OPEN, kernel)
        Mask = cv.dilate(Mask, kernel, iterations=1)

    
        contours,_ = cv.findContours(Mask.copy(), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        center = None

    
        if len(contours) > 0:
    	 
            cnt = sorted(contours, key = cv.contourArea, reverse = True)[0]
        
            ((x, y), radius) = cv.minEnclosingCircle(cnt)
        
            cv.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        
            M = cv.moments(cnt)
            center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

         
            if center[1] <= 65:
                if 10 <= center[0] <= 120 and 1<=center[1]<=70:
                    Blue_p = [deque(maxlen=512)]
                    Green_p = [deque(maxlen=512)]
                    Red_p = [deque(maxlen=512)]
                    Yellow_p = [deque(maxlen=512)]
                    Cyan_p=[deque(maxlen=512)]
                    index_of_blue_col = 0
                    index_of_green_col = 0
                    index_of_red_col = 0
                    index_of_yellow_col = 0
                    index_of_cyan_col=0
                    window[67:,:,:] = 0
            
                elif 120 <= center[0] <= 200:
                    colorin = 0 
                elif 210 <= center[0] <= 310:
                    colorin = 1 
                elif 320 <= center[0] <= 420:
                    colorin = 2 
                elif 430 <= center[0] <= 530:
                    colorin = 3 
                elif 530 <= center[0]<=630:
                    colorin=4
            else :
                if colorin == 0:
                    Blue_p[index_of_blue_col].appendleft(center)
                elif colorin == 1:
                    Green_p[index_of_green_col].appendleft(center)
                elif colorin == 2:
                    Red_p[index_of_red_col].appendleft(center)
                elif colorin == 3:
                    Yellow_p[index_of_yellow_col].appendleft(center)
                elif colorin == 4:
                    Cyan_p[index_of_cyan_col].appendleft(center)
    
        else:
            Blue_p.append(deque(maxlen=512))
            index_of_blue_col += 1
            Green_p.append(deque(maxlen=512))
            index_of_green_col += 1
            Red_p.append(deque(maxlen=512))
            index_of_red_col += 1
            Yellow_p.append(deque(maxlen=512))
            index_of_yellow_col += 1

     
        points = [Blue_p, Green_p, Red_p, Yellow_p,Cyan_p]
        for i in range(len(points)):
            for j in range(len(points[i])):
                for k in range(1, len(points[i][j])):
                    if points[i][j][k - 1] is None or points[i][j][k] is None:
                        continue
                    cv.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 4,cv.LINE_AA)
                    cv.line(window, points[i][j][k - 1], points[i][j][k], colors[i], 4)

    
        cv.imshow("Air Doodle", window)
        cv.imshow("Real time", frame)
        cv.imshow("mask",Mask)

	 
        if cv.waitKey(1) ==27:
            break


cap.release()
cv.destroyAllWindows()