# USAGE:
# default parameters:
#   python shape_finder.py
# custom parameters:
#   python shape_finder.py --circles 2 --squares 2 --triangles 2 --seed 0
# simplified parameters values
#   python shape_finder.py -c 2 -sq 2 -t 2 -sd 0
#
# Create by Mehrdad Pourfathi
# Date: 9/23/2020

# import modules
import numpy as np
import cv2
# import skimage.segmentation as seg
import logging
import argparse
import matplotlib.pyplot as plt
import active_contour

# setup log configuration.
logging.basicConfig(level=logging.DEBUG, filemode='w', filename='ouptut.log')

# construct argument parser
ap = argparse.ArgumentParser()
ap.add_argument('-c', '--circles', default=0,
                help="number of circles, default is 0")
ap.add_argument('-sq', '--squares', default=1, 
                help="number of rectangles, default is 1")
ap.add_argument('-t', '--triangles', default=0, 
                help="number of triangles, default is 0")
ap.add_argument('-sd', '--seed', type=int, default=1,
                help="seed for random generator, default is 1")
args = vars(ap.parse_args())


def image_maker(circles, squares, triangles, seed, res=(480,640)):
    '''
    creates a black and white image made with randomly placed circles,
    squares and triangles with borders and white background.
    '''
    # initialize image
    img = np.ones(res, dtype = "uint8")*255
    # set seed value
    np.random.seed(int(seed))
    # put random circles
    for i in range(int(circles)):
        # select the position and radius of the circles with uniform distribution.
        x = np.random.randint(100,540)
        y = np.random.randint(100,380)
        r = np.random.randint(50,100)
        cv2.circle(img, (x,y), r, 0, 1)
    # put random rectangles
    for i in range(int(squares)):
        # randomly select the edges of the rectangle
        x = np.random.randint(100,540,1)
        y = np.random.randint(100,380,1)
        d = np.random.randint(50,150,1)
        cv2.rectangle(img, (x, x+d), (y, y+d), 0,   1)
    # put random triangles
    for i in range(int(triangles)):
        # randomly select 3 vertices to generate a triangle.
        vertices = np.random.randint(40, 480, (3,2))
        cv2.drawContours(img, [vertices], 0, 0, 1)

    return img


def laplacian_filter(img):
    '''
    Applies a 2D laplacian filter on the image
    '''
    kernel = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], dtype=np.float32)
    img = cv2.filter2D(img, -1, kernel)

    return img


def segment_shapes(img):
    '''
    segment circles, rectangles and triangles and draw their boundaries.
    '''
    # find corders and points crossing points.
    corners = cv2.goodFeaturesToTrack(img, 30, 0.2, 5)
    for corner in corners:
        x,y = corner.ravel()
        cv2.circle(img,(x,y),5,255,-1)

        contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Find the rotated rectangles and ellipses for each contour
        minRect = [None]*len(contours)
        minEllipse = [None]*len(contours)
        for i, c in enumerate(contours):
            minRect[i] = cv2.minAreaRect(c)
            if c.shape[0] > 5:
                minEllipse[i] = cv2.fitEllipse(c)

        # Draw contours + rotated rects + ellipses
        ## [zeroMat]
        drawing = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
        ## [zeroMat]
        ## [forContour]
        for i, c in enumerate(contours):
            color = (0,0,255)
            # contour
            cv2.drawContours(drawing, contours, i, color)
            # ellipse
            if c.shape[0] > 5:
                cv2.ellipse(drawing, minEllipse[i], color, 2)
            # rotated rectangle
            box = cv2.boxPoints(minRect[i])
            box = np.intp(box) #np.intp: Integer used for indexing (same as C ssize_t; normally either int32 or int64)
            cv2.drawContours(drawing, [box], 0, color)
        ## [forContour]

        ## [showDrawings]
        # Show in a window
        cv2.imshow('Contours', drawing)
        ## [showDrawings]
        return img



    return img


if __name__ == '__main__':
    # produce sample image
    
    img = image_maker(**args)
    cv2.imshow('Original Image', img)

    # find edges with laplacian filter
    # img = laplacian_filter(img)
    # cv2.imshow('Laplacian Image', img)

    # apply segmentation
    img = segment_shapes(img)
    # cv2.imshow('Hough Linear', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()