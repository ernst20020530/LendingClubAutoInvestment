

from FilterBase import FilterBase


class Inquery(FilterBase):
    def __init__(self, arg, logFile, monitorLog, fileLog):
        super(Inquery, self).__init__('INQUERY', arg, logFile, monitorLog, fileLog)

        self.showField = ['inqLast6Mths','mthsSinceRecentInq']


    def GetShowFields(self):
        return self.showField



