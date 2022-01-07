import collections
import logging
import os
import os.path
import time
from threading import Thread

import deepspeech
import numpy as np
import webrtcvad
from halo import Halo

from ColorManager import ColorManager

import Controlify as sp


class DeepSpeechTranslator:

    FRAME_LENGTH = 640

    def __init__(self, models_dir, scorer_name, model_name=None, spinner=True, aggressiveness=3):
        self.spinner = spinner
        self.listening = False
        self.time_of_wake_word = 0
        if model_name is None:
            self.load_deepspeech_model(models_dir, scorer_name)
        else:
            self.load_deepspeech_model(models_dir, scorer_name, model_name)
        self.vad = webrtcvad.Vad(aggressiveness)

    def load_deepspeech_model(self, models_dir, scorer_name, model_name='deepspeech-0.8.2-models.tflite'):
        if os.path.isdir(models_dir):
            print('Initializing model...')
            model_path = os.path.join(models_dir, model_name)
            scorer_path = os.path.join(models_dir, scorer_name)

            logging.info("ARGS.model: %s", model_path)
            self.model = deepspeech.Model(model_path)
            logging.info("ARGS.scorer: %s", scorer_path)
            self.model.enableExternalScorer(scorer_path)

            self.stream_context = self.model.createStream()

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

    def vad_collector(self, frame_generator, padding_ms=300, ratio=0.75, frames=None):
        """Generator that yields series of consecutive audio frames comprising each utterence, separated by yielding a single None.
            Determines voice activity by ratio of frames in padding_ms. Uses a buffer to include padding_ms prior to being triggered.
            Example: (frame, ..., frame, None, frame, ..., frame, None, ...)
                      |---utterence---|        |---utterence---|
        """
        frames = self.frames_collector(frame_generator)
        # num_padding_frames = padding_ms // frame_duration_ms
        ring_buffer = collections.deque(maxlen=15)
        triggered = False

        for frame in frames:
            if len(frame) < self.FRAME_LENGTH:
                return

            is_speech = self.vad.is_speech(frame, 16000)

            if not triggered:
                ring_buffer.append((frame, is_speech))
                num_voiced = len([f for f, speech in ring_buffer if speech])
                if num_voiced > ratio * ring_buffer.maxlen:
                    triggered = True
                    for f, s in ring_buffer:
                        yield f
                    ring_buffer.clear()

            else:
                yield frame
                ring_buffer.append((frame, is_speech))
                num_unvoiced = len([f for f, speech in ring_buffer if not speech])
                if num_unvoiced > ratio * ring_buffer.maxlen:
                    triggered = False
                    yield None
                    ring_buffer.clear()

    def listen(self, frame_generator, color):
        frames = self.vad_collector(frame_generator)
        color_manager = ColorManager(color)
        color_manager.start()
        self.time_of_wake_word = time.time()
        while True:
            spinner = None
            if self.spinner:
                spinner = Halo(spinner='line')

            for frame in frames:
                if frame is not None:
                    # print(len(frame))
                    if spinner: spinner.start()
                    logging.debug("streaming frame")
                    self.stream_context.feedAudioContent(np.frombuffer(frame, np.int16))
                else:
                    # print('frame is None')
                    if spinner: spinner.stop()
                    logging.debug("end utterence")
                    text = self.stream_context.finishStream()
                    print('said: ' + text)
                    if 'next' in text:
                        sp.next_track()
                    elif text == 'previous':
                        sp.previous_track()
                    elif text == 'stop' or text == 'pause':
                        sp.pause_playback()
                    elif text == 'play' or text == 'start':
                        sp.start_playback()
                    self.stream_context = self.model.createStream()
                    if (time.time() - self.time_of_wake_word) > 5:
                        return