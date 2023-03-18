class Sentence:
    def __init__(self, role: str = "", content: str = "") -> None:
        self.role = role
        self.content = content


class ChatManager:
    def __init__(self, title: str = "New Chat") -> None:
        self.title = title
        self.context = []
        self.contextFormat = []
        self.html = ""

    def __len__(self):
        return len(self.context)

    def __getitem__(self, index):
        return self.context[index].content

    def __setitem__(self, index, sentence: Sentence):
        self.context[index] = sentence
        self.contextFormat[index]["content"] = {
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

    def __repr__(self) -> str:
        return "\n".join([sentence.content for sentence in self.context])
