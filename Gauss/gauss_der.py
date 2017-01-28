import math
import time

import numpy as np
from PyQt5.QtGui import QImage, QColor, qRgb


def gaussX(x, y, sigma):
    return (-x / (2 * math.pi * sigma ** 4)) * math.exp(- (x * x + y * y) / (2 * sigma * sigma))


def gaussY(x, y, sigma):
    return (-y / (2 * math.pi * sigma ** 4)) * math.exp(- (x * x + y * y) / (2 * sigma * sigma))


def gauss_funcXY(x, y, sigma):
    return (1 / (sigma * math.sqrt(2 * math.pi))) * math.exp(- (x * x + y * y) / (2 * sigma * sigma))


def gauss_der(img, sigma):
    print("------------Gaussian derivate---------")
    n = math.ceil(3 * sigma)
    matrixX = []
    matrixY = []
    for i in range(-n + 1, n):
        tempX = []
        tempY = []
        for j in range(-n + 1, n):
            tempX.append(gauss_funcXY(i, j, sigma))
            tempY.append(gaussY(i, j, sigma))

        matrixX.append(tempX)
        matrixY.append(tempY)

    matrixX = np.array(matrixX)
    matrixY = np.array(matrixY)

    print(np.array(matrixY))

    imageX = QImage(img)
    imageY = QImage(img)

    new_color_tableX = []
    new_color_tableY = []
    t = time.time()
    color_tableX = np.array(
        [[QColor(imageX.pixel(i, j)).getRgb()[:3] for j in range(imageX.height())] for i in range(imageX.width())])
    color_tableY = np.array(
        [[QColor(imageX.pixel(i, j)).getRgb()[:3] for j in range(imageX.height())] for i in range(imageX.width())])

    for i in range(1, img.width() - 1):
        for j in range(1, img.height() - 1):
            for c in range(3):
                color_tableY[i][j][c] = color_tableY[i][j + 1][c] - color_tableY[i][j][c]

    for i in range(img.width()):
        tempX = []
        tempY = []
        for j in range(img.height()):
            result_colorX = [0] * 3
            result_colorY = [0] * 3
            sum = 0
            for c in range(3):
                if i + n < img.width() and j + n < img.height() and i - n + 1 >= 0 and j - n + 1 >= 0:
                    if i == 2 and j == 2:
                        print(color_tableX[i - n + 1: i + n, j - n + 1: j + n, c])
                    result_colorX[c] = ((matrixX * color_tableY[i - n + 1: i + n, j - n + 1: j + n, c]).sum()
                                        / matrixX.sum())
                    result_colorY[c] = (matrixY * color_tableY[i - n + 1: i + n, j - n + 1: j + n, c]).sum()
                else:
                    result_colorX[c] = color_tableX[i][j][c]
                    result_colorY[c] = color_tableY[i][j][c]
            print(
                i, j, ": ", color_tableX[i][j][0], " -> ", int(result_colorX[0]), "\t\t\t", color_tableY[i][j][0],
                " -> ",
                int(result_colorY[0]))

            tempX.append(result_colorX)
            tempY.append(result_colorY)
        new_color_tableX.append(tempX)
        new_color_tableY.append(tempY)

    for i in range(img.width()):
        for j in range(img.height()):
            imageX.setPixel(i, j, qRgb(int(new_color_tableX[i][j][0]), int(new_color_tableX[i][j][1]),
                                       int(new_color_tableX[i][j][2])))
            imageY.setPixel(i, j, qRgb(int(new_color_tableY[i][j][0]), int(new_color_tableY[i][j][1]),
                                       int(new_color_tableY[i][j][2])))

    # pixs = [
    #     [64, 77, 85, 87, 64],
    #     [75, 29, 102, 181, 179],
    #     [56, 72, 183, 253, 226],
    #     [50, 96, 218, 237, 206],
    #     [59, 86, 187, 235, 227]
    # ]
    # maxpixs = np.array([[256] * 5] * 5)
    # pixs = np.array(pixs)
    #
    # product = maxpixs * matrixY
    # print(product)
    # print(product.sum())

    return imageX, imageY
