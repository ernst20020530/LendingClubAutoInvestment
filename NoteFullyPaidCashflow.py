

import NoteCashflowBase


class NoteFullyPaidCashflow(NoteCashflowBase.NoteCashflowBase):
    def __init__(self, note):
        NoteCashflowBase.NoteCashflowBase.__init__(self, 'Fully Paid', note)


    def GetPrincipalIntrisicValue(self, note):
        pmt = self.GetPMT(note)
        paymentCount = self.GetPaymentReceivedHorizon(note)
        if paymentCount == 0:
            return note['noteAmount']

        return note['noteAmount'] - (pmt * paymentCount - note['interestReceived'])


