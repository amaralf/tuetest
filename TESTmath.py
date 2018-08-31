# Software developed and tested exclusively and exquisitely for T.E.S.T. 2018
# By T.T.P. Franken and R.P.W. Schmidt.

# The Math file
# The Math file

# ===================IMPORTS=================

# fourier
import numpy as np
from scipy.fftpack import fft

# sine_wave
import Adafruit_ADS1x15
import Adafruit_MCP4725
import math
import time

# =================RUNMETHODS================
# in order of calling.


def actuation():
    """Actuation function"""
    sine, cosine, dac1, dac2 = init()
    actuate = time.time()
    act_time = 0
    while act_time <= 10:
        act_time = time.time() - actuate
        dac1.set_voltage(cosine[int(10000*act_time)])      # sample values from waves according to act_time
        dac2.set_voltage(sine[int(10000*act_time)])


def get_values():
    """This function reads the values from the ADC. Here we also initialize the ADC, set the GAIN and perform
       the measurement."""
    adc = Adafruit_ADS1x15.ADS1115()
    # of 2/3, dependent on the desired range
    GAIN = 1
    # create some arrays
    times = []
    adc_values = []

    # call the init function here for ease of use
    sine, cosine, dac1, dac2 = init()
    start_time = time.time()
    delta = 0
    while delta <= 0.2:
        delta = time.time() - start_time
        times.append(delta)
        # sample values from waves according to delta
        dac1.set_voltage(cosine[int(10000*delta)])
        dac2.set_voltage(sine[int(10000*delta)])
        # read the adc and store bitstring values in an array
        adc_values.append(adc.read_adc(0, gain=GAIN))
    dac1.set_voltage(int(2048))
    dac2.set_voltage(int(2048))
    return times, adc_values


def fourierten(time, amplitude):
    """This function is called during the execution. It calls both functions below it."""
    x, y = fourier(time, amplitude)
    i = find_ten(x)
    # x[i] is the value[index] in [hzvals] closest to 10Hz which has the highest accompanying peak, y[i]
    return x[i], y[i]


# ===================FOURIER=================
# other functions


def fourier(time, amplitude):
    """The actual Fourier transformation. To be honest, we had to Google this and we found something that worked. Should 
       you really want some kind of explanation-ish, contact T.T.P. Franken."""
    N = len(time)  # size
    T = time[len(time)-1]/N  # step
    yf = fft(amplitude)  # fourier transformation
    hzvals = np.linspace(0.0, 1.0/(2.0*T), int(N/2))
    amplitudes = 2.0/N * np.abs(yf[:N//2])
    return hzvals, amplitudes


def find_ten(x):
    """This function finds the location of the peak on the x-axis: thus the Hz value which has the highest peak closest
       to 10Hz."""
    closestindex = 0
    index = 0
    closestdistance = np.inf
    for num in x:
        distance = abs(num-10)
        if distance < closestdistance:
            closestdistance = distance
            closestindex = index
        index += 1
    return closestindex


# ===================SINE-WAVE=================
# other functions.

def init():
    """Initialisation function for measurements. Here we initialize both DAC's and create a Sine and Cosine for
       sampling."""
    dac1 = Adafruit_MCP4725.MCP4725()
    dac2 = Adafruit_MCP4725.MCP4725(address=0x63, busnum=1)
    dac1.set_voltage(int(2048))
    dac2.set_voltage(int(2048))
    sine = []
    cosine = []

    # create a sine and cosine wave for sampling
    for i in range(100000):
        sine.append(int(2048 + 2048 * math.sin(0.001 * math.pi * i)))
        cosine.append(int(2048 + 2048 * math.cos(0.001 * math.pi * i)))
    for i in range(100):
        sine.append(int(2048))
        cosine.append(int(2048))
    return sine, cosine, dac1, dac2



