from threading import Thread


class Worker(Thread):
    def __init__(self, data, process, parent):
        Thread.__init__(self)
        self.data = data
        self.process = process
        self.parent = parent

    def run(self):
        print("run worker")
        self.process.start(self, self.data)

    def end_task_notify(self, data):
        self.parent.end_task(self, data)
