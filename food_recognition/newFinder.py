from cv2 import cv2
import numpy as np
import time
import imutils

img1 = cv2.imread("first.jpg")
img2 = cv2.imread("first.jpg")
diff = cv2.absdiff(img1, img2)
mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

th = 150
imask =  mask>th
canvas = np.zeros_like(img2)
canvas[imask] = 255
canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)

# find contours over mask
contours, hierarchy = cv2.findContours(canvas, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for c in contours:
    rect = cv2.boundingRect(c)
    if rect[2] < 100 or rect[3] < 100: continue
    # print cv2.contourArea(c)
    x,y,w,h = rect
    try:
        roi = img2[y:y+h, x:x+w]
        roi = cv2.resize(roi, (224,224), interpolation = cv2.INTER_AREA)
        cv2.imshow("Show",roi)
        cv2.waitKey(0)
    except cv2.error:
        time.sleep(0.1)
    cv2.rectangle(img2,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.putText(img2,'Food Detected',(x+w+10,y+h),0,0.3,(0,255,0))
cv2.imshow("Show",img2)
cv2.waitKey(0)
cv2.destroyAllWindows()