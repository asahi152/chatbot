import os
from datetime import datetime

class Logger:
    def __init__(self):
        # 创建logs目录
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # 生成带日期的日志文件名
        date = datetime.now().strftime("%Y%m%d")
        self.log_file = os.path.join(log_dir, f"chat_log_{date}.txt")
    
    def log_conversation(self, user_input, ai_response):
        """记录对话内容"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n[{timestamp}]\n")
            f.write(f"User: {user_input}\n")
            f.write(f"Assistant: {ai_response}\n")
            f.write("-" * 50 + "\n")

# 使用示例
if __name__ == "__main__":
    logger = Logger()
    logger.log_conversation("你好", "你好!我是AI助手")