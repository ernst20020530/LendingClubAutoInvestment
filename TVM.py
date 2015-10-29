

import CashFlowCalcuator


error = -100000



def PMT(rate, n, pv, fv):
    global error
    pmtLO = 0
    pmtHI = max([abs(pv), abs(fv)])

    loopCount = 0
    while loopCount < 500:
        loopCount += 1
        pmtMiddle = (pmtLO + pmtHI) / float(2)
        
        cashFlow = [pv]
        for i in range(0, n - 1):
            cashFlow.append(pmtMiddle)
        cashFlow.append(pmtMiddle + fv)

        npv = CashFlowCalcuator.npv(rate, cashFlow)
        #print(str(pmtMiddle) + '\t' + str(pmtLO) + '\t' + str(pmtHI) + '\t' + str(npv))
        if abs(npv) < 0.001:
            return pmtMiddle
        elif npv < 0:
            pmtLO = pmtMiddle
        else:
            pmtHI = pmtMiddle

    return error

