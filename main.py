import numpy as np
import cv2
import mss

# global screenshot tool (thread safe)
sct = mss.mss()

def get_top_left():
    monitor_left = {'top': 0, 'left': 0, 'width': 300, 'height': 100}
    screen_left = sct.grab(monitor_left)
    return np.array(screen_left, dtype="uint8")

def get_top_right():
    monitor_right = {'top': 50, 'left': 1920 - 400, 'width': 300, 'height': 50}
    screen_right = sct.grab(monitor_right)
    return np.array(screen_right)


from distTransform import dist_transform, dist_transform_cv2
from templateSearch import template_search

# defines small UI template
templateSmall = cv2.imread('assets/EdgeMaskSmall.png', cv2.IMREAD_GRAYSCALE)

if __name__ == '__main__':
    while True:
        #get_top_right()
        img = get_top_left()

        # we only care about leftmost half for crown checks
        crownSpace = img[0:75, 0:150]

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
            show = cv2.circle(img, (x, y), 3, (255, 0, 0), 3)
        else:
            show = img

        # show the screenshot with the circle
        cv2.imshow("output", crownSpace)
        cv2.waitKey(1)

        # logs min for thresholding purposes
        print("Current min:", min)