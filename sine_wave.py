import Adafruit_ADS1x15
import Adafruit_MCP4725
import math
import time
import matplotlib.pyplot as plt
from scipy.fftpack import fft


def get_values():
    """Make a sine and cosine wave and store the relevant values in arrays.
    Input: -
    Output: array value1, with the cosine wave values. array value2, with the sine wave values.
            array times, with the measurement times."""
    # initialization
    adc = Adafruit_ADS1x15.ADS1115()
    dac1 = Adafruit_MCP4725.MCP4725()
    dac2 = Adafruit_MCP4725.MCP4725(address=0x63, busnum=1)

    dac1.set_voltage(int(2048))
    dac2.set_voltage(int(2048))
    
    GAIN = 1  # of 2/3, afhankelijk van de range
    delta = 0
    value1 = []
    value2 = []
    times = []
    adc_values = []
    sine = []
    cosine = []

    for i in range(2000):
        sine.append(int(2048 + 2048*math.sin(0.001*math.pi*i)))
        cosine.append(int(2048 + 2048*math.cos(0.001*math.pi*i)))
    for i in range(100):
        sine.append(int(2048))
        cosine.append(int(2048))
    
    # get the actual values
    
#   while True:
    start_time = time.time()
    while delta <= 0.2:
        delta = time.time() - start_time
        times.append(delta)
        # value1.append(math.cos(10*math.pi*delta))
        # value2.append(math.sin(10*math.pi*delta))
        # dac1.set_voltage(int(2048 + 2048*math.cos(10*math.pi*delta)))
        # dac2.set_voltage(int(2048 + 2048*math.sin(10*math.pi*delta)))
        dac1.set_voltage(cosine[int(10000*delta)])
        dac2.set_voltage(sine[int(10000*delta)])
        adc_values.append(adc.read_adc(3, gain=GAIN))

    dac1.set_voltage(int(2048))
    dac2.set_voltage(int(2048))
    # print(len(adc_values), len(times))
    print(times)
    print(len(adc_values))
    # print(fft(adc_values))
    # return times, value1, value2


def plot(times, value1, value2):
    """Plot graph of sine and cosine wave.
    Input: array value1 with the cosine wave values. array value2 with the sine waves.
           array times with the measurement times.
    Output: a graph (non-variable)."""
    plt.xlabel('Time in seconds')
    plt.ylabel('Amplitude')
    plt.plot(times, value1)
    plt.axis([0, 1, -1.5, 1.5])
    plt.plot(times, value2)
    plt.axis([0, 1, -1.5, 1.5])
    plt.show()

