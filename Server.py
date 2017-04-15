import socket
from threading import Thread
import select
from CalculationUnit import CalculationUnit

class ServerDispatcher(Thread):
    def __init__(self,dispatcher, gate, sizeBuffer, maxClientSocket):
        Thread.__init__(self)
        self.dispatcher = dispatcher
        self.GATE = gate
        self.SIZE_BUFFER = sizeBuffer
        self.MAX_CLIENT = maxClientSocket
        self.lookupCalculationUnit2Socket = dict()
        self.lookupSocket2CalculationUnit = dict()
        self.lookupSocket2Resultat = dict()
        self.server_socket = None
        self.serverOnline = True

    def stop_server(self):
        self.serverOnline = False

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', self.GATE))
        server_socket.listen(self.MAX_CLIENT)
        # Add server socket to the list of readable connections
        self.server_socket = server_socket

        print("server started on port " + str(self.GATE) + " [ok]")
        print("=============SERVEUR ONLINE=============")
        while self.serverOnline:
            list_socket = list(self.lookupCalculationUnit2Socket.values())
            list_socket.append(self.server_socket)
            read_sockets, write_sockets, error_sockets = select.select(list_socket, [], [], 2)
            for sock in read_sockets:
                # New connection
                if sock == server_socket:
                    sockfd, addr = server_socket.accept()
                    print("Client (%s) connected" % addr)

                else:
                    # Data recieved from client, process it
                    try:
                        # In Windows, sometimes when a TCP program closes abruptly,
                        # a "Connection reset by peer" exception will be thrown
                        data = sock.recv(self.SIZE_BUFFER).decode('utf-8').rstrip()
                        dataTab = data.split("\r\n")
                        for data in dataTab:
                            print("----")
                            print(data)
                            print(data == "ENDRESULT")
                            print("----")
                            if len(data) == 0:
                                self.lookupSocket2CalculationUnit[sock].on_disconnect()
                                del self.lookupCalculationUnit2Socket[self.lookupSocket2CalculationUnit[sock]]
                                del self.lookupSocket2CalculationUnit[sock]
                                sock.close()

                            if data == "RESULT":
                                self.lookupSocket2Resultat[sock] = ""

                            elif data == "ENDRESULT":
                                print("ENDRESULT!!")
                                listRslt = eval(self.lookupSocket2Resultat[sock])
                                self.dispatcher.join(self.lookupSocket2CalculationUnit[sock].get_node_index(), listRslt)

                            elif isinstance(self.lookupSocket2Resultat[sock], str):
                                #  si STR alors on attend un résultat
                                self.lookupSocket2Resultat[sock] += data

                    # client disconnected, so remove from socket list
                    except Exception as err:
                        self.lookupSocket2CalculationUnit[sock].on_disconnect()
                        del self.lookupCalculationUnit2Socket[self.lookupSocket2CalculationUnit[sock]]
                        del self.lookupSocket2CalculationUnit[sock]
                        sock.close()

        for client in list(self.lookupCalculationUnit2Socket.values()):
            client.close()

        self.server_socket.close()

        print("=============SERVEUR OFFLINE=============")

    def connect(self, calcul_unit):
        """

        :param calcul_unit:
        :type calcul_unit: CalculationUnit
        :return:
        """
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_sock.connect((calcul_unit.get_address(), calcul_unit.get_gate()))
            self.lookupCalculationUnit2Socket[calcul_unit] = client_sock
            self.lookupSocket2CalculationUnit[client_sock] = calcul_unit
            self.lookupSocket2Resultat[client_sock] = None
            calcul_unit.on_connect()
        except socket.timeout:
            return False

        return True

    def send(self, calculation_unit, message):
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
        socketClient = self.lookupCalculationUnit2Socket[calculation_unit]
        paquet = len(message) // self.SIZE_BUFFER

        if len(message) % self.SIZE_BUFFER == 0:
            for i in range(paquet):
                socketClient.send(message[i * self.SIZE_BUFFER: self.SIZE_BUFFER * (i + 1)])
        else:
            for i in range(paquet + 1):
                socketClient.send(message[(self.SIZE_BUFFER * i):min(len(message), self.SIZE_BUFFER * (i + 1))])
