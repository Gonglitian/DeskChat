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
