from PyQt5.QtGui import QImage, QColor, qRgb
import numpy as np


def gauss_func(x, sigma):
    return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(- x*x / (2 * sigma * sigma))


# this function and next one are necessary for replacing each pixel by
# difference between this pixel and it's neighbor
def derivateX(table):

    new_table = np.zeros(table.shape, float)
    for x in range(table.shape[0] - 1):
        for y in range(table.shape[1]):
            new_table[x][y] = table[x][y] - table[x + 1][y]

    return new_table


def derivateY(table):

    new_table = np.zeros(table.shape, float)
    for x in range(table.shape[0]):
        for y in range(table.shape[1] - 1):
            new_table[x][y] = table[x][y] - table[x][y + 1]

    return new_table


# build color table with shifts for correct work with extreme pixels
# this couple of functions just reflects extreme pixels as additional pixels
def create_color_table(image, radius):
    color_table = np.zeros((image.width() + 2*radius, image.height() + 2*radius, 3), float)

    for x in range(image.width() + 2*radius):
        for y in range(image.height() + 2*radius):
            if radius <= x < image.width() + radius and radius <= y < image.height() + radius:
                i, j = x - radius, y - radius
                color_table[x, y] = np.array(QColor(image.pixel(i, j)).getRgb()[:3])

    return update_color_table(color_table, radius)


def update_color_table(color_table, radius):

    w, h = color_table.shape[:2]
    for x in range(w):
        for y in range(h):
            i, j = x, y

            if radius <= x < w - radius and radius <= y < h - radius:
                continue

            if x < radius:
                i += radius
            if y < radius:
                j += radius
            if x >= w - radius:
                i -= radius
            if y >= h - radius:
                j -= radius

            color_table[x, y] = color_table[i, j]

    return color_table


# use this function if you need some subset of origin matrix
# where i, j are coordinates of central point of new subset
# n is a radius new subset
# dir is direction (x or y) if you want to get one-dimensional array
def select_submatrix(matrix, i, j, n, dir=''):
    # print(matrix.shape, type(matrix))
    if dir == 'x':
        return matrix[i - n: i + n + 1, j]
    elif dir == 'y':
        return matrix[i, j - n: j + n + 1]
    else:
        return matrix[i - n: i + n + 1, j - n: j + n + 1]


def gauss_filter(img, sigma, *, der=""):

    # copy of original image
    image = QImage(img)

    height = image.height()
    width = image.width()
    radius = int(np.ceil(3*sigma))

    color_table = create_color_table(image, radius)
    new_color_table = np.zeros(color_table.shape, float)

    # building Gaussian kernel
    # using separable property
    gauss_matrix = []
    for i in range(-radius, radius + 1):
        gauss_matrix.append(gauss_func(i, sigma))

    # convolution with Gaussian function
    for dir in ['x', 'y']:

        # we start traversal all pixels with considering the shift = radius
        for i in range(radius, width + radius):
            for j in range(radius, height + radius):

                # select matrix for multiplying with kernel
                selected_matrix = select_submatrix(color_table, i, j, radius, dir=dir)

                # do it for each color in the pixel
                for c in range(3):
                    one_color_matrix = selected_matrix[:, c]
                    new_color_table[i][j][c] = sum(one_color_matrix * gauss_matrix)

        if (dir == 'x'):
            color_table = update_color_table(new_color_table, radius)
            new_color_table = np.zeros(color_table.shape, float)

    if der == "x":
        new_color_table = derivateX(new_color_table)
    elif der == "y":
        new_color_table = derivateY(new_color_table)

    # build new image
    for i in range(width):
        for j in range(height):
            image.setPixel(i, j, qRgb(*new_color_table[i + radius, j + radius]))

    return image






