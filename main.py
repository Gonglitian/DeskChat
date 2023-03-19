import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtGui


from src.utils import *
from src.Mainwindow import Ui_MainWindow
from src.globals import *
from src.request_thread import RequestTask
from src.chat_manager import *

zipimporter_fix()
import copy
import markdown
import pickle


class DemoMain(QMainWindow, Ui_MainWindow):
    def __init__(self):
        #
        self.globalHtml = []
        self.requestThreadList = []
        self.timeThreadList = []
        self.loadedHistory = []
        self.itemList = []
        #
        self.unrenderStr = ""
        self.curRenderLength = 0
        self.rerenderCount = 0
        self.isRunning = False
        self.slm = QStringListModel()
        # 初始化父类
        super().__init__()
        # 初始化界面
        self.setupUi(self)
        self.initQTextBrowser()
        self.loadHistory()
        # 绑定按钮逻辑.toPlainText
        self.send_btn.setEnabled(False)
        self.send_btn.clicked.connect(self.getAnwser)
        shortcut = QShortcut(QKeySequence("Enter"), self)
        shortcut.activated.connect(self.send_btn.click)
        self.shut_btn.clicked.connect(self.shutRequestTask)
        self.saveChat_btn.clicked.connect(self.saveHistory)
        self.summary_btn.clicked.connect(self.summaryChat)
        self.deleteLast_btn.clicked.connect(self.deleteLastChat)
        self.regen_btn.clicked.connect(self.regenLastChat)
        self.newChat_btn.clicked.connect(self.newChat)
        # 其它组件逻辑
        self.user_text.textChanged.connect(self.dealNoInput)
        self.user_text.setLineWrapMode(QTextEdit.NoWrap)
        self.historyView.clicked.connect(self.showChat)

    def dealNoInput(self):
        if self.user_text.toPlainText() != "" and not self.isRunning:
            self.send_btn.setEnabled(True)
        else:
            self.send_btn.setEnabled(False)

    def dealTaskInformation(self, infomation: list):
        self.pingNum.setNum(infomation[0])

    def deleteLastChat(self):
        reply = QMessageBox.question(
            self,
            "Delete Item",
            "Are you sure to delete last Chat?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        m = len(myChat)
        if reply == QMessageBox.Yes and m >= 2:
            if m % 2 == 0:
                myChat.pop()
                myChat.pop()
            else:
                myChat.pop()
            self.render()

    def finishRequestTask(self):
        self.isRunning = False
        if self.user_text.toPlainText():
            self.send_btn.setEnabled(True)
        self.shut_btn.setEnabled(False)

    def getAnwser(self):
        self.startRequestTask(self.user_text.toPlainText(), False)

    def getSummary(self, summary: str, forTitle: bool):
        if forTitle:
            myChat.title = summary
            if len(myChat) > 2:
                invalid_chars = '\\/:*?"<>.|'
                summary = summary.replace("\n", "")
                for char in invalid_chars:
                    summary = summary.replace(char, "")
                myChat.pop()
                myChat.pop()
                with open(f"./user/{summary}.pickle", "wb") as f:
                    pickle.dump(myChat, f)
                self.render()
                self.loadHistory()

    def initQTextBrowser(self):
        with open("./state/mycss.css", "r", encoding="utf-8") as f:
            mycss = f.read()

        # self.bot_text.setStyleSheet(mycss)
        self.bot_text.document().setDefaultStyleSheet(mycss)

    def keyPressEvent(self, event):
        key = event.key()
        if self.user_text.hasFocus() and key == Qt.Key_Return:
            self.send_btn.click()
        elif event.modifiers() == Qt.ControlModifier and key == Qt.Key_S:
            self.saveChat_btn.click()
        elif event.key() == Qt.Key_Return:
            ...
        elif event.key() == Qt.Key_Return:
            ...
        elif event.key() == Qt.Key_Return:
            ...
        elif event.key() == Qt.Key_Return:
            ...
        elif event.key() == Qt.Key_Return:
            ...
        elif event.key() == Qt.Key_Return:
            ...
        elif event.key() == Qt.Key_Return:
            ...

    def loadHistory(self, folderPath: str = "./user"):  # list[0] = ["user","hello!"]
        # 从文件中读取并反序列化列表
        self.loadedHistory.clear()
        file_names = [f for f in os.listdir(folderPath) if f.endswith("pickle")]
        for file_name in file_names:
            file_path = os.path.join(folderPath, file_name)
            with open(file_path, "rb") as f:
                data = pickle.load(f)
                self.loadedHistory.append(data)
        self.slm.setStringList([name.replace(".pickle", "") for name in file_names])
        self.historyView.setModel(self.slm)

    def newChat(self):
        myChat.clear()
        self.render()

    def regenLastChat(self):
        if not self.isRunning:
            if len(myChat) >= 2:
                myChat.pop()
                lastUserSentence = myChat.pop().content
                self.startRequestTask(lastUserSentence, False)

    def render(self):
        self.bot_text.clear()  # TODO
        html = ""
        content = ""
        for sentence in myChat:
            content += sentence.content
            markedContent = markdown.markdown(
                sentence.content, extensions=["fenced_code", "codehilite"]
            )
            html += f'<div class="{sentence.role}"><div>{markedContent}</div></div>'

        # self.tokensNum.setNum(calcTokens(content))
        self.bot_text.setHtml(html)
        self.bot_text.moveCursor(QtGui.QTextCursor.End)

    def saveHistory(self):
        self.startRequestTask(summaryTitleString, True)

    def showChat(self, index: QModelIndex):
        myChat.clear()
        print("cleared,now id is :", id(myChat))
        loadChat = copy.copy(self.loadedHistory[index.row()])
        for sentence in loadChat:
            myChat.append(Sentence(sentence.role, sentence.content))
        print("content is :\n", myChat)
        self.render()

    def showErrorMessage(self, error: str):
        QMessageBox.critical(self, "Error", error)

    def shutRequestTask(self):
        self.updateStatus("中止生成回答")
        for thread in self.requestThreadList:
            thread.finishSignal.emit()
            thread.runPermission = False
            del thread
        self.shut_btn.setEnabled(False)

    def startRequestTask(self, content: str, summaryFlag: bool):
        if not self.isRunning:
            self.isRunning = True
            self.updateStatus("等待回答")
            self.send_btn.setEnabled(False)
            self.shut_btn.setEnabled(True)
            requestTask = RequestTask(content, summaryFlag=summaryFlag)
            self.user_text.clear()
            # 使线程不会在startRequestTask函数结束时回收内存
            self.requestThreadList.append(requestTask)
            # 绑定线程信号
            requestTask.renderSignal.connect(self.render)
            requestTask.finishSignal.connect(self.finishRequestTask)
            requestTask.stateUpdateSignal.connect(self.updateStatus)
            requestTask.errorSignal.connect(self.showErrorMessage)
            requestTask.summaryFinishSignal.connect(self.getSummary)
            requestTask.informationUpdateSignal.connect(self.dealTaskInformation)
            requestTask.start()

    def summaryChat(self):
        self.startRequestTask(summaryString, False)

    def updateDelay(self, delay: int):
        self.pingNum.setNum(delay)

    def updateStatus(self, message: str):
        self.statusBar().showMessage(message)


# mmmmmmmmmmnmjkhjbjnja


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 实例化页面并展示
    demo_win = DemoMain()
    demo_win.show()
    sys.exit(app.exec_())
