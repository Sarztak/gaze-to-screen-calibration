from sklearn.ensemble import RandomForestRegressor
import pyautogui as pg
import pandas as pd
from tkinter import *

model_x = RandomForestRegressor()
model_y = RandomForestRegressor()
left = pd.read_csv('left.csv')
right = pd.read_csv('right.csv')
x = left.landmark_x.to_numpy().reshape(-1, 1)
y = left.landmark_y.to_numpy().reshape(-1, 1)
model_x.fit(x, left.screen_x.to_numpy())
model_y.fit(y, left.screen_y.to_numpy())
pred_x = model_x.predict(x)
pred_y = model_y.predict(y)


root = Tk()
height, width = pg.size().height, pg.size().width
canvas = Canvas(root, width=width, height=height)
npoints = 10
radius = 50
for i in range(npoints):
    canvas.create_oval(pred_x[i], pred_y[i], pred_x[i] - 50, pred_y[i] - 50, outline = "black", fill = "red",width = 4)
canvas.pack()
root.mainloop()
