import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QThread, pyqtSignal  # 导入线程模块
from PyQt5 import QtGui
from PyQt5.QtGui import QTextCursor
from Mainwindow import Ui_MainWindow
import markdown
import requests, json
import traceback


API_URL = "https://api.openai.com/v1/chat/completions"
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {apiKey}"}

bot = []
bot_format = []
botFlag = True
userFlag = 1 - botFlag


totalCount = 0
testHtml = """
<html>
<head>
    <style type="text/css">
        div {
            border-radius: 10px; /* 圆角半径为 10px */
            background-color: #EFEFEF;
            padding: 10px;
        }
    </style>
</head>
<body>
    <div>Hello, world!</div>
</body>
</html>
"""


class DemoMain(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # 初始化父类
        super().__init__()
        # 初始化界面
        self.setupUi(self)
        self.initQTextBrowser()
        # 绑定逻辑
        self.send_btn.setEnabled(False)
        self.send_btn.clicked.connect(self.startRequestTask)
        self.shut_btn.clicked.connect(self.shutRequestTask)
        self.user_text.textChanged.connect(self.dealNoInput)
        # self.test_btn.clicked.connect(self.addBotFrame)

        #
        self.globalHtml = []
        self.threadList = []
        #
        self.unrenderStr = ""
        self.curRenderLength = 0
        self.rerenderCount = 0

    def startRequestTask(self):
        self.updataStatus("等待回答")
        self.send_btn.setEnabled(False)
        self.shut_btn.setEnabled(True)
        requestTask = RequestTask(self.user_text.toPlainText())
        self.user_text.clear()
        self.threadList.append(requestTask)

        requestTask.renderSignal.connect(self.render)
        requestTask.finishSignal.connect(self.finishRequestTask)
        requestTask.stateUpdateSignal.connect(self.updataStatus)

        requestTask.start()

    def finishRequestTask(self):
        if self.user_text.toPlainText():
            self.send_btn.setEnabled(True)
        self.shut_btn.setEnabled(False)
        # print(self.bot_text.toHtml())

    def shutRequestTask(self):
        self.updataStatus("中止生成回答")
        if len(bot) != 0:
            bot.pop()
            bot_format.pop()
        for thread in self.threadList:
            thread.finishSignal.emit()
            thread.runPermission = False
        self.shut_btn.setEnabled(False)

    def render(self):
        self.bot_text.clear()
        html = ""
        for chat in bot:
            # print(chat[1])
            markedContent = markdown.markdown(
                chat[1], extensions=["fenced_code", "codehilite"]
            )
            html += (
                f'<div class="user" style="margin-left: auto;">{markedContent}</div>'
            )
        self.bot_text.setHtml(html)
        self.bot_text.moveCursor(QtGui.QTextCursor.End)
        # python 线性回归

    def updataStatus(self, message: str):
        self.statusBar().showMessage(message)

    def initQTextBrowser(self):
        mycss = """ 
            .user {
                background-color: #d9d9e3;
                border-radius: 5px;
                padding: 5px;
                margin-left: 50%;
            }

            .robot {
                background-color: #D58777;
                border-radius: 5px;
                padding: 5px;
            }
            code {
                display: inline;
                white-space: break-spaces;
                border-radius: 6px;
                margin: 0 2px 0 2px;
                padding: .2em .4em .1em .4em;
                background-color: rgba(175,184,193,0.2);
            }
            pre {
                display: block;
                white-space: pre;
                background-color: hsla(0, 0%, 0%, 72%);
                border: solid 5px var(--color-border-primary) !important;
                border-radius: 8px;
                padding: 0 1.2rem 1.2rem;
                margin-top: 1em !important;
                color: #FFF;
                box-shadow: inset 0px 8px 16px hsla(0, 0%, 0%, .2)
            }
            pre code, pre code code {
                font-family: Cascadia Code, monospace,'宋体';
                background-color: transparent !important;
                margin: 0;
                padding: 0;
            }
        """
        self.bot_text.setStyleSheet(mycss)
        self.bot_text.document().setDefaultStyleSheet(mycss)
        ...

    def dealNoInput(self):
        if self.user_text.toPlainText() != "":
            self.send_btn.setEnabled(True)
        else:
            self.send_btn.setEnabled(False)


# mmmmmmmmmmnmjkhjbjnja
# self.bot_text.setText(answer)


class RequestTask(QThread):
    renderSignal = pyqtSignal()
    finishSignal = pyqtSignal()
    stateUpdateSignal = pyqtSignal(str)

    def __init__(self, inputSentence: str):
        super(RequestTask, self).__init__()
        self.inputSentence = inputSentence
        self.runPermission = True

    def run(self):
        bot.append([userFlag, self.inputSentence])
        bot_format.append({"role": "user", "content": self.inputSentence})
        self.renderSignal.emit()
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": bot_format,  # [{"role": "user", "content": f"{inputs}"}],
            "temperature": 1,  # 1.0,
            "top_p": 1,  # 1.0,
            "n": 1,
            "stream": True,
            "presence_penalty": 0,
            "frequency_penalty": 0,
        }
        print(bot_format)
        partialWords = ""
        try:
            response = requests.post(
                API_URL, headers=headers, json=payload, stream=True
            )
        except Exception as e:
            traceback.print_exc()
        bot.append([botFlag, partialWords])
        bot_format.append({"role": "assistant", "content": partialWords})
        for chunk in response.iter_lines():
            self.stateUpdateSignal.emit("回答生成中")
            # print(f"chunk:{chunk}")
            if chunk:
                try:
                    data = json.loads(chunk.decode()[6:])
                    delta = data["choices"][0]["delta"]
                    # print(data)
                    if len(delta) == 0:
                        break
                except Exception as e:
                    traceback.print_exc()
                    break
                status_text = f"id: {data['id']}, finish_reason: {data['choices'][0]['finish_reason']}"
                partial = delta["content"] if "content" in delta else ""
                if not self.runPermission:
                    del response  # 传输流不会立即停止
                    return self.finishSignal.emit()
                bot[-1][1] += partial
                bot_format[-1]["content"] += partial
                self.renderSignal.emit()
            if not self.runPermission:
                del response  # 传输流不会立即停止
                return self.finishSignal.emit()
        self.stateUpdateSignal.emit("生成完毕")
        self.finishSignal.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 实例化页面并展示
    demo_win = DemoMain()
    demo_win.show()
    sys.exit(app.exec_())
