import cv2 as cv
import math
import numpy as np

def hough_transform(img):
    #We are taking in an image as a parameter
    #This image does not have to be black and white
        
    #Getting edges 
    edges = cv.Canny(img, 50, 150, apertureSize = 3)
    
    #Computing the (x1, y1) and (x2, y2) values of the edges detected above
    lines_found = cv.HoughLinesP(edges, 1, np.pi / 180, 100,10)
    
    #For each line found, we will plot the line onto the image passed in
    for i in lines_found:    
        x1,y1,x2,y2 = i[0]
        cv.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
    #cv.imwrite('detected_lines.png', img)
    return img, lines_found

#Code used to test above function
#img = cv.imread('example.png')
#img = hough_transform(img)