import cv2




from getUI import *
from distTransform import dist_transform, dist_transform_cv2
from templateSearch import template_search
from ParseText import get_timer

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

        # works best on 300 dpi minimum so we scale up our image for more pixels
        f = 3
        size = (imgR.shape[1] * f, imgR.shape[0] * f)
        scaled = cv2.resize(imgR, size)
        # tesseract v4 wants black text so we invert the image
        inverted = cv2.bitwise_not(scaled)
        # also bump up the contrast
        inverted = cv2.addWeighted(inverted, 3.2, inverted, 0, -175)
        cv2.imshow('imageR', inverted)
        timer = get_timer(imgR)
        # print(timer)

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