# import jieba
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtGui


def zipimporter_fix():
    from zipimport import zipimporter

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        exec(self.get_code(module.__name__), module.__dict__)

    zipimporter.create_module = create_module
    zipimporter.exec_module = exec_module
