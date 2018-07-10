import scipy as s
import numpy as n
import scipy.optimize as so
import random as r
import matplotlib.pyplot as plt


def initialize():
    points = []
    truepoints = []
    for i in range(50):
        points.append(f((i, 1, 2, 3)) + (1000*r.random()-500))
        truepoints.append(f((i, 1, 2, 3)))
    return points, truepoints


def f(k):
    return k[1]*k[0]*k[0]+k[2]*k[0]+k[3]


def plot(points, truepoints):
    plt.xlabel('x')
    plt.ylabel('y')
    axisx = [i for i in range(50)]
    plt.plot(axisx, points, linestyle="", marker='o')
    plt.plot(axisx, truepoints)
    res_1 = so.leastsq(f, axisx)
    #plt.plot(res_1)
    plt.show()
    return res_1
