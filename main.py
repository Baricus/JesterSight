import cv2

from getUI import *
from distTransform import dist_transform, dist_transform_cv2
from templateSearch import template_search
from ParseText import get_timer

# defines small UI template
templateSmall = cv2.imread('assets/EdgeMaskSmall.png', cv2.IMREAD_GRAYSCALE)

def check_crown(thresh):
    """
    checks for the true crown in the image
    :param thresh: the threshold for the crown's presence (200 is our current)
    :return: the position if present, nothing if not
    """
    imgL = get_top_left()

    # we only care about leftmost half for crown checks
    crownSpace = imgL[0:75, 0:150]

    # tries to find crown in image
    # tends to find false positives of the rope pile if in frame
    # tends to detect some other strong corners with current threshold
    dsts = dist_transform_cv2(crownSpace)
    pos, min = template_search(dsts, templateSmall, thresh)

    # TODO color checks

    # debug printing
    """
    # if we found the image, draw a circle
    # otherwise do nothing
    if position != None:
        x, y = position
        show = cv2.circle(imgL, (x, y), 3, (255, 0, 0), 3)
    else:
        show = imgL

    # show the screenshot with the circle
    cv2.imshow("output", crownSpace)
    cv2.waitKey(1)
    """

    return pos


def check_timer():
    """
    checks for the timer's presence
    :return: the # seconds in the level time or -1 if not found
    """
    imgR = get_top_right()
    # works best on 300 dpi minimum so we scale up our image for more pixels
    f = 3
    size = (imgR.shape[1] * f, imgR.shape[0] * f)
    scaled = cv2.resize(imgR, size)
    # tesseract v4 wants black text so we invert the image
    inverted = cv2.bitwise_not(scaled)
    # also bump up the contrast
    inverted = cv2.addWeighted(inverted, 3.2, inverted, 0, -175)

    # debug display
    cv2.imshow('timer', inverted)
    cv2.waitKey(1)

    return get_timer(imgR)


if __name__ == '__main__':
    while True:
        # position = check_crown(200)

        # TODO swap to timer?

        print(check_timer())