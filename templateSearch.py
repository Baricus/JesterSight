import cv2
import numpy as np

def templateSearch(distT, template, threshold):
    """
    templateSearch

    Takes in the distance transform of an image and
    returns the location of the template in the image
    if it is below the threshold
    :param distT: the distance transform of an image
    :param template: the template kernel (greyscale)
    :return: (x,y) if in the threshold or None
    """
    # compute search space (all template positions)
    height, width = distT.shape
    Theight, Twidth = template.shape

    maxX = width - Twidth
    maxY = height - Theight

    # get's nonwhite locations in template
    pixels = np.argwhere(template != 255)

    # brute force search
    minLoc = (0, 0)
    minSum = np.inf

    for x in range(maxX):
        for y in range(maxY):
            locations = pixels + [y,x]
            print(locations)
            print("---------")
            curSum = np.sum(distT[locations])
            if curSum < minSum:
                minSum = curSum
                minLoc = (x, y)

    if minSum < threshold:
        return minLoc
    else:
        return None


# test code
from distTransform import *
example = cv.imread('example.png')[0:100, 0:200]
dists = dist_transform(example)
template = cv.imread('assets/EdgeMaskSmall.png', cv.IMREAD_GRAYSCALE)

pos = templateSearch(dists, template, 100000000000)
if pos != None:
    x, y = pos
    show = cv.circle(example, (y, x), 3, (255, 0, 0), 3)
    cv.imshow("test", show)
    cv.waitKey(0)