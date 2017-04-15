class Table:
    def __init__(self, number_of_calculation_units, size):
        self.N = number_of_calculation_units
        self.nodes = [Node() for x in range(0, number_of_calculation_units)]
        self.index = 0
        self.nodeIndex = 0
        self.size = size
        self.threshold = size // self.N

    def to_string(self):
        message = []
        for i in range(self.N):
            message.extend(self.nodes[i].dataArray)

        return message

    def get_node(self, i):
        return self.nodes[i]

    def append(self, data):
        if self.size == self.index:
            return False
        print(self.nodeIndex)
        print(self.index)
        if (not self.index == 0) and (self.index % self.threshold == 0):
            self.nodeIndex += 1

        self.nodes[self.nodeIndex].append(data)
        self.index += 1
        return True


class Node:
    def __init__(self):
        self.dataArray = []

    def append(self, data):
        self.dataArray.append(data)

    def set_data(self, liste):
        self.dataArray = liste

    def get_data(self):
        return self.dataArray
