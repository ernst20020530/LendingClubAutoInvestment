

import ICashFlowState
import TVM
import CashFlowCalcuator
from datetime import datetime

class NoteExpectedCashflow(ICashFlowState.ICashFlowState):

    def __init__(self, note):
        self.m_cashflow = [-note['noteAmount']]
        pmt = TVM.PMT(note['interestRate'] / 1200, note['loanLength'], -note['noteAmount'], 0)


        if note[loanStatus] == 'Current':
            for i in range(0, note['loanLength']):
                self.m_cashflow.append(pmt)
        elif note[loanStatus] == 'Charged Off':
            paymentsCount = abs(note['lastPaymentDateVar'] - note['issueDateVar'])


        #self.m_irr = CashFlowCalcuator.irr(self.m_cashflow) * 12
        #if self.m_irr == TVM.error:
        #    self.m_irr = 0


    def GetCashflow(self):
        return self.m_cashflow




