from threading import Thread
import socket
import select
import pickle


class Client(Thread):
    def __init__(self, manager, gate, size_buffer):
        Thread.__init__(self)
        self.GATE = gate
        self.SIZE_BUFFER = size_buffer
        self.manager = manager
        self.MAX_CLIENT = 1
        self.master = None
        self.CONNECTION_LIST = []  # liste des unités de calcul connectés (socket)
        self.serverOnline = True

    def stop_server(self):
        self.serverOnline = False

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', self.GATE))
        server_socket.listen(self.MAX_CLIENT)
        # Add server socket to the list of readable connections
        self.CONNECTION_LIST.append(server_socket)

        print("server started on port " + str(self.GATE) + " [ok]")
        print("=============SERVEUR ONLINE=============")
        while self.serverOnline:
            read_sockets, write_sockets, error_sockets = select.select(self.CONNECTION_LIST, [], [])
            for sock in read_sockets:
                # New connection
                if sock == server_socket:
                    sockfd, addr = server_socket.accept()
                    self.CONNECTION_LIST.append(sockfd)
                    self.master = sockfd
                    print("Client (%s, %s) connected" % addr)

                else:
                    # Data recieved from client, process it
                    try:
                        data = sock.recv(self.SIZE_BUFFER).decode('utf-8').rstrip()
                        if len(data) == 0:
                            self.CONNECTION_LIST.pop(self.CONNECTION_LIST.index(sock))
                            sock.close()
                            self.master = None
                            break

                        linesdata = data.splitlines()
                        for data in linesdata:
                            self.manager.on_message(data)



                    # client disconnected, so remove from socket list
                    except Exception as err:
                        self.CONNECTION_LIST.pop(self.CONNECTION_LIST.index(sock))
                        self.master = None

        print("=============SERVEUR OFFLINE=============")
        server_socket.close()
        self.master.close()

    def send(self, message):
        """
        Transmet à l'unite de calcul un message

        :param message:
        :type message: str
        :param calculation_unit:
        :type calculation_unit: CalculationUnit
        :return:
        :rtype: None
        """

        if not message[-2:] == "\r\n":
            message += "\r\n"

        message = message.encode('utf-8')

        paquet = len(message) // self.SIZE_BUFFER

        if len(message) % self.SIZE_BUFFER == 0:
            for i in range(paquet):
                self.master.send(message[i * self.SIZE_BUFFER: self.SIZE_BUFFER * (i + 1)])
        else:
            for i in range(paquet + 1):
                self.master.send(message[(self.SIZE_BUFFER * i):min(len(message), self.SIZE_BUFFER * (i + 1))])
