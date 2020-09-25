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
import argparse
from utils.utils import *


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


def find_points_on_circle(img, corners):
    '''
    finds points that are on the circle:
    '''


if __name__ == '__main__':
    # produce sample image
    img, img_color = image_maker(**args)
    cv2.imshow('Original Image', img)

    # find cirlces()
    find_circles(img, img_color)

    # find corners and other critical points and show them with circles.
    corners = find_important_points(img, param=0.4, max_points = 30)
    draw_corners(img.copy(), corners, label='corner points')

    # find squares
    square_corners = find_squares(img, img_color, corners)
    # update corners once squares are found
    for i in square_corners:
        corners.remove(i)
    draw_corners(img.copy(), corners, label='critical points with no square')

    # # find triangles
    # find_triangles(img, img_color, corners)


    # cv2.imshow('Hough Linear', img)
    # find_shapes(img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()