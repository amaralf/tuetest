import sine_wave as s
import fourier as f
import time as t


def getAmp():
    """Input: none
       Output: single amplitude of +- 10Hz freq as measured."""
    time, adc_values = s.get_values()
    x, y = f.fourierten(time, adc_values)
    return y


def getResult(avg):
    """Input: single amplitude
       Output: single result value"""

    return avg
    # TODO


def run():
    """Input: none
       Output: none"""
    for x in range(20):
        measurements = []
        s.actuation()
        for z in range(10):
            y = getAmp()
            measurements.append(y)
        res = getResult(sum(measurements) / len(measurements))
        t.sleep(10)
        return measurements, res


def run_test():
    t, d, m = f.load_test_data()
    x, measurements = f.test_data_fourier(d)
    res = getResult(sum(measurements) / len(measurements))
    print(res)
    return measurements, res
