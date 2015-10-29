

from FilterBase import FilterBase


class Mortgage(FilterBase):
    def __init__(self, arg, logFile, monitorLog, fileLog):
        super(Mortgage, self).__init__('MORTGAGE', arg, logFile, monitorLog, fileLog)

        self.showField = ['mortAcc']


    def GetShowFields(self):
        return self.showField

