

from FilterBase import FilterBase
from FilterBase import PercentileNode


class Bankruptcies(FilterBase):

    FIELD_MaxpubRecBankruptcies = 'MaxpubRecBankruptcies'
    FIELD_MaxmthsSinceRecentBcDlq = 'MaxmthsSinceRecentBcDlq'

    def __init__(self, arg, logFile, monitorLog, fileLog):
        super(Bankruptcies, self).__init__('BANKRUPTCIES', arg, logFile, monitorLog, fileLog)

        self.showField = ['mthsSinceRecentBcDlq','pubRecBankruptcies']
        self.percentileField = [PercentileNode('mthsSinceRecentBcDlq',True), PercentileNode('pubRecBankruptcies',True)]


    def Filter(self, notes):
        notes = self.SetMaxmthsSinceRecentBcDlq(notes, self.arg[Bankruptcies.FIELD_MaxmthsSinceRecentBcDlq])
        notes = self.SetMaxpubRecBankruptcies(notes, self.arg[Bankruptcies.FIELD_MaxpubRecBankruptcies])
        return notes


    def GetShowFields(self):
        return self.showField


    def GetPercentileFields(self):
        return self.percentileField


    def SetMaxmthsSinceRecentBcDlq(self, notes, maxmthsSinceRecentBcDlq):
        filteredList = []
        for i in notes:
            if i['mthsSinceRecentBcDlq'] == None or i['mthsSinceRecentBcDlq'] <= maxmthsSinceRecentBcDlq:
                filteredList.append(i)
        return filteredList


    def SetMaxpubRecBankruptcies(self, notes, maxpubRecBankruptcies):
        filteredList = []
        for i in notes:
            if i['pubRecBankruptcies'] == None or i['pubRecBankruptcies'] <= maxpubRecBankruptcies:
                filteredList.append(i)
        return filteredList


