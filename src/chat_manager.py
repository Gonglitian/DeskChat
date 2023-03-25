from PyQt5.QtCore import *

import copy


class Sentence:
    def __init__(self, role: str = "", content: str = "") -> None:
        self.role = role
        self.content = content


class ChatManager():
    def __init__(self, title: str = "New Chat") -> None:
        self.title = title
        self.context = []
        self.contextFormat = []
        self.html = ""
        self.is_saved = False

    def __len__(self):
        return len(self.context)

    def __getitem__(self, index):
        return self.context[index]

    def __setitem__(self, index, sentence: Sentence):
        self.context[index] = sentence
        self.contextFormat[index] = {
            "role": sentence.role,
            "content": sentence.content,
        }

    def __delitem__(self, index):
        del self.context[index]
        del self.contextFormat[index]

    def __iter__(self):
        return iter(self.context)

    def append(self, sentence: Sentence):
        self.context.append(sentence)
        self.contextFormat.append({"role": sentence.role, "content": sentence.content})

    def pop(self, index=-1):
        if len(self) == 0:
            return 0
            self.contextFormat.pop(index)
        return self.context.pop(index)

    def generateHtml(self):
        pass

    def appendPartialWords(self, PartialWords):
        self.context[-1].content += PartialWords
        self.contextFormat[-1]["content"] += PartialWords

    def clear(self):
        self.context.clear()
        self.contextFormat.clear()

    def setValue(self, chat):
        self.clear()
        self.title = chat.title
        for x in chat:
            self.append(x)

    def __repr__(self) -> str:
        return "\n".join([sentence.content for sentence in self.context])
