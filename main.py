from mss import mss
import time
import cv2 as cv
import numpy as np

def detect(img1, img2):
    


# sets monitor positions and initializes mss
monitor = {"top": 0, "left": 0, "width": 160, "height": 135}
sct = mss()

# loads in reference true crown
crown = np.array(cv.imread(cv.samples.findFile('crown.png'), cv.IMREAD_GRAYSCALE))

frames = 0
avgFPS = 0

while True:
    a = time.time()

    # grabs image and converts to greyscale for processing
    img = np.array(sct.grab(monitor))
    grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    detect(crown, grey)
    
    b = time.time()
    avgFPS = (avgFPS * frames) + (1 / (b - a))
    frames += 1
    avgFPS = avgFPS / frames
    print("fps: {}".format(avgFPS))



