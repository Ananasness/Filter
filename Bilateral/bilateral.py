import numpy as np
from PyQt5.QtGui import QImage, QColor, qRgb


def create_color_tables(image, radius):
    red = np.zeros((image.width() + 2 * radius, image.height() + 2 * radius), float)
    green = np.zeros((image.width() + 2 * radius, image.height() + 2 * radius), float)
    blue = np.zeros((image.width() + 2 * radius, image.height() + 2 * radius), float)

    # fill up color table for filtering
    for x in range(image.width() + 2 * radius):
        for y in range(image.height() + 2 * radius):
            i, j = x - radius, y - radius
            if x < radius:
                i += radius
            if y < radius:
                j += radius
            if x >= image.width() + radius:
                i -= radius
            if y >= image.height() + radius:
                j -= radius

            red[x][y], green[x][y], blue[x][y] = QColor(image.pixel(i, j)).getRgb()[:3]

    colors = np.array([red, green, blue])
    return colors

def bilateral(img, sigma, radius):

    constant1 = 1 / (sigma * np.sqrt(2 * np.pi))
    constant2 = - 1 / (2 * sigma * sigma)

    gauss_func = np.vectorize(lambda x: constant1 * np.exp(x * x * constant2))

    # window radius
    # radius = 5
    # window size
    window_size = radius * 2 + 1
    image = QImage(img)
    height = image.height()
    width = image.width()

    colors = create_color_tables(image, radius)
    new_color_table = np.zeros((width + 2 * radius, height + 2 * radius, 3), float)

    # some preparing for the filter

    # Values of the distances from center to other pixels into the window in X and Y coordinates
    dX = np.array([[i for i in range(- radius, radius + 1)] for _ in range(window_size)])
    dY = np.array([[j for _ in range(window_size)] for j in range(- radius, radius + 1)])

    # Compute value of distance as a Euclidean distance
    # and than to compute value of Gaussian function for future filtering
    space = gauss_func(np.hypot(dX, dY))


    for x in range(radius, width + radius):
        for y in range(radius, height + radius):
            result_color = []

            for color in colors:
                # select work zone (window) from color table
                section = color[x - radius: x + radius + 1, y - radius: y + radius + 1]
                # matrix = [[color[x, y]] * window_size] * window_size
                delta = np.full((window_size, window_size), color[x, y])

                range = gauss_func(section - delta)

                product = range * space
                W = sum(product)

                result = W / sum(section * product)
                result_color.append(result)

            new_color_table[x][y] = result_color


    print(image.width(),image.height())
    print(len(new_color_table), len(new_color_table[0]))

    for i in range(image.width()):
        for j in range(image.height()):
            r, g, b = new_color_table[i][j]
            image.setPixel(i, j, qRgb(r, g, b))

    return image









