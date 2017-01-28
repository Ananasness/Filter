import numpy as np
from PyQt5.QtGui import QImage, QColor, qRgb




def create_color_tables(image, radius):
    color_table = np.zeros((image.width() + 2 * radius, image.height() + 2 * radius, 3), float)

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

            color_table[x, y] = np.array(QColor(image.pixel(i, j)).getRgb()[:3])

    return color_table


def bilateral(img, sigma, radius):

    constant1 = 1 / (sigma * np.sqrt(2 * np.pi))
    constant2 = - 1 / (2 * sigma * sigma)

    gauss_func = np.vectorize(lambda x: constant1 * np.exp(x * x * constant2))  # ???

    # window radius
    # radius = 5
    # window size
    window_size = radius * 2 + 1
    image = QImage(img)
    height = image.height()
    width = image.width()

    color_table = create_color_tables(image, radius)
    new_color_table = np.zeros(color_table.shape, float)

    # some preparing for the filter

    # Values of the distances from center to other pixels into the window in X and Y coordinates
    dX = np.array([[i for i in range(- radius, radius + 1)] for _ in range(window_size)])
    dY = np.array([[j for _ in range(window_size)] for j in range(- radius, radius + 1)])

    # Compute value of distance as a Euclidean distance
    # and than to compute value of Gaussian function for future filtering
    space = gauss_func(np.hypot(dX, dY))

    for x in range(radius, width + radius):
        for y in range(radius, height + radius):
            for color in range(3):
                # select work zone (window) from color table
                section = color_table[x - radius: x + radius + 1, y - radius: y + radius + 1, color]

                # matrix = [[color[x, y]] * window_size] * window_size
                delta = np.full((window_size, window_size), color_table[x, y, color])

                y_range = gauss_func(section - delta)

                product = y_range * space
                # print( type(product))
                normalization = product.sum()

                result = (section * product).sum() / normalization

                new_color_table[x][y][color] = result

    # print(image.width(),image.height())
    # print(len(new_color_table), len(new_color_table[0]))

    # new image from color table
    for i in range(width):
        for j in range(height):
            image.setPixel(i, j, qRgb(*new_color_table[i + radius, j + radius]))

    return image









