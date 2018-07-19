import sine_wave as s
import fourier as f


def getAmp():
    """Input: none
       Output: single amplitude of +- 10Hz freq as measured."""
    time, adc_values = s.get_values()
    x, y = f.fourierten(time, adc_values)
    print(x, y)
    return y


def getResult(avg):
    """Input: single amplitude
       Output: single result value"""

    return avg
    # TODO


def run():
    """Input: none
       Output: none"""
    measurements = []
    for x in range(20):
        y = getAmp()
        measurements.append(y)
    print(measurements)
    res = getResult(sum(measurements) / len(measurements))
    print(res)
