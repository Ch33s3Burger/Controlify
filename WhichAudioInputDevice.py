import pyaudio
import os


def get_audio_devices():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        print(p.get_device_info_by_index(i))


print(os.getcwd())
get_audio_devices()
