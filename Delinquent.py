

from FilterBase import FilterBase
from FilterBase import PercentileNode


class Delinquent(FilterBase):

    FIELD_MaxaccNowDelinq = 'MaxaccNowDelinq'
    FIELD_Maxdelinq2Yrs = 'Maxdelinq2Yrs'
    FIELD_MaxmthsSinceLastDelinq = 'MaxmthsSinceLastDelinq'
    FIELD_NumAcctsEver120Ppd = 'numAcctsEver120Ppd'

    def __init__(self, arg, logFile, monitorLog, fileLog):
        super(Delinquent, self).__init__('DELINQUENT', arg, logFile, monitorLog, fileLog)

        self.showField = ['accNowDelinq','delinq2Yrs','delinqAmnt','mthsSinceLastDelinq','mthsSinceRecentRevolDelinq','numAcctsEver120Ppd']
        self.percentileField = [PercentileNode('accNowDelinq', True), 
                                PercentileNode('delinq2Yrs', True),
                                PercentileNode('delinqAmnt', True), 
                                PercentileNode('mthsSinceLastDelinq', True),
                                PercentileNode('mthsSinceRecentRevolDelinq', True),
                                PercentileNode('numAcctsEver120Ppd', True)]
    
    def Filter(self, notes):
        notes = self.SetMaxaccNowDelinq(notes,self.arg[Delinquent.FIELD_MaxaccNowDelinq])
        notes = self.SetMaxdelinq2Yrs(notes,self.arg[Delinquent.FIELD_Maxdelinq2Yrs])
        notes = self.SetMaxmthsSinceLastDelinq(notes,self.arg[Delinquent.FIELD_MaxmthsSinceLastDelinq])
        notes = self.SetNumAcctsEver120Ppd(notes,self.arg[Delinquent.FIELD_NumAcctsEver120Ppd])
        return notes


    def GetShowFields(self):
        return self.showField


    def GetPercentileFields(self):
        return self.percentileField


    def SetMaxaccNowDelinq(self, notes, maxaccNowDelinq):
        filteredList = []
        for i in notes:
            if i['accNowDelinq'] <= maxaccNowDelinq:
                filteredList.append(i)
        return filteredList


    def SetMaxdelinq2Yrs(self, notes, maxdelinq2Yrs):
        filteredList = []
        for i in notes:
            if i['delinq2Yrs'] <= maxdelinq2Yrs:
                filteredList.append(i)
        return filteredList


    def SetMaxmthsSinceLastDelinq(self, notes,maxmthsSinceLastDelinq):
        filteredList = []
        for i in notes:
            if i['mthsSinceLastDelinq'] <= maxmthsSinceLastDelinq:
                filteredList.append(i)
        return filteredList


    def SetNumAcctsEver120Ppd(self, notes,maxnumAcctsEver120Ppd):
        filteredList = []
        for i in notes:
            if i['numAcctsEver120Ppd'] <= maxnumAcctsEver120Ppd:
                filteredList.append(i)
        return filteredList




