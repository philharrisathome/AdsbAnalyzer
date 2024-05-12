import socket

import ReceiverInterface

class SBSReceiver(ReceiverInterface.ReceiverInterface):

    __socket = None
    __ip = ''
    __port = 0
    __logfilename = None
    __logfile = None
    __buffer = ''

    # Expects params of form {"ip": "192.168.1.7", "port": 30003, ["logfile": 'adsbdata.txt']}
    def __init__(self, params):
        self.__ip = params['ip']
        self.__port = params['port']
        if 'logfile' in params:
            self.__logfilename = params['logfile']

    # Returns True on success, False on failed
    def open(self) -> bool:
        # Open the socket
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((self.__ip, self.__port))
        # Open the logfile (if present)
        if self.__logfilename:
            self.__logfile = open(self.__logfilename, 'wb')

        return True

    def close(self) -> None:
        self.__socket.close()
        if self.__logfile:
            self.__logfile.close()

    def getMessages(self) -> list[str]:
        rx = self.__socket.recv(128)
        # Save to the log file (if open)
        if self.__logfile:
            self.__logfile.write(rx)
        # Process the messages
        self.__buffer += str(rx, "utf-8")
        msgs = self.__buffer.splitlines(True)
        if not msgs[-1].endswith('\n'):
            self.__buffer = msgs[-1]
            msgs.pop()
        return msgs

