import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import openai
from PyQt5 import QtGui
from Mainwindow import Ui_MainWindow
import markdown
import requests, json
from utils import *

apiKey = "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"
openai.api_key = apiKey

API_URL = "https://api.openai.com/v1/chat/completions"
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {apiKey}"}

global bot, bot_format
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
        self.loadHistory()
        # 绑定逻辑
        self.send_btn.setEnabled(False)
        self.send_btn.clicked.connect(self.startRequestTask)
        self.shut_btn.clicked.connect(self.shutRequestTask)
        self.user_text.textChanged.connect(self.dealNoInput)
        self.saveChat_btn.clicked.connect(self.saveHistory)
        self.summary_btn.clicked.connect(self.Summary)
        self.deleteLast_btn.clicked.connect(self.deleteLastChat)
        # self.test_btn.clicked.connect(self.addBotFrame)

        #
        self.globalHtml = []
        self.threadList = []
        self.loadedHistory = []
        self.itemList = []
        #
        self.unrenderStr = ""
        self.curRenderLength = 0
        self.rerenderCount = 0

    def startRequestTask(self):
        self.updateStatus("等待回答")
        self.send_btn.setEnabled(False)
        self.shut_btn.setEnabled(True)
        requestTask = RequestTask(self.user_text.toPlainText())
        self.user_text.clear()
        self.threadList.append(requestTask)

        requestTask.renderSignal.connect(self.render)
        requestTask.finishSignal.connect(self.finishRequestTask)
        requestTask.stateUpdateSignal.connect(self.updateStatus)

        requestTask.start()

    def finishRequestTask(self):
        if self.user_text.toPlainText():
            self.send_btn.setEnabled(True)
        self.shut_btn.setEnabled(False)
        self.threadList = []

        # print(self.bot_text.toHtml())

    def shutRequestTask(self):
        self.updateStatus("中止生成回答")
        if len(bot) != 0:
            bot.pop()
            bot_format.pop()
        for thread in self.threadList:
            thread.finishSignal.emit()
            thread.runPermission = False
            del thread
        self.shut_btn.setEnabled(False)

    def render(self):
        self.bot_text.clear()
        html = ""
        for chat in bot:
            # print(chat)
            markedContent = markdown.markdown(
                chat[1], extensions=["fenced_code", "codehilite"]
            )
            html += (
                f'<div class="user" style="margin-left: auto;">{markedContent}</div>'
            )
        self.bot_text.setHtml(html)
        self.bot_text.moveCursor(QtGui.QTextCursor.End)
        # python 线性回归

    def updateStatus(self, message: str):
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

    def saveHistory(self):
        summary = self.summaryTitle()
        bot.insert(0, ["title", summary])
        m = len(os.listdir("./user"))
        with open(f"./user/history.pickle_{m}", "wb") as f:
            pickle.dump(bot, f)
            m += 1

    def loadHistory(self, filePath: str = "./user"):  # list[0] = ["user","hello!"]
        # 从文件中读取并反序列化列表
        for i in range(len(os.listdir(filePath))):
            with open(f"{filePath}/historyList.pickle_{i}", "rb") as f:
                history = pickle.load(f)
                self.loadedHistory.append(history[1:])
                self.itemList.append(history[0][1])
                self.historyList.addItem(history[0][1])

    def summaryTitle(self):
        self.Summary()
        while len(self.threadList) != 0:
            print(len(self.threadList))
        title = bot[-1][1]
        bot.pop()
        bot.pop()
        bot_format.pop()
        bot_format.pop()
        self.render()
        return title

    def Summary(self):
        input = "请帮我总结一下上述对话的内容，实现减少字数的同时，保证对话的质量。在总结中不要加入这一句话。"
        self.updateStatus("等待回答")
        self.send_btn.setEnabled(False)
        self.shut_btn.setEnabled(True)
        requestTask = RequestTask(input)
        self.user_text.clear()
        self.threadList.append(requestTask)

        requestTask.renderSignal.connect(self.render)
        requestTask.finishSignal.connect(self.finishRequestTask)
        requestTask.stateUpdateSignal.connect(self.updateStatus)
        requestTask.errorSignal.connect(self.showErrorMessage)
        requestTask.start()

    def deleteLastChat(self):
        reply = QMessageBox.question(
            self,
            "Delete Item",
            "Are you sure to delete last Chat?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            bot.pop()
            bot.pop()
            bot_format.pop()
            bot_format.pop()
            print(bot)
            self.render()

    def showErrorMessage(error: str):
        # 创建一个警告框
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)

        # 设置警告框的标题和正文
        msg.setWindowTitle("Error")
        msg.setText("Error detected in operation.")
        msg.setInformativeText(error)
        # 显示警告框
        msg.exec()


# mmmmmmmmmmnmjkhjbjnja


class RequestTask(QThread):
    renderSignal = pyqtSignal()
    finishSignal = pyqtSignal()
    stateUpdateSignal = pyqtSignal(str)
    errorSignal = pyqtSignal(str)

    def __init__(self, inputSentence: str, summaryFlag: bool):
        super(RequestTask, self).__init__()
        self.inputSentence = inputSentence
        self.runPermission = True
        self.summaryFlag = summaryFlag

    def run(self):
        bot.append([userFlag, self.inputSentence])
        bot_format.append({"role": "user", "content": self.inputSentence})
        self.renderSignal.emit()

        if not self.summaryFlag:
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
            with requests.Session() as session:
                try:
                    response = session.post(
                        API_URL, headers=headers, json=payload, stream=True
                    )
                    partialWords = ""
                    # 新增空元素，准备接受流式传输内容
                    bot.append([botFlag, partialWords])
                    bot_format.append({"role": "assistant", "content": partialWords})
                    # 开始获取流式传输内容
                    for chunk in response.iter_lines():
                        self.stateUpdateSignal.emit("回答生成中")
                        if not self.runPermission:
                            response.raw.close()
                            return self.finishSignal.emit()  # 中止函数并发出中止信号
                        if chunk:
                            try:
                                data = json.loads(chunk.decode()[6:])
                                delta = data["choices"][0]["delta"]
                                # print(data)
                                if len(delta) == 0:
                                    break
                            except Exception as e:
                                self.errorSignal.emit(f"{e}")
                                break
                            status_text = f"id: {data['id']}, finish_reason: {data['choices'][0]['finish_reason']}"
                            partial = delta["content"] if "content" in delta else ""
                            bot[-1][1] += partial
                            bot_format[-1]["content"] += partial
                            self.renderSignal.emit()
                except Exception as e:
                    self.errorSignal.emit(f"{e}")

            self.stateUpdateSignal.emit("生成完毕")
        else:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=bot_format,
                )
                content = response["choices"][0]["message"]["content"]
                totalTokens = response["usage"]["total_tokens"]
                bot.append(content)
                bot_format.append({"role": "assistant", "content": content})
                self.stateUpdateSignal.emit("生成完毕")
            except Exception as e:
                self.errorSignal.emit(f"{e}")

        self.finishSignal.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 实例化页面并展示
    demo_win = DemoMain()
    demo_win.show()
    sys.exit(app.exec_())
