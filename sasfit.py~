# sasfit
# routines and models for fitting scattering data

from scipy import *
from scipy.optimize import *
from scipy.io import read_array

#definitions for specific models   

#definition of the Guinier model for a sphere with a flat background
def guinier(q,param):
    if len(param) != 3:
        print "Wrong number of parameters for Guinier fit"
        return -1
        
    if len(q) == 0:
        print"No Q values to evaluate"
        return -1
    
    else:   
        return param[0]*exp((-1/3)*(param[1]**2)*(q**2)) + param[2]

#calculate the residuals for a fit
def guinier_residuals(param, i, q):

    err = i-guinier(q, param)
    return err

#Least squares fitting routine for Guinier
def fit_guinier(data):
    
    i=data[:,1] # Pass data from 2d array to two times 1d
    q=data[:,0]

    param_0 = array([1,1,0]) # Set reasonable initial values for Guinier fit
           
    least_squares_fit = leastsq(guinier_residuals, param_0, args=(i, q))
    return least_squares_fit

