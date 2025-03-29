import cv2
import mediapipe as mp
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pyautogui as pg
from typing import Tuple
from tkinter import *
import time
import threading


cap = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)


left_eye = [
    362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398
]
right_eye = [
    133, 33, 7, 163, 144, 145, 153, 154, 155, 173, 157, 158, 159, 160, 161, 246
]
left_iris_center = [473]
right_iris_center = [468]
face_center = [6]
eyestrip = [
    27, 28, 56, 190, 243, 112, 26, 22, 23, 24, 110, 25, 130, 247, 30, 29, 257, 259, 260, 467, 359, 255, 339, 254, 253, 252, 256, 341, 463, 414, 286, 258
]

eye_landmarks = left_eye + right_eye + left_iris_center + \
    right_iris_center + eyestrip 

while True:
    ret, frame = cap.read()
    if not ret:
        break

    fh, fw, *_ = frame.shape 
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)    
    results = face_mesh.process(rgb_frame).multi_face_landmarks
    if results:
        landmarks = results[0].landmark
        for idx in eye_landmarks:
            x, y = int(landmarks[idx].x * fw), int(landmarks[idx].y * fh)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
        cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()


