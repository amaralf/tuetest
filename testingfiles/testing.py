# # interpolation
# import random  # used for simulation only.
# import scipy  # vital for the interpolation.
# import scipy.interpolate  # vital for the interpolation.
# # ===================INTERPOLATION=================
#
#
# def simulate():
#     """Simulate an ADC output in three numbers.
#     Input: -
#     Output: int a, between 0 and 32767, double b, between 0.0 and 5.0, bitstring c.
#     a=c in value, both are converted from b."""
#     b = random.uniform(0.00, 5.00)
#     # print(number)
#     a = int(b*(pow(2, 15)-1)/5.0)
#     # print(a)
#     c = bin(a)
#     return a, b, c
#
#
# def simulate_group():
#     """Use simulate() 10 times and return the 10 points in an array.
#     Input: -
#     Output: point tuple array h"""
#     h = []
#     for i in range(10):
#         j = simulate()
#         h.append(j)
#     return h
#
#
# def set_point(a, b, x, y):
#     """put a point, defined by a as its x-coordinate and b as its y-coordinate
#     in the array of the x and y coordinates.
#     Input: x-coordinate a, y-coordinate b, x-coordinate array x, y-coordinate array y
#     Output: - """
#     x.append(a)
#     y.append(b)
#
#
# def set_point_group(h, x, y):
#     """Put an array of points h in the arrays of the x and y coordinates.
#     Input: array with point tuples h, x-coordinate array x, y-coordinate array y.
#     Output: - """
#     for i in h:
#         x.append(i[0])
#         y.append(i[1])
#
#
# def print_points(x, y):
#     """Print all the points in the x and y coordinates array
#     Input: x-coordinate array x, y-coordinate array y.
#     Output: - (printed in console)"""
#     for z in range(len(x)):
#         print("("+str(x[z])+", "+str(y[z])+")")
#
#
# def initialize():
#     """make an array for the x coordinates and the y coordinates
#     and put the two extremes in there ((0, 0.0) and (32767, 5.0)).
#     Input: -
#     Output: x-coordinate array x, y-coordinate array y."""
#     x = []
#     y = []
#     set_point(0, 0.0, x, y)
#     set_point(pow(2, 15)-1, 5.0, x, y)
#     return x, y
#
#
# def get_function(x, y):
#     """Use scipy Interpolate to make a calibration curve.
#     Reference: https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp1d.html
#     Input: x-coordinate array x, y-coordinate array y.
#     Output: function f."""
#     f = scipy.interpolate.interp1d(x, y)
#     return f
#
#
# def interpolate(c, f):
#     """Intepolate point c with function f.
#     Input: value c, between 0 and 32767, function f, interpolation function.
#     Output: value k, between 0.0 and 5.0"""
#     k = f(c)
#     k = k.flatten()[0]
#     return k
#
#
# def simulated_ex_initialize():
#     """A method to make the simulation easier by calling the other methods in sequence.
#     Input: -
#     Output: x-coordinate array x, y-coordinate array y, interpolation function f"""
#     x, y = initialize()
#     p = simulate_group()
#     set_point_group(p, x, y)
#     # print_points(x, y)
#     f = get_function(x, y)
#     # plot_graph(x, y)
#     return x, y, f


# def plot_graph(x, y):
#     """plot the x and y coordinate arrays to a graph
#     Input: x and y coordinate arrays
#     Output: graph (non-variable)"""
#     plt.xlabel('Bitstring')
#     plt.ylabel('Volt')
#     plt.plot(x, y, marker='o')
#     plt.axis([0, 32767, 0.0, 5.0])
#     plt.show()

# TODO: Write interpolation tests.


# def make_sine():
#     # Get x values of the sine wave
#     time = np.linspace(0, 0.2, 20)
#     frequency = 10  # hertz
#     w = frequency*(2*np.pi)
#     # Amplitude of the sine wave is sine of a variable like time
#     amplitude = np.sin(w*time)
#     # Plot a sine wave using time and amplitude obtained for the sine wave
#     plt.plot(time, amplitude)
#     # Give a title for the sine wave plot
#     plt.title('Sine wave')
#     # Give x axis label for the sine wave plot
#     plt.xlabel('Time')
#     # Give y axis label for the sine wave plot
#     plt.ylabel('Amplitude = sin(time)')
#     plt.grid(True, which='both')
#     plt.axhline(y=0, color='k')
#     plt.show()
#     return time, amplitude


# def initialize_f():
#     time1 = [1.2159347534179688e-05, 0.01201176643371582, 0.023653745651245117, 0.035660505294799805,
#              0.048452138900756836, 0.06030440330505371, 0.07195305824279785, 0.08367443084716797, 0.09540987014770508,
#              0.10707855224609375, 0.11869525909423828, 0.13054752349853516, 0.14247393608093262, 0.15423583984375,
#              0.1658763885498047, 0.17781972885131836, 0.18955039978027344, 0.20127224922180176]
#     wave1 = [14365, 10491, 11621, 17371, 25038, 29436, 29013, 23811, 16719, 11330, 10312, 14351, 21343, 27454, 29431,
#              26975, 20539, 13622]
#     time2 = [8.821487426757812e-06, 0.011968612670898438, 0.023641109466552734, 0.03393983840942383,
#              0.04433846473693848, 0.05458998680114746, 0.06473612785339355, 0.07487940788269043, 0.0850977897644043,
#              0.09535956382751465, 0.10550093650817871, 0.11561751365661621, 0.12573027610778809, 0.13593220710754395,
#              0.1462996006011963, 0.1565103530883789, 0.16662931442260742, 0.17674732208251953, 0.18695783615112305,
#              0.19711709022521973, 0.20723867416381836]
#     wave2 = [12206, 10350, 13094, 18703, 24937, 29093, 29679, 26430, 20558, 14560, 10703, 10451, 13896, 19749, 25772,
#              28853, 29048, 25583, 19671, 13941, 10388]
#     time3 = [1.4543533325195312e-05, 0.012311935424804688, 0.023920059204101562, 0.034155845642089844,
#              0.04441499710083008, 0.05466270446777344, 0.06482958793640137, 0.07497477531433105, 0.08509325981140137,
#              0.09536337852478027, 0.10574102401733398, 0.11623549461364746, 0.126786470413208, 0.1370389461517334,
#              0.14725852012634277, 0.15747499465942383, 0.1676163673400879, 0.17786288261413574, 0.18806052207946777,
#              0.19827866554260254, 0.2084972858428955]
#     wave3 = [23424, 28932, 29658, 26652, 20942, 14930, 10976, 10512, 13778, 19717, 25674, 28929, 28807, 25033, 18946,
#              13320, 10335, 11218, 15495, 21628, 26946]
#     graph = list(zip(time2, wave2));
#     graph = sorted(graph, key=lambda l:l[0])
#     plt.xlabel('Time in seconds')
#     plt.ylabel('Wave')
#     x = [i[0] for i in graph]
#     y = [i[1] for i in graph]
#     plt.plot(x, y, marker='o')
#     plt.show()2
#     return time2, wave2
