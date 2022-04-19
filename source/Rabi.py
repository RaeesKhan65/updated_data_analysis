import numpy as np
from scipy.optimize import curve_fit




def rabifunc(x, a1,a2,a3,a4,a5):
    return a1 + a2 * np.cos(2*np.pi*x/a3 + a4) * np.exp(-a5*x)

def fitrabi(x1,y1,yerr,pguess):
    """ this function takes in data and fits it to a rabi function and then returns"""

    popt, pcov = curve_fit(rabifunc, x1, y1, sigma=yerr, p0=pguess,maxfev=10000)

    return popt,np.sqrt(np.diag(pcov))

def my_fitfunc(x, a, b):
    return a * x + b

def renorm(content,rabiguess):
    xdata, ydata, yerr = content
    popt, perr = fitrabi(xdata,ydata,yerr,rabiguess)
    bkgd = popt[0]
    contrast = popt[1]
    renormdat = 0.5+(ydata - bkgd)/(2*contrast)
    renormerr = yerr/(2*contrast)
    return xdata,ydata,renormdat,renormerr,popt,perr,yerr

def process_rabi(content):
    tempsig,tempref,numavgs,timestart,timestep = content

    tempsig = np.array_split(tempsig, numavgs)
    tempref = np.array_split(tempref, numavgs)

    #average along the rows
    signal = np.average(tempsig,axis=0)
    reference = np.average(tempref,axis=0)
    meanref = np.mean(reference)

    #calculate errors in signal and reference and then the x and y data
    sigerr=np.sqrt(signal)
    referr = np.sqrt(reference)
    xdata = np.linspace(timestart,timestep*len(signal),len(signal))
    ydata = (signal - reference)/meanref

    #error bar calculation is not perfect yet, error in meanref needs to
    #be taken into account
    errb = np.sqrt(sigerr**2 + referr**2)/meanref/np.sqrt(numavgs)

    return xdata,ydata,errb

