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

def templateSearchUI(distT, template, threshold, screenDim):
    """
    templateSearchUI

    Takes in the distance transform of an image and
    returns the location of the template in the image
    if it is below the threshold
    :param distT: the distance transform of an image
    :param template: the template kernel (greyscale)
    :param threshold: TODO
    :param screenDim: overall dimensions of screen
    :return: (x,y) if in the threshold or None
    """
    # compute search space (all template positions)
    height, width = distT.shape
    sHeight, sWidth = screenDim
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
# from distTransform import *
# import cv2 as cv
# example = cv.imread('example.png')[0:50, 25:120]
# template = cv.imread('assets/EdgeMaskSmall.png', cv.IMREAD_GRAYSCALE)
#
# start = time.perf_counter()
# dists = dist_transform(example)
# end = time.perf_counter()
# print("Time to dist_transform is:", end-start)
#
# start = time.perf_counter()
# pos, min = template_search(dists, template, 250)
# end = time.perf_counter()
# print("Time to template search is:", end-start)
#
# print("min value of func is:", min)
#
# if pos != None:
#     x, y = pos
#     show = cv.circle(example, (x, y), 3, (255, 0, 0), 3)
#     cv.imshow("test", show)
#     cv.waitKey(0)


# test code HUD
from distTransform import *
# from main.py. No circular import
def top_left_region(width, height):
    left = width * (2 / 100)  # 2% from the left
    top = height * (0 / 100)  # 0% from the top
    right = left + (width * (4.5 / 100)) # +4.5% right
    lower = top + (height * (4.5 / 100)) # +4.5% down
    return int(left), int(top), int(right), int(lower)

import cv2 as cv
import os
gridImg = list()
gridCount = 0
baseDir = './assets/tests/'
template = cv.imread('./assets/EdgeMaskSmall.png', cv.IMREAD_GRAYSCALE)
popDir = os.getcwd()
os.chdir(baseDir)
# allFiles = os.walk(baseDir)
allFiles = os.walk('.')
# region test globals

pxScale = 75
gridMod = 15

# endregion test globals

for root, dirs, files in allFiles:
    path = root.split(os.sep)
    # print((len(path) - 1) * '---', os.path.basename(root))
    for itFile in files:
        if(not itFile.endswith(('.jpg', '.png')) or os.path.isdir(itFile)):
            continue
        imagePath = '/'.join(path) + '/' + itFile
        print(imagePath)
        example = cv.imread(imagePath)
        height, width, _ = example.shape
        # print(width, height)
        left, top, right, lower = top_left_region(width, height)
        example = example[top:lower, left:right]
        start = time.perf_counter()
        dists = dist_transform(example)
        end = time.perf_counter()
        print("Time to dist_transform is:", end-start)
        start = time.perf_counter()
        pos, min = templateSearch(dists, template, 250)
        end = time.perf_counter()
        print("Time to template search is:", end-start)
        print("min value of func is:", min)
        result = ''
        if pos != None:
            # x, y = pos
            show = cv.circle(example, pos, 3, (255, 0, 0), 3)
            result = 'crown'
        else:
            # Did not find a position, show image that failed with white circle
            show = cv.circle(example, (0, 0), 3, (255, 255, 255), 5)
            result = 'no-crown'
        show = cv.resize(show, (int(pxScale*1.777), pxScale))
        show = cv.putText(show, result, (0,pxScale), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        if(gridCount >= 120):
            continue
        if(gridCount % gridMod == 0):
            gridImg.append([None]*gridMod)
        # gridImg[gridCount // gridMod].append(show)
        gridImg[gridCount // gridMod][gridCount % gridMod] = show
        gridCount += 1

def hconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    h_min = min(im.shape[0] for im in im_list)
    im_list_resize = [cv2.resize(im, (int(im.shape[1] * h_min / im.shape[0]), h_min), interpolation=interpolation)
                      for im in im_list]
    return cv2.hconcat(im_list_resize)

def vconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    w_min = min(im.shape[1] for im in im_list)
    im_list_resize = [cv2.resize(im, (w_min, int(im.shape[0] * w_min / im.shape[1])), interpolation=interpolation)
                      for im in im_list]
    return cv2.vconcat(im_list_resize)

def concat_tile_resize(im_list_2d, interpolation=cv2.INTER_CUBIC):
    im_list_v = [hconcat_resize_min(im_list_h, interpolation=cv2.INTER_CUBIC) for im_list_h in im_list_2d]
    return vconcat_resize_min(im_list_v, interpolation=cv2.INTER_CUBIC)
# horCon = list()
# for x in gridImg:
#     horCon = np.hstack(x)
#     cv.imshow("grid", horCon)
#     cv.waitKey(0)
# rootCon = np.vstack(horCon)

horCon = cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in gridImg])
# horCon = concat_tile_resize(gridImg)
cv.imshow("grid", horCon)
cv2.waitKey(0)
# cv.imshow("grid", gridImg)
os.chdir(popDir)
