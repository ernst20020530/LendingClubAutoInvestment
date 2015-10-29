__author__ = 'bwang'


import threading
import NotesPurchaseProcessor
import NotesOwnedAnalysis
import sys
import time
import bwLendingClub
import LogDateInfo
import CashFlowCalcuator
import TVM


logFileName = 'LendingClubLog'

args = ['EXIT',                     #exit application
        'AUTO_ON',                  #auto invest on
        'AUTO_OFF',                 #auto invest off
        'MANUAL'                    #manual invest
        'MONITORLOG_ON',
        'MONITORLOG_OFF',
        'FILELOG_ON',
        'FILELOG_OFF',
        'SHOW_ACASH',
        'SHOW_STATUS',
        'SEARCH_NOTES']

timerThread = None
lendingProcessor = None



def ShowAvailableFund():
    global g_lendingclub
    print(LogDateInfo.LogDateInfo('Available Cash:' + str(NotesPurchaseProcessor.g_lendingclub.AvailableCash())))


def ShowStatus():
    global lendingProcessor
    logStream = 'File Log:'
    if lendingProcessor.GetFileLog():
        logStream += 'Enalbed'
    else:
        logStream += 'Disalbed'

    logStream += '\tMonitor Log:'
    if lendingProcessor.GetMonitorLog():
        logStream += 'Enalbed'
    else:
        logStream += 'Disalbed'

    logStream += '\t'
    if lendingProcessor.IsAutoInvestment():
        logStream += 'AutoInvestment ON'
    else:
        logStream += 'AutoInvestment OFF'

    print(LogDateInfo.LogDateInfo(logStream).GetLogStream())





def ControlLoop():
    global timerThread
    global lendingProcessor

    while 1:
        input = str(sys.stdin.readline())
        if input == 'EXIT\n':
            if lendingProcessor.IsAutoInvestment():
                timerThread.cancel()
            break;
        elif input == 'AUTO_ON\n':
            lendingProcessor.EnableAutoInvestment()
            timerThread = threading.Timer(1,ExecuteLendingProcessor)
            timerThread.start()

        elif input == 'AUTO_OFF\n':
            timerThread.cancel()
            lendingProcessor.DisableAutoInvestment()

        elif input == 'MANUAL\n':
            lendingProcessor.Invest()

        elif input == 'MONITORLOG_ON\n':
            lendingProcessor.EnableMonitorLog()
        elif input == 'MONITORLOG_OFF\n':
            lendingProcessor.DisableMonitorLog()
        elif input == 'FILELOG_ON\n':
            lendingProcessor.EnableFileLog()
        elif input == 'FILELOG_OFF\n':
            lendingProcessor.DisableFileLog()
        elif input == 'SHOW_ACASH\n':
            ShowAvailableFund()
        elif input == 'SHOW_STATUS\n':
            ShowStatus()
        elif input == 'SEARCH_NOTES\n':
            lendingProcessor.SearchNotes()
        else:
            log = 'Incorrect argument, Please enter:\n'
            for a in args:
                log += a + '\n'
            print(log)



def ExecuteLendingProcessor():
    global timerThread
    global lendingProcessor

    lendingProcessor.AutoInvest()
    timerThread = threading.Timer(43200,ExecuteLendingProcessor)
    timerThread.start()


if __name__ == '__main__':

    #pmt = TVM.PMT(0.007417, 36, -25, 0)

    lendingProcessor = NotesPurchaseProcessor.NotesPurchaseProcessor(logFileName,True,True)

    #notesOwned = NotesPurchaseProcessor.g_lendingclub.NotesOwnedDetail()
    #no1 = NotesOwnedAnalysis.NotesOwnedAnalysis(notesOwned, 'loanStatus', ['Current'])
    ##no1 = NotesOwnedAnalysis.NotesOwnedAnalysis(notesOwned, 'loanId', [717399])

    #no2 = NotesOwnedAnalysis.NotesOwnedAnalysis(notesOwned, 'loanStatus', ['Charged Off'])
    #no3 = NotesOwnedAnalysis.NotesOwnedAnalysis(notesOwned, 'loanStatus', ['Fully Paid'])

    #no1.Combine(no2).Combine(no3)

    
    #no1.CalculateIRRAndNPVForeachNote(0.009, 0.0163)
    #no1.ShowIRRAndNPVStatistics()
    #no1.ShowTotalInterestReceived()

    #no1.CashflowWeightedReturn()

    #a = 0
    ControlLoop()






