import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Simple Amortization Table
def amoritization(loan, APR, payment, referenceDate=None):
    '''
    Calculates an amoritization shedule assuming monthly payments.
    Returns Pandas DataFrame of schdule.
    
    Parameters
    ----------
    loan: float
        Amount of loan
    APR: float
        APR in decimal
    payment: float
        the monthly payment
    referenceDate: string
        reference date for DateTime Index
    Returns
    -------
    amoritizationTable: DataFrame
        DataFrame with DateTime Index
    '''
    # Initialize values
    period = 0
    balance = loan
    # Initialize arrays to append results to 
    periods= np.array(period)
    interestPaid = np.zeros(1)
    principalPaid= np.zeros(1)
    principal= loan
    # Rate per month
    rper = APR/12
    # Iterate while the loan is not paid off 
    while balance > 0:
        # Increace Period
        period += 1
        # Calculate interest in the period
        intamt = rper * balance
        # Calculate payment towards principal
        paidamt = payment - intamt
        # Reduce the balance
        balance = balance - paidamt
        # Append periods, interest, payment, & balance to arrays
        periods       = np.append(periods      , period)
        interestPaid  = np.append(interestPaid , intamt)
        principalPaid = np.append(principalPaid, paidamt)
        principal     = np.append(principal    , balance)
        # Check if the balance is less than the payment
        if balance  < payment:
            payment = balance + (rper*balance) 
    # Create a DateTime of the results
    time = pd.date_range(start=pd.to_datetime('today').date(), 
                         periods=period+1, freq='M')
    # Dictionary of results 
    results = { 
                'time'      : time,
                'periods'   : periods,
                'interest'  : interestPaid,
                'principal' : principalPaid,
                'balance'   : principal
              }
    # Create DataFrame from Dictionary
    amoritizationTable = pd.DataFrame.from_records(results, index=['time'])
    return amoritizationTable


def loanNpv(loanAmt, APR, loan):
    '''
    Gives the NPV of the loan given loan amount and amoritization schedule
    Parameters
    ----------
    loanAmt: float
        Original loan amount
    loan: DataFrame
        AMoritizaion schedule 
    Returns
    -------
    NPV: Float
        Net present value
    '''
    # Calculate the cash flows (monthly payment) 
    pmt = -(loan.interest + loan.principal).values
    # Set time 0 to inflow of loanAmount
    pmt[0] = loanAmt
    # Calculate NPV
    NPV = np.npv(APR, pmt)
    return NPV

