

from FilterBase import FilterBase
from FilterBase import PercentileNode


class BorrowerGeneral(FilterBase):


    Field_HomeOwnership = 'HomeOwnership'
    Field_MinempLength = 'MinempLength'
    Field_MaxPrepaymentAndIncomeRatio = 'MaxPrepaymentAndIncomeRatio'
    Field_Purpose = 'Purpose'


    def __init__(self, arg, logFile, monitorLog, fileLog):
        super(BorrowerGeneral, self).__init__('BORROWER GENERAL', arg, logFile, monitorLog, fileLog)

        self.showField = ['empLength','homeOwnership','annualInc','isIncV','purpose','dti','prepaymentAndIncomeRatio']
        self.percentileField = [PercentileNode('empLength', False), PercentileNode('dti', True), PercentileNode('prepaymentAndIncomeRatio', True)]
        

    def Filter(self, notes):
        notes = self.SetHomeOwnership(notes, self.arg[BorrowerGeneral.Field_HomeOwnership])
        notes = self.SetMinempLength(notes, self.arg[BorrowerGeneral.Field_MinempLength])
        notes = self.SetMaxPrepaymentAndIncomeRatio(notes, self.arg[BorrowerGeneral.Field_MaxPrepaymentAndIncomeRatio])
        notes = self.SetPurpose(notes, self.arg[BorrowerGeneral.Field_Purpose])
        return notes


    def GetShowFields(self):
        return self.showField

    def GetPercentileFields(self):
        return self.percentileField
          
    #homeOwnership      RENT, OWN, MORTGAGE, OTHER
    def SetHomeOwnership(self,notes,homeOwnership):
        filteredList = []
        for i in notes:
            for j in homeOwnership:
                if i['homeOwnership'] == j:
                    filteredList.append(i)
                    break;
        return filteredList
    
        
    #empLength      int
    def SetMinempLength(self,notes,minEmpLength):
        filteredList = []
        for i in notes:
            if i['empLength'] >= minEmpLength:
                filteredList.append(i);
        return filteredList

    
    def SetMaxPrepaymentAndIncomeRatio(self, notes, maxPrepaymentAndIncomeRatio):
        filteredList = []
        for i in notes:
            prepaymentAndIncomeRatio = i['installment'] * 12 / i['annualInc']
            i['prepaymentAndIncomeRatio'] = prepaymentAndIncomeRatio
            if prepaymentAndIncomeRatio <= maxPrepaymentAndIncomeRatio:
                filteredList.append(i)
        return filteredList


    #purpose        debt_consolidation, medical, home_improvement, renewable_energy, small_business, wedding, vacation, moving, house, car, major_purchase, credit_card, other
    def SetPurpose(self, notes, purpose):
        filteredList = []
        for i in notes:
            for j in purpose:
                if i['purpose'] == j:
                    filteredList.append(i)
                    break;
        return filteredList


