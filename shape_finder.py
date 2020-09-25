# USAGE:
# default parameters:
#   python shape_finder.py
# custom parameters:
#   python shape_finder.py --circles 2 --squares 2 --triangles 1 --seed 0
# simplified parameters values
#   python shape_finder.py -c 2 -sq 2 -t 1 -sd 823
#
# Create by Mehrdad Pourfathi
# Date: 9/23/2020

# import modules
import numpy as np
import cv2
# import skimage.segmentation as seg
import argparse
import active_contour
import itertools
from utils import *
import time


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
    img_color = np.ones((res[0], res[1], 3), dtype = "uint8")*255
    # set seed value
    np.random.seed(int(seed))
    # put random circles
    for i in range(int(circles)):
        # select the position and radius of the circles with uniform distribution.
        x = np.random.randint(100,380)
        y = np.random.randint(100,430)
        r = np.random.randint(40,80)
        cv2.circle(img_color, (x,y), r, 0, 1)
    # put random rectangles
    for i in range(int(squares)):
        # randomly select the edges of the rectangle
        x = np.random.randint(100,380,1)
        y = np.random.randint(100,430,1)
        d = np.random.randint(40,80,1)
        cv2.rectangle(img_color, (x, x+d), (y, y+d), 0, 1)
    # put random triangles
    for i in range(int(triangles)):
        # randomly select 3 vertices to generate a triangle.
        vertices = np.random.randint(40, 480, (3,2))
        cv2.drawContours(img_color, [vertices], 0, 0, 1)

    # return the grau scale image
    img = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

    return img, img_color


def find_important_points(image, param=0.4, max_points = 30):
    '''
    find corner and cross points
    '''
    corners = cv2.goodFeaturesToTrack(img, max_points, param, 5)
    corners = [list(i.ravel()) for i in corners] 
    return image, corners

def draw_corners(image, corners, label='corners'):
    '''
    draws corners.
    '''
    for corner in corners:
        x,y = corner[0], corner[1]
        cv2.circle(image, (x,y),5,0,-1)
    cv2.imshow(label, image)
    # return image


def find_squares(img, image_color, corners):
    '''
    find squares. 
    '''
    new_corners = []
    # select four points 
    for pts in itertools.permutations(corners, 4):
        list_of_four_corners = [[list(pp.ravel()) for pp in pts]]
        # print(pts)
        p = np.array(list_of_four_corners, np.int32)
        img_square = img.copy()
        # create a polygon with 4 points
        img_square = cv2.polylines(img_square, [p], True, (0,255,0), thickness=3)
        perimeter = cv2.arcLength(p, True)
        approx = cv2.approxPolyDP(p, 0.1 * perimeter, True)
        # create the convex hull of the polygon
        squares = cv2.convexHull(approx)
        # check if square
        if len(approx) == 4 and check_if_square(approx, 0.1, [87, 93]):
            cv2.drawContours(img_color, [squares], 0, (0,255,0), 1)
        else:
            # add points to new corner list
            for i in list_of_four_corners:
                if i not in new_corners:
                    new_corners.append(i)
    cv2.imshow('squares', img_color)
    return new_corners


def circle_finder(img, img_color):
    '''
    find cirlces using Circle Hough Transform
    '''
    # copy output
    output = np.ones_like(img)*255

    # find circles
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 2, 30)

    # draw circles
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(output, (x, y), r, (0, 0, 255), 4)
        # subtraction_img = cv2.erode()
        # # show the output image
        cv2.imshow("output", output)

    return circles, output


if __name__ == '__main__':
    # produce sample image
    img, img_color = image_maker(**args)
    cv2.imshow('Original Image', img)

    # find corners and other critical points and show them with circles.
    image = img.copy()
    img, find_important_points(imagimagee, param=0.4, max_points = 30):


    print(corners)
    # find rectangles.
    # new_corners = find_squares(img, img_color, corners)
    # print(len(new_corners))
    # show critical points without the squares.
    # draw_corners(img.copy(), new_corners, label='critical points with no square')

    # cv2.imshow('Hough Linear', img)
    # find_shapes(img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()