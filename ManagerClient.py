import importlib

from Worker import Worker
from Process import Process
import Client


class ManagerClient:
    def __init__(self,  gate, size_buffer):
        self.waitLinesCode = False
        self.waitData = False
        self.codeTransmitted = None
        self.className = None
        self.data = None
        self.worker = None
        self.server = Client.Client(self, gate, size_buffer)

    def start(self):
        with open("./module/process.py", 'a+', encoding='utf-8') as fd:
            fd.write("")
        self.server.start()

    def end_task(self, worker, data):
        print(data)
        self.server.send("RESULT")
        self.server.send(str(data))
        self.server.send("ENDRESULT")

    def on_message(self, message):
        if len(message) > 4 and message[0:4] == "CODE":
            message = message.split('-')
            self.codeTransmitted = ""
            self.className = message[1]
            self.waitLinesCode = True

        elif message == "ENDCODE":
            self.waitLinesCode = False
            print(self.codeTransmitted)
            with open("./module/process.py", 'w+', encoding='utf-8') as fd:
                fd.write(self.codeTransmitted)

            self.codeTransmitted = None

        elif message == "DATA":
            self.waitData = True
            self.data = ""

        elif message == "ENDDATA":
            self.waitData = False
            self.data = eval(self.data)
            print(self.data)

        elif message == "RUN":
            clazz = getattr(importlib.import_module("module.process"), self.className)
            process = clazz()
            self.worker = Worker(self.data, process, self)
            self.worker.start()

        elif self.waitData:
            self.data += message
            
        elif self.waitLinesCode:
            self.codeTransmitted += message + "\n"

if __name__ == '__main__':

    manager = ManagerClient(4898, 4096)
    manager.start()
