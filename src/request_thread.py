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
    stateUpdateSignal = pyqtSignal(str)
    errorSignal = pyqtSignal(str)
    summaryFinishSignal = pyqtSignal(str, bool)
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
                startTime = time.time()
                response = session.post(
                    API_URL, headers=headers, json=payload, stream=True
                )
                endTime = time.time()
                self.informationList.append(int((endTime - startTime) * 1000))
                content = ""
                # 新增空元素，准备接受流式传输内容
                myChat.append(Sentence(ASSISTANT, content))

                # 开始获取流式传输内容
                for chunk in response.iter_lines():
                    self.stateUpdateSignal.emit("回答生成中")
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
                                f"Message from API:{chunk.decode()},\n{traceback.format_exc()}"
                            )
                            break
                        # status_text = f"id: {data['id']}, finish_reason: {data['choices'][0]['finish_reason']}"
                        partialWords = delta["content"] if "content" in delta else ""
                        myChat.appendPartialWords(partialWords)

                        self.informationUpdateSignal.emit(self.informationList)
                        self.renderSignal.emit()

            except Exception as e:
                self.errorSignal.emit(traceback.format_exc())
        if self.summaryFlag:
            if myChat[-2] == summaryString:
                self.summaryFinishSignal.emit(myChat[-1], False)
            else:
                self.summaryFinishSignal.emit(myChat[-1], True)
        self.stateUpdateSignal.emit("生成完毕")

        self.finishSignal.emit()
