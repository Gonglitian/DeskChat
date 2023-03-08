import sys
import openai
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QThread  # 导入线程模块
from Mainwindow import Ui_MainWindow
import markdown
import markdown.extensions.fenced_code
import markdown.extensions.codehilite

system = "system"
user = "user"
assistant = "assistant"

openai.api_key = "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"
systemPromt = ''


class DemoMain(QMainWindow, Ui_MainWindow):

    def __init__(self):
        # 初始化父类
        super(DemoMain, self).__init__()
        #
        self.bot = []
        self.requests_ = []
        self.requests_.append({"role": system, "content": systemPromt})
        #
        self.click_t = 0
        self.response_t = 0
        # 调用Ui_Form的setupUi()方法构建页面
        self.setupUi(self)
    #     self.bot_text.setHtml("""<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/highlight.js/10.7.2/styles/vs2015.min.css">
    # <script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/10.7.2/highlight.min.js"></script>
    # <script>hljs.initHighlightingOnLoad();</script>""")
        self.bind_logits()

    def bind_logits(self):
        self.send_btn.clicked.connect(self.getAnswer)

    def getResponse(self):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.requests_
        )
        return response

    def getAnswer(self):

        self.click_t += 1
        print(self.click_t)
        inputSentence = self.user_text.toPlainText()
        self.bot.append(inputSentence)
        self.requests_.append({"role": user, "content": inputSentence + "\n"})

        try:
            answer = self.getResponse()["choices"][0]["message"]["content"]
            self.response_t += 1
            self.bot.append(answer)
            self.requests_.append({"role": assistant, "content": answer})
            self.renderText()

        except openai.error.AuthenticationError:
            print("openai.error.AuthenticationError")
            return 0
        except openai.error.Timeout:
            print("openai.error.Timeout")
            return 0
        except openai.error.APIConnectionError:
            print("openai.error.APIConnectionError")
            return 0
        except openai.error.RateLimitError:
            print("openai.error.RateLimitError")
            return 0
        except:
            print("Extra Wrong")
            return 0

    def renderText(self):
        text = ""
        for sentence in self.bot:
            text += sentence
        text = markdown.markdown(text, extensions=['fenced_code', 'codehilite'])
        print(text)
        self.bot_text.setText(text)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 实例化页面并展示
    demo_win = DemoMain()
    demo_win.show()

    sys.exit(app.exec_())
