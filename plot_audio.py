import numpy as np
import matplotlib.pyplot as plt
import wave
import sys

filename = sys.argv[1]

wf = wave.open(filename, 'rb')

chunk = 1024

data = []

temp = 1

while temp:
	temp = wf.readframes(chunk)
	data.extend([int(x) for x in temp])

plt.plot(np.arange(len(data)), data)
plt.show()