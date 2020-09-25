# USAGE:
# default parameters:
#   python shape_finder.py
# custom parameters:
#   python shape_finder.py --circles 3 --squares 4 --triangles 3 --seed 823
# simplified parameters values
#   python shape_finder.py -c 3 -sq 4 -t 3 -sd 823
#
# Create by Mehrdad Pourfathi
# Date: 9/23/2020

# import modules
import numpy as np
import cv2
import argparse
from utils.general_utils import *


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


if __name__ == '__main__':
    # produce sample image
    img, img_color = image_maker(**args)
    cv2.imshow('Original Image', img)

    # find cirlces()
    circles = find_circles(img, img_color, block_size=1.6)
    # print(circles)

    # find corners and other critical points and show them with circles.
    corners = find_corner_points(img, quality=0.1, max_points=30, min_dist=10)
    draw_corners(img.copy(), corners, label='corner points')

    # remove points on the circle
    find_points_on_circle(img, corners, circles)

    # find squares
    square_corners = find_squares(img, img_color, corners)
    # update corners once squares are found
    for i in square_corners:
        corners.remove(i)
    draw_corners(img.copy(), corners, label='critical points with no square')

    # find triangles (to be completed)
    # find_triangles(img, img_color, corners)

    cv2.waitKey(0)
    cv2.destroyAllWindows()