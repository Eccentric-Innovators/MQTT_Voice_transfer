import pyaudio
import wave
import paho.mqtt.client as mqtt
import paho.mqtt.publish as pub

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
filename = "received.wav"

p = pyaudio.PyAudio()  # Create an interface to PortAudio

stream = p.open(format = sample_format, channels = channels, rate = fs, output = True)

def on_connect(client, userdata, flags, rc):
	client.subscribe("wcnAudio")
	print("Connected!")

frames = []

def on_message(client, userdata, msg):
	stream.write(msg.payload)
	frames.append(msg.payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.mqtt-dashboard.com", 1883, 60)

try:
	while True:
		client.loop()
except KeyboardInterrupt:
	stream.close()
	# Terminate the PortAudio interface
	p.terminate()
	client.disconnect()

	print('Closing...')

	# Save the recorded data as a WAV file
	wf = wave.open(filename, 'wb')
	wf.setnchannels(channels)
	wf.setsampwidth(p.get_sample_size(sample_format))
	wf.setframerate(fs)
	wf.writeframes(b''.join(frames))
	wf.close()