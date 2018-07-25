import Adafruit_ADS1x15
import time
import TESTmath as il


adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1  # of 2/3, afhankelijk van de range

x, y = il.initialize()
f = il.get_function(x, y)
start_time = time.time()

while (time.time() - start_time) <= 0.2:  
    value = adc.read_adc(0, gain=GAIN)
    b = il.interpolate(value, f)
    il.set_point(value, b, x, y)
    print(x, y)
il.plot_graph(x, y)

