import numpy as np
import cv2
import skimage.segmentation as seg
import matplotlib.pyplot as plt


def circle_points(resolution, center, radius):
    """
    Generate points which define a circle on an image.Centre refers to the centre of the circle
    """   
    radians = np.linspace(0, 2*np.pi, resolution)
    c = center[1] + radius*np.cos(radians)
    r = center[0] + radius*np.sin(radians)

    return np.array([c, r]).T


def active_contour_segmentation(img, x0, y0, radius, alpha=0.06, beta=0.3, *, show_plots=False):
    '''
    segment circles, rectangles and triangles and draw their boundaries.
    '''
    # laplacian transform
    # img = cv2.distanceTransform(img.astype('uint8'), cv2.DIST_L2, 5)
    points = circle_points(radius, [y0, x0], 100)[:-1]
    snake = seg.active_contour(img, points, alpha=alpha, beta=beta)
    if show_plots:
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.imshow(img, cmap=plt.cm.gray)
        ax.plot(points[:, 0], points[:, 1], '--r', lw=3)
        ax.plot(snake[:, 0], snake[:, 1], '-b', lw=3)
        plt.show()
    return snake