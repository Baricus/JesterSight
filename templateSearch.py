import time

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

    maxX = width - Twidth - 1
    maxY = height - Theight - 1

    # get's nonwhite locations in template
    pixels = np.argwhere(template != 255)

    # brute force search
    minLoc = (0, 0)
    minSum = np.inf

    for x in range(maxX):
        for y in range(maxY):
            locations = pixels + [y, x]
            # this indexing sucked but it works now
            curSum = np.sum(distT[locations[:,0], locations[:,1]])
            if curSum <= minSum:
                minSum = curSum
                minLoc = (x, y)

    if minSum < threshold:
        # shifts minLoc to be the center of the template
        minLoc = (minLoc[0] + int(Twidth/2), minLoc[1] + int(Theight/2))
        return minLoc, minSum
    else:
        return None, minSum


# test code
from distTransform import *
import cv2 as cv
example = cv.imread('example.png')[0:50, 25:120]
template = cv.imread('assets/EdgeMaskSmall.png', cv.IMREAD_GRAYSCALE)

start = time.perf_counter()
dists = dist_transform(example)
end = time.perf_counter()
print("Time to dist_transform is:", end-start)

start = time.perf_counter()
pos, min = templateSearch(dists, template, 250)
end = time.perf_counter()
print("Time to template search is:", end-start)

print("min value of func is:", min)

if pos != None:
    x, y = pos
    show = cv.circle(example, (x, y), 3, (255, 0, 0), 3)
    cv.imshow("test", show)
    cv.waitKey(0)