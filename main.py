from modules.asr import RealtimeASR
from modules.chat import ChatBot
from modules.tts import FastSpeech2TTS
from config.settings import MODEL_PATH

class VoiceAssistant:
    def __init__(self):
        print("初始化语音助手...")
        # 初始化各个模块
        self.asr = RealtimeASR(MODEL_PATH)
        self.chatbot = ChatBot()
        self.tts = FastSpeech2TTS()
        
    def on_speech_recognized(self, text):
        """处理识别到的语音"""
        if not text:  # 如果识别结果为空
            return
            
        print(f"用户: {text}")
        
        # 获取ChatGPT回复
        response = self.chatbot.get_response(text)
        print(f"助手: {response}")
        
        # 将回复转换为语音
        self.tts.synthesize(response)

    def run(self):
        """运行语音助手"""
        try:
            print("语音助手已启动，请说话...")
            # 开始监听，传入回调函数
            self.asr.start_listening(callback_fn=self.on_speech_recognized)
            
        except KeyboardInterrupt:
            print("\n程序已停止")
        except Exception as e:
            print(f"发生错误: {str(e)}")
        finally:
            # 重置对话历史
            self.chatbot.reset_conversation()

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()