import sine_wave as s
import fourier as f


def getAmp():
    """Input: nothing
       Output: single amplitude of +- 10Hz freq as measured."""
    time, adc_values = s.get_values()
    x, y = f.fourierten(time, adc_values)
    print(x, y)
    return y


def getResult(y):
    """Input: single amplitude
       Output: single result value"""
    print("hey")
    return 8
    # TODO


def run():
    measurements = []
    for x in range(20):
        y = getAmp()
        res = getResult(y)
        measurements.append(res)
