from main import get_per_region

import cv2
import os
import time

# test code HUD
from dist_transform import *
from template_search import template_search
# from main.py. No circular import

# region test globals

gridImg = list()
gridCount = 0
baseDir = './assets/tests/'
template = cv2.imread('./assets/EdgeMaskSmall.png', cv2.IMREAD_GRAYSCALE)
popDir = os.getcwd()
os.chdir(baseDir)
# allFiles = os.walk(baseDir)
allFiles = os.walk('.')
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
        example = cv2.imread(imagePath)
        height, width, _ = example.shape
        # print(width, height)
        left, top, right, lower = get_per_region(width, height, 2, 0, 4.5, 4.5)
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
            show = cv2.circle(example, pos, 3, (255, 0, 0), 3)
            result = 'yes'
        else:
            # Did not find a position, show image that failed with white circle
            show = cv2.circle(example, (0, 0), 3, (255, 255, 255), 5)
            result = 'no'
        show = cv2.resize(show, (int(pxScale*1.777), pxScale))
        show = cv2.putText(show, result, (0,pxScale), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        if(gridCount >= 120):
            continue
        if(gridCount % gridMod == 0):
            gridImg.append([None]*gridMod)
        # gridImg[gridCount // gridMod].append(show)
        gridImg[gridCount // gridMod][gridCount % gridMod] = show
        gridCount += 1

# def hconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
#     h_min = min(im.shape[0] for im in im_list)
#     im_list_resize = [cv2.resize(im, (int(im.shape[1] * h_min / im.shape[0]), h_min), interpolation=interpolation)
#                       for im in im_list]
#     return cv2.hconcat(im_list_resize)

# def vconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
#     w_min = min(im.shape[1] for im in im_list)
#     im_list_resize = [cv2.resize(im, (w_min, int(im.shape[0] * w_min / im.shape[1])), interpolation=interpolation)
#                       for im in im_list]
#     return cv2.vconcat(im_list_resize)

# def concat_tile_resize(im_list_2d, interpolation=cv2.INTER_CUBIC):
#     im_list_v = [hconcat_resize_min(im_list_h, interpolation=cv2.INTER_CUBIC) for im_list_h in im_list_2d]
#     return vconcat_resize_min(im_list_v, interpolation=cv2.INTER_CUBIC)

# horCon = list()
# for x in gridImg:
#     horCon = np.hstack(x)
#     cv.imshow("grid", horCon)
#     cv.waitKey(0)
# rootCon = np.vstack(horCon)

horCon = cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in gridImg])
# horCon = concat_tile_resize(gridImg)
cv2.imshow("grid", horCon)
cv2.waitKey(0)
# cv.imshow("grid", gridImg)
os.chdir(popDir)