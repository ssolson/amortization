import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from amort import amoritization, loanNpv
from graphics import plotAmoritization

#===========================================================
# House
#===========================================================
# House loan
loanAmt=329657.27
# Standard Payments
house0 = amoritization(loan=loanAmt, APR=.03875, payment=1583.02)
houseNPV = loanNpv(loanAmt, 0.03875, house0)
import ipdb; ipdb.set_trace()
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

