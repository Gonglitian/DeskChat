import sys
import openai
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
        self.send_btn.clicked.connect(self.startRequestTask)
        self.shut_btn.clicked.connect(self.shutRequestTask)
        # self.test_btn.clicked.connect(self.addBotFrame)

        #
        self.globalHtml = []
        self.threadList = []
        #
        self.unrenderStr = ""
        self.curRenderLength = 0
        self.rerenderCount = 0

    def startRequestTask(self):
        self.updataStatus("等待响应")
        self.send_btn.setEnabled(False)
        requestTask = RequestTask(self.user_text.toPlainText())
        self.user_text.clear()
        self.threadList.append(requestTask)

        requestTask.renderUserSignal.connect(self.renderUser)
        requestTask.renderDivSignal.connect(self.renderDiv)
        requestTask.renderBotSignal.connect(self.renderBot)
        requestTask.finishSignal.connect(self.finishRequestTask)
        requestTask.stateUpdateSignal.connect(self.updataStatus)
        requestTask.start()

    def finishRequestTask(self):
        self.send_btn.setEnabled(True)
        self.bot_text.moveCursor(QtGui.QTextCursor.End)
        print(self.bot_text.toHtml())
    def shutRequestTask(self):
        self.updataStatus("中止生成回答")
        bot.pop()
        for thread in self.threadList:
            thread.finishSignal.emit()
            thread.terminate()

    def renderUser(self, content: str):
        markedContent = markdown.markdown(
            content, extensions=["fenced_code", "codehilite"]
        )
        print(markedContent)
        html = f'<div class="user" style="margin-left: auto;">{markedContent}</div>'
        # 插入HTML代码到文本框中
        # self.bot_text.append(html)
        # self.bot_text.moveCursor(QtGui.QTextCursor.End)  # 将光标移动到文本末尾
        self.bot_text.append(html)

    def renderDiv(self):
        html = f'<div class="robot"></div>'
        self.bot_text.append(html)
        self.bot_text.moveCursor(QtGui.QTextCursor.End)
        cursor = self.bot_text.textCursor()
        cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, 6)

    def renderBot(self, delta: str):
        self.unrenderStr += delta
        self.rerenderCount += 1
        if self.rerenderCount % 10 == 0:
            self.rerender()
        # print(markedContent)
        self.bot_text.insertHtml(delta)

    def rerender(self):
        self.unrenderLength = len(self.unrenderStr)
        cursor = self.bot_text.textCursor()

        markedContent = markdown.markdown(
            self.unrenderStr, extensions=["fenced_code", "codehilite"]
        )
        unrenderStr = ""
        self.curRenderLength += len(markedContent)
        cursor.movePosition(
            QTextCursor.Left,
            QTextCursor.KeepAnchor,
            self.curRenderLength + self.unrenderLength,
        )
        cursor.deleteChar()
        self.bot_text.insertHtml(markedContent)

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
        """
        self.bot_text.setStyleSheet(mycss)
        self.bot_text.document().setDefaultStyleSheet(mycss)
        ...


# mmmmmmmmmmnmjkhjbjnja
# self.bot_text.setText(answer)


class RequestTask(QThread):
    renderUserSignal = pyqtSignal(str)
    renderBotSignal = pyqtSignal(str)
    renderDivSignal = pyqtSignal()
    finishSignal = pyqtSignal()
    stateUpdateSignal = pyqtSignal(str)

    def __init__(self, inputSentence: str):
        super(RequestTask, self).__init__()
        self.inputSentence = inputSentence

    def run(self):
        bot.append([userFlag, self.inputSentence])
        self.renderUserSignal.emit(self.inputSentence)
        bot_format.append({"role": "user", "content": self.inputSentence})
        print(bot_format)
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
        partialWords = ""

        # try:
        response = requests.post(API_URL, headers=headers, json=payload, stream=True)
        self.renderDivSignal.emit()
        # print(1)
        bot.append([botFlag, partialWords])
        for chunk in response.iter_lines():
            # print(chunk.decode())
            # # print(len(json.loads(chunk.decode())))
            # check whether each line is non-empty
            if chunk:
                # decode each line as response data is in bytes
                try:
                    data = json.loads(chunk.decode()[6:])
                    if len(data["choices"][0]["delta"]) == 0:
                        # print(3)
                        break
                except Exception as e:
                    break
                data = json.loads(chunk.decode()[6:])
                delta = data["choices"][0]["delta"]
                # print(data)
                status_text = f"id: {data['id']}, finish_reason: {data['choices'][0]['finish_reason']}"
                partial = delta["content"] if "content" in delta else ""
                partialWords += partial
                # print(data["choices"][0]["delta"])
                print(partial)
                # print(partialWords)
                bot[-1][1] = partialWords
                self.renderBotSignal.emit(partial)
        # except openai.error.AuthenticationError:
        #     bot.pop()
        #     bot_format.pop()
        #     self.stateUpdateSignal.emit("API验证错误。")
        #     print("API验证错误。")
        # except openai.error.Timeout:
        #     bot.pop()
        #     bot_format.pop()
        #     self.stateUpdateSignal.emit("请求超时。")
        #     print("请求超时。")
        # except openai.error.APIConnectionError:
        #     bot.pop()
        #     bot_format.pop()
        #     self.stateUpdateSignal.emit("API连接错误。")
        #     print("API连接错误。")
        # except openai.error.RateLimitError:
        #     bot.pop()
        #     bot_format.pop()
        #     self.stateUpdateSignal.emit("请求频繁。")
        #     print("请求频繁。")
        # except:
        #     bot.pop()
        #     bot_format.pop()
        #     self.stateUpdateSignal.emit("未知错误。")
        #     print("未知错误。")

        bot.append(partialWords)
        self.finishSignal.emit()

    def getPartialContent(self):
        ...

    def buildContentStream(self):
        ...


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 实例化页面并展示
    demo_win = DemoMain()
    demo_win.show()
    sys.exit(app.exec_())
