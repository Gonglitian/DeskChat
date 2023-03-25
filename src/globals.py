from src.chat_manager import ChatManager
from src.utils import *
import datetime

apiKey = 0
API_URL = "https://api.openai.com/v1/chat/completions"
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {apiKey}"}

summaryString = "请总结以上对话,不超过100个字。"
summaryTitleString = "make summary for this conversation in English, less than 3 words"

global myChat, delay
myChat = ChatManager(title=("New Chat " + processTime(datetime.datetime.now())))
delay = 0

SYS = "system"
USER = "user"
ASSISTANT = "assistant"

AUTORENAME = False

icon_dir = "./resource/icons/"
user_dir = "./user/"

with open("./state/mycss.css", "r", encoding="utf-8") as f:
    mycss = f.read()

initialHtml = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Chat</title>
    <style>{mycss}</style>
</head>
<body>
<div id = "chat-page" class="chat-wrap"></div>
</body>
</html>"""
