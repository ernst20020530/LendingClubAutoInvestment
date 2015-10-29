__author__ = 'bwang'


import requests
import json
import LogLine
import LogNote
import LogDateInfo

lendingClubID = '910072'

class bwLendingClub:

    headers = {'Authorization':{'Authorization':'c4JzxMD+2N2bqYGrAPWYyBAzi40='},'Content-Type':{'Content-Type':'application/json; charset=utf-8'}}
    urlAvailableCash = 'https://api.lendingclub.com/api/investor/v1/accounts/' + lendingClubID + '/availablecash'
    urlOwned = 'https://api.lendingclub.com/api/investor/v1/accounts/' + lendingClubID + '/'
    urlOwnedDetail = 'https://api.lendingclub.com/api/investor/v1/accounts/' + lendingClubID + '/detailednotes'
    urlListed = 'https://api.lendingclub.com/api/investor/v1/loans/listing'
    urlAddFunds = 'https://api.lendingclub.com/api/investor/v1/accounts/' + lendingClubID + '/funds/add'
    urlCreatePortfolio = 'https://api.lendingclub.com/api/investor/v1/accounts/' + lendingClubID + '/portfolios'
    urlSubmitOrder = 'https://api.lendingclub.com/api/investor/v1/accounts/' + lendingClubID + '/orders'
    payload = {'login_email': 'ernst20020530@gmail.com','login_password': 'maomao1QA2WS3ED'}
    showAll = {'showAll':'true'}
    investLimit = 25

    def __init__(self,id = 'ernst20020530@gmail.com',password = 'maomao1QA2WS3ED'):
        self.id = id
        self.password = password
        self.session = requests.Session()
        b = bwLendingClub.headers['Authorization']
        self.session.headers.update(bwLendingClub.headers['Authorization'])
        self.session.headers.update(bwLendingClub.headers['Content-Type'])

    def Summary(self):
        return  self.session.get(bwLendingClub.urlOwned + 'summary',data = bwLendingClub.payload).json()

    def NotesOwned(self):
        json_response = self.session.get(bwLendingClub.urlOwned + 'notes',data = bwLendingClub.payload).json()
        return json_response['myNotes']

    def NotesListd(self):
        json_response = self.session.get(bwLendingClub.urlListed,params = bwLendingClub.showAll).json()
        return json_response['loans']

    def NotesOwnedDetail(self):
        json_response = self.session.get(bwLendingClub.urlOwnedDetail,data = bwLendingClub.payload).json()
        return json_response['myNotes']

    def IsNotesOwned(self, noteId):
        notes = self.NotesOwned()
        for n in notes:
            if n['loanId'] == noteId:
                return True
        else:
            return False


    def TransferOnce(self, amount):
        x = {'transferFrequency':'LOAD_NOW','amount':amount}
        d = json.dumps(x)
        return self.session.post(bwLendingClub.urlAddFunds,data = d)

    def AvailableCash(self):
        return self.Summary()['availableCash']

    def AccruedInterest(self):
        return self.Summary()['accruedInterest']

    def OutstandingPrincipal(self):
        return self.Summary()['outstandingPrincipal']

    def ReceivedInterest(self):
        return self.Summary()['receivedInterest']

    def ReceivedPrincipal(self):
        return self.Summary()['receivedPrincipal']

    def SubmitNotes(self, notes, filterList, logFile):
        availableCash = self.AvailableCash()
        index = 0
        orders = []
        #if there is no more notes available, jump out of the loop
        while availableCash > self.investLimit and index < len(notes):
            n = notes[index]

            #we have owned this load
            if self.IsNotesOwned(n['id']):
                index += 1
                continue

            individual = {"loanId": n['id'],"requestedAmount":self.investLimit}
            orders.append(individual)

            availableCash -= self.investLimit

            x = {"aid":lendingClubID, "orders" : orders}
            self.session.post(bwLendingClub.urlSubmitOrder,data = json.dumps(x))
            logStream = LogNote.LogNote('{------  NOTES SUBMITTED  ------}', n, index, filterList).GetLogStream()
            #display submitted note on screen
            print(logStream)
            #log the submitted note on screen
            logFile.writelines(logStream)

            index += 1
        else:
            logStream = LogDateInfo.LogDateInfo('No notes submitted, Available Fund:' + str(availableCash)).GetLogStream()
            #display submitted note on screen
            print(logStream)
            #log the submitted note on screen
            logFile.writelines(logStream)
            return

        logStream = LogDateInfo.LogDateInfo('notes submitted, Available Fund:' + str(availableCash)).GetLogStream()
        #display submitted note on screen
        print(logStream)
        #log the submitted note on screen
        logFile.writelines(logStream)






