from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse
import random as rng
from shape_finder import image_maker

rng.seed(12345)


## [findContours]
# Find contours
contours, _ = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
## [findContours]

# Find the rotated rectangles and ellipses for each contour
minRect = [None]*len(contours)
minEllipse = [None]*len(contours)
for i, c in enumerate(contours):
    minRect[i] = cv.minAreaRect(c)
    if c.shape[0] > 5:
        minEllipse[i] = cv.fitEllipse(c)

# Draw contours + rotated rects + ellipses
## [zeroMat]
drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
## [zeroMat]
## [forContour]
for i, c in enumerate(contours):
    color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
    # contour
    cv.drawContours(drawing, contours, i, color)
    # ellipse
    if c.shape[0] > 5:
        cv.ellipse(drawing, minEllipse[i], color, 2)
    # rotated rectangle
    box = cv.boxPoints(minRect[i])
    box = np.intp(box) #np.intp: Integer used for indexing (same as C ssize_t; normally either int32 or int64)
    cv.drawContours(drawing, [box], 0, color)
## [forContour]

## [showDrawings]
# Show in a window
cv.imshow('Contours', drawing)
## [showDrawings]

## [setup]
# Load source image
# parser = argparse.ArgumentParser(description='Code for Creating Bounding rotated boxes and ellipses for contours tutorial.')
# parser.add_argument('--input', help='Path to input image.', default='stuff.jpg')
# args = parser.parse_args()

# src = cv.imread(cv.samples.findFile(args.input))
src = image_maker(1, 1, 1, 2, res=(480,640))

# Convert image to gray and blur it
# src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
src_gray = cv.blur(src, (3,3))
## [setup]

## [createWindow]
# Create Window
source_window = 'Source'
cv.namedWindow(source_window)
cv.imshow(source_window, src)
## [createWindow]
## [trackbar]
max_thresh = 255
thresh = 100 # initial threshold
# cv.createTrackbar('Canny Thresh:', source_window, thresh, max_thresh, thresh_callback)
thresh_callback(thresh)
## [trackbar]

cv.waitKey()