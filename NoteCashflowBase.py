

import TVM
import CashFlowCalcuator


class NoteCashflowBase:

    def __init__(self, noteStatus, note):
        self.m_cashflow = []

        if note['loanStatus'] != noteStatus:
            return

        paymentCount = self.GetPaymentReceivedHorizon(note)
        if paymentCount == 0:
            return

        self.m_cashflow.append(-note['noteAmount'])
        principal = self.GetPrincipalIntrisicValue(note)
        pmt = self.GetPMT(note)

        if paymentCount == 1:

            #balloom payment, including last payment and principal
            self.m_cashflow.append(pmt + principal)
        else:
            for i in range(0, paymentCount - 1):
                self.m_cashflow.append(pmt)

            #balloom payment, including last payment and principal
            self.m_cashflow.append(pmt + principal)


    def GetCashflow(self):
        return self.m_cashflow


    # the present value of all the future cash flow
    def GetPrincipalIntrisicValue(self, note):
        return note['principalPending']


    def GetPaymentReceivedHorizon(self, note):
        beginningDateVar = 0
        if note['issueDateVar'] > note['orderDateVar']:
            beginningDateVar = note['issueDateVar']
        else:
            beginningDateVar = note['orderDateVar']

        return int(note['lastPaymentDateVar']) - int(beginningDateVar)


    def GetPMT(self,note):
        investmentAmount = 0
        if note['noteAmount'] == 25 or note['noteAmount'] == 50:
            investmentAmount = note['noteAmount']
        else:
            investmentAmount = 25
        return TVM.PMT(note['interestRate'] / 1200, note['loanLength'], -investmentAmount, 0)



    def IRR(self):
        if len(self.m_cashflow) == 0:
            return 0
        elif self.m_cashflow[0] == 0:
            return 0
        irr = CashFlowCalcuator.irr2(self.m_cashflow) * float(12)
        if irr == TVM.error:
            irr = 0

        return irr


    def NPV(self, rate):
        if len(self.m_cashflow) == 0:
            return 0
        elif self.m_cashflow[0] == 0:
            return 0
        return CashFlowCalcuator.npv(rate/12, self.m_cashflow)
