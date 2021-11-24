import cv2 as cv
import numpy as np

LEFT = [50, 37, 35] #Color of the left side of the crown
RIGHT = [33, 23, 21] #Color of the right side of the crown

#Note: When passing in x and y points, you need to be very careful.
#I tried it with a larger MOE but it was returning true even though it was not the crown.

 
def color_check(img, xpos, ypos):
    #This functions takes in an image being looked at and 
    #the center point of what we believe is potentially the crown.
    #The output is false if the color to the left and right of the given point 
    #does not match the color of the crown or the output is true if the color 
    #to he left and right of the given point matches the color of the crown
    height, width, channels = img.shape
    if xpos < 3 or xpos > width-3:
        return False
    if ypos < 3 or ypos > height-3:
        return False

    # grabs 2 3x3 patches to left and right of crown by 3 spaces
    lpatch = img[ypos-1:ypos+2,xpos-5:xpos-2]
    rpatch = img[ypos-1:ypos+2,xpos+3:xpos+6]

    l_hsv = cv.cvtColor(lpatch, cv.COLOR_BGR2HSV)
    lowerY = np.array([20, 80, 100])
    upperY = np.array([30, 200, 255])
    mYellow = cv.inRange(l_hsv, lowerY, upperY)

    r_hsv = cv.cvtColor(rpatch, cv.COLOR_BGR2HSV)
    lowerR = np.array([0, 140, 100])
    upperR = np.array([20, 220, 255])
    mRed = cv.inRange(r_hsv, lowerR, upperR)

    if np.average(mYellow) > 200 and np.average(mRed) > 200:
        return True
    return False

#Code used to test funcion
#This will display all the available mouse click events  
#events = [i for i in dir(cv) if 'EVENT' in i]
#print(events)
#img = cv.imread('example2.png')

#def click_event(event, x, y, flags, params):

    #right-click event value is 2
    #if event == cv.EVENT_LBUTTONDOWN:
        #print (color_check(img, x, y))
        #print (img[ x, y])
        
#print(img[182, 345]) #right
#print(img[160, 345]) #left

#cv.imshow("image", img)
#cv.namedWindow('image')
#cv.setMouseCallback("image", click_event)
#cv.waitKey(0)