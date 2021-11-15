import numpy as np
import cv2
import mss

# global screenshot tool (thread safe)
sct = mss.mss()

def get_top_left():
    sct = mss.mss()
    monitor_left = {'top': 0, 'left': 0, 'width': 300, 'height': 100}
    screen_left = sct.grab(monitor_left)
    img_left = np.array(screen_left)
    cv2.imshow('image', img_left)
    cv2.waitKey(10)

def top_left_region(width, height):
    left = width * 2 // 100  # 2% from the left
    top = height * 0 // 100  # 5% from the top
    right = left + width * 4.5 // 100 # +4.5% right
    lower = top + height * 4.5 // 100 # +4.5% down
    return (left, top, right, lower)

def get_top_left_UI():
    """
    get_top_left_UI

    Screenshot and grab a region (left: 2%, top: 0%, right: +4.5%, lower: +4.5%) of monitor
    :return: image of cropped region
    :return (width, height) of entire screen
    """
    with mss.mss() as sct:
        # Use the 1st monitor
        monitor = sct.monitors[1]

        # left = monitor["left"] + monitor["width"] * 2 // 100  # 2% from the left
        # top = monitor["top"] + monitor["height"] * 0 // 100  # 5% from the top
        # right = left + monitor["width"] * 4.5 // 100 # +4.5% right
        # lower = top + monitor["height"] * 4.5 // 100 # +4.5% down
        # bbox = (left, top, right, lower)
        bbox = top_left_region(monitor["width"], monitor["height"])

        # Grab the picture
        # Using PIL would be something like:
        # im = ImageGrab(bbox=bbox)
        img_left = sct.grab(bbox)
        return np.array(img_left), (monitor["width"], monitor["height"])

    # sct = mss.mss()
    # monitor_left = {'top': 0, 'left': 0, 'width': 300, 'height': 100}
    # screen_left = sct.grab(monitor_left)
    # img_left = np.array(screen_left)
    # cv2.imshow('image', img_left)
    # cv2.waitKey(10)

def get_top_right():
    sct = mss.mss()
    monitor_right = {'top': 50, 'left': 1920 - 400, 'width': 300, 'height': 50}
    screen_right = sct.grab(monitor_right)
    img_right = np.array(screen_right)
    cv2.imshow('image', img_right)
    cv2.waitKey(10)

from distTransform import dist_transform, dist_transform_cv2
from templateSearch import template_search, templateSearchUI

# defines small UI template
templateSmall = cv2.imread('assets/EdgeMaskSmall.png', cv2.IMREAD_GRAYSCALE)

if __name__ == '__main__':
    while True:
        #get_top_right()
        # img = get_top_left()
        img, screenDim = get_top_left_UI()

        # we only care about leftmost half for crown checks
        # crownSpace = img[0:75, 0:150]
        crownSpace = img

        # tries to find crown in image
        # tends to find false positives of the rope pile if in frame
        # tends to detect some other strong corners with current threshold
        dsts = dist_transform_cv2(crownSpace)
        # pos, min = template_search(dsts, templateSmall, 200) # threshold needs adjusting!
        pos, min = template_searchUI(dsts, templateSmall, 200, screenDim) # threshold needs adjusting!

        # TODO color checks

        # TODO swap to timer?

        # if we found the image, draw a circle
        # otherwise do nothing
        if pos != None:
            x, y = pos
            show = cv2.circle(img, (x, y), 3, (255, 0, 0), 3)
        else:
            show = img

        # show the screenshot with the circle
        cv2.imshow("output", crownSpace)
        cv2.waitKey(1)

        # logs min for thresholding purposes
        print("Current min:", min)