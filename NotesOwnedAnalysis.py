

import bwLendingClub
import NotesPurchaseProcessor
import NoteExpectedCashflow
import NoteFullyPaidCashflow
import array
import CashFlowCalcuator
import NoteCashflowFactory
import LogLine


class NotesOwnedAnalysis:


    def __init__(self, sourceNotes, field, values):
        self.m_noteCashflowFac = NoteCashflowFactory.NoteCashflowFactory()

        self.targetNotesSet = []
        for n in sourceNotes:
            for v in values:
                if n[field] == v:
                     self.targetNotesSet.append(n)
                     break
        
        self.targetNotesSet = self.CalculateLoanHorizonForeachNote(self.targetNotesSet)


    def Combine(self, notesOwnedAnalysisInstance):
        self.targetNotesSet.extend(notesOwnedAnalysisInstance.targetNotesSet)
        return self


    def GetNotesSet(self):
        return self.targetNotesSet

    
    def ShowTotalInterestReceived(self):
        totalInterestReceived = 0
        for n in self.targetNotesSet:
            totalInterestReceived += n['interestReceived']

        print(LogLine.LogLine('TotalInterestReceived').logElement('TotalInterestReceived',totalInterestReceived).Get())


    def CashflowWeightedReturn(self):
        cashflowList = self.CashflowWeightedReturnCashFlow()
        irr = CashFlowCalcuator.ConsolidateIRR(cashflowList)
        print(LogLine.LogLine('ConsolidateIRR').logElement('ConsolidateIRR',irr))


    def TimeWeightedReturn(self):
        cashflowList = self.CashflowWeightedReturnCashFlow()

        #if len(cashflowList) == 1:
        #    for index in range(0, len(cashflowList) - 1):



    #targetStatusSetsName: field of loanStatus
    #threeyrRequiredRate: three years required rate
    #fiveyrRequiredRate: five years required rate
    #return the notes set including the irr and npv respecitvely

    def CalculateIRRAndNPVForeachNote(self, threeyrRequiredRate, fiveyrRequiredRate):
        for n in self.targetNotesSet:
            nc = None
            if n['loanStatus'] == 'Current':
                nc = self.m_noteCashflowFac.CreateIntance('NoteCurrentCashflow', n)
            elif n['loanStatus'] == 'Charged Off':
                nc = self.m_noteCashflowFac.CreateIntance('NoteChargeoffCashflow', n)
            elif n['loanStatus'] == 'Fully Paid':
                nc = self.m_noteCashflowFac.CreateIntance('NoteFullyPaidCashflow', n)

            n['irr'] = nc.IRR()

            if int(n['loanLength']) == 60:
                n['npv'] = nc.NPV(fiveyrRequiredRate)
            elif int(n['loanLength']) == 36:
                n['npv'] = nc.NPV(threeyrRequiredRate)

            print(LogLine.LogLine('CurrentNote Return').logField('loanId',n).logField('loanStatus',n).logField('noteAmount',n).logField('grade',n).logField('interestRate',n).logField('irr',n).logField('npv',n).Get())
        return self.targetNotesSet


    def ShowIRRAndNPVForeachNote(self, threeyrRequiredRate, fiveyrRequiredRate):
        for n in self.targetNotesSet:
            print(LogLine.LogLine('CurrentNote Return').logField('loanId',n).logField('loanStatus',n).logField('noteAmount',n).logField('grade',n).logField('interestRate',n).logField('irr',n).logField('npv',n).Get())


    def ShowIRRAndNPVStatistics(self):
        irrList = []
        npvList = []
        for n in self.targetNotesSet:
            if n['irr'] == 0:
                continue
            irrList.append(n['irr'])
            npvList.append(n['npv'])

        irrMean = Statistics.mean(irrList)
        npvMean = Statistics.mean(npvList)

        irrStandDeviation = Statistics.stand_deviation(irrList)
        npvStandDeviation = Statistics.stand_deviation(npvList)

        print(LogLine.LogLine('IRR').logElement('Mean',irrMean).logElement('Stand Deviation',irrStandDeviation).Get())
        print(LogLine.LogLine('NPV').logElement('Mean',npvMean).logElement('Stand Deviation',npvStandDeviation).Get())

        a = 0
                

    def CalculateLoanHorizonForeachNote(self, targeSet, orderDateArray = None, maturityDateVarArray = None):
        for t in targeSet:
            orderDateArray = str(t['orderDate']).split('-')
            orderDateVar = int(orderDateArray[0]) * 12 + int(orderDateArray[1])

            t['orderDateVar'] = orderDateVar
            if orderDateArray != None:
                orderDateArray.append(t['orderDateVar'])

            issueDateArray = str(t['issueDate']).split('-')
            issueDateVar = int(issueDateArray[0]) * 12 + int(issueDateArray[1])
            t['issueDateVar'] = issueDateVar

            t['maturityDateVar'] = orderDateVar + int(t['loanLength'])
            if maturityDateVarArray != None:
                maturityDateVarArray.append(t['maturityDateVar'])

            if not t['lastPaymentDate'] == None:
                lastPaymentDateArray = str(t['lastPaymentDate']).split('-')
                lastPaymentDateVar = int(lastPaymentDateArray[0]) * 12 + int(lastPaymentDateArray[1])
                t['lastPaymentDateVar'] = lastPaymentDateVar
            else:
                t['lastPaymentDateVar'] = t['orderDateVar']
        return targeSet


    def CashflowWeightedReturnCashFlow(self):
        orderDateVarArray = self.GetOrderDateVarList()
        maturityDateVarArray = self.GetMaturityDateVarList()

        earliestDate = min(orderDateVarArray)
        maxMaturityDate = max(maturityDateVarArray)
        cashflowList = array.array('f')
        for i in range(0, maxMaturityDate - earliestDate + 1):
            cashflowList.append(0)

        for t in self.targetNotesSet:
            t['orderDateVar'] -= earliestDate

            if t['loanStatus'] == 'Current':
                nc = self.m_noteCashflowFac.CreateIntance('NoteCurrentCashflow', t)
            elif t['loanStatus'] == 'Charged Off':
                nc = self.m_noteCashflowFac.CreateIntance('NoteChargeoffCashflow', t)
            elif t['loanStatus'] == 'Fully Paid':
                nc = self.m_noteCashflowFac.CreateIntance('NoteFullyPaidCashflow', t)

            if nc == None:
                print('error: Cannot create ' + self.m_noteCashflowType + ' instance!')
                continue
            cf = nc.GetCashflow()
            for i in range(0, len(cf)):
                cashflowList[i + t['orderDateVar']] += cf[i]

        return cashflowList




    def GetOrderDateVarList(self):
        orderDateVarList = []
        for n in self.targetNotesSet:
            orderDateVarList.append(n['orderDateVar'])
        return orderDateVarList


    def GetMaturityDateVarList(self):
        maturityDateVarList = []
        for n in self.targetNotesSet:
            maturityDateVarList.append(n['maturityDateVar'])
        return maturityDateVarList

        


