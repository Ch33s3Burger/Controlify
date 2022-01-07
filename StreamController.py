import os

from AudioStreamCopier import AudioStreamCopier
from STT_DeepSpeech import DeepSpeechTranslator
from WakeWordDetection import WakeWordDetection


class StreamController(AudioStreamCopier):

    def __init__(self, models_dir, scorer_name, model_name=None, sensitivity=0.3):
        super().__init__()
        self.stt_deepspeech = DeepSpeechTranslator(models_dir, scorer_name, model_name=model_name)
        self.wakeword_detection = WakeWordDetection(sensitivity)

    def frame_generator(self):
        """Generator that yields all audio frames from microphone."""
        if self.input_rate == self.RATE_PROCESS:
            while True:
                yield self.read()
        else:
            while True:
                yield self.read_resampled()

    def start_speech_recocnition(self):
        frame_generator = self.frame_generator()
        while True:
            color = self.wakeword_detection.detect_wake_word(frame_generator)
            self.stt_deepspeech.listen(frame_generator, color)


if __name__ == '__main__':

    DEFAULT_SAMPLE_RATE = 16000

    import argparse

    parser = argparse.ArgumentParser(description="Stream from microphone to DeepSpeech using VAD")

    parser.add_argument('-v', '--vad_aggressiveness', type=int, default=3,
                        help="Set aggressiveness of VAD: an integer between 0 and 3, 0 being the least aggressive about filtering out non-speech, 3 the most aggressive. Default: 3")
    parser.add_argument('--nospinner', action='store_true',
                        help="Disable spinner")
    parser.add_argument('-w', '--savewav',
                        help="Save .wav files of utterences to given directory")
    parser.add_argument('-f', '--file',
                        help="Read from .wav file instead of microphone")

    parser.add_argument('-m', '--model', required=True,
                        help="Path to the model (protocol buffer binary file, or entire directory containing all standard-named files for model)")
    parser.add_argument('-s', '--scorer',
                        help="Path to the external scorer file.")
    parser.add_argument('-d', '--device', type=int, default=None,
                        help="Device input index (Int) as listed by pyaudio.PyAudio.get_device_info_by_index(). If not provided, falls back to PyAudio.get_default_device().")
    parser.add_argument('-r', '--rate', type=int, default=DEFAULT_SAMPLE_RATE,
                        help=f"Input device sample rate. Default: {DEFAULT_SAMPLE_RATE}. Your device may require 44100.")
    parser.add_argument('-k', '--keyboard', action='store_true',
                        help="Type output through system keyboard")
    ARGS = parser.parse_args()
    if ARGS.savewav:
        os.makedirs(ARGS.savewav, exist_ok=True)

    sc = StreamController(ARGS.model, ARGS.scorer)
    sc.start_speech_recocnition()
