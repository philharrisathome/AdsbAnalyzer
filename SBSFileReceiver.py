import time

import ReceiverInterface

class SBSFileReceiver(ReceiverInterface.ReceiverInterface):

    __logfilename = None
    __logfile = None
    __msgCount = 10
    __pauseInterval = 0.1

    # Expects params of form {'logfile': 'adsbdata.txt', ['msgcount': 10,] ['pause': 0.02]}
    def __init__(self, params):
        self.__logfilename = params['logfile']
        if 'msgcount' in params:
            self.__msgCount = params['msgcount']
        if 'pause' in params:
            self.__pauseInterval = params['pause']

    def open(self) -> bool:
        if self.__logfilename:
            self.__logfile = open(self.__logfilename, 'r')
        return not self.__logfile.closed

    def close(self) -> None:
        self.__logfile.close()

    def getMessages(self) -> list[str]:
        # Read 10 messages at a time, then pause
        msgs = []
        for i in range(0, self.__msgCount):
            m = self.__logfile.readline()
            if m.endswith('\n'):
                msgs.append(m)
            else:
                pass
        time.sleep(self.__pauseInterval)
        return msgs

