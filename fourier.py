from numpy import linspace, pi, sin, abs, inf
from scipy.fftpack import fft
import matplotlib.pyplot as plt


def load_test_data():
    f = open("testdata_laserlab.txt")
    lines = f.readlines()
    time = []
    data = []
    magnet = []
    for x in lines:
        time.append(x.split('\t')[0])
        data.append(x.split('\t')[3])
        magnet.append(x.split('\t')[4])
    f.close()
    step = 5011;
    pulsestime = []
    pulsesdata = []
    pulsesmagnet = []
    while step < len(time):
        nextstep = step + 1000
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
        step+=50000
    return pulsestime, pulsesdata, pulsesmagnet


def test_data_fourier(data):
    time = linspace(0, 0.2, len(data[0]))
    fourierx = []
    fouriery = []
    tenhzx = []
    tenhzy = []
    for x in range(0, 20):
        # plt.plot(time[x], data[x])
        # plt.title('Test Laserlab %d' % x+1)
        # plt.xlabel('Time')
        # plt.ylabel('Data')
        # plt.axhline(y=0, color='k')
        # plt.show()
        x, y = fourierten(time, data[x])
        fourierx.append(x)
        fouriery.append(y)
    return fourierx, fouriery


def plot(y):
    x = linspace(0, 20, 20)
    plt.plot(x, y)
    # Give a title for the sine wave plot
    plt.title('Fourier')
    # Give x axis label for the sine wave plot
    plt.xlabel('Number of pulses')
    # Give y axis label for the sine wave plot
    plt.ylabel('Amplitude = sin(time)')
    plt.grid(True, which='both')
    plt.axhline(y=0, color='k')
    plt.show()


def make_sine():
    # Get x values of the sine wave
    time = linspace(0, 0.2, 20)
    frequency = 10  # hertz
    w = frequency*(2*pi)
    # Amplitude of the sine wave is sine of a variable like time
    amplitude = sin(w*time)
    # Plot a sine wave using time and amplitude obtained for the sine wave
    plt.plot(time, amplitude)
    # Give a title for the sine wave plot
    plt.title('Sine wave')
    # Give x axis label for the sine wave plot
    plt.xlabel('Time')
    # Give y axis label for the sine wave plot
    plt.ylabel('Amplitude = sin(time)')
    plt.grid(True, which='both')
    plt.axhline(y=0, color='k')
    plt.show()
    return time, amplitude


def initialize():
    time1 = [1.2159347534179688e-05, 0.01201176643371582, 0.023653745651245117, 0.035660505294799805, 0.048452138900756836, 0.06030440330505371, 0.07195305824279785, 0.08367443084716797, 0.09540987014770508, 0.10707855224609375, 0.11869525909423828, 0.13054752349853516, 0.14247393608093262, 0.15423583984375, 0.1658763885498047, 0.17781972885131836, 0.18955039978027344, 0.20127224922180176]
    wave1 = [14365, 10491, 11621, 17371, 25038, 29436, 29013, 23811, 16719, 11330, 10312, 14351, 21343, 27454, 29431, 26975, 20539, 13622]
    time2 = [8.821487426757812e-06, 0.011968612670898438, 0.023641109466552734, 0.03393983840942383, 0.04433846473693848, 0.05458998680114746, 0.06473612785339355, 0.07487940788269043, 0.0850977897644043, 0.09535956382751465, 0.10550093650817871, 0.11561751365661621, 0.12573027610778809, 0.13593220710754395, 0.1462996006011963, 0.1565103530883789, 0.16662931442260742, 0.17674732208251953, 0.18695783615112305, 0.19711709022521973, 0.20723867416381836]
    wave2 = [12206, 10350, 13094, 18703, 24937, 29093, 29679, 26430, 20558, 14560, 10703, 10451, 13896, 19749, 25772, 28853, 29048, 25583, 19671, 13941, 10388]
    time3 = [1.4543533325195312e-05, 0.012311935424804688, 0.023920059204101562, 0.034155845642089844, 0.04441499710083008, 0.05466270446777344, 0.06482958793640137, 0.07497477531433105, 0.08509325981140137, 0.09536337852478027, 0.10574102401733398, 0.11623549461364746, 0.126786470413208, 0.1370389461517334, 0.14725852012634277, 0.15747499465942383, 0.1676163673400879, 0.17786288261413574, 0.18806052207946777, 0.19827866554260254, 0.2084972858428955]
    wave3 = [23424, 28932, 29658, 26652, 20942, 14930, 10976, 10512, 13778, 19717, 25674, 28929, 28807, 25033, 18946, 13320, 10335, 11218, 15495, 21628, 26946]
    graph = list(zip(time2, wave2));
    graph = sorted(graph, key=lambda l:l[0])
    plt.xlabel('Time in seconds')
    plt.ylabel('Wave')
    x = [i[0] for i in graph]
    y = [i[1] for i in graph]
    plt.plot(x, y, marker='o')
    plt.show()
    return time2, wave2


def fourier(time, amplitude):
    N = len(time)  # size
    T = time[len(time)-1]/N  # step probably
    yf = fft(amplitude)  # fourier transform
    hzvals = linspace(0.0, 1.0/(2.0*T), N/2)
    amplitudes = 2.0/N * abs(yf[:N//2])
    fig, ax = plt.subplots()
    ax.plot(hzvals, amplitudes)
    ax.grid(True)
    plt.xlabel('Hz')
    plt.show()
    return hzvals, amplitudes



def fourierten(time, amplitude):
    x, y = fourier(time, amplitude)
    i = find_ten(x)
    return x[i], y[i]


def find_ten(x):
    closestindex = 0
    closest = inf
    index = 0
    closestdistance = inf
    for num in x:
        distance = abs(num-10)
        if distance < closestdistance:
            closest = num
            closestdistance = distance
            closestindex = index
        index += 1
    print(closest)
    print(closestdistance)
    return closestindex
