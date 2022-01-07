import struct
import sys

import pvporcupine


COLORS_RGB = dict(
    blue=(0, 0, 255),
    green=(0, 255, 0),
    orange=(255, 128, 0),
    pink=(255, 51, 153),
    purple=(128, 0, 128),
    red=(255, 0, 0),
    white=(255, 255, 255),
    yellow=(255, 255, 51),
    off=(0, 0, 0),
)

KEYWORDS_COLOR = {
    'alexa': 'yellow',
    'computer': 'white',
    'hey google': 'red',
    'hey siri': 'purple',
    'jarvis': 'pink',
    'picovoice': 'green',
    'porcupine': 'blue',
    'bumblebee': 'orange',
    'terminator': 'off',
}


class WakeWordDetection:

    RATE_PROCESS = 16000
    FRAME_LENGTH = 1024

    def __init__(self, sensitivity):
        super().__init__()
        self._keywords = list(KEYWORDS_COLOR.keys())
        self._porcupine = pvporcupine.create(keywords=self._keywords, sensitivities=[sensitivity] * len(KEYWORDS_COLOR))
        self._return = None

    def __del__(self):
        self._porcupine.delete()

    def frames_collector(self, frame_generator):
        frames_with_specific_length = None
        for frame in frame_generator:
            if frames_with_specific_length is None:
                frames_with_specific_length = frame
            else:
                frames_with_specific_length += frame
            if len(frames_with_specific_length) == self.FRAME_LENGTH:
                yield frames_with_specific_length
                frames_with_specific_length = None

    def detect_wake_word(self, frame_generator):
        frames = self.frames_collector(frame_generator)
        print('Awaiting WakeWord')
        for frame in frames:
            if len(frame) < self.FRAME_LENGTH:
                return

            pcm = struct.unpack_from("h" * self._porcupine.frame_length, frame)

            keyword_index = self._porcupine.process(pcm)
            if keyword_index >= 0:
                print("detected '%s'" % self._keywords[keyword_index])
                return COLORS_RGB[KEYWORDS_COLOR[self._keywords[keyword_index]]]
        print('No Frames')
