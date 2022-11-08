import numpy as np
import random
import torchvision.datasets as datasets
import base64
from io import BytesIO
import matplotlib.pyplot as plt


class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if other.x == self.x and other.y==self.y:
            return True
        return False

    def __str__(self):
        return "x="+str(self.x) + ",y=" + str(self.y)

    def __hash__(self):
        return hash(str(self))

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)

def norm(point):
    return abs(point.x) + abs(point.y)

def binarise_img(pic):
    pic = np.array(pic)
    new_img = np.zeros(pic.shape)
    for x in range(pic.shape[1]):
        for y in range(pic.shape[0]):
            if pic[y,x] == 0:
                new_img[y,x] = 1
    return new_img

def sense_1(point, picture):
    xlen = picture.shape[1]
    ylen = picture.shape[0]
    if point.x >= 0 and point.y >= 0 and point.x < xlen and point.y < ylen:
        val = picture[point.y, point.x]
        if val > 0:
            return True
    return False



class IdsGenerator:
    def __init__(self):
        self.id = -1

    def generate_id(self):
        self.id += 1
        return self.id


class HtmlLogger:
    def __init__(self, name):
        self.name = name
        self.html = ''

    def add_line_little(self):
        self.html += "<hr>"

    def add_line_big(self):
        self.html += "<hr style=\"height:10px;background:gray\">"

    def add_text(self, text):
        self.html += text + '<br>'

    def add_fig(self, fig):
        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        self.html += '<img src=\'data:image/png;base64,{}\'>'.format(encoded) + '<br>'
        plt.close(fig)

    def save(self):
        filename = self.name + '.html'
        with open(filename, 'w') as f:
            f.write(self.html)


def my_dist(point1, point2):
    dx = abs(point1.x - point2.x)
    dy = abs(point1.y - point2.y)
    return dx+dy

def my_norm(point):
    return abs(point.x) + abs(point.y)

def get_coords_for_radius(center, radius):
    #|x|+|y|=radius ->  |y|=radius-|x|
    # x>0  -> y1 = radius-|x|
    if radius == 0:
        return [Point(center.x, center.y)]

    points = []
    for modx in range(0, radius+1):
        mody = radius - modx
        # x>0
        if modx != 0 and mody != 0:
            points.append(Point(modx + center.x, mody + center.y))
            points.append(Point(-modx + center.x, mody + center.y))
            points.append(Point(modx + center.x, -mody + center.y))
            points.append(Point(-modx + center.x, -mody + center.y))

        if modx == 0 and mody != 0:
            points.append(Point(modx+center.x, mody+center.y))
            points.append(Point(modx + center.x, -mody + center.y))

        if modx != 0 and mody == 0:
            points.append(Point(modx+center.x, mody+center.y))
            points.append(Point(-modx + center.x, mody + center.y))
    return points


def get_coords_less_or_eq_raduis(center, radius):
    points = []
    for r in range(0, radius+1):
        r_points = get_coords_for_radius(center.x, center.y, r)
        points = points + r_points
    return points