

from NoteCurrentCashflow import NoteCurrentCashflow
from NoteChargeoffCashflow import NoteChargeoffCashflow
from NoteFullyPaidCashflow import NoteFullyPaidCashflow


class NoteCashflowFactory:

    def __init__(self):
        pass

    def CreateIntance(self, noteCashflowType, note):
        if not globals().has_key(noteCashflowType):
            return None
        else:
            return globals()[noteCashflowType](note)


