import cv2
import mediapipe as mp
import pandas as pd
from tkinter import *
import pyautogui as pg
import time
import threading
import numpy as np
from collections import defaultdict

SCREEN_HEIGHT = 1599
SCREEN_WIDTH = 2599
left, right = defaultdict(list), defaultdict(list)

def do_calibration():
    left_eye = [473]
    right_eye = [468]
    cap = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    

    for i in range(10):
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)    
        results = face_mesh.process(rgb_frame).multi_face_landmarks
        if results:
            landmarks = results[0].landmark
            for idx in left_eye:
                left['landmark_x'].append(landmarks[idx].x)
                left['landmark_y'].append(landmarks[idx].y)
                left['screen_x'].append(pg.position().x) 
                left['screen_y'].append(pg.position().y)

            for idx in right_eye:
                right['landmark_x'].append(landmarks[idx].x)
                right['landmark_y'].append(landmarks[idx].y)
                right['screen_x'].append(pg.position().x)
                right['screen_y'].append(pg.position().y)

                
        
        time.sleep(0.2)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
    pd.DataFrame(left).to_csv('left.csv', index=False)
    pd.DataFrame(right).to_csv('right.csv', index=False)
    cap.release()
    cv2.destroyAllWindows()


root = Tk()
height, width = pg.size().height, pg.size().width
canvas = Canvas(root, width=width, height=height)
np.random.seed(2000)
npoints = 10
px = np.random.randint(100, 2000, npoints)
py = np.random.randint(100, 1000, npoints)
radius = 50
for i in range(npoints):
    canvas.create_oval(px[i], py[i], px[i] - 50, py[i] - 50, outline = "black", fill = "red",width = 4)
canvas.pack()
root.update()
time.sleep(1)
t = threading.Thread(target=do_calibration)
t.start()
