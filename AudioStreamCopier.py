import queue
import wave

import numpy as np
from scipy import signal
import pyaudio


class AudioStreamCopier(object):

    FORMAT = pyaudio.paInt16
    RATE_PROCESS = 16000
    CHANNELS = 1
    BLOCKS_PER_SECOND = 250

    def __init__(self, device: int = 0, input_rate=RATE_PROCESS, callback=None, file=None):
        def proxy_callback(in_data, frame_count, time_info, status):
            # pylint: disable=unused-argument
            if self.chunk is not None:
                in_data = self.wf.readframes(self.chunk)
            callback(in_data)
            return None, pyaudio.paContinue

        if callback is None:
            callback = lambda in_data: self.buffer_queue.put(in_data)

        self.buffer_queue = queue.Queue()

        self.input_rate = input_rate
        self.sample_rate = self.RATE_PROCESS
        self.block_size = int(self.RATE_PROCESS / float(self.BLOCKS_PER_SECOND))
        self.block_size_input = int(self.input_rate / float(self.BLOCKS_PER_SECOND))
        self.pa = pyaudio.PyAudio()

        kwargs = {
            'format': self.FORMAT,
            'channels': self.CHANNELS,
            'rate': self.input_rate,
            'input': True,
            'frames_per_buffer': self.block_size,
            'stream_callback': proxy_callback,
        }
        self.chunk = None

        if device:
            kwargs['input_device_index'] = device
        elif file is not None:
            self.chunk = 512
            self.wf = wave.open(file, 'rb')
        self.audio_stream = self.pa.open(**kwargs)
        self.audio_stream.start_stream()

    def resample(self, data):
        """
        Microphone may not support our native processing sampling rate, so
        resample from stream_rate to RATE_PROCESS here for webrtcvad,
        deepspeech and pvporcupine

        Args:
            data (binary): Input audio stream
        """
        data16 = np.fromstring(string=data, dtype=np.int16)
        resample_size = int(len(data16) / self.input_rate * self.RATE_PROCESS)
        resample = signal.resample(data16, resample_size)
        resample16 = np.array(resample, dtype=np.int16)
        return resample16.tostring()

    def read_resampled(self):
        """Return a block of audio data resampled to 16000hz, blocking if necessary."""
        return self.resample(data=self.buffer_queue.get())

    def read(self):
        """Return a block of audio data, blocking if necessary."""
        return self.buffer_queue.get()

    def destroy(self):
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.pa.terminate()

    frame_duration_ms = property(lambda self: 1000 * self.block_size // self.sample_rate)