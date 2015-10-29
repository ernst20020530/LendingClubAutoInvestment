__author__ = 'bwang'

import requests
from bwLendingClub import bwLendingClub

Current = 'Current'
FullyPaid = 'Fully Paid'
ChargedOff = 'Charged Off'
Late31_120 = 'Late (31-120 days)'
InReview = 'In Review'


loanStatusCount = { Current:0,FullyPaid:0,ChargedOff : 0,Late31_120 : 0,InReview : 0}


g_lendingclub = bwLendingClub()

if __name__ == '__main__':

    response = g_lendingclub.NotesOwned()

    for r in response:
        if r['loanStatus'] == Current:
            loanStatusCount[Current] += 1
        elif r['loanStatus'] == FullyPaid:
            loanStatusCount[FullyPaid] += 1
        elif r['loanStatus'] == ChargedOff:
            loanStatusCount[ChargedOff] += 1
        elif r['loanStatus'] == Late31_120:
            loanStatusCount[Late31_120] += 1
        elif r['loanStatus'] == InReview:
            loanStatusCount[InReview] += 1

    print('Current:'+str(loanStatusCount[Current]))
    print('Fully Paid:'+str(loanStatusCount[FullyPaid]))
    print('Charged Off:'+str(loanStatusCount[ChargedOff]))
    print('Late (31-120 days):'+str(loanStatusCount[Late31_120]))
    print('In Review:'+str(loanStatusCount[InReview]))


    g_lendingclub.NotesListd()


