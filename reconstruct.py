import scipy.io.wavfile
import math
import numpy as np

import seaborn as sns
import matplotlib.pylab as plt

rate, datamaster = scipy.io.wavfile.read('soundfiles/orig.wav')
print(len(datamaster))

databuf = np.arange(len(datamaster), dtype=np.int16)

#ring with r = 0.15 and 24 microphones

mic = 24

resX = 120 # max degree
resY = 120 # max degree

angX = 0
angY = 0

r = 0.15 # radius
c = 343 # speed of sound

delay = 0
frame = np.zeros(shape=(resX,resY)) # framebuffer

for x in range(-resX/2, resX/2):
    for y in range(-resY/2, resY/2):

        correlation = 0
        for a in range(mic): # for each microphone
            rate, datacor = scipy.io.wavfile.read('soundfiles/' + str(a) + ".wav")
            delay = np.tan(x * np.pi / 180.) * r * np.cos((2.*np.pi*a)/mic)
            delay = delay + np.tan(y * np.pi / 180.) * r * np.sin((2.*np.pi*a)/mic)
            delay = int((delay / c) * rate) # delay in samples

            for i in range(32): # correlation window size
                correlation = correlation + (float(datacor[i+100+delay]) * 0.001 * float(datamaster[i+100]) * 0.001)
                # plus 100 so we can "go back in time"

        frame[x+resX / 2][y+resY / 2] = correlation
ax = sns.heatmap(frame, linewidth=0)
plt.show()
