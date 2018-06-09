import Adafruit_ADS1x15
import Adafruit_MCP4725
import math
import time


def get_values():
    """Make a sine and cosine wave and store the relevant values in arrays.
    Input: -
    Output: array adc_values, with the readout values from the detector.
            array times, with the measurement times.
            new set values for dac1 and dac2"""
    # initialization of all peripherals
    adc = Adafruit_ADS1x15.ADS1115()
    dac1 = Adafruit_MCP4725.MCP4725()
    dac2 = Adafruit_MCP4725.MCP4725(address=0x63, busnum=1)
    dac1.set_voltage(int(2048))
    dac2.set_voltage(int(2048))
    GAIN = 1                        # of 2/3, dependent on the desired range
    times = []                      # create some arrays
    adc_values = []
    sine = []
    cosine = []

    # create a sine and cosine wave for sampling
    for i in range(2000):
        sine.append(int(2048 + 2048*math.sin(0.001*math.pi*i)))
        cosine.append(int(2048 + 2048*math.cos(0.001*math.pi*i)))
    for i in range(100):
        sine.append(int(2048))
        cosine.append(int(2048))

    start_time = time.time()
    delta = 0
    while delta <= 0.2:
        delta = time.time() - start_time
        times.append(delta)
        dac1.set_voltage(cosine[int(10000*delta)])      # sample values from waves according to delta
        dac2.set_voltage(sine[int(10000*delta)])
        adc_values.append(adc.read_adc(3, gain=GAIN))   # read the adc and store values in array
    dac1.set_voltage(int(2048))
    dac2.set_voltage(int(2048))
    return times, adc_values
