import os
from cv2 import cv2
import numpy as np
import pandas as pd
import time

from collections import Counter
from picamera.array import PiRGBArray
from picamera import PiCamera

from keras.callbacks import Callback
from keras.backend import clear_session
from keras.models import Model, load_model
from keras.layers import Dense, Input, Flatten
from keras.applications import ResNet50, MobileNet, Xception, DenseNet121

from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split

from keras_model import build_model

camera = PiCamera()
rawCapture = PiRGBArray(camera)
time.sleep(2)

#y_boundaries = ([50, 50, 150], [80, 255, 250 ]) #yellow
#r_boundaries = (([15, 0, 60], [50, 50, 255])) #red

y_boundaries = ([60,121,114],[90,142,139])
r_boundaries = ([40,40,83],[68,80,150])

#y_boundaries = ([144,191,196],[217,255,253])

y_lower = np.array(y_boundaries[0], dtype = "uint8")
y_upper = np.array(y_boundaries[1], dtype = "uint8")

r_lower = np.array(r_boundaries[0], dtype = "uint8")
r_upper = np.array(r_boundaries[1], dtype = "uint8")

def identify(image):

    mask_y = cv2.inRange(image, y_lower, y_upper)
    y = cv2.countNonZero(mask_y)

    mask_r = cv2.inRange(image, r_lower, r_upper)
    r = cv2.countNonZero(mask_r)

    print(y,r)

    if y > r:
        return "Banana"
    else:
        return "Apple"

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
MEAN = np.array([51.072815, 51.072815, 51.072815])
STD = np.array([108.75629,  92.98068,  85.61884])

f = open("categories.txt", "r")
categories = f.readline().split(",")
print(categories)
#categories = [
#'healthy', 'junk', 'dessert', 'appetizer', 'mains', 'soups', 'carbs', 'protein', 'fats', 'meat'
#]

#parser = argparse.ArgumentParser()
#parser.add_argument('--image', help = 'Path to the image to be predicted', required = True)
#parser.add_argument('--saved_model', help = 'Path of the saved model', required = True)

#args = parser.parse_args()

modelPath = os.path.join("model.h5")

model = build_model('inference', model_path = modelPath)

#cap = cv2.VideoCapture(0)
#ret, img1 = cap.read()
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        img1 = frame.array
        break

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Capture frame-by-frame
    img2 = frame.array
    img2Clone = img2.copy()
    diff = cv2.absdiff(img1, img2)
    mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    th = 50
    imask =  mask>th
    canvas = np.zeros_like(img2)
    canvas[imask] = 255
    canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)

    roi = None
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
        except cv2.error:
            time.sleep(0.1)
        cv2.rectangle(img2Clone,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText(img2Clone,'Food Detected',(x+w+10,y+h),0,0.3,(0,255,0))
    # Display the resulting frame
    if roi is not None:
        cv2.imshow("Show",roi)
        img = np.expand_dims(roi, axis = 0)
        for i in range(3):
            img[:, :, :, i] = (img[:, :, :, i] - MEAN[i]) / STD[i]
        prediction = np.round(model.predict(img)[0])
        labels = [categories[idx] for idx, current_prediction in enumerate(prediction) if current_prediction == 1]
        print('Prediction:', labels)

        print(identify(roi))
    img1 = img2
    cv2.imshow('oho',img2Clone)
    cv2.imshow('ohoho',canvas)
    rawCapture.truncate(0)
    time.sleep(0.5)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
