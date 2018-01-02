import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    
    lower_yellow = np.array([10, 65, 90])
    upper_yellow = np.array([40, 255, 255])
    #lower_yellow_hsv = cv2.cvtColor(lower_yellow, cv2.COLOR_BGR2HSV)
    #upper_yellow_hsv = cv2.cvtColor(upper_yellow, cv2.COLOR_BGR2HSV);
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('result', result)
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)

    k = cv2.waitKey(5)
    if k == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
