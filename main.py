from mss import mss
from apscheduler.schedulers.background import BackgroundScheduler
import time
import cv2 as cv
import numpy as np

def detect(img):
    #converts to HSV
    hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # masks against both yellow and red
    lowerY = np.array([20, 80, 100])
    upperY = np.array([30, 200, 200])
    mYellow = cv.inRange(hsv_img, lowerY, upperY)

    lowerR = np.array([0, 150, 120])
    upperR = np.array([20, 220, 200])
    mRed = cv.inRange(hsv_img, lowerR, upperR)

    # combines for a true crown mask
    mTot = mRed+mYellow

    # takes mean of pixels in each mask (we only care about channel 0)
    channelsY = cv.mean(mYellow)
    channelsR = cv.mean(mRed)

    # prints the masks and original image (debug)
    print(channelsY[0], channelsR[0])
    cv.imshow('Matches', mTot)
    #cv.imshow('orig', img)
    cv.waitKey(1)
    
    if (channelsY[0] > 50 and channelsR[0] > 50):
        return True
    return False

# 
def beep():
    print("BEEP")


# sets monitor positions and initializes mss
monitor = {"top": 8, "left": 40, "width": 65, "height": 27}
sct = mss()

# sets up the scheduler for the timer
scheduler = BackgroundScheduler()
beepJob = scheduler.add_job(beep, 'interval', seconds=22, id='main_beep')
beepJob.pause()
isRunning = False;
scheduler.start()

# counter for max misses
counter = 100

while True:
    a = time.time()

    # grabs image and converts to greyscale for processing
    img = np.array(sct.grab(monitor))
    #grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # if we don't find the image 100 "frames" in a row, about 1 sec,
    # stop the timer
    if detect(img):
        counter = 100
    else:
        counter -= 1

    if counter <= 0:
        counter = 0
        beepJob.pause()
        isRunning = False
    else:
        if not isRunning:
            beepJob.resume()
            isRunning = True
