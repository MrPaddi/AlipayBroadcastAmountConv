import os
import unittest
from random import uniform

from pydub import AudioSegment

from gen_broadcast_audio import (_audio_segment_from_wav, gen_batch_audio,
                                 _get_file_abs_path, conv_amount_to_mandarin,
                                 gen_single_audio, is_usable_dir)


class GenAudio(unittest.TestCase):

    def setUp(self):
        self.dst_dir = "export_test"
        if not is_usable_dir(self.dst_dir):
            raise OSError("目录不可写， 检查目录权限：{}".format(self.dst_dir))
            

    def test_is_usable_dir(self):
        self.assertTrue(is_usable_dir(os.path.join("test1", "test2", "test3")))
        self.assertRaises(OSError, is_usable_dir, "128#@!@##$%#$%^&*ad]d123")
    
    def test_audio_segment_from_wav(self):
        self.assertIsInstance(_audio_segment_from_wav("tts_0.wav"), AudioSegment)
        self.assertRaises(FileNotFoundError, _audio_segment_from_wav, "tts_01.wav")
    
    def test_gen_single_audio(self):
        random_amount = "4025.40"

        _, amount_mandarin, amount_audio = gen_single_audio(random_amount)
        self.assertIsInstance(amount_audio, AudioSegment)

        export_file_path = os.path.join(self.dst_dir, amount_mandarin+".wav")
        amount_audio.export(export_file_path, format="wav")
        self.assertTrue(os.path.isfile(export_file_path))
    
    def test_gen_batch_audio(self):
        count = 50
        batch_amount = ("{:.2f}".format(uniform(0,100)) for i in range(count))
        
        for _, amount_mandarin, amount_audio in gen_batch_audio(batch_amount):
            self.assertIsInstance(amount_audio, AudioSegment)
            export_file_path = os.path.join(self.dst_dir, amount_mandarin+".wav")
            amount_audio.export(export_file_path, format="wav")
            self.assertTrue(os.path.isfile(export_file_path))
            
            
    

        