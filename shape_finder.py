# USAGE:
# default parameters:
#   python shape_finder.py
# custom parameters:
#   python shape_finder.py --circles 2 --rectangles 2 --triangles 2 --seed 0
# simplified parameters values
#   python shape_finder.py -c 2 -r 2 -t 2 -s 0
#
# Create by Mehrdad Pourfathi
# Date: 9/23/2020

# import modules
import numpy as np
import cv2
import skimage.segmentation as seg
import argparse
import matplotlib.pyplot as plt

# construct argument parser
ap = argparse.ArgumentParser()
ap.add_argument('-c', '--circles', default=0,
                help="number of circles, default is 0")
ap.add_argument('-r', '--rectangles', default=1, 
                help="number of rectangles, default is 1")
ap.add_argument('-t', '--triangles', default=0, 
                help="number of triangles, default is 0")
ap.add_argument('-s', '--seed', type=int, default=1,
                help="seed for random generator, default is 1")
args = vars(ap.parse_args())


def image_maker(n_circles, n_rectangles, n_triangles, res=(480,640)):
    '''
    creates a black and white image made with randomly placed circles,
    rectangles and triangles with borders and white background.
    '''
    # initialize image
    img = np.ones(res, dtype = "uint8")*255
    # set seed value
    np.random.seed(int(args['seed']))
    # put random circles
    for i in range(int(n_circles)):
        # select the position and radius of the circles with uniform distribution.
        x = np.random.randint(100,540)
        y = np.random.randint(100,380)
        r = np.random.randint(30,100)
        cv2.circle(img, (x,y), r, 0, 1)
    # put random rectangles
    for i in range(int(n_rectangles)):
        # randomly select the edges of the rectangle
        x = np.random.randint(20,620,2)
        y = np.random.randint(20,460,2)
        cv2.rectangle(img, (min(x), max(x)), (min(y), max(y)), 0, 1)
    # put random triangles
    for i in range(int(n_triangles)):
        # randomly select 3 vertices to generate a triangle.
        vertices = np.random.randint(20,480,(3,2))
        cv2.drawContours(img, [vertices], 0, 0, 1)

    return img


def laplacian_filter(img):
    '''
    Applies a 2D laplacian filter on the image
    '''
    kernel = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], dtype=np.float32)
    img = cv2.filter2D(img, cv2.CV_32F, kernel)
    return img


def circle_points(resolution, center, radius):
    """
    Generate points which define a circle on an image.Centre refers to the centre of the circle
    """   
    radians = np.linspace(0, 2*np.pi, resolution)
    c = center[1] + radius*np.cos(radians)
    r = center[0] + radius*np.sin(radians)

    return np.array([c, r]).T


def segment_shapes(img):
    '''
    segment circles, rectangles and triangles and draw their boundaries.
    '''
    # laplacian transform
    # img = cv2.distanceTransform(img.astype('uint8'), cv2.DIST_L2, 5)
    points = circle_points(250, [330, 76], 100)[:-1]
    snake = seg.active_contour(img, points, alpha=0.06, beta=0.3)
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.imshow(img, cmap=plt.cm.gray)
    ax.plot(points[:, 0], points[:, 1], '--r', lw=3)
    ax.plot(snake[:, 0], snake[:, 1], '-b', lw=3)
    plt.show()
    # return img


if __name__ == '__main__':
    # produce sample image
    img = image_maker(args['circles'], args['rectangles'], args['triangles'])
    cv2.imshow('Original Image', img)

    # find edges with laplacian filter
    # img = laplacian_filter(img)
    # cv2.imshow('Laplacian Image', img)

    # apply segmentation
    img = segment_shapes(img)
    # cv2.imshow('Segmented Image', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()