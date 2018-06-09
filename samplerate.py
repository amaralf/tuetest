import Adafruit_ADS1x15
import time

GAIN = 1 #of 2/3, afhankelijk van de range
timeout = 1 #in seconds
timestart = time.time()

first = []
second = []

adc = Adafruit_ADS1x15.ADS1115()

#print('Reading values, press Ctrl-C to quit')
#print('| {0:>6} |'.format(*range(1)))
#print('-' * 10)

while time.time() < timestart + timeout:
    values = [0]
    for i in range(1):
        values[i] = adc.read_adc(0,gain=GAIN)
        first.append(values)
    #print('| {0:>6} |'.format(*values))
print(len(first))

#print('Reading values, press Ctrl-C to quit')
#print('| {0:>6} |'.format(*range(1)))
#print('-' * 10)

timestart2 = time.time()

while time.time() < timestart2 + timeout:
    adc = Adafruit_ADS1x15.ADS1115()
    values = [0]
    for i in range(1):
        values[i] = adc.read_adc(0,gain=GAIN)
        second.append(values)
    #print('| {0:>6} |'.format(*values))

print(len(second))
print(len(first)-len(second))