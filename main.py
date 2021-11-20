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


has_crown = False
acquire_time = -1
prev_time = -1;

# time into the cycle to warn player (eventually plus sound to play)
alarms = [22-5, 22-4, 22-3, 22-2]
unfired_alarms = alarms.copy()

if __name__ == '__main__':
    while True:
        # TODO determine level

        # if we don't have the crown, check if we do and continue
        if not has_crown:
            has_crown = check_crown(200)

        # if we do have the crown, start checking for time
        if has_crown:
            cur_time = check_timer()
            # filter invalid times
            if cur_time < 0:
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
                        print("WARNING:", time)

                        # pop the time so it stops firing
                        unfired_alarms.pop(0)

            # resets every 22 seconds
            if acquire_time + 22 < cur_time:
                acquire_time = acquire_time + 22
                unfired_alarms = alarms.copy()

            print("cur_time:", cur_time)
            print("acquire_time:", acquire_time)
            print()