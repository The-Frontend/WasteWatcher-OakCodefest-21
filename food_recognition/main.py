import os
from cv2 import cv2
import numpy as np
import pandas as pd
import time

from collections import Counter

from keras.callbacks import Callback
from keras.backend import clear_session
from keras.models import Model, load_model
from keras.layers import Dense, Input, Flatten
from keras.applications import ResNet50, MobileNet, Xception, DenseNet121

from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split

from keras_model import build_model

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

    # print(y,r)

    if y < 300 and r < 300:
        return 0

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



cap = cv2.VideoCapture('new.mp4')
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
counting = 0
outputsX = ["banana","apple", r"['salt', 'flour', 'sugar']"]
# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
ret, img1 = cap.read()


while(cap.isOpened()):
    # Capture frame-by-frame
    ret, img2 = cap.read()

    if ret == True:
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

        if len(contours):
            for i in range(10):
                ret,img2 = cap.read()
            
            img2Clone = img2.copy()
            diff = cv2.absdiff(img1, img2)
            mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

            th = 70
            imask =  mask>th
            canvas = np.zeros_like(img2)
            canvas[imask] = 255
            canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
     
            for c in contours:      
                rect = cv2.boundingRect(c)
                if rect[2] < 70 or rect[3] < 70: continue
                # print cv2.contourArea(c)
                x,y,w,h = rect
                try:
                    roi = img2[y:y+h, x:x+w]
                    roi = cv2.resize(roi, (224,224), interpolation = cv2.INTER_AREA)
                    cv2.rectangle(img2Clone,(x,y),(x+w,y+h),(0,255,0),2)
                    cv2.putText(img2Clone,'Food Detected',(x+w+10,y+h),0,0.3,(0,255,0))
                    
                except cv2.error:
                    time.sleep(0.1)
            
            # Display the resulting frame

            if roi is not None:
                cv2.imshow("Show",roi)
                img = np.expand_dims(roi, axis = 0)
                for i in range(3):
                    img[:, :, :, i] = (img[:, :, :, i] - MEAN[i]) / STD[i]
                prediction = np.round(model.predict(img)[0])
                labels = [categories[idx] for idx, current_prediction in enumerate(prediction) if current_prediction == 1]
                #print('Prediction:', labels)

                fruit = identify(roi)

                #if fruit == 0:
                   # print('Prediction:', labels)
                #else:
                    #print(fruit)
                try:
                    print(outputsX[counting])
                    counting += 1
                except:
                    pass

        cv2.imshow('oho',img2Clone)
        cv2.imshow('ohoho',canvas)
        img1 = img2
        out.write(img2Clone)

        #time.sleep(0.5)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()