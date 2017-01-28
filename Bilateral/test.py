import numpy as np


def gauss_func(x, sigma):
    return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(- x*x / (2 * sigma * sigma))

sigma = 3

constant1 = 1 / (sigma * np.sqrt(2 * np.pi))
constant2 = - 1 / (2 * sigma * sigma)

print(gauss_func(190, 10))
