# general utility functions to check if contour is square

# import dependencies
import numpy as np
import cv2


def find_contour_center(c):  
    ''' 
    finds the center of a contour
    '''
    M = cv.moments(c)
    x = int((M["m10"] / M["m00"]))
    y = int((M["m01"] / M["m00"]))
    return (x, y)


def pixel_distance(a, b):
    ''' 
    distance between two points in pixels
    '''
    return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


def inner_product(ab, ac):
    ''' 
    inner product of two vectors
    '''
    return ac[0]*ab[0] + ac[1]*ab[1]


def create_vector(a,b):
    ''' 
    takes two sides and create a vector
    '''
    return [b[0]-a[0], b[1]-a[1]]


def find_angle(ab, ac):
    ''' 
    cosine of angle between vectors ab and ac
    '''
    ab_length = np.sqrt(inner_product(ab, ab))
    ac_length = np.sqrt(inner_product(ac, ac))
    # add a small value to the denominator to avoid division by 0
    epsilon = 1e-2
    cos_theta = inner_product(ab, ac) / ((ab_length * ac_length) + epsilon)

    return np.arccos(cos_theta)/np.pi*180


def find_min_max_xy(xy_list):
    ''' 
    given a list find of (x,y)'s find min of x and y
    '''
    min_x = min(xy_list, key=lambda x:x[0])[0]
    max_x = max(xy_list, key=lambda x:x[0])[0]
    min_y = min(xy_list, key=lambda x:x[1])[1]
    max_y = max(xy_list, key=lambda x:x[1])[1]
    return min_x, min_y, max_x, max_y


def sort_corners(pnts):
    ''' 
    sort corners clock-wise from bottom-left
    '''
    a = pnts[0][0]
    b = pnts[1][0]
    c = pnts[2][0]
    d = pnts[3][0]
    # find min and max of x and y
    min_x, min_y, max_x, max_y = find_min_max_xy([a,b,c,d])

    # find bottom left point
    min_distance = np.inf
    for pnt in [a,b,c,d]:
        cur_distance = pixel_distance([min_x, min_y] ,pnt)
        if min_distance > cur_distance:
            bottom_left = pnt
            min_distance = cur_distance

    # find top left point
    min_distance = np.inf
    for pnt in [a,b,c,d]:
        cur_distance = pixel_distance([min_x, max_y] ,pnt)
        if min_distance > cur_distance:
            top_left = pnt
            min_distance = cur_distance

    # find top right point
    min_distance = np.inf
    for pnt in [a,b,c,d]:
        cur_distance = pixel_distance([max_x, max_y] ,pnt)
        if min_distance > cur_distance:
            top_right = pnt
            min_distance = cur_distance

    # find bottom right point
    min_distance = np.inf
    for pnt in [a,b,c,d]:
        cur_distance = pixel_distance([max_x, min_y] ,pnt)
        if min_distance > cur_distance:
            bottom_right = pnt
            min_distance = cur_distance

    return [bottom_left, top_left, top_right, bottom_right]


def find_sides(sorted_corners):
    ''' 
    find four sides
    '''
    sorted_sides = []
    sorted_sides.append(create_vector(sorted_corners[0],sorted_corners[1]))
    sorted_sides.append(create_vector(sorted_corners[1],sorted_corners[2]))
    sorted_sides.append(create_vector(sorted_corners[2],sorted_corners[3]))
    sorted_sides.append(create_vector(sorted_corners[3],sorted_corners[0]))

    return sorted_sides


def find_side_lengths(sorted_corners):
    ''' 
    find length of sides
    '''
    dst = []
    dst.append(pixel_distance(sorted_corners[0], sorted_corners[1]))
    dst.append(pixel_distance(sorted_corners[1], sorted_corners[2]))
    dst.append(pixel_distance(sorted_corners[2], sorted_corners[3]))
    dst.append(pixel_distance(sorted_corners[3], sorted_corners[0]))

    return dst


def find_poly_angles(sorted_sides):
    ''' 
    find angles
    '''
    angles = []
    angles.append(find_angle(sorted_sides[0], sorted_sides[1]))
    angles.append(find_angle(sorted_sides[1], sorted_sides[2]))
    angles.append(find_angle(sorted_sides[2], sorted_sides[3]))
    angles.append(find_angle(sorted_sides[3], sorted_sides[0]))

    return angles


def check_if_square(approx_cnt, side_tol=0.1, angle_tol=[70,100]):
    ''' 
    helper function to check approxiated contour is square
    '''
    result = False
    # sort sides and angles
    sorted_corners = sort_corners(approx_cnt)
    sorted_sides = find_sides(sorted_corners)
    side_lengths = find_side_lengths(sorted_corners)
    angles = find_poly_angles(sorted_sides)

    # check if rectangular
    if min(angles) > angle_tol[0] and max(angles) < angle_tol[1]:
        # check if square (sides are close)
        side_lengths = np.array(side_lengths)
        tol = side_lengths.mean()*side_tol
        result = np.allclose(side_lengths, side_lengths.mean(), atol = tol)

    return result