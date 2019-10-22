import pyaudio
import wave
import paho.mqtt.client as mqtt
import paho.mqtt.publish as pub

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
filename = "sent.wav"

p = pyaudio.PyAudio()  # Create an interface to PortAudio

print('Recording')

stream = p.open(format=sample_format, channels=channels, rate=fs, frames_per_buffer=chunk, input=True)

def on_connect(client, userdata, flags, rc):
	print("Connected. Start talking!")

client = mqtt.Client()
client.on_connect = on_connect

client.connect("broker.mqtt-dashboard.com", 1883, 60)

frames = []

try:
	while True:
		data = stream.read(chunk)
		frames.append(data)
		client.publish('wcnAudio', data)
		client.loop()
except KeyboardInterrupt:
	# Stop and close the stream 
	stream.stop_stream()
	stream.close()
	# Terminate the PortAudio interface
	p.terminate()
	client.disconnect

	print('Finished recording')

	# Save the recorded data as a WAV file
	wf = wave.open(filename, 'wb')
	wf.setnchannels(channels)
	wf.setsampwidth(p.get_sample_size(sample_format))
	wf.setframerate(fs)
	wf.writeframes(b''.join(frames))
	wf.close()