import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from amort import amoritization as amort


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

