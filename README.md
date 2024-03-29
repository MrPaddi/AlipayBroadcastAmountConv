# 支付宝语音播报金额转换工具

语音格式：
```
支付宝到账 十二点五 元
```

代码库主要用于对支付宝金额生成/解析

## 支付宝金额语音生成

语音生成需要两步，获取发音单字和单字拼接成语音

### 1. 获取发音的单字
```
from num2upper import conv_amount_to_mandarin

assert conv_amount_to_mandarin("12.50") == "十二点五"
```

### 2. 根据单字拼接语音
在`alipay_word_wav`目录下基本的支付宝单字语音，使用 [Pydub](https://github.com/jiaaro/pydub) 对语音进行拼接
```
import os
from pydub import AudioSegment
from gen_broadcast_audio import gen_single_audio

dst_dir = "export"
random_amount = "4025.40"
_, amount_mandarin, amount_audio = gen_single_audio(random_amount)
assert isinstance(amount_audio, AudioSegment)
export_file_path = os.path.join(dst_dir, amount_mandarin+".wav")
amount_audio.export(export_file_path, format="wav")
```
批量文件生成可以使用`gen_batch_audio`。详情参考`gen_broadcast_audio.py`

*注：`Pydub`依赖[ffmpeg](http://ffmpeg.org/)*，相关资源请自行到网上查阅

## 支付宝语音金额解析

语音解析也需要两步，一个是语音识别，另一个是金额转换

### 1. 语音识别
国内各大厂有较成熟的语音识别工具，请查阅相关的资料文档进行调用

### 2. 金额转化
根据语音识别可以获得格式如`支付宝到账十二点五元`的内容，在简单的提取大写金额部分后可直接转化提取
```
from upper2num import conv_mandarin_to_amount

assert conv_mandarin_to_amount("十二点五") == 12.5
```

---
** 备注 **

1. 工具集诞生于支付宝语音识别项目准备数据集阶段，巧妇难为无米之炊啊

2. 网上很多金额转换的代码基于文书的，和支付宝语音发音并不一致。虽然有的改一改能用，但是...不好看😂

3. `conv_amount_to_mandarin`没有美感，有更好的实现或者重构方案请告诉我

4. 遇到什么bug请务必记得来打我的脸，脸已就位，诸君，请动手吧! 



