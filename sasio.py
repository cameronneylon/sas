# sasio
# routines for loading specific data types

from scipy import *
from scipy.io import read_array

def loadi22(file):
    return read_array(file, lines=(3,-1))


    
