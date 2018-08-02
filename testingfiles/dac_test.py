import Adafruit_MCP4725
import time
import math


def init():
    dac1 = Adafruit_MCP4725.MCP4725()
    dac2 = Adafruit_MCP4725.MCP4725(address=0x63, busnum=1)
    dac1.set_voltage(int(2048))
    dac2.set_voltage(int(2048))
    sine = []
    cosine = []

    # create a sine and cosine wave for sampling
    for i in range(20000):
        sine.append(int(2048 + 2048 * math.sin(0.001 * math.pi * i)))
        cosine.append(int(2048 + 2048 * math.cos(0.001 * math.pi * i)))
    for i in range(500):
        sine.append(int(2048))
        cosine.append(int(2048))
    return sine, cosine, dac1, dac2


def start():
    sine, cosine, dac1, dac2 = init()
    actuate = time.time()
    act_time = 0
    while act_time <= 10:
        act_time = time.time() - actuate
        dac1.set_voltage(cosine[int(2000*act_time)])      # sample values from waves according to act_time
        dac2.set_voltage(sine[int(2000*act_time)])
