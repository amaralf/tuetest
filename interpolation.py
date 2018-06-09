import random  # used for simulation only.
import scipy  # vital for the interpolation.
import scipy.interpolate  # vital for the interpolation.
import matplotlib.pyplot as plt
import numpy
# print(plt.get_backend())


def simulate():
    """Simulate an ADC output in three numbers.
    Input: -
    Output: int a, between 0 and 32767, double b, between 0.0 and 5.0, bitstring c.
    a=c in value, both are converted from b."""
    b = random.uniform(0.00, 5.00)
    # print(number)
    a = int(b*(pow(2, 15)-1)/5.0)
    # print(a)
    c = bin(a)
    return a, b, c


def simulate_group():
    """Use simulate() 10 times and return the 10 points in an array.
    Input: -
    Output: point tuple array h"""
    h = []
    for i in range(10):
        j = simulate()
        h.append(j)
    return h


def set_point(a, b, x, y):
    """put a point, defined by a as its x-coordinate and b as its y-coordinate
    in the array of the x and y coordinates.
    Input: x-coordinate a, y-coordinate b, x-coordinate array x, y-coordinate array y
    Output: - """
    x.append(a)
    y.append(b)


def set_point_group(h, x, y):
    """Put an array of points h in the arrays of the x and y coordinates.
    Input: array with point tuples h, x-coordinate array x, y-coordinate array y.
    Output: - """
    for i in h:
        x.append(i[0])
        y.append(i[1])


def print_points(x, y):
    """Print all the points in the x and y coordinates array
    Input: x-coordinate array x, y-coordinate array y.
    Output: - (printed in console)"""
    for z in range(len(x)):
        print("("+str(x[z])+", "+str(y[z])+")")


def initialize():
    """make an array for the x coordinates and the y coordinates
    and put the two extremes in there ((0, 0.0) and (32767, 5.0)).
    Input: -
    Output: x-coordinate array x, y-coordinate array y."""
    x = []
    y = []
    set_point(0, 0.0, x, y)
    set_point(pow(2, 15)-1, 5.0, x, y)
    return x, y


def get_function(x, y):
    """Use scipy Interpolate to make a calibration curve.
    Reference: https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp1d.html
    Input: x-coordinate array x, y-coordinate array y.
    Output: function f."""
    f = scipy.interpolate.interp1d(x, y)
    return f


def interpolate(c, f):
    """Intepolate point c with function f.
    Input: value c, between 0 and 32767, function f, interpolation function.
    Output: value k, between 0.0 and 5.0"""
    k = f(c)
    k = k.flatten()[0]
    return k


def simulated_ex_initialize():
    """A method to make the simulation easier by calling the other methods in sequence.
    Input: -
    Output: x-coordinate array x, y-coordinate array y, interpolation function f"""
    x, y = initialize()
    p = simulate_group()
    set_point_group(p, x, y)
    # print_points(x, y)
    f = get_function(x, y)
    plot_graph(x, y)
    return x, y, f


def plot_graph(x, y):
    """plot the x and y coordinate arrays to a graph
    Input: x and y coordinate arrays
    Output: graph (non-variable)"""
    plt.xlabel('Bitstring')
    plt.ylabel('Volt')
    plt.plot(x, y, marker='o')
    plt.axis([0, 32767, 0.0, 5.0])
    plt.show()

# TODO: Write interpolation tests.
