

import NoteCashflowBase

class NoteChargeoffCashflow(NoteCashflowBase.NoteCashflowBase):
    def __init__(self, note):
        NoteCashflowBase.NoteCashflowBase.__init__(self, 'Charged Off', note)


    def GetPrincipalIntrisicValue(self, note):
        return 0

