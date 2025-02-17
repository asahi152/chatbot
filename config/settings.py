# OpenAI 配置
API_KEY = "732a9a231689443eb067de5d345550fa"
ENDPOINT = "https://tzydemo1219.openai.azure.com/"
DEPLOYMENT = "gpt-4o"  

# Vosk 语音识别配置
MODEL_PATH = "models/vosk-model-small-cn-0.22"
SAMPLE_RATE = 16000
VAD_AGGRESSIVENESS = 3  # VAD灵敏度 (0-3)

# 音频配置
FRAME_DURATION = 30  # 每帧持续时间（毫秒）
SILENCE_THRESHOLD = 1.0  # 静音判断阈值（秒）
SPEAKING_THRESHOLD = 0.3  # 说话判断阈值（秒）

# TTS配置
TTS_MODEL_NAME = "tts_models/zh-CN/baker/fastspeech2"
TTS_SAMPLE_RATE = 22050
TTS_ENABLE_GPU = True
TTS_SHOW_PROGRESS = False

# 日志配置
LOG_FILE = "chat_logs.txt"
ERROR_LOG_FILE = "error_logs.txt"

# 其他配置
DEBUG = True  # 调试模式开关
