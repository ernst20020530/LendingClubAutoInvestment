

from FilterBase import FilterBase
from FilterBase import PercentileNode


class BorrowCredit(FilterBase):

    Field_ficoDif = 'ficoDif'
    Field_ficoCV = 'ficoCV'
    Field_totCurBalRatio = 'totCurBalRatio'
    Field_MaxtotCurBalRatio = 'MaxtotCurBalRatio'
    Field_MinFicoRange = 'MinFicoRange'
    Field_MaxmthsSinceLastMajorDerog = 'MaxmthsSinceLastMajorDerog'
    Field_MaxnumTl90gDpd24m = 'MaxnumTl90gDpd24m'
    Field_MaxnumTl30dpd = 'MaxnumTl30dpd'
    Field_MaxnumTl120dpd2m = 'MaxnumTl120dpd2m'
    Field_MaxchargeoffWithin12Mths = 'MaxchargeoffWithin12Mths'
    Field_Maxcollections12MthsExMed = 'Maxcollections12MthsExMed'

    def __init__(self, arg, logFile, monitorLog, fileLog):
        super(BorrowCredit, self).__init__('BORROWER CREDIT', arg, logFile, monitorLog, fileLog)

        self.showField = ['ficoRangeLow',
                          'ficoRangeHigh',
                          'totHiCredLim',
                          BorrowCredit.Field_totCurBalRatio,
                          'numTl90gDpd24m',
                          'numTl30dpd',
                          'numTl120dpd2m',
                          'chargeoffWithin12Mths',
                          'collections12MthsExMed']

        self.percentileField = [PercentileNode(BorrowCredit.Field_ficoCV,False),
                                PercentileNode('numTl90gDpd24m', True),
                                PercentileNode('numTl30dpd', True),
                                PercentileNode('numTl120dpd2m', True),
                                PercentileNode('chargeoffWithin12Mths', True),
                                PercentileNode('collections12MthsExMed', True)]


    def Filter(self, notes):
        notes = self.CalculateficoDif(notes)
        notes = self.CalculateTotCurBalRatio(notes)
        notes = self.SetMinFicoRange(notes, self.arg[BorrowCredit.Field_MinFicoRange])
        notes = self.SetMaxtotCurBalRatio(notes, self.arg[BorrowCredit.Field_MaxtotCurBalRatio])
        notes = self.SetMaxmthsSinceLastMajorDerog(notes, self.arg[BorrowCredit.Field_MaxmthsSinceLastMajorDerog])
        notes = self.SetMaxnumTl90gDpd24m(notes, self.arg[BorrowCredit.Field_MaxnumTl90gDpd24m])
        notes = self.SetMaxnumTl30dpd(notes, self.arg[BorrowCredit.Field_MaxnumTl30dpd])
        notes = self.SetMaxnumTl120dpd2m(notes, self.arg[BorrowCredit.Field_MaxnumTl120dpd2m])
        return notes


    def GetShowFields(self):
        return self.showField


    def GetPercentileFields(self):
        return self.percentileField


    def CalculateficoDif(self, notes):
        for n in notes:
            n[BorrowCredit.Field_ficoDif] = n['ficoRangeHigh'] - n['ficoRangeLow']
            n[BorrowCredit.Field_ficoCV] = (n['ficoRangeHigh'] + n['ficoRangeLow']) / float(n[BorrowCredit.Field_ficoDif])
        return notes


    def CalculateTotCurBalRatio(self, notes):
        for n in notes:
            n[BorrowCredit.Field_totCurBalRatio] = n['totCurBal'] / float(n['totHiCredLim'])
        return notes


    def SetMinFicoRange(self, notes, ficoRangeLow):
        filteredList = []
        for i in notes:
            if i['ficoRangeLow'] >= ficoRangeLow:
                filteredList.append(i)
        return filteredList
    
    #mthsSinceLastMajorDerog        int
    def SetMaxmthsSinceLastMajorDerog(self, notes, maxmthsSinceLastMajorDerog):
        filteredList = []
        for i in notes:
            if i['mthsSinceLastMajorDerog'] <= maxmthsSinceLastMajorDerog:
                filteredList.append(i)
        return filteredList


    def SetMaxnumTl90gDpd24m(self, notes, maxnumTl90gDpd24m):
        filteredList = []
        for i in notes:
            if i['numTl90gDpd24m'] == None or i['numTl90gDpd24m'] <= maxnumTl90gDpd24m:
                filteredList.append(i)
        return filteredList


    def SetMaxnumTl30dpd(self, notes, maxnumTl30dpd):
        filteredList = []
        for i in notes:
            if i['numTl30dpd'] == None or i['numTl30dpd'] <= maxnumTl30dpd:
                filteredList.append(i)
        return filteredList


    def SetMaxnumTl120dpd2m(self, notes, maxnumTl120dpd2m):
        filteredList = []
        for i in notes:
            if i['numTl120dpd2m'] == None or i['numTl120dpd2m'] <= maxnumTl120dpd2m:
                filteredList.append(i)
        return filteredList


    def SetMaxChargeoffWithin12Mths(self, notes, maxChargeoffWithin12Mths):
        filteredList = []
        for i in notes:
            if i['chargeoffWithin12Mths'] == None or i['chargeoffWithin12Mths'] <= maxChargeoffWithin12Mths:
                filteredList.append(i)
        return filteredList


    def SetMaxcollections12MthsExMed(self, notes, maxcollections12MthsExMed):
        filteredList = []
        for i in notes:
            if i['collections12MthsExMed'] == None or i['collections12MthsExMed'] <= maxcollections12MthsExMed:
                filteredList.append(i)
        return filteredList


    def SetMaxtotCurBalRatio(self, notes, maxtotCurBalRatio):
        filteredList = []
        for i in notes:
            if i[BorrowCredit.Field_totCurBalRatio] <= maxtotCurBalRatio:
                filteredList.append(i)
        return filteredList
