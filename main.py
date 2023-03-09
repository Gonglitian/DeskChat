import sys
import openai
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QThread, pyqtSignal  # 导入线程模块
from Mainwindow import Ui_MainWindow
import markdown

openai.api_key = "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"
bot = []
bot_format = []


class DemoMain(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # 初始化父类
        super().__init__()
        # 初始化界面
        self.setupUi(self)
        # 绑定逻辑
        self.send_btn.clicked.connect(self.startRequestTask)
        #
        self.threadList = []

    def startRequestTask(self):
        self.send_btn.setEnabled(False)
        requestTask = RequestTask(self.user_text.toPlainText())
        self.threadList.append(requestTask)
        requestTask.renderSignal.connect(self.renderContent)
        requestTask.finishSignal.connect(self.finishRequestTask)
        requestTask.start()

    def finishRequestTask(self):
        self.send_btn.setEnabled(True)
        self.renderContent()

    def renderContent(self):
        self.bot_text = []
        for sentence in bot:
            markedSentence = markdown.markdown(
                sentence, extensions=["fenced_code", "codehilite"]
            )
            print(markedSentence)
            self.bot_text.append(markedSentence)


# mmmmmmmmmmnmjkhjbjnja
# self.bot_text.setText(answer)


class RequestTask(QThread):
    renderSignal = pyqtSignal()
    finishSignal = pyqtSignal()

    def __init__(self, inputSentence: str):
        super(RequestTask, self).__init__()
        self.inputSentence = inputSentence

    def run(self):
        bot.append(self.inputSentence)
        self.renderSignal.emit()
        bot_format.append({"role": "user", "content": self.inputSentence})

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=bot_format,
            )
            content = response["choices"][0]["message"]["content"]
            totalTokens = response["usage"]["total_tokens"]
            bot.append(content)
            bot_format.append({"role": "assistant", "content": content})

            print(bot)
        except openai.error.AuthenticationError:
            bot.pop()
            bot_format.pop()
            print("API验证错误。")
        except openai.error.Timeout:
            bot.pop()
            bot_format.pop()
            print("请求超时。")
        except openai.error.APIConnectionError:
            bot.pop()
            bot_format.pop()
            print("API连接错误。")
        except openai.error.RateLimitError:
            bot.pop()
            bot_format.pop()
            print("请求频繁。")
        except:
            bot.pop()
            bot_format.pop()
            print("未知错误。")
        self.finishSignal.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 实例化页面并展示
    demo_win = DemoMain()
    demo_win.show()
    sys.exit(app.exec_())
