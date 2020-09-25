## Shape Finder

Written by: Mehrdad Pourfathi

Date: 9/25/2020


This is a simple routine written with OpenCV with Python back-end to Find randomly position circles, squares and triangles in a binary image. 

#### Dependencies:
* numpy
* OpenCV 2
* itertools
* argparse


#### How to run:
In terminal run the code as:

`python shape_finder.py --circles 3 --squares 4 --triangles 3 --seed 823`

or its short version
`python shape_finder.py -c 3 -sq 4 -t 3 -sd 823`

#### Flags:
c: number of circles
sq: number of squares
t: number of triangles
sd: seed to random generator


#### Algorithm:
1. First we generate a 640x480 image white background and randomly positioned squres, triangles and circles with black boundary, using the `image_maker()` function.

![](figures/input.png)

