import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtGui


from src.utils import *
from src.globals import *
from src.request_thread import RequestTask
from src.chat_manager import *

zipimporter_fix()
import copy
import markdown
import pickle
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, StandardTitleBar

from qfluentwidgets import (
    MessageDialog,
    MessageBox,
    setTheme,
    Theme,
    StateToolTip,
    ComboBox,
    RoundMenu,
)
from src.chat_page_ui import Ui_chat_page_ui


class chatPage(QFrame, Ui_chat_page_ui, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # 初始化界面
        self.setupUi(self)
        setTheme(Theme.DARK)
        #
        self.setButtonIcon(self.send_btn, "send.png")
        self.setButtonIcon(self.menu_btn, "application-menu.png")
        self.bindMenuActions()
        self.comboBox.setCurrentIndex(0)
        self.comboBox.currentIndexChanged.connect(self.showChat)
        self.user_text.setContextMenuPolicy(Qt.NoContextMenu)
        with open("resource/demo.qss", encoding="utf-8") as f:
            self.setStyleSheet(f.read())
        # self.show()
        ###################
        #
        self.stateTooltip = None
        #
        self.requestThreadList = []
        self.loadedHistory = []
        #
        self.currentComboBoxIdex = 0
        #
        self.isRunning = False
        #
        self.initQTextBrowser()
        self.loadHistory()
        # 绑定按钮逻辑.toPlainText
        self.send_btn.setEnabled(False)
        self.send_btn.clicked.connect(self.getAnwser)
        shortcut = QShortcut(QKeySequence("Enter"), self)
        shortcut.activated.connect(self.send_btn.click)
        # self.shut_btn.clicked.connect(self.shutRequestTask)

        # 其它组件逻辑
        self.user_text.textChanged.connect(self.dealNoInput)
        self.user_text.setLineWrapMode(QTextEdit.NoWrap)

    def showMenu(self):
        # 显示menu
        cursor_pos = QCursor.pos()
        self.menu.exec_(cursor_pos, ani=True)

    ######################################
    def bindMenuActions(self):
        # 创建QAction菜单项
        menu = RoundMenu(parent=self)
        newAction = QAction(QIcon(icon_dir + "newlybuild.png"), "New")
        newAction.setShortcut("Ctrl+N")
        newAction.triggered.connect(self.newChat)

        compressionAction = QAction(QIcon(icon_dir + "compression.png"), "Summary")
        compressionAction.triggered.connect(self.summaryChat)
        compressionAction.setShortcut("Ctrl+B")

        deleteAction = QAction(QIcon(icon_dir + "delete.png"), "DeleteLast")
        deleteAction.triggered.connect(self.deleteLastChat)
        deleteAction.setShortcut("Delete")

        regenAction = QAction(QIcon(icon_dir + "refresh.png"), "Redo")
        regenAction.triggered.connect(self.regenLastChat)
        regenAction.setShortcut("Ctrl+R")

        saveAction = QAction(QIcon(icon_dir + "save-one.png"), "Save")
        saveAction.triggered.connect(self.saveHistory)
        saveAction.setShortcut("Ctrl+S")

        # 将QAction添加到QMenu控件中
        menu.addAction(newAction)
        menu.addAction(compressionAction)
        menu.addAction(deleteAction)
        menu.addAction(regenAction)
        menu.addAction(saveAction)

        self.menu = menu
        self.menu_btn.clicked.connect(self.showMenu)
        # self.menu_btn.setArrowType(Qt.ArrowType.NoArrow)

    def dealNoInput(self):
        if self.user_text.toPlainText() != "" and not self.isRunning:
            self.send_btn.setEnabled(True)
        else:
            self.send_btn.setEnabled(False)

    def dealTaskInformation(self, infomation: list):
        self.ping.setText(f"延迟:{infomation[0]}ms")

    def deleteLastChat(self):
        m = len(myChat)
        # w = MessageDialog(title, content, self)
        w = MessageBox("Delete Item", "Are you sure to delete last Chat?", self)
        if w.exec() and m >= 2:
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
        # self.shut_btn.setEnabled(False)

    def getAnwser(self):
        self.startRequestTask(self.user_text.toPlainText(), False)

    def getSummary(self, forTitle: bool):
        if forTitle:
            if len(myChat) > 2:
                invalid_chars = '\\/:*?"<>.|'
                myChat.title = myChat.title.replace("\n", "")
                for char in invalid_chars:
                    myChat.title = myChat.title.replace(char, "")
                myChat.pop()
                myChat.pop()
                with open(f"./user/{myChat.title}.pickle", "wb") as f:
                    pickle.dump(myChat, f)
                self.render()
                self.loadHistory()

    def initQTextBrowser(self):
        # with open("./state/mycss.css", "r", encoding="utf-8") as f:
        #     mycss = f.read()

        # # self.bot_html.setStyleSheet(mycss)
        # self.bot_html.document().setDefaultStyleSheet(mycss)
        ...
    def insertHtml(self,content):

        pass
    def loadHistory(self, folderPath: str = "./user"):  # list[0] = ["user","hello!"]
        if 'user' not in os.listdir('./'):
            os.mkdir('./user')
        self.loadedHistory.clear()
        file_names = [f for f in os.listdir(folderPath) if f.endswith("pickle")]
        for file_name in file_names:
            file_path = os.path.join(folderPath, file_name)
            with open(file_path, "rb") as f:
                data = pickle.load(f)
                self.loadedHistory.append(data)
        self.comboBox.items.clear()
        self.comboBox.addItems([name.replace(".pickle", "") for name in file_names])

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
        self.bot_html.setHtml("")  # TODO
        html = ""
        content = ""
        for sentence in myChat:
            content += sentence.content
            markedContent = markdown.markdown(
                sentence.content, extensions=["fenced_code", "codehilite"]
            )
            html += f'<div class="{sentence.role}"><div>{markedContent}</div></div>'

        # self.tokensNum.setNum(calcTokens(content))
        html_composed = html_head+html+html_tail
        #print(html_composed)
        self.bot_html.setHtml(html_composed)
        #self.bot_html.moveCursor(QtGui.QTextCursor.End)
        #url = QUrl.fromLocalFile('./state/chat_page.html')
        #self.bot_html.load(url)

    def saveHistory(self):
        self.startRequestTask(summaryTitleString, True)

    def setButtonIcon(self, button, icon_name):
        image = QPixmap(icon_dir + icon_name)
        icon = QIcon(image)
        icon_size = QSize(30, 30)
        button.setText("")
        button.setIcon(icon)
        button.setFixedSize(icon_size.width() + 6, icon_size.height() + 6)
        button.setIconSize(icon_size)
        button.setContentsMargins(3, 3, 3, 3)

    def showChat(self, index):
        myChat.clear()
        # print("cleared,now id is :", id(myChat))
        print(index)
        loadChat = copy.copy(self.loadedHistory[index])
        for sentence in loadChat:
            myChat.append(Sentence(sentence.role, sentence.content))
        # print("content is :\n", myChat)
        self.render()

    def showErrorMessage(self, error: str):
        w = MessageBox("Error", error, self)
        w.exec()

    def shutRequestTask(self):
        self.updateStatus("中止生成回答", True)
        for thread in self.requestThreadList:
            thread.finishSignal.emit()
            thread.runPermission = False
            del thread
        self.shut_btn.setEnabled(False)

    def startRequestTask(self, content: str, summaryFlag: bool):
        if not self.isRunning:
            self.isRunning = True
            self.updateStatus("等待回答", False)
            self.send_btn.setEnabled(False)
            # self.shut_btn.setEnabled(True)
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

    def updateStatus(self, message: str, done: bool):
        if not done:
            if not self.stateTooltip:
                self.stateTooltip = StateToolTip("Chat", message, self)
                self.stateTooltip.move(
                    self.width() * 0.85 - self.stateTooltip.width() / 2,
                    self.height() * 0.8 - self.stateTooltip.height() / 2,
                )

                self.stateTooltip.show()
            else:
                self.stateTooltip.setContent(message)
        else:
            self.stateTooltip.setContent(message)
            self.stateTooltip.setState(True)
            self.stateTooltip = None
