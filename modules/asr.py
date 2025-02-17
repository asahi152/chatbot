import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json
import numpy as np
import webrtcvad
import time

from config.settings import (
    SAMPLE_RATE,
    VAD_AGGRESSIVENESS,
    FRAME_DURATION,
    SILENCE_THRESHOLD,
    SPEAKING_THRESHOLD
)

"""语音识别，带有VAD检测"""
class RealtimeASR:
    def __init__(self, model_path, sample_rate=SAMPLE_RATE, vad_aggressiveness=VAD_AGGRESSIVENESS):
        # 初始化Vosk模型
        self.model = Model(model_path)
        self.sample_rate = sample_rate
        self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
        self.audio_queue = queue.Queue()
        
        # 初始化VAD
        self.vad = webrtcvad.Vad(vad_aggressiveness)
        self.frame_duration = FRAME_DURATION
        self.silence_threshold = SILENCE_THRESHOLD
        self.speaking_threshold = SPEAKING_THRESHOLD
        
        # 状态变量
        self.is_speaking = False
        self.last_speech_time = time.time()
        self.speech_buffer = []
        self.silence_start_time = None
        
    def is_speech(self, audio_chunk):
        try:
            return self.vad.is_speech(audio_chunk, self.sample_rate)
        except:
            return False

#音频流回调函数            
    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.audio_queue.put(bytes(indata))
    
    def process_audio(self, audio_data):
        if self.recognizer.AcceptWaveform(audio_data):
            result = json.loads(self.recognizer.Result())
            return result.get('text', '').strip()
        return ''

    def start_listening(self, callback_fn=None):
        try:
            with sd.RawInputStream(
                samplerate=self.sample_rate,
                blocksize=int(self.sample_rate * self.frame_duration / 1000),
                dtype='int16',
                channels=1,
                callback=self.audio_callback
            ):
                print("开始监听，请说话...")
                
                while True:
                    audio_data = self.audio_queue.get()
                    is_speech = self.is_speech(audio_data)
                    current_time = time.time()
                    
                    if is_speech:
                        if not self.is_speaking:
                            self.is_speaking = True
                            self.speech_buffer = []
                            print("检测到说话...")
                        
                        self.last_speech_time = current_time
                        self.speech_buffer.append(audio_data)
                        self.silence_start_time = None
                        
                    else:  # 当前帧是静音
                        if self.is_speaking:
                            if self.silence_start_time is None:
                                self.silence_start_time = current_time
                            
                            # 判断是否说完话（静音持续超过阈值）
                            if current_time - self.silence_start_time > self.silence_threshold:
                                # 处理完整的语音片段
                                if self.speech_buffer:
                                    audio_segment = b''.join(self.speech_buffer)
                                    text = self.process_audio(audio_segment)
                                    if text and callback_fn:
                                        callback_fn(text)
                                
                                # 重置状态
                                self.is_speaking = False
                                self.speech_buffer = []
                                print("等待下一次说话...")
                            else:
                                # 静音还不够长，继续收集数据
                                self.speech_buffer.append(audio_data)
                        
        except KeyboardInterrupt:
            print("\n停止录音")
        except Exception as e:
            print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    def print_result(text):
        print(f"识别结果: {text}")
        
    MODEL_PATH = "models/vosk-model-small-cn-0.22"  # 替换为你的模型路径
    asr = RealtimeASR(MODEL_PATH)
    asr.start_listening(callback_fn=print_result)