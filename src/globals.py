from src.chat_manager import ChatManager

apiKey = "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"
API_URL = "https://api.openai.com/v1/chat/completions"
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {apiKey}"}

summaryString = "请总结以上对话,不超过100个字。"
summaryTitleString = "make summary for this conversation in English, less than 3 words"

global myChat, delay
myChat = ChatManager()
delay = 0

SYS = "system"
USER = "user"
ASSISTANT = "assistant"
