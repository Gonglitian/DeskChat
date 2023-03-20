from src.chat_manager import ChatManager

apiKey = 0
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


icon_dir = "./resource/icons/"

html_head = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Chat</title>
    <link href="./state/mycss.css" type="text/css" rel="stylesheet"></link>
</head>
<body>"""

html_tail = """</body>
</html>"""
