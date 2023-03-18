# coding:utf-8
import sys
from PyQt5.QtCore import Qt, QRect, QSize, QPoint
from PyQt5.QtGui import QIcon, QPainter, QImage, QBrush, QColor, QFont, QPixmap, QCursor
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QStackedWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QMenu,
    QAction,
)

from qfluentwidgets import (
    NavigationInterface,
    NavigationItemPostion,
    NavigationWidget,
    MessageBox,
    isDarkTheme,
    setTheme,
    Theme,
    RoundMenu,
    getIconColor,
    Theme,
    FluentIconBase,
)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, StandardTitleBar
from enum import Enum

from chatwindow import Ui_chat_window

icon_dir = "./resource/icons/"


def setButtonIcon(button, icon_name):
    image = QPixmap(icon_dir + icon_name)
    icon = QIcon(image)
    icon_size = QSize(30, 30)
    button.setText("")
    button.setIcon(icon)
    button.setFixedSize(icon_size.width() + 6, icon_size.height() + 6)
    button.setIconSize(icon_size)
    button.setContentsMargins(3, 3, 3, 3)


def bindMenuActions(window):
    # 创建QAction菜单项
    menu = RoundMenu(parent=window)
    newAction = QAction(QIcon(icon_dir + "newlybuild.png"), "New")
    newAction.setShortcut("Ctrl+N")
    newAction.triggered.connect(window.newChat)

    compressionAction = QAction(QIcon(icon_dir + "compression.png"), "Summary")
    compressionAction.triggered.connect(window.summary)
    compressionAction.setShortcut("Ctrl+B")

    deleteAction = QAction(QIcon(icon_dir + "delete.png"), "DeleteLast")
    deleteAction.triggered.connect(window.deleteLast)
    deleteAction.setShortcut("Delete")

    regenAction = QAction(QIcon(icon_dir + "refresh.png"), "Redo")
    regenAction.triggered.connect(window.regenLast)
    regenAction.setShortcut("Ctrl+R")

    saveAction = QAction(QIcon(icon_dir + "save-one.png"), "Save")
    saveAction.triggered.connect(window.saveChat)
    saveAction.setShortcut("Ctrl+S")

    # 将QAction添加到QMenu控件中
    menu.addAction(newAction)
    menu.addAction(compressionAction)
    menu.addAction(deleteAction)
    menu.addAction(regenAction)
    menu.addAction(saveAction)

    window.menu = menu
    window.menu_btn.clicked.connect(window.showMenu)
    # window.menu_btn.setArrowType(Qt.ArrowType.NoArrow)


def initComboBox(window):
    window.comboBox.addItems(
        ["shoko 🥰", "西宫硝子", "aiko", "柳井爱子1111111111111111111111111"]
    )
    window.comboBox.setCurrentIndex(0)
    window.comboBox.currentTextChanged.connect(print)
    window.comboBox.move(200, 200)


class chatwindow(QFrame, Ui_chat_window):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        setButtonIcon(self.send_btn, "send.png")
        setButtonIcon(self.menu_btn, "application-menu.png")
        bindMenuActions(self)
        initComboBox(self)
        self.user_input.setContextMenuPolicy(Qt.NoContextMenu)
        with open("resource/demo.qss", encoding="utf-8") as f:
            self.setStyleSheet(f.read())
        self.show()

    def showMenu(self):
        # 显示menu
        cursor_pos = QCursor.pos()
        self.menu.exec_(cursor_pos, ani=True)

    def newChat(self):
        print("new chat")

    def summary(self):
        print("summary")

    def deleteLast(self):
        print("deleteLast")

    def regenLast(self):
        print("regenLast")

    def saveChat(self):
        print("saveChat")


class Widget(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        # self.label = QLabel(text, self)
        # self.label.setAlignment(Qt.AlignCenter)
        self.text_edit = QTextEdit()
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.text_edit)
        self.setObjectName(text.replace(" ", "-"))

        # mycode
        # vlayout = QVBoxLayout(self)

        self.button1 = QPushButton("Click me!")
        self.button2 = QPushButton("Click me!")
        self.button3 = QPushButton("Click me!")
        self.hBoxLayout.addWidget(self.button1)
        self.hBoxLayout.addWidget(self.button2)
        self.hBoxLayout.addWidget(self.button3)
        with open("resource/demo.qss", encoding="utf-8") as f:
            self.setStyleSheet(f.read())


class AvatarWidget(NavigationWidget):
    """Avatar widget"""

    def __init__(self, parent=None):
        super().__init__(isSelectable=False, parent=parent)
        self.avatar = QImage("resource/shoko.png").scaled(
            24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.SmoothPixmapTransform | QPainter.Antialiasing)

        painter.setPen(Qt.NoPen)

        if self.isPressed:
            painter.setOpacity(0.7)

        # draw background
        if self.isEnter:
            c = 255 if isDarkTheme() else 0
            painter.setBrush(QColor(c, c, c, 10))
            painter.drawRoundedRect(self.rect(), 5, 5)

        # draw avatar
        painter.setBrush(QBrush(self.avatar))
        painter.translate(8, 6)
        painter.drawEllipse(0, 0, 24, 24)
        painter.translate(-8, -6)

        if not self.isCompacted:
            painter.setPen(Qt.white if isDarkTheme() else Qt.black)
            font = QFont("Segoe UI")
            font.setPixelSize(14)
            painter.setFont(font)
            painter.drawText(QRect(44, 0, 255, 36), Qt.AlignVCenter, "zhiyiYo")


class Window(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.setTitleBar(StandardTitleBar(self))

        # use dark theme mode
        setTheme(Theme.DARK)

        self.hBoxLayout = QHBoxLayout(self)
        self.navigationInterface = NavigationInterface(self, showMenuButton=True)
        self.stackWidget = QStackedWidget(self)

        # create sub interface
        self.chatInterface = chatwindow(self)
        self.historyInterface = Widget("Music Interface", self)
        self.promptInterface = Widget("Video Interface", self)
        self.settingInterface = Widget("Setting Interface", self)

        self.stackWidget.addWidget(self.chatInterface)
        self.stackWidget.addWidget(self.historyInterface)
        self.stackWidget.addWidget(self.promptInterface)
        self.stackWidget.addWidget(self.settingInterface)
        # initialize layout
        self.initLayout()

        # add items to navigation interface
        self.initNavigation()

        self.initWindow()

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

    def initNavigation(self):
        self.navigationInterface.addItem(
            routeKey=self.chatInterface.objectName(),
            icon=(icon_dir + "robot.png"),
            text="Chat",
            onClick=lambda: self.switchTo(self.chatInterface),
        )
        self.navigationInterface.addItem(
            routeKey=self.historyInterface.objectName(),
            icon=QIcon(QPixmap(icon_dir + "history.png")),
            text="History",
            onClick=lambda: self.switchTo(self.historyInterface),
        )
        self.navigationInterface.addItem(
            routeKey=self.promptInterface.objectName(),
            icon=(icon_dir + "prompt.png"),
            text="Prompt",
            onClick=lambda: self.switchTo(self.promptInterface),
        )

        self.navigationInterface.addSeparator()

        # add custom widget to bottom
        self.navigationInterface.addWidget(
            routeKey="avatar",
            widget=AvatarWidget(),
            onClick=self.showMessageBox,
            position=NavigationItemPostion.BOTTOM,
        )

        self.navigationInterface.addItem(
            routeKey=self.settingInterface.objectName(),
            icon=FIF.SETTING,
            text="Settings",
            onClick=lambda: self.switchTo(self.settingInterface),
            position=NavigationItemPostion.BOTTOM,
        )

        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.stackWidget.setCurrentIndex(1)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon("resource/logo.png"))
        self.setWindowTitle("PyQt-Fluent-Widgets")
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.setQss()

    def setQss(self):
        color = "dark" if isDarkTheme() else "light"
        with open(f"resource/{color}/demo.qss", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationInterface.setCurrentItem(widget.objectName())

    def showMessageBox(self):
        w = MessageBox(
            "This is a help message",
            "You clicked a customized navigation widget. You can add more custom widgets by calling `NavigationInterface.addWidget()` 😉",
            self,
        )
        w.exec()


if __name__ == "__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()
