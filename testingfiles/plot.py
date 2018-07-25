import numpy as np
import matplotlib.pyplot as plt


def read_file():
    data = []
    file = open("Measurements_Patient_1.txt", "r")
    for entry in list(file):
        entry = entry.replace('\n', '')
        data.append(float(entry))
    return data


def plot():
    y = read_file()
    x = np.linspace(0, 20, 20)
    plt.plot(x, y, marker='o', color='b')
    # Give a title for the sine wave plot
    plt.title('Fourier')
    # Give x axis label for the sine wave plot
    plt.xlabel('Number of pulses')
    # Give y axis label for the sine wave plot
    plt.ylabel('Amplitude = sin(time)')
    plt.grid(True, which='both')
    plt.axhline(y=0, color='k')
    plt.show()
