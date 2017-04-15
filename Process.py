from abc import ABCMeta
from abc import abstractmethod


class Process(metaclass=ABCMeta):
    def __init__(self):
        self.table = None
        self.parent = None

    def start(self, parent, table):
        self.parent = parent
        self.table = table
        self.process(self.table)
        self.end_task_notify_parent()

    def end_task_notify_parent(self):
        self.parent.end_task_notify(self.table)

    def get_table(self):
        return self.table

    def process(self, table):
        print('d')
