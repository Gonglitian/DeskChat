# import jieba
import time
import requests
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtGui


# def calcTokens(content: str) -> int:
#     # 将英文单词和标点用空格分隔
#     content = "".join([c if c.isalnum() else " " for c in content])
#     # 对中文部分使用jieba分词
#     seg_list = jieba.lcut(content, cut_all=False)
#     # 过滤空格和空字符串
#     return len([token for token in seg_list if token.strip()])
