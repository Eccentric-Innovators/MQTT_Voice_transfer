import pyaudio
import threading

chunk = 1024
sample_format = pyaudio.paInt16
channels = 2
fs = 44100

p = pyaudio.PyAudio()

inStream = p.open(format=sample_format, channels=channels, rate=fs, frames_per_buffer=chunk, input=True)

outStream = p.open(format = sample_format, channels = channels, rate = fs, output = True)

delay = .2

frames = []

print("Start!")

for i in range(0, int(fs / chunk * delay)):
	frames.append(inStream.read(chunk))

class StoppableThread(threading.Thread):
	def __init__(self, target):
		threading.Thread.__init__(self, target = target)
	
	def stop(self):
		self._stop()

def rec():
	while True:
		frames.append(inStream.read(chunk))

def play():
	while frames:
		outStream.write(frames.pop(0))

try:
	recT = StoppableThread(target=rec)
	playT = StoppableThread(target=play)
	recT.daemon = True
	playT.daemon = True
	recT.start()
	playT.start()
	while True:
		i = 1
except KeyboardInterrupt:
	recT.stop()
	playT.stop()
	inStream.stop_stream()
	inStream.close()
	outStream.close()
	p.terminate()
	exit()