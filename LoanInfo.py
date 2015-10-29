

from FilterBase import FilterBase
from FilterBase import PercentileNode


class LoanInfo(FilterBase):

    FIELD_Grade = 'Grade'
    FIELD_FundPercentage = 'FundPercentage'

    def __init__(self, arg, logFile, monitorLog, fileLog):
        super(LoanInfo, self).__init__('LOAN INFO', arg, logFile, monitorLog, fileLog)

        self.showField = ['id', 'memberId', 'term', 'intRate', 'grade', 'installment', 'fundedAmount', 'loanAmount', LoanInfo.FIELD_FundPercentage, FilterBase.sumPercentile]
        self.percentileField = [PercentileNode('intRate',False),
                                PercentileNode(LoanInfo.FIELD_FundPercentage,False,100)]

    def Start(self, notes):
        for n in notes:
            n[FilterBase.sumPercentile] = 0
        return notes
    
       
    def Filter(self, notes):
        notes = self.CalculateFundPercentage(notes)
        notes = self.SetGrade(notes,self.arg[LoanInfo.FIELD_Grade])
        return notes


    def GetShowFields(self):
        return self.showField


    def GetPercentileFields(self):
        return self.percentileField


    #grade  'A','B','C'
    def SetGrade(self,notes,gradeList):
        filteredList = []
        for i in notes:
            for j in gradeList:
                if i['grade'] == j:
                    filteredList.append(i)
                    break;
        return filteredList


    def CalculateFundPercentage(self, notes):
        for n in notes:
            n[LoanInfo.FIELD_FundPercentage] = n['fundedAmount'] / float(n['loanAmount'])
        return notes


    


        
