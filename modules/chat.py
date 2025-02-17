from openai import AzureOpenAI
from config.settings import (
    API_KEY,
    ENDPOINT,
    DEPLOYMENT
)
from modules.logger import Logger

#调用chatgpt的API
class ChatBot:    
    def __init__(self):
        # 初始化Azure OpenAI客户端
        self.client = AzureOpenAI(
            azure_endpoint=ENDPOINT,
            api_key=API_KEY,
            api_version="2024-02-01"  
        )
        self.logger = Logger()
        
        # 存储对话历史
        self.conversation_history = [
            {"role": "system", "content": "你是一个AI助手，可以帮助用户回答问题。"}
        ]
        
    def get_response(self, user_input):
        try:
            # 添加用户输入到对话历史
            self.conversation_history.append(
                {"role": "user", "content": user_input}
            )
            
            # 调用API获取响应
            response = self.client.chat.completions.create(
                model=DEPLOYMENT,
                messages=self.conversation_history,
                temperature=0.7,
                max_tokens=800
            )
            
            # 获取响应文本
            ai_response = response.choices[0].message.content
            
            # 添加AI响应到对话历史
            self.conversation_history.append(
                {"role": "assistant", "content": ai_response}
            )
            
            # 控制对话历史长度，防止过长
            if len(self.conversation_history) > 10:
                # 保留system提示和最近的4轮对话
                self.conversation_history = (
                    self.conversation_history[:1] +
                    self.conversation_history[-8:]
                )
            
            # 记录对话
            self.logger.log_conversation(user_input, ai_response)
            
            return ai_response
            
        except Exception as e:
            print(f"GPT API调用错误: {str(e)}")
            return "抱歉，我现在无法正常回答，请稍后再试。"

#重置对话历史   
    def reset_conversation(self):
        self.conversation_history = [
            {"role": "system", "content": "你是一个友好的AI助手，可以帮助用户回答问题。"}
        ]

if __name__ == "__main__":
    chatbot = ChatBot()
    
    try:
        while True:
            user_input = input("你: ")
            if user_input.lower() in ['退出', 'quit', 'exit']:
                break
                
            response = chatbot.get_response(user_input)
            print(f"AI: {response}")
            
    except KeyboardInterrupt:
        print("\n程序已终止")