import scipy.io.wavfile
import math
import numpy as np

import seaborn as sns
import matplotlib.pylab as plt
import time

rate, data = scipy.io.wavfile.read('oh-yeah-2.wav')
print(len(data))

#ring with r = 0.15 and 24 microphones

rate = 96000 #samplerate in Hz

mic = 16

angX = 30
angY = 15
rx = 0.15
ry = 0.15
c = 343

delay = 0

resX = 120 # max degree
resY = 70 # max degree

mu, sigma = 0, 8000

datanew = np.arange(int(rate*0.1), dtype=np.int16)
datamaster = np.arange(int(rate*0.1), dtype=np.int16)

frame = np.zeros(shape=(resY,resX)) # framebuffer

for i in range(0, int(rate * 0.1)): # use a 0.1sec long snipped
    datamaster[i] = data[i+10000][0] # ...from somewhere in the middle of the sampple


for mic in range(2, 32):
    datacor = np.zeros(shape=(mic,len(datamaster)), dtype=np.int16)

    for a in range(mic):
        delay = np.tan(angX * np.pi / 180.) * rx * np.cos((2.*np.pi*a)/mic)
        delay = delay + np.tan(angY * np.pi / 180.) * ry * np.sin((2.*np.pi*a)/mic)
        delay = int((delay / c) * rate)

        for i in range(0, int(rate * 0.1)):
            datacor[a][i] = data[i+10000+delay][0]

        noise = np.random.normal(mu, sigma, datanew.shape)
        datacor[a] = datacor[a] + noise

    delay = 0

    for x in range(-resX/2, resX/2):
        for y in range(-resY/2, resY/2):

            correlation = 0
            for a in range(mic):
                delay = np.tan(x * np.pi / 180.) * rx * np.cos((2.*np.pi*a)/mic)
                delay = delay + np.tan(y * np.pi / 180.) * ry * np.sin((2.*np.pi*a)/mic)
                delay = int((delay / c) * rate) # delay in samples

                master = datamaster[100:132] * 0.001
                slave = datacor[a][100+delay:132+delay] * 0.001

                correlation = correlation + np.correlate(master, slave)

            frame[y+resY / 2][x+resX / 2] = correlation

    fig, ax = plt.subplots(1, 1)
    plt.tight_layout()
    sns.heatmap(frame**2, linewidth=0, ax=ax, square=True,)
    plt.savefig('colorlist.png')
    print(mic)
