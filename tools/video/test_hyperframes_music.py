import tempfile
import unittest
import wave
from pathlib import Path
from build_hyperframes_music import DURATION, SAMPLE_RATE, synth_sample, write_music_bed

class HyperFramesMusicTests(unittest.TestCase):
    def test_synth_is_deterministic_and_bounded(self):
        self.assertEqual(synth_sample(3.25), synth_sample(3.25))
        for timestamp in (0.0, 0.5, 4.25, 8.5, 12.75, 16.9):
            left, right = synth_sample(timestamp)
            self.assertLessEqual(abs(left), 0.6)
            self.assertLessEqual(abs(right), 0.6)

    def test_writer_outputs_stereo_pcm_at_expected_duration(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ambient.wav"
            write_music_bed(path)
            with wave.open(str(path), "rb") as wav:
                self.assertEqual(wav.getnchannels(), 2)
                self.assertEqual(wav.getsampwidth(), 2)
                self.assertEqual(wav.getframerate(), SAMPLE_RATE)
                self.assertEqual(wav.getnframes(), round(SAMPLE_RATE * DURATION))
                self.assertAlmostEqual(wav.getnframes() / wav.getframerate(), DURATION)

    def test_writer_produces_non_silent_audio(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ambient.wav"
            write_music_bed(path)
            with wave.open(str(path), "rb") as wav:
                data = wav.readframes(wav.getnframes())
            self.assertTrue(any(byte != 0 for byte in data))

if __name__ == "__main__":
    unittest.main(verbosity=2)
