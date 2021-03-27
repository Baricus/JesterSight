from mss import mss
import time
import cv2
import numpy

# sets monitor positions and initializes mss
monitor = {"top": 0, "left": 0, "width": 160, "height": 135}
sct = mss()

# loads in reference true crown


frames = 0
avgFPS = 0

while True:
    a = time.time()

    # grabs image and converts to greyscale for processing
    img = numpy.array(sct.grab(monitor))
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        

    cv2.imshow('Gray image', grey)
    cv2.waitKey(1)
    
    b = time.time()
    avgFPS = (avgFPS * frames) + (1 / (b - a))
    frames += 1
    avgFPS = avgFPS / frames
    print("fps: {}".format(avgFPS))



