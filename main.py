import numpy as np
import cv2
import mss

def get_top_left():
    sct = mss.mss()
    monitor_left = {'top': 0, 'left': 0, 'width': 300, 'height': 100}
    screen_left = sct.grab(monitor_left)
    img_left = np.array(screen_left)
    cv2.imshow('image', img_left)
    cv2.waitKey(10)

def get_top_right():
    sct = mss.mss()
    monitor_right = {'top': 50, 'left': 1920 - 400, 'width': 300, 'height': 50}
    screen_right = sct.grab(monitor_right)
    img_right = np.array(screen_right)
    cv2.imshow('image', img_right)
    cv2.waitKey(10)


if __name__ == '__main__':
    while True:
        #get_top_right()
        get_top_left()
