

import math


def payback_of_investment(investment, cashflows):
    """The payback period refers to the length of time required 
       for an investment to have its initial cost recovered.
       
       >>> payback_of_investment(200.0, [60.0, 60.0, 70.0, 90.0])
       3.1111111111111112
    """
    total, years, cumulative = 0.0, 0, []
    if not cashflows or (sum(cashflows) < investment):
        raise Exception("insufficient cashflows")
    for cashflow in cashflows:
        total += cashflow
        if total < investment:
            years += 1
        cumulative.append(total)
    A = years
    B = investment - cumulative[years-1]
    C = cumulative[years] - cumulative[years-1]
    return A + (B/C)


def payback(cashflows):
    """The payback period refers to the length of time required
       for an investment to have its initial cost recovered.
       
       (This version accepts a list of cashflows)
       
       >>> payback([-200.0, 60.0, 60.0, 70.0, 90.0])
       3.1111111111111112
    """
    investment, cashflows = cashflows[0], cashflows[1:]
    if investment < 0 : investment = -investment
    return payback_of_investment(investment, cashflows)


def npv(rate, cashflows):
    """The total present value of a time series of cash flows.
    
        >>> npv(0.1, [-100.0, 60.0, 60.0, 60.0])
        49.211119459053322
    """
    total = 0.0
    for i, cashflow in enumerate(cashflows):
        total += cashflow / (1 + rate)**i
    return total


def npv2(rate, cashflows):
    total = 0
    i = 0
    for cf in cashflows:
        total += cf / math.pow( 1+ rate, i)
        i += 1

    return total


def irr(cashflows, iterations=1000):
    """The IRR or Internal Rate of Return is the annualized effective 
       compounded return rate which can be earned on the invested 
       capital, i.e., the yield on the investment.
       
       >>> irr([-100.0, 60.0, 60.0, 60.0])
       0.36309653947517645

    """
    rate = 1.0
    investment = cashflows[0]
    for i in range(1, iterations+1):
        rate *= (1 - npv(rate, cashflows) / investment)
    return rate


def irr2(cashflows):

    irrValue = irr(cashflows)
    npvValue = abs(npv(irrValue,cashflows))
    pre = npvValue
    b = 0
    if irrValue == 0:
        while(irrValue > -1 and pre >= npvValue):
            irrValue -= 0.005
            pre = npvValue
            npvValue = abs(npv(irrValue,cashflows))
            a = 0

    return irrValue


def ConsolidateIRR(cashflows):
    irrValue = -0.99
    npvValue = abs(npv(irrValue,cashflows))
    pre = npvValue
    b = 0
    while(irrValue < 1 and pre >= npvValue):
        irrValue += 0.0001
        pre = npvValue
        npvValue = abs(npv(irrValue,cashflows))
        a = 0

    return irrValue




#def irr2(cashflows):

#    irrValue = float(-0.5)
#    npvValue = abs(npv(irrValue,cashflows))
#    pre = npvValue
#    while(irrValue < 1 and pre >= npvValue):
#        irrValue += 0.001
#        pre = npvValue
#        npvValue = abs(npv(irrValue,cashflows))
#        a = 0

#    return irrValue