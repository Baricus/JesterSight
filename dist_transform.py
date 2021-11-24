import math
import numpy as np
import cv2 as cv


def dist_transform(img):
    """
    takes in an image and computes it's
    distance transform with a 2 pass algorithm.
    This is probably too slow so using cv2's
    implementation in the final is probably good
    :param img: an image to calculate the transform on
    :return: the distance transform of img
    """
    height = img.shape[0]
    width = img.shape[1]

    # get's edges using cv2 canny
    # values set by hand based on example.png
    edges = np.zeros((height, width))
    dists = np.copy(edges)
    edges = cv.Canny(img, 150, 250)
    # modifies edges to dist transform
    dists[edges != 255] = 255
    dists[edges == 255] = 0

    # computes distance transform (manhattan)
    for y in range(height):
        for x in range(width):
            L = math.inf
            U = math.inf
            if x != 0:
                L = dists[y][x - 1]
            if y != 0:
                U = dists[y - 1][x]
            dists[y][x] = min(L + 1, U + 1, dists[y][x])

    for y in range(height - 1, -1, -1):
        for x in range(width - 1, -1, -1):
            L = math.inf
            U = math.inf
            if x != width - 1:
                L = dists[y][x + 1]
            if y != height - 1:
                U = dists[y + 1][x]
            dists[y][x] = min(L + 1, U + 1, dists[y][x])

    return dists

def dist_transform_cv2(img):
    """
    computes the distance transform using cv2
    fully.  This computes the canny edges and then
    passes those into the distance transform of cv2

    :param img: the image to compute the transform
    :return: a cv2 distance transform
    """

    height = img.shape[0]
    width = img.shape[1]

    # get's edges using cv2 canny
    # values set by hand based on example.png
    edges = np.zeros((height, width), dtype="uint8")
    dists = np.copy(edges)
    edges = cv.Canny(img, 150, 250)

    # modifies edges to dist transform
    dists[edges != 255] = 255
    dists[edges == 255] = 0

    dists = cv.distanceTransform(dists, cv.DIST_L1, 5)

    return dists

# example use
# dists = dist_transform(cv.imread('example.png')[0:100, 0:200])
# dists2 = dist_transform_cv2(cv.imread('example.png')[0:100, 0:200])
# cv.imshow('myDist', dists/dists.max())
# cv.imshow('cv2Dist', (dists2/dists2.max()))
# cv.waitKey(0)