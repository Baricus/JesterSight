import numpy as np
import cv2
import mss
import pytesseract

# detect the center slash of the timer(detects as a 7)
def parse_string(string):
    mid = string.find('70')
    if mid == -1:
        # return a -1 if not found
        return -1
    else:
        # return the two numbers before the middle
        return string[mid - 2:mid]

# get a screenshot of the top left corner of the screen
def get_top_left():
    sct = mss.mss()
    monitor_left = {'top': 0, 'left': 0, 'width': 300, 'height': 100}
    screen_left = sct.grab(monitor_left)
    img_left = np.array(screen_left)
    cv2.imshow('image', img_left)
    cv2.waitKey(10)

# get a screenshot of the top right corner of the screen
def get_top_right():
    sct = mss.mss()
    monitor_right = {'top': 50, 'left': 1920 - 405, 'width': 250, 'height': 50}
    screen_right = sct.grab(monitor_right)
    img_right = np.array(screen_right)
    cv2.imshow('image', img_right)
    cv2.waitKey(10)
    # detect text in the image using pytesseract
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    print(parse_string(pytesseract.image_to_string(img_right, config=custom_config)))


if __name__ == '__main__':
    while True:
        get_top_right()
        # get_top_left()
