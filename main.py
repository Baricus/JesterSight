import cv2

from get_ui import *
from dist_transform import dist_transform_cv2
from template_search import template_search
from parse_text import get_timer, get_level
from check_color_rgb import color_check

# defines small UI template
templateSmall = cv2.imread('assets/EdgeMaskSmall.png', cv2.IMREAD_GRAYSCALE)


def check_crown(thresh):
    """
    checks for the true crown in the image
    :param thresh: the threshold for the crown's presence (200 is our current)
    :return: true if the crown is present, false if not
    """
    imgL = get_top_left()

    # we only care about leftmost half for crown checks
    crownSpace = imgL[0:75, 0:150]

    # tries to find crown in image
    # tends to find false positives of the rope pile if in frame
    # tends to detect some other strong corners with current threshold
    dsts = dist_transform_cv2(crownSpace)
    pos, min = template_search(dsts, templateSmall, thresh)

    if pos is not None:
        x, y = pos
        colors = color_check(crownSpace, x, y)

        if not colors:
            pos = None

    # debug printing

    # if we found the image, draw a circle
    # otherwise do nothing
    if pos is not None:
        x, y = pos
        show = cv2.circle(imgL, (x, y), 3, (255, 0, 0), 3)
    else:
        show = imgL

    # show the screenshot with the circle
    cv2.imshow("crown", crownSpace)
    cv2.waitKey(1)

    if pos is not None:
        return True
    return False

def check_timer():
    """
    checks for the timer's presence
    :return: the # seconds in the level time or -1 if not found
    """
    imgR = get_top_right()
    # works best on 300 dpi minimum so we scale up our image for more pixels
    f = 2
    size = (imgR.shape[1] * f, imgR.shape[0] * f)
    scaled = cv2.resize(imgR, size)
    inverted = cv2.bitwise_not(scaled)
    # also bump up the contrast
    inverted = cv2.addWeighted(inverted, 4, inverted, 0, -175)
    # erode it slightly
    eroded = cv2.erode(inverted, None, iterations=1)
    ret, threshed = cv2.threshold(eroded, 230, 255, cv2.THRESH_BINARY_INV)

    # debug display
    cv2.imshow('timer', imgR)
    cv2.imshow('timer processed', threshed)
    cv2.waitKey(1)

    return get_timer(threshed)


def check_level():
    """
    checks the level number
    :return: the level number
    """
    # capture the level number and return the string
    imgT = get_level_num()
    f = 4
    size = (imgT.shape[1] * f, imgT.shape[0] * f)
    scaled = cv2.resize(imgT, size)
    inverted = cv2.bitwise_not(scaled)
    # also bump up the contrast
    inverted = cv2.addWeighted(inverted, 5, inverted, 0, -200)
    # erode it slightly
    eroded = cv2.erode(inverted, None, iterations=0)
    blurred = cv2.blur(eroded, (5,5))
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    ret, out = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)
    out = cv2.blur(out, (4, 4))

    cv2.imshow("test", out)
    level = get_level(out)
    print(level)
    global prev_level
    dash = level.find('-')
    if dash == -1:
        return "paused"
    elif level == prev_level:
        prev_level = level
        return "same"
    elif level != prev_level:
        prev_level = level
        return "new"
    else:
        return "same"

has_crown = False
acquire_time = -1
prev_time = -1
prev_level = None

# time into the cycle to warn player (eventually plus sound to play)
alarms = [22 - 5, 22 - 4, 22 - 3, 22 - 2, 22-1]
unfired_alarms = alarms.copy()

level = None
if __name__ == '__main__':

    while True:
        # if we don't have the crown, check if we do and continue
        if not has_crown:
            has_crown = check_crown(200)
            if has_crown:
                # check levels
                level = check_level()
                if level == "same":
                    print("Unpaused, resuming timer")
                    # timer setup already
                elif level == "new":
                    print("Next level, resetting timer")
                    prev_time = -1
                    acquire_time = -1
                else:
                    # couldn't determine
                    print("Couldn't tell if new level, assuming same level")

        # if we do have the crown, start checking for time
        if has_crown:
            cur_time = check_timer()

            # if we can't get the time, set has_crown to false so we re-check
            if cur_time < 0:
                has_crown = False
                continue

            # if we have no previous time get it
            if prev_time == -1:
                prev_time = cur_time

            # TODO ensure time delta isn't too great
            # (needs tweaking)
            if abs(cur_time - prev_time) > 3:
                prev_time = cur_time
                continue

            # if we don't have the acquired time, get it
            if acquire_time == -1:
                acquire_time = cur_time
            # if not, check if we're past a warning time:
            else:
                # TODO add sounds to alarms (tuples of seconds_left, time)
                if len(unfired_alarms) > 0:
                    time = unfired_alarms[0] + acquire_time
                    if time <= cur_time:
                        print("WARNING:", len(unfired_alarms))

                        # pop the time so it stops firing
                        unfired_alarms.pop(0)

            # resets every 22 seconds
            if acquire_time + 22 < cur_time:
                acquire_time = acquire_time + 22
                unfired_alarms = alarms.copy()
                print()