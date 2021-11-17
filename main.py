import numpy as np
import cv2
import mss
import pytesseract


# global screenshot tool (thread safe)
sct = mss.mss()

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
    monitor_left = {'top': 0, 'left': 0, 'width': 300, 'height': 100}
    screen_left = sct.grab(monitor_left)
    return np.array(screen_left, dtype="uint8")

# get a screenshot of the top right corner of the screen
def get_top_right():
    monitor_right = {'top': 50, 'left': 1920 - 400, 'width': 300, 'height': 50}
    screen_right = sct.grab(monitor_right)
    return np.array(screen_right)


def getTimer(timezone):
    # detect text in the image using pytesseract
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    print(parse_string(pytesseract.image_to_string(timezone, config=custom_config)))


# code for grabbing data
    # sct = mss.mss()
    # monitor_right = {'top': 50, 'left': 1920 - 405, 'width': 250, 'height': 50}
    # screen_right = sct.grab(monitor_right)
    # img_right = np.array(screen_right)
    # cv2.imshow('image', img_right)
    # cv2.waitKey(10)
    # # detect text in the image using pytesseract
    # custom_config = r'--oem 3 --psm 6 outputbase digits'
    # print(parse_string(pytesseract.image_to_string(img_right, config=custom_config)))

from distTransform import dist_transform, dist_transform_cv2
from templateSearch import template_search

# defines small UI template
templateSmall = cv2.imread('assets/EdgeMaskSmall.png', cv2.IMREAD_GRAYSCALE)

if __name__ == '__main__':
    while True:
        imgR = get_top_right()
        imgL = get_top_left()

        # we only care about leftmost half for crown checks
        crownSpace = imgL[0:75, 0:150]

        # tries to find crown in image
        # tends to find false positives of the rope pile if in frame
        # tends to detect some other strong corners with current threshold
        dsts = dist_transform_cv2(crownSpace)
        pos, min = template_search(dsts, templateSmall, 200) # threshold needs adjusting!

        # TODO color checks

        # TODO swap to timer?

        # if we found the image, draw a circle
        # otherwise do nothing
        if pos != None:
            x, y = pos
            show = cv2.circle(imgL, (x, y), 3, (255, 0, 0), 3)
        else:
            show = imgL

        # show the screenshot with the circle
        cv2.imshow("output", crownSpace)
        cv2.waitKey(1)

        # logs min for thresholding purposes
        print("Current min:", min)
