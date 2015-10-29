

#from threading import Thread
import threading
import time
import requests
from bwLendingClub import bwLendingClub
from NotesSort import NotesSort
import threading
import LogNotes
from datetime import datetime

from LoanInfo import LoanInfo
from BorrowerGeneral import BorrowerGeneral
from Delinquent import Delinquent
from Bankruptcies import Bankruptcies
from PublicRecord import PublicRecord
from BorrowCredit import BorrowCredit
from CurrentAccounts import CurrentAccounts
from Inquery import Inquery
from Mortgage import Mortgage
from FilterBase import FilterBase


Current = 'Current'
FullyPaid = 'Fully Paid'
ChargedOff = 'Charged Off'
Late31_120 = 'Late (31-120 days)'
InReview = 'In Review'
Issued = 'Issued'


loanStatusCount = { Current:0,FullyPaid:0,ChargedOff : 0,Late31_120 : 0,InReview : 0,Issued : 0}


g_lendingclub = bwLendingClub()



class NotesPurchaseProcessor:

    def __init__(self, logFileName, monitorLog = False, fileLog = False):

        now = datetime.now()
        logFileName += str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '-' + str(now.hour) + '-' + str(now.minute) + '-' + str(now.second) + '.lg'
        self.logFile = open(logFileName, 'w')
        self.monitorLog = monitorLog
        self.fileLog = fileLog
        self.autoInvestment = False
        self.lock = threading.Lock()

        arg = {
                'CURRENT ACCOUNTS':
                    {
                        'MaxpercentBcGt75': 20,         # 0 ~ 100    
                        'MaxbcUtil': 40                 # 0 ~ 100    
                    },
                'INQUERY':{},
                'MORTGAGE':{},
                'BORROWER CREDIT':
                    {
                        'MaxtotCurBalRatio': 0.6,
                        'MinFicoRange': 700,
                        'MaxmthsSinceLastMajorDerog': 0,
                        'MaxnumTl90gDpd24m': 0,
                        'MaxnumTl30dpd': 0,
                        'MaxnumTl120dpd2m': 0,
                        'MaxchargeoffWithin12Mths': 0,
                        'Maxcollections12MthsExMed': 0
                    },
                'PUBLIC RECORD':
                    {
                        'MaxmthsSinceLastRecord': 0,
                        'MaxmthsSinceLastMajorDerog': 0    
                    },
                'BANKRUPTCIES':
                    {
                        'MaxmthsSinceRecentBcDlq': 0,
                        'MaxpubRecBankruptcies': 0    
                    },
                'LOAN INFO':
                    {
                        'Grade':['A','B','C']    
                    },
                'DELINQUENT':
                    {
                        'MaxaccNowDelinq': 0,
                        'Maxdelinq2Yrs': 0,
                        'MaxmthsSinceLastDelinq': 0,
                        'numAcctsEver120Ppd': 0
                    },
                'BORROWER GENERAL':
                    {
                        'HomeOwnership': ['OWN','MORTGAGE','RENT'],
                        'MinempLength': 60,                                                                 # employment at least 60 months
                        'MaxPrepaymentAndIncomeRatio': 0.1,
                        'Purpose': ['debt_consolidation', 'credit_card']
                    }
                }

        self.filterList = []
        self.filterList.append(LoanInfo(arg, self.logFile, monitorLog, fileLog))
        self.filterList.append(BorrowerGeneral(arg, self.logFile, monitorLog, fileLog))
        self.filterList.append(Delinquent(arg, self.logFile, monitorLog, fileLog))
        self.filterList.append(Bankruptcies(arg, self.logFile, monitorLog, fileLog))
        self.filterList.append(PublicRecord(arg, self.logFile, monitorLog, fileLog))
        self.filterList.append(BorrowCredit(arg, self.logFile, monitorLog, fileLog))
        self.filterList.append(CurrentAccounts(arg, self.logFile, monitorLog, fileLog))
        self.filterList.append(Inquery(arg, self.logFile, monitorLog, fileLog))
        self.filterList.append(Mortgage(arg, self.logFile, monitorLog, fileLog))

    def EnableAutoInvestment(self):
        self.lock.acquire()
        self.autoInvestment = True
        self.lock.release()


    def DisableAutoInvestment(self):
        self.lock.acquire()
        self.autoInvestment = False
        self.lock.release()


    def IsAutoInvestment(self):
        self.lock.acquire()
        autoInvestment = self.autoInvestment
        self.lock.release()
        return autoInvestment


    def EnableMonitorLog(self):
        self.lock.acquire()
        self.monitorLog = True
        self.lock.release()

        for node in self.filterList:
            node.EnableMonitorLog()


    def DisableMonitorLog(self):
        self.lock.acquire()
        self.monitorLog = False
        self.lock.release()

        for node in self.filterList:
            node.DisableMonitorLog()


    def GetMonitorLog(self):
        self.lock.acquire()
        monitorLog = self.monitorLog
        self.lock.release()
        return monitorLog


    def EnableFileLog(self):
        self.lock.acquire()
        self.fileLog = True
        self.lock.release()

        for node in self.filterList:
            node.EnableFileLog()


    def DisableFileLog(self):
        self.lock.acquire()
        self.fileLog = False
        self.lock.release()

        for node in self.filterList:
            node.DisableFileLog()


    def GetFileLog(self):
        self.lock.acquire()
        fileLog = self.fileLog
        self.lock.release()
        return fileLog


    def AutoInvest(self):
        if self.IsAutoInvestment():
            self.Execute()


    def Invest(self):
        self.Execute()


    def SearchNotes(self):
        lists = g_lendingclub.NotesListd()
        
        for node in self.filterList:
            lists = node.Start(lists)

        for node in self.filterList:
            lists = node.Filter(lists)

        for node in self.filterList:
            lists = node.CalculatePercentiles(lists)

        if len(lists) == 0:
            return None

        lists = self.StartSumPercentiles(lists)

        ns = NotesSort(lists, self.logFile, self.monitorLog, self.fileLog)
        ns.SortOnPrimaryField(FilterBase.sumPercentile, True)
        logStream = LogNotes.LogNotes('{------  SORT RESULT  ------}', ns.notesFiltered, self.filterList).GetLogStream()
        if self.monitorLog:
            print(logStream)
        if self.fileLog:
            self.logFile.writelines(logStream)

        return ns.notesFiltered


    def Execute(self):
        lists = self.SearchNotes()
        if not lists == None:
            g_lendingclub.SubmitNotes(lists, self.filterList, self.logFile)



    def StartSumPercentiles(self, notes):
        if len(notes) == 0:
            return notes

        for node in self.filterList:
            notes = node.SumPercentiles(notes)
        return notes
