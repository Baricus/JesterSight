# getUI.py - holds functions for grabbing the screenshots in the program

import mss
import numpy as np

# global screenshot tool (thread safe)
sct = mss.mss()


def get_top_left():
    """
    :return: a screenshot of the top left UI (1080p configured)
    """
    monitor_left = {'top': 0, 'left': 0, 'width': 300, 'height': 100}
    screen_left = sct.grab(monitor_left)
    return np.array(screen_left, dtype="uint8")



def get_top_right():
    """
    :return: a screenshot of the top right UI (1080p configured)
    """
    monitor_right = {'top': 50, 'left': 1920 - 325, 'width': 175, 'height': 50}
    screen_right = sct.grab(monitor_right)
    return np.array(screen_right)