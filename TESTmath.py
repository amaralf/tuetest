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

# ===================FOURIER=================


def load_test_data(name):
    namestring = "./textfiles/" + name + ".txt"
    print(namestring)
    f = open(namestring)
    lines = f.readlines()
    time = []
    data = []
    magnet = []
    for x in lines:
        time.append(x.split('\t')[0])
        data.append(x.split('\t')[3])
        magnet.append(x.split('\t')[4])
    f.close()
    step = -1
    found = False
    while not found:
        laststep = step
        step += 1
        if abs(float(magnet[step]) - float(magnet[laststep])) > 0.15:
            found = True
    print(step)
    pulsestime = []
    pulsesdata = []
    pulsesmagnet = []
    while step < len(time):
        nextstep = step
        found = False
        while not found:
            laststep = nextstep
            nextstep += 1
            if abs(float(magnet[nextstep]) - float(magnet[laststep])) > 0.15:
                found = True
        print("ends: ", nextstep)
        sub = ((nextstep - step)/20)
        nextsubstep = step
        pulsetime = []
        pulsedata = []
        pulsemagnet = []
        while step < nextstep:
            # if step == nextsubstep:
            # nextsubstep += sub
            pulsetime.append(time[step])
            pulsedata.append(data[step])
            pulsemagnet.append(magnet[step])
            step += 1
        pulsetime = [float(i) for i in pulsetime]
        pulsedata = [float(i) for i in pulsedata]
        pulsestime.append(pulsetime)
        pulsesdata.append(pulsedata)
        pulsesmagnet.append(pulsemagnet)
        found = False
        while not found:
            laststep = step
            step += 1
            if step < len(time):
                if abs(float(magnet[step]) - float(magnet[laststep])) > 0.15:
                    found = True
            if step == len(time):
                found = True
        print(step)
    return pulsestime, pulsesdata, pulsesmagnet


def test_data_fourier(data):
    fourierx = []
    fouriery = []
    tenhzx = []
    tenhzy = []
    for x in range(0, len(data)):
        time = np.linspace(0, (len(data[x]) * 0.0002), len(data[x]))
        print(len(data[x]))
        x, y = fourierten(time, data[x])
        fourierx.append(x)
        fouriery.append(y)
    return fourierx, fouriery


def fourier(time, amplitude):
    N = len(time)  # size
    T = time[len(time)-1]/N  # step probably
    yf = fft(amplitude)  # fourier transform
    hzvals = np.linspace(0.0, 1.0/(2.0*T), int(N/2))
    amplitudes = 2.0/N * np.abs(yf[:N//2])
    return hzvals, amplitudes


def fourierten(time, amplitude):
    x, y = fourier(time, amplitude)
    i = find_ten(x)
    print(y[i])
    return x[i], y[i]


def find_ten(x):
    closestindex = 0
    closest = np.inf
    index = 0
    closestdistance = np.inf
    for num in x:
        distance = abs(num-10)
        if distance < closestdistance:
            closest = num
            closestdistance = distance
            closestindex = index
        index += 1
    # print(closest)
    # print(closestdistance)
    return closestindex


# ===================SINE-WAVE=================

def init():
    """Initialisation function for measurements"""
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


def get_values():
    """Make a sine and cosine wave and store the relevant values in arrays.
    Input: -
    Output: array adc_values, with the readout values from the detector.
            array times, with the measurement times.
            new set values for dac1 and dac2"""
    # initialization of all peripherals
    adc = Adafruit_ADS1x15.ADS1115()
    GAIN = 1                        # of 2/3, dependent on the desired range
    times = []                      # create some arrays
    adc_values = []

    sine, cosine, dac1, dac2 = init()
    start_time = time.time()
    delta = 0
    while delta <= 0.2:
        delta = time.time() - start_time
        times.append(delta)
        dac1.set_voltage(cosine[int(10000*delta)])      # sample values from waves according to delta
        dac2.set_voltage(sine[int(10000*delta)])
        adc_values.append(adc.read_adc(0, gain=GAIN))   # read the adc and store values in array
    dac1.set_voltage(int(2048))
    dac2.set_voltage(int(2048))
    return times, adc_values


def actuation():
    """Actuation function
    Input: -
    Output: - """
    sine, cosine, dac1, dac2 = init()
    actuate = time.time()
    act_time = 0
    while act_time <= 10:
        act_time = time.time() - actuate
        dac1.set_voltage(cosine[int(10000*act_time)])      # sample values from waves according to act_time
        dac2.set_voltage(sine[int(10000*act_time)])
    time.sleep(20)
