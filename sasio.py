# sasio
# routines for loading specific data types

from numpy import loadtxt

def loadi22(file):        
    return loadtxt(file, skiprows=3)


    
