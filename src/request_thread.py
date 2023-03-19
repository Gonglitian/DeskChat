from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import traceback
import time
from src.chat_manager import Sentence, ChatManager
import requests, json
from src.globals import *


class RequestTask(QThread):
    renderSignal = pyqtSignal()
    finishSignal = pyqtSignal()
    stateUpdateSignal = pyqtSignal(str, bool)
    errorSignal = pyqtSignal(str)
    summaryFinishSignal = pyqtSignal(bool)
    informationUpdateSignal = pyqtSignal(list)

    def __init__(self, inputSentence: str, summaryFlag: bool):
        super(RequestTask, self).__init__()
        self.inputSentence = inputSentence
        self.runPermission = True
        self.summaryFlag = summaryFlag
        self.informationList = []

    def run(self):
        myChat.append(Sentence(USER, self.inputSentence))
        self.renderSignal.emit()
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": myChat.contextFormat,  # [{"role": "user", "content": f"{inputs}"}],
            "temperature": 1,  # 1.0,
            "top_p": 1,  # 1.0,
            "n": 1,
            "stream": True,
            "presence_penalty": 0,
            "frequency_penalty": 0,
        }
        with requests.Session() as session:
            try:
                self.stateUpdateSignal.emit("正在连接...", False)
                startTime = time.time()
                response = session.post(
                    API_URL, headers=headers, json=payload, stream=True, timeout=5
                )
                endTime = time.time()

                self.informationList.append(int((endTime - startTime) * 1000))
                self.informationUpdateSignal.emit(self.informationList)

                content = ""
                # 新增空元素，准备接受流式传输内容
                myChat.append(Sentence(ASSISTANT, content))

                # 开始获取流式传输内容
                for chunk in response.iter_lines():
                    self.stateUpdateSignal.emit("回答生成中", False)
                    if not self.runPermission:
                        response.raw.close()
                        return self.finishSignal.emit()  # 中止函数并发出中止信号
                    if chunk and len(chunk) > 14:  # >14：为了显示完整的错误信息
                        try:
                            data = json.loads(chunk.decode()[6:])
                            delta = data["choices"][0]["delta"]
                            if len(delta) == 0:
                                break
                        except Exception as e:
                            self.errorSignal.emit(
                                f"Message from API:\n{chunk.decode()},\n{traceback.format_exc()}"[
                                    :500
                                ]
                                + "\n..."
                            )
                            break
                        # status_text = f"id: {data['id']}, finish_reason: {data['choices'][0]['finish_reason']}"
                        partialWords = delta["content"] if "content" in delta else ""
                        myChat.appendPartialWords(partialWords)

                        self.renderSignal.emit()

            except Exception as e:
                self.errorSignal.emit(traceback.format_exc()[:500] + "\n...")
        if self.summaryFlag:
            if myChat[-2].content == summaryString:
                self.summaryFinishSignal.emit(False)
            else:
                myChat.title = myChat[-1].content
                self.summaryFinishSignal.emit(True)
        self.stateUpdateSignal.emit("生成完毕", True)

        self.finishSignal.emit()
