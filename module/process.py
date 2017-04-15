from Process import Process


class MyProcess(Process):
    def __init__(self):
        super().__init__()

    def process(self, table):
        print("DAVAI")
        for i in range(len(table)):
            table[i] = table[i] * table[i]
