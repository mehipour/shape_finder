# utility functions

# import dependencies
import numpy as np
import cv2
import itertools
from utils.square_utils import *


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


def find_corner_points(image, quality=0.3, max_points = 30, min_dist = 10):
    '''
    Use Shi-Tomasi Corner Detector to find corners and important points
    '''
    corners = cv2.goodFeaturesToTrack(image, max_points, quality, min_dist)
    corners = [list(i.ravel()) for i in corners] 

    return corners


def draw_corners(image, corners, label='corners'):
    '''
    draws corners.
    '''
    for corner in corners:
        x,y = corner[0], corner[1]
        cv2.circle(image, (x,y), 5 , 0, -1)
    cv2.imshow(label, image)


def find_squares(img, image_color, corners):
    '''
    Find squares, takes an image and returns all the corners that build a square.
    Also draws the squares.
    '''
    square_corners = set()
    
    # select four points 
    for pts in itertools.permutations(corners, 4):
        p = np.array(pts, np.int32)
        img_square = img.copy()
        # create a polygon with 4 points
        img_square = cv2.polylines(img_square, [p], True, (0,255,0), thickness=3)
        perimeter = cv2.arcLength(p, True)
        approx = cv2.approxPolyDP(p, 0.1 * perimeter, True)
        # create the convex hull of the polygon
        squares = cv2.convexHull(approx)

        # check if the select points make a square
        if len(approx) == 4 and check_if_square(approx, 0.1, [87, 93]):
            cv2.drawContours(image_color, [squares], 0, (0,255,0), 4)
            # store points if they make square
            for i in p:
                square_corners.add(tuple(i))
    # show squares
    cv2.imshow('squares', image_color)
    # convert set to list
    square_corners = [list(i) for i in square_corners]

    return square_corners


def find_circles(img, img_color, block_size=1.6):
    '''
    find cirlces using Circle Hough Transform
    '''

    # apply circle hough transform
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, block_size, 100)

    # draw circles
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(img_color, (x, y), r, (0, 0, 255), 4)
        # show the output image
        cv2.imshow("circles", img_color)

    return circles

# function incomplete
# def find_triangles(img, image_color, corners):
#     '''
#     Find triangles, takes an image and returns all the corners that build a square.
#     Also draws the triangles.
#     '''
#     triangle_corners = set()
    
#     # select four points 
#     for pts in itertools.permutations(corners, 3):
#         p = np.array(pts, np.int32)
#         img_square = img.copy()
#         # create a polygon with 4 points
#         img_square = cv2.polylines(img_square, [p], True, (0,255,0), thickness=3)
#         perimeter = cv2.arcLength(p, True)
#         approx = cv2.approxPolyDP(p, 0.1 * perimeter, True)
#         # create the convex hull of the polygon
#         triangles = cv2.convexHull(approx)

#         # check if the select points make a square
#         if len(approx) == 3:
#             cv2.drawContours(img_color, [triangles], 0, (255,0,0), 1)
#             # store points if they make square
#             for i in p:
#                 triangle_corners.add(tuple(i))
#     cv2.imshow('triangles', img_color)
#     triangle_corners = [list(i) for i in triangle_corners]

#     return triangle_corners
