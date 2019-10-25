import os
from warnings import warn

from pydub import AudioSegment

from num2upper import conv_amount_to_mandarin


WAV_BASIC_DIR = os.path.join(os.path.dirname(__file__), "alipay_word_wav")

_get_file_abs_path = lambda x: os.path.abspath(os.path.join(WAV_BASIC_DIR, x))

_get_speech_mandarin = lambda x: "".join(())


def _audio_segment_from_wav(filename):
    file_path = _get_file_abs_path(filename)
    if not os.access(file_path, os.F_OK):
        raise FileNotFoundError(file_path)
    return AudioSegment.from_wav(file_path)

SUCCESS_WAV = _audio_segment_from_wav("tts_success.wav")

YUAN_WAV = _audio_segment_from_wav("tts_yuan.wav")

UPPER_WAV_MAPPING = {
    "零": _audio_segment_from_wav("tts_0.wav"),
    "一": _audio_segment_from_wav("tts_1.wav"),
    "二": _audio_segment_from_wav("tts_2.wav"),
    "三": _audio_segment_from_wav("tts_3.wav"),
    "四": _audio_segment_from_wav("tts_4.wav"),
    "五": _audio_segment_from_wav("tts_5.wav"),
    "六": _audio_segment_from_wav("tts_6.wav"),
    "七": _audio_segment_from_wav("tts_7.wav"),
    "八": _audio_segment_from_wav("tts_8.wav"),
    "九": _audio_segment_from_wav("tts_9.wav"),
    "十": _audio_segment_from_wav("tts_ten.wav"),
    "百": _audio_segment_from_wav("tts_hundred.wav"),
    "千": _audio_segment_from_wav("tts_thousand.wav"),
    "万": _audio_segment_from_wav("tts_ten_thousand.wav"),
    "亿": _audio_segment_from_wav("tts_ten_million.wav"),
    "点": _audio_segment_from_wav("tts_dot.wav"),
}

def is_usable_dir(dir_path):
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path, mode=0o755)
    if not os.access(dir_path, os.W_OK):
        return False
    return True
    

def gen_single_audio(amount_str):
    amount_mandarin = conv_amount_to_mandarin(amount_str)

    alipay_speech = SUCCESS_WAV
    for char in amount_mandarin:
        if char in UPPER_WAV_MAPPING:
            alipay_speech += UPPER_WAV_MAPPING[char]
        else:
            warn("? 怎么会出现{}这个字符呢? 参数为{}, 转换为{}".format(char, amount_str, amount_mandarin))
    alipay_speech += YUAN_WAV
    return amount_str, amount_mandarin, alipay_speech


gen_batch_audio = lambda x: (gen_single_audio(i) for i in x)


if __name__ == "__main__":
    from random import uniform
    from time import strftime, localtime

    dst_dir = "export"

    if not is_usable_dir(dst_dir):
        raise OSError("目录不可写， 检查目录权限：{}".format(dst_dir))

    count = 500
    batch_amount = ("{:.2f}".format(uniform(0,1000)) for i in range(count))
    
    for _, amount_mandarin, amount_audio in gen_batch_audio(batch_amount):
        export_file_path = os.path.join(dst_dir, amount_mandarin+".wav")
        amount_audio.export(export_file_path, format="wav")
        # 文件名即为该wav文件的label
        print("[生成文件]：{}".format(export_file_path))

            