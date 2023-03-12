# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1151, 885)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(-10, 10, 1031, 831))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(14)
        self.frame.setFont(font)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.chat_control = QtWidgets.QFrame(self.frame)
        self.chat_control.setGeometry(QtCore.QRect(10, 660, 671, 53))
        self.chat_control.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.chat_control.setFrameShadow(QtWidgets.QFrame.Raised)
        self.chat_control.setObjectName("chat_control")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.chat_control)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.saveChat_btn = QtWidgets.QPushButton(self.chat_control)
        self.saveChat_btn.setObjectName("saveChat_btn")
        self.horizontalLayout_2.addWidget(self.saveChat_btn)
        self.regen_btn = QtWidgets.QPushButton(self.chat_control)
        self.regen_btn.setObjectName("regen_btn")
        self.horizontalLayout_2.addWidget(self.regen_btn)
        self.deleteLast_btn = QtWidgets.QPushButton(self.chat_control)
        self.deleteLast_btn.setObjectName("deleteLast_btn")
        self.horizontalLayout_2.addWidget(self.deleteLast_btn)
        self.summary_btn = QtWidgets.QPushButton(self.chat_control)
        self.summary_btn.setObjectName("summary_btn")
        self.horizontalLayout_2.addWidget(self.summary_btn)
        self.newChat_btn = QtWidgets.QPushButton(self.chat_control)
        self.newChat_btn.setObjectName("newChat_btn")
        self.horizontalLayout_2.addWidget(self.newChat_btn)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setGeometry(QtCore.QRect(10, 720, 670, 61))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.curSys_btn = QtWidgets.QLineEdit(self.frame_4)
        self.curSys_btn.setGeometry(QtCore.QRect(10, 30, 451, 21))
        self.curSys_btn.setObjectName("curSys_btn")
        self.label_4 = QtWidgets.QLabel(self.frame_4)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 151, 16))
        self.label_4.setObjectName("label_4")
        self.loadSys_btn = QtWidgets.QPushButton(self.frame_4)
        self.loadSys_btn.setGeometry(QtCore.QRect(470, 30, 93, 28))
        self.loadSys_btn.setObjectName("loadSys_btn")
        self.information = QtWidgets.QFrame(self.frame)
        self.information.setGeometry(QtCore.QRect(860, 10, 161, 81))
        self.information.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.information.setFrameShadow(QtWidgets.QFrame.Raised)
        self.information.setObjectName("information")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.information)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.information)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.label_2 = QtWidgets.QLabel(self.information)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.bot_text = QtWidgets.QTextBrowser(self.frame)
        self.bot_text.setGeometry(QtCore.QRect(12, 12, 671, 591))
        self.bot_text.setStyleSheet("border-radius: 20px")
        self.bot_text.setObjectName("bot_text")
        self.btns = QtWidgets.QFrame(self.frame)
        self.btns.setGeometry(QtCore.QRect(690, 590, 117, 81))
        self.btns.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.btns.setFrameShadow(QtWidgets.QFrame.Raised)
        self.btns.setObjectName("btns")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.btns)
        self.verticalLayout.setObjectName("verticalLayout")
        self.user_text = QtWidgets.QTextEdit(self.frame)
        self.user_text.setGeometry(QtCore.QRect(10, 610, 591, 41))
        self.user_text.setMinimumSize(QtCore.QSize(0, 0))
        self.user_text.setObjectName("user_text")
        self.historyList = QtWidgets.QListView(self.frame)
        self.historyList.setGeometry(QtCore.QRect(700, 11, 151, 641))
        self.historyList.setObjectName("historyList")
        self.send_btn = QtWidgets.QPushButton(self.frame)
        self.send_btn.setGeometry(QtCore.QRect(600, 610, 81, 21))
        self.send_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.send_btn.setObjectName("send_btn")
        self.shut_btn = QtWidgets.QPushButton(self.frame)
        self.shut_btn.setGeometry(QtCore.QRect(600, 630, 81, 21))
        self.shut_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.shut_btn.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.shut_btn.setObjectName("shut_btn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1151, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.saveChat_btn.setText(_translate("MainWindow", "保存对话"))
        self.regen_btn.setText(_translate("MainWindow", "重新生成"))
        self.deleteLast_btn.setText(_translate("MainWindow", "删除上条对话"))
        self.summary_btn.setText(_translate("MainWindow", "总结对话"))
        self.newChat_btn.setText(_translate("MainWindow", "新的对话"))
        self.label_4.setText(_translate("MainWindow", "System Prompt"))
        self.loadSys_btn.setText(_translate("MainWindow", "加载模版"))
        self.label_3.setText(_translate("MainWindow", "当前tokens:"))
        self.label_2.setText(_translate("MainWindow", "api访问速度:"))
        self.bot_text.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.send_btn.setText(_translate("MainWindow", "发送"))
        self.shut_btn.setText(_translate("MainWindow", "中止"))
