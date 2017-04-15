class CalculationUnit:
    def __init__(self, addr, gate):
        self.address = addr
        self.gate = gate
        self.connected = False
        self.process = None
        self.index = None
        self.state = None

    def get_address(self):
        """
        :return: address IP
         :rtype: str
        """
        return self.address

    def get_gate(self):
        """
        :return: gate connection
         :rtype: str
        """
        return self.gate

    def get_process(self):
        """
        :return: a process object
        :rtype: Process
        """
        return self.process

    def get_code_process(self):
        """
        :return: code of process object
        :rtype: str
        """
        contain = None
        with open(self.process.__class__.__name__ + ".py", 'r', encoding='utf-8') as fd:
            contain = fd.read()

        return contain

    def get_node_index(self):
        """

        :return:  index
        """
        return self.index

    def set_node_index(self, index):
        self.index = index

    def attach_process(self, process_obj):
        self.process = process_obj

    def is_connected(self):
        return self.connected

    def is_deconnected(self):
        return not self.connected

    def on_deconnect(self):
        self.connected = False

    def on_connect(self):
        self.connected = True

