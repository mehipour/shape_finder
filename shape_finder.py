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


def create_template(img, img_color):
    template_image = np.ones_like(img, dtype='uint8')*255
    template_image = cv2.rectangle(template_image, (240, 320),(240, 320), 0, 1)
    contours, hierarchy = cv2.findContours(template_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    print(hierarchy)
    # remove the alrgest contour since it is the picture's frame
    contours = sorted(contours, key=cv2.contourArea, reverse=False)[:-1]

    for c in contours:
        template_contour = cv2.convexHull(c)
        # cv2.drawContours(img_color,[template_contour],0,(0,255,0),2)
    # cv2.matchShapes(contour template, contour method, method parameter)

    # find contours in the image
    contours, _ = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=False)[:-1]

    for c in contours:
        match = cv2.matchShapes(template_contour, c, 1, 0.0)
        print(match)
        if 0.01 < match < 5:
            cv2.drawContours(img_color,[c],0,(0,255,0),2)
            cv2.imshow('matched shapes', img_color)

         # continue video feed until 'q' is pressed
        key = cv2.waitKey(1) & 0xFF
        # if 'n' is pressed count side go to new side
        if key == ord('n'):
            continue

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
        x = np.random.randint(100,540)
        y = np.random.randint(100,380)
        r = np.random.randint(20,50)
        cv2.circle(img_color, (x,y), r, 0, -1)
    # put random rectangles
    for i in range(int(squares)):
        # randomly select the edges of the rectangle
        x = np.random.randint(100,540,1)
        y = np.random.randint(100,380,1)
        d = np.random.randint(20,50,1)
        cv2.rectangle(img_color, (x, x+d), (y, y+d), 0, -1)
    # put random triangles
    for i in range(int(triangles)):
        # randomly select 3 vertices to generate a triangle.
        vertices = np.random.randint(40, 480, (3,2))
        cv2.drawContours(img_color, [vertices], 0, 0, -1)

    # return the grau scale image
    img = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

    return img, img_color


def laplacian_filter(img):
    '''
    Applies a 2D laplacian filter on the image
    '''
    kernel = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], dtype=np.float32)
    img = cv2.filter2D(img, -1, kernel)

    return img


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


def segment_shapes(img):
    '''
    segment circles, rectangles and triangles and draw their boundaries.
    '''


    # find corders and points crossing points.
    # corners = cv2.goodFeaturesToTrack(img, 30, 0.2, 5)
    # for corner in corners:
    #     x,y = corner.ravel()
    #     cv2.circle(img,(x,y),5,255,-1)

    #     contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #     # Find the rotated rectangles and ellipses for each contour
    #     minRect = [None]*len(contours)
    #     minEllipse = [None]*len(contours)
    #     for i, c in enumerate(contours):
    #         minRect[i] = cv2.minAreaRect(c)
    #         if c.shape[0] > 5:
    #             minEllipse[i] = cv2.fitEllipse(c)

    #     # Draw contours + rotated rects + ellipses
    #     ## [zeroMat]
    #     drawing = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    #     ## [zeroMat]
    #     ## [forContour]
    #     for i, c in enumerate(contours):
    #         color = (0,0,255)
    #         # contour
    #         cv2.drawContours(drawing, contours, i, color)
    #         # ellipse
    #         if c.shape[0] > 5:
    #             cv2.ellipse(drawing, minEllipse[i], color, 2)
    #         # rotated rectangle
    #         box = cv2.boxPoints(minRect[i])
    #         box = np.intp(box) #np.intp: Integer used for indexing (same as C ssize_t; normally either int32 or int64)
    #         cv2.drawContours(drawing, [box], 0, color)
    #     ## [forContour]

    #     ## [showDrawings]
    #     # Show in a window
    #     cv2.imshow('Contours', drawing)
        ## [showDrawings]

    return img


if __name__ == '__main__':
    # produce sample image
    
    
    img, img_color = image_maker(**args)
    cv2.imshow('Original Image', img)

    # find edges with laplacian filter
    # img = laplacian_filter(img)
    # cv2.imshow('Laplacian Image', img)

    # apply segmentation
    circles, output = circle_finder(img, img_color)

    # cv2.imshow('Hough Linear', img)
    create_template(img, img_color)

    cv2.waitKey(0)
    cv2.destroyAllWindows()