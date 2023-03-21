from src.chat_manager import ChatManager

apiKey = "sk-xZWnNf1EtOwJH3MlKh9pT3BlbkFJwlKjfp8UYpw9liSv8S6"
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

with open("./state/mycss.css", "r", encoding="utf-8") as f:
    mycss = f.read()

html_head = f"""<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Chat</title>
    <style>{mycss}</style>
    </link>
</head>

<body>"""

html_tail = """</body>

</html>"""

# html_code = """<!DOCTYPE html>
# <html>
#   <head>
#     <title>Test HTML page</title>
#   </head>
#   <body>
#     <h1>Hello, world!</h1>
#     <p>This is a test page.</p>
#   </body>
# </html>"""
# self.bot_html.setHtml(html_code)
