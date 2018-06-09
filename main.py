import sine_wave as s
import fourier as f


def run():
    time, adc_values = s.get_values()
    x, y = f.fourier(time, adc_values)
    print(x, y)