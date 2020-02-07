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

#def seriesNPV(investment, cashflows, ):

def plotAmoritization(loan, fmt='.', label=None, title=None, ax=None):
    '''
    Plot of time vs interest and principal over life of the loan

    Parameters
    ----------
    loan: DataFrame
        AMortization table 
    Returns
    --------
    ax: figure
        plot of the amoritizaton schdule
    '''
    
    ax = _xy_plot(loan.index, loan.interest,  fmt=fmt ,label=f'Interest Paid {label}',ax=ax)
    ax = _xy_plot(loan.index, loan.principal, fmt=fmt, label=f'Principal Paid {label}', ax=ax)
    return ax

def _xy_plot(x, y, fmt='.', label=None, xlabel=None, ylabel=None, title=None, ax=None):
    """
    Base function to plot any x vs y data
    Parameters
    ----------
    x: array-like
        Data for the x axis of plot
    y: array-like
        Data for y axis of plot
        
    Returns
    -------
    ax : matplotlib.pyplot axes
    
    """
    if ax is None:
        plt.figure(figsize=(16,8))
        params = {'legend.fontsize': 'x-large',
                 'axes.labelsize': 'x-large',
                 'axes.titlesize':'x-large',
                 'xtick.labelsize':'x-large',
                 'ytick.labelsize':'x-large'}
        plt.rcParams.update(params)
        ax = plt.gca()
        
    ax.plot(x, y, fmt, label=label, markersize=7)
    
    ax.grid(b=True, which='both')
    
    if label:
        ax.legend()
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    plt.tight_layout()
    return ax
#===========================================================
# House
#===========================================================
# House loan
loanAmt=329657.27
# Standard Payments
house0 = amoritization(loan=loanAmt, APR=.03875, payment=1583.02)

ax = plotAmoritization(house0, fmt='k<')

# Extra 600 per month
house600 = amoritization(loan=loanAmt, APR=.03875, payment=1583.02+600)
ax = plotAmoritization(house600, label='+600', fmt='b.', ax=ax)
import ipdb; ipdb.set_trace()

#===========================================================
# Student
#===========================================================
# Standard Payments
#student0 = amoritization(loan=11026.96, APR=.0531, payment=200)
student0 = amoritization(loan=11026.96, APR=.03875, payment=200)
# Extra 600 per month
#student600 = amoritization(loan=11026.96, APR=.0531, payment=200+600)
student600 = amoritization(loan=11026.96, APR=.03875, payment=200+600)




#===========================================================
# Start extra 600 on House after 600 on student 
#===========================================================
# Get total periods until student ends
periodsOnStudent600 = len(student600)-1

#Clip house0 after student ends and calculate with 600 until after
house0B = house0[0:periodsOnStudent600+1].copy(deep=True)

# Get balance after student loan ends
remainingPrincipal = house0.principal[periodsOnStudent600]

# Calculate new house 600
house600B = amoritization(loan=remainingPrincipal, APR=.03875, payment=1583.02+600)


biggestLoanCost = house600.interestPaid.sum() + student0.interestPaid.sum()
biggestAPRCost  = student600.interestPaid.sum()+house0B.interestPaid.sum()+house600B.interestPaid.sum() 



# Interest saved house
print(f'Interest Saved House with $600: {house0.interestPaid.sum()-house600.interestPaid.sum()}')

# Interest saved student
print(f'Interest Saved Student $600: {student0.interestPaid.sum()-student600.interestPaid.sum()}')

print(f'biggestLoanCost: ${biggestLoanCost:.2f}')
print(f'biggestAPRCost : ${biggestAPRCost:.2f}')

import ipdb; ipdb.set_trace()

