from TTS.api import TTS
import torch
import numpy as np
import soundfile as sf
from config.settings import (
    TTS_SAMPLE_RATE,
    TTS_MODEL_NAME,
    TTS_ENABLE_GPU,
    TTS_SHOW_PROGRESS
)
from modules.audio_utils import AudioUtils

class FastSpeech2TTS:
    def __init__(self):
        # 使用配置文件中的参数
        self.tts = TTS(
            model_name=TTS_MODEL_NAME,
            progress_bar=TTS_SHOW_PROGRESS,
            gpu=TTS_ENABLE_GPU and torch.cuda.is_available()
        )
        
    def synthesize(self, text, duration_control=1.0):
        try:
            # 生成语音
            wav = self.tts.tts(
                text=text,
                speed=duration_control
            )
            # 归一化音频
            wav = AudioUtils.normalize_audio(wav)
            # 直接播放
            AudioUtils.play_audio(wav, TTS_SAMPLE_RATE)
            # 保存音频（如果需要）
            # AudioUtils.save_audio(wav, "output.wav", TTS_SAMPLE_RATE)
            return np.array(wav)
            
        except Exception as e:
            print(f"TTS生成错误: {str(e)}")
            return None

# 使用示例
if __name__ == "__main__":
    # 初始化TTS模型
    tts = FastSpeech2TTS()
    
    # 测试中文
    wav = tts.synthesize(
        text="你好，我是语音助手。", 
        duration_control=1.0
    )
    
    if wav is not None:
        # 保存音频
        sf.write("output.wav", wav, TTS_SAMPLE_RATE)