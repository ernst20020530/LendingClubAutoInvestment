

from FilterBase import FilterBase
from FilterBase import PercentileNode


class PublicRecord(FilterBase):

    Field_MaxmthsSinceLastRecord = 'MaxmthsSinceLastRecord'
    Field_MaxmthsSinceLastMajorDerog = 'MaxmthsSinceLastMajorDerog'


    def __init__(self, arg, logFile, monitorLog, fileLog):
        super(PublicRecord, self).__init__('PUBLIC RECORD', arg, logFile, monitorLog, fileLog)

        self.showField = ['mthsSinceLastRecord','mthsSinceLastMajorDerog']
        self.percentileField = [PercentileNode('mthsSinceLastRecord', True), 
                                PercentileNode('mthsSinceLastMajorDerog', True)]

        
    def Filter(self, notes):
        notes = self.GetMaxmthsSinceLastRecord(notes, self.arg[PublicRecord.Field_MaxmthsSinceLastRecord])
        notes = self.GetMaxmthsSinceLastMajorDerog(notes, self.arg[PublicRecord.Field_MaxmthsSinceLastMajorDerog])
        return notes

    def GetShowFields(self):
        return self.showField


    def GetPercentileFields(self):
        return self.percentileField


    def GetMaxmthsSinceLastRecord(self, notes, maxmthsSinceLastRecord):
        filteredList = []
        for i in notes:
            if i['mthsSinceLastRecord'] == None or i['mthsSinceLastRecord'] <= maxmthsSinceLastRecord:
                filteredList.append(i)
        return filteredList


    def GetMaxmthsSinceLastMajorDerog(self, notes, maxmthsSinceLastMajorDerog):
        filteredList = []
        for i in notes:
            if i['mthsSinceLastMajorDerog'] == None or i['mthsSinceLastMajorDerog'] <= maxmthsSinceLastMajorDerog:
                filteredList.append(i)
        return filteredList

