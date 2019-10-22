import numpy as np
import wave

wf = wave.open("sent.wav", 'rb')

chunk = 1024

sent = []

temp = 1

while temp:
	temp = wf.readframes(chunk)
	sent.extend([int(x) for x in temp])

wf = wave.open("received.wav", 'rb')

chunk = 1024

recd = []

temp = 1

while temp:
	temp = wf.readframes(chunk)
	recd.extend([int(x) for x in temp])

print("Audio received perfectly?", (np.array(sent)==np.array(recd)).all())