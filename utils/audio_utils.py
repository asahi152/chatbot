import numpy as np
import soundfile as sf
import sounddevice as sd
from config.settings import TTS_SAMPLE_RATE

class AudioUtils:
    @staticmethod
    def play_audio(audio_data, sample_rate=TTS_SAMPLE_RATE):
        """播放音频数据"""
        try:
            sd.play(audio_data, sample_rate)
            sd.wait()  # 等待音频播放完成
        except Exception as e:
            print(f"音频播放错误: {str(e)}")

    @staticmethod
    def save_audio(audio_data, filename, sample_rate=TTS_SAMPLE_RATE):
        """保存音频到文件"""
        try:
            sf.write(filename, audio_data, sample_rate)
            return True
        except Exception as e:
            print(f"音频保存错误: {str(e)}")
            return False

    @staticmethod
    def load_audio(filename):
        """加载音频文件"""
        try:
            audio_data, sample_rate = sf.read(filename)
            return audio_data, sample_rate
        except Exception as e:
            print(f"音频加载错误: {str(e)}")
            return None, None

    @staticmethod
    def normalize_audio(audio_data):
        """音频归一化"""
        try:
            return audio_data / np.max(np.abs(audio_data))
        except Exception as e:
            print(f"音频归一化错误: {str(e)}")
            return audio_data

# 使用示例
if __name__ == "__main__":
    # 测试音频功能
    test_audio, sr = AudioUtils.load_audio("test.wav")
    if test_audio is not None:
        # 归一化
        normalized_audio = AudioUtils.normalize_audio(test_audio)
        # 播放
        AudioUtils.play_audio(normalized_audio, sr)
        # 保存
        AudioUtils.save_audio(normalized_audio, "normalized_test.wav", sr)