

from FilterBase import FilterBase
from FilterBase import PercentileNode
from datetime import datetime


class CurrentAccounts(FilterBase):

    FIELD_MaxpercentBcGt75 = 'MaxpercentBcGt75'
    FIELD_MaxbcUtil = 'MaxbcUtil'
    FIELD_earliestCrLineComparable = 'earliestCrLineComparable'

    def __init__(self, arg, logFile, monitorLog, fileLog):
        super(CurrentAccounts, self).__init__('CURRENT ACCOUNTS', arg, logFile, monitorLog, fileLog)

        self.showField = ['accOpenPast24Mths','numIlTl','totCollAmt','earliestCrLine','percentBcGt75','bcUtil']
        self.percentileField = [PercentileNode('accOpenPast24Mths', True),
                                PercentileNode(CurrentAccounts.FIELD_earliestCrLineComparable, True),
                                PercentileNode('percentBcGt75', True),
                                PercentileNode('bcUtil', True)]


    def GetShowFields(self):
        return self.showField


    def GetPercentileFields(self):
        return self.percentileField


    def Filter(self, notes):
        notes = self.CalculateEarliestCrLine(notes)
        notes = self.SetMaxPercentBcGt75(notes,self.arg[CurrentAccounts.FIELD_MaxpercentBcGt75])
        notes = self.SetMaxbcUtil(notes,self.arg[CurrentAccounts.FIELD_MaxbcUtil])
        return notes


    def SetMaxPercentBcGt75(self, notes, maxPercentBcGt75):
        filteredList = []
        for i in notes:
            if i['percentBcGt75'] == None or i['percentBcGt75'] <= maxPercentBcGt75:
                filteredList.append(i)
        return filteredList


    def SetMaxbcUtil(self, notes, maxbcUtil):
        filteredList = []
        for i in notes:
                if i['bcUtil'] == None or i['bcUtil'] <= maxbcUtil:
                    filteredList.append(i)
        return filteredList


    def CalculateEarliestCrLine(self, notes):
        for n in notes:
            array = str(n['earliestCrLine']).split('-')
            if len(array) >= 2:
                n[CurrentAccounts.FIELD_earliestCrLineComparable] = int(array[0]) * 100 + int(array[1])
            else:
                n[CurrentAccounts.FIELD_earliestCrLineComparable] = datetime.now().year * 100 + datetime.now().month
        return notes
