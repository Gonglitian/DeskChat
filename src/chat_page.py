import os
import time

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import pickle

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
from src.utils import *
from src.globals import *

from src.request_thread import RequestTask
from src.chat_manager import *

import datetime


class chatPage(QFrame, Ui_chat_page_ui, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # 初始化界面
        self.setupUi(self)
        setTheme(Theme.DARK)
        with open("resource/demo.qss", encoding="utf-8") as f:
            self.setStyleSheet(f.read())
        #
        self.stateTooltip = None
        self.isRunning = False
        #
        self.requestThreadList = []
        self.loadedHistory = []
        #
        self.currentComboBoxIdex = 0
        self.div_nums = 0

        # 绑定按钮逻辑
        self.send_btn.setEnabled(False)
        self.send_btn.clicked.connect(self.getAnwser)
        # self.send_btn.clicked.connect(self.test_updateChat)
        # self.shut_btn.clicked.connect(self.shutRequestTask)

        # 其它组件逻辑
        self.setButtonIcon(self.send_btn, icon_dir + "send.png")
        self.setButtonIcon(self.menu_btn, icon_dir + "application-menu.png")
        self.bindMenuActions()
        self.comboBox.setCurrentIndex(0)
        self.comboBox.currentIndexChanged.connect(self.showChat)
        self.user_text.setContextMenuPolicy(Qt.NoContextMenu)
        self.user_text.textChanged.connect(self.dealNoInput)
        self.user_text.setLineWrapMode(QTextEdit.NoWrap)

        #
        self.bot_html.setHtml(initialHtml)
        self.initQTextBrowser()
        self.loadHistory()
        self.newChat()

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
        saveAction.triggered.connect(self.saveCurrentChat)
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
        if not self.isRunning:
            m = len(myChat)
            # w = MessageDialog(title, content, self)
            w = MessageBox("Delete Item", "Are you sure to delete last Chat?", self)
            if w.exec():
                if m % 2 == 0:
                    myChat.pop()
                    myChat.pop()
                else:
                    myChat.pop()
            self.updateChat()

    def finishRequestTask(self):
        self.isRunning = False
        if self.user_text.toPlainText():
            self.send_btn.setEnabled(True)
        # self.shut_btn.setEnabled(False)

    def getAnwser(self):
        if not self.isRunning:
            self.startRequestTask(self.user_text.toPlainText(), False)

    def getSummary(self, forTitle: bool):
        if forTitle:
            if len(myChat) > 2:
                invalid_chars = '\\/:*?"<>.|，。、'
                myChat.title = myChat.title.replace("\n", "")
                for char in invalid_chars:
                    myChat.title = myChat.title.replace(char, "")
                myChat.pop()
                myChat.pop()
                self.saveByTitle()

    def initQTextBrowser(self):
        # with open("./state/mycss.css", "r", encoding="utf-8") as f:
        #     mycss = f.read()

        # # self.bot_html.setStyleSheet(mycss)
        # self.bot_html.document().setDefaultStyleSheet(mycss)
        ...

    def keyPressEvent(self, event):
        if event.key() == 16777220:  # 回车键的键码值
            self.send_btn.click()

    def loadHistory(self):
        if "user" not in os.listdir("./"):
            os.mkdir(user_dir)
        self.loadedHistory.clear()
        file_names = [f for f in os.listdir(user_dir) if f.endswith("pickle")]
        for file_name in file_names:
            file_path = os.path.join(user_dir, file_name)
            with open(file_path, "rb") as f:
                data = pickle.load(f)
                self.loadedHistory.append(data)

        self.comboBox.items.clear()
        self.comboBox.addItems([name.replace(".pickle", "") for name in file_names])

    def newChat(self):
        if not self.isRunning:
            if len(myChat) > 0 and not myChat.is_saved:
                w = MessageBox("Unsaved Chat", "Are you sure to swich to another Chat leaving this unsaved?", self)
                user_choice = w.exec()
                if user_choice:
                    myChat.clear()
                    myChat.title = ("New Chat " + processTime(datetime.datetime.now()))

                    self.loadedHistory.append(myChat)
                    self.comboBox.addItem(myChat.title)
                    chat_index = self.comboBox.items.index(myChat.title)
                    self.comboBox.setCurrentIndex(chat_index)
                    self.showChat(chat_index)

    def regenLastChat(self):
        if not self.isRunning:
            if len(myChat) >= 2:
                myChat.pop()
                lastUserSentence = myChat.pop().content
                self.startRequestTask(lastUserSentence, False)

    def updateChat(self):
        tokens = 0
        myChat.is_saved = False
        if self.comboBox.items[self.comboBox.currentIndex()][-1] != '*':
            self.comboBox.items[self.comboBox.currentIndex()] += '*'
        my_html = ''''''
        for sentence in myChat:
            tokens += count_token(sentence)
            # markdown转html
            marked_content = parse_text(sentence.content)
            marked_content = convert_mdtext(marked_content)
            marked_content = marked_content.replace("\n", "<br>")
            my_html += f'<div class="{sentence.role}-bubble">{marked_content}</div>'
            self.div_nums += 1

        # TEST INPUT : python linear regression,show me the code
        # print(my_html)
        self.token.setText(f"当前Tokens:{tokens}")
        self.bot_html.page().runJavaScript(f"""
        document.getElementById('chat-page').innerHTML = '{my_html}';
        """)

    def saveByTitle(self):
        if len(myChat.title.split(" ")) > 5:
            file_name = " ".join(myChat.title.split(" ")[:5])
        else:
            file_name = myChat.title
        if (file_name + ".pickle") not in os.listdir(user_dir):
            with open(os.path.join(user_dir, file_name + ".pickle"), 'wb') as f:
                f.write(pickle.dumps(myChat))
        else:
            with open(os.path.join(user_dir, file_name, str(time.time())[:5], ".pickle"), 'wb') as f:
                f.write(pickle.dumps(myChat))
        myChat.is_saved = True
        self.loadHistory()
        self.comboBox.setCurrentIndex(self.comboBox.items.index(myChat.title))
        self.showChat(self.comboBox.items.index(myChat.title))

    def saveCurrentChat(self):
        if not self.isRunning:
            if AUTORENAME:
                self.startRequestTask(summaryTitleString, True)
            else:
                options = QFileDialog.Options()
                options |= QFileDialog.DontUseNativeDialog
                file_name = QFileDialog.getSaveFileName(self, 'Save file', user_dir, filter="Pickle file (*.pickle)")
                if file_name[0]:
                    print(file_name)
                    myChat.title = get_file_name(file_name[0])
                self.saveByTitle()

    def setButtonIcon(self, button, icon_path):
        image = QPixmap(icon_path)
        icon = QIcon(image)
        icon_size = QSize(30, 30)
        button.setText("")
        button.setIcon(icon)
        button.setFixedSize(icon_size.width() + 6, icon_size.height() + 6)
        button.setIconSize(icon_size)
        button.setContentsMargins(3, 3, 3, 3)

    def showChat(self, index):
        myChat.setValue(self.loadedHistory[index])
        self.updateChat()

    def showErrorMessage(self, error: str):
        w = MessageBox("Error", error, self)
        w.exec()

    def shutRequestTask(self):
        self.updateStatus("中止生成回答", True)
        for thread in self.requestThreadList:
            thread.finishSignal.emit()
            thread.runPermission = False
            del thread
        # self.shut_btn.setEnabled(False)

    def startRequestTask(self, content: str, summaryFlag: bool):
        if not self.isRunning:
            self.isRunning = True
            self.updateStatus("等待回答", False)
            self.send_btn.setEnabled(False)
            # self.shut_btn.setEnabled(True)
            requestTask = RequestTask(content, summaryFlag=summaryFlag)
            self.user_text.clear()
            # 使线程不会在startRequestTask函数结束时被回收内存
            self.requestThreadList.append(requestTask)
            # 绑定线程信号
            requestTask.finishSignal.connect(self.finishRequestTask)
            requestTask.stateUpdateSignal.connect(self.updateStatus)
            requestTask.errorSignal.connect(self.showErrorMessage)
            requestTask.summaryFinishSignal.connect(self.getSummary)
            requestTask.informationUpdateSignal.connect(self.dealTaskInformation)
            requestTask.updateChatSignal.connect(self.updateChat)
            requestTask.start()

    def summaryChat(self):
        if not self.isRunning:
            self.startRequestTask(summaryString, False)

    def updateStatus(self, message: str, done: bool):
        if not done:
            if not self.stateTooltip:
                self.stateTooltip = StateToolTip("Chat", message, self)
                self.stateTooltip.move(
                    int(self.width() * 0.85 - self.stateTooltip.width() / 2),
                    int(self.height() * 0.8 - self.stateTooltip.height() / 2),
                )

                self.stateTooltip.show()
            else:
                self.stateTooltip.setContent(message)
        else:
            self.stateTooltip.setContent(message)
            self.stateTooltip.setState(True)
            self.stateTooltip = None
