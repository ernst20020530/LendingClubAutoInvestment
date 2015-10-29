

from datetime import datetime

class LogDateInfo(object):
    def __init__(self, logTitle):
        self.log = '[Time]\t'
        self.log += datetime.now().__str__() + '\n'
        self.log += logTitle + '\n'

    def GetLogStream(self):
        return self.log


