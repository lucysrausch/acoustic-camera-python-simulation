import scipy.io.wavfile
import math
import numpy as np

rate, data = scipy.io.wavfile.read('oh-yeah-2.wav')
print(len(data))

datanew = np.arange(int(rate*0.1), dtype=np.int16)


#ring with r = 0.15 and 24 microphones

mic = 24

angX = 30
angY = 20
r = 0.15
c = 343

delay = 0

mu, sigma = 0, 10000

for i in range(0, int(rate * 0.1)): # use a 0.1sec long snipped
    datanew[i] = data[i+10000][0] # ...from somewhere in the middle of the sampple
scipy.io.wavfile.write("soundfiles/" + "orig.wav", rate, datanew)

for a in range(mic):
    delay = np.tan(angX * np.pi / 180.) * r * np.cos((2.*np.pi*a)/mic)
    delay = delay + np.tan(angY * np.pi / 180.) * r * np.sin((2.*np.pi*a)/mic)
    delay = int((delay / c) * rate)
    print(delay)
    for i in range(0, int(rate * 0.1)):
        datanew[i] = data[i+10000+delay][0]

    noise = np.random.normal(mu, sigma, datanew.shape)
    datanew = datanew + noise
    scipy.io.wavfile.write("soundfiles/" + str(a) + ".wav", rate, datanew)
