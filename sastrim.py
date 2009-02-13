# sastrim
# routines for trimming and processing scattering curves

from numpy import *

def mask_data(data_to_mask, mask):
        """Take an input Q-I data array and filter out points defined by mask

        Takes a 2d Q-I array and generates a new array containing only
        the points defined by non-zero values in the array mask. Mask
        is a 1d array which is converted internally to a 2d array with
        both columns the same. The numpy routine extract is then used
        to generate a 2d array with the zero values in mask removed.
        """

    mask_2d = [mask[:], mask[:]]
    return extract(mask_2d, data_to_mask)

def generate_mask(data, mask_ranges)
        """"Generates a 1d mask of len(data) from values in mask_range

        Takes the values in mask_range which contains values in Q to 
        remove from the dataset in the form of a 2xn array. Iterates 
        along the data array determining whether the Q values lie 
        within the range(s) to be masked.
        """

    q_mask = data[:,0]
    mask = q_mask[:] # make a slice copy of q list because we will change it
    
    n = 0
    for a in len(q_mask):
        if q_mask[a] > mask_ranges[n,0] and q_mask[a] < mask_ranges[n,1]:
            mask[a] = 0
               
        if q_mask[a] => mask_ranges[n,1]:
            n = n + 1
            
            if n > (len(mask_ranges) - 1) break
            
            if q_mask[a] >mask_ranges[n,0] and q_mask[a] < mask_ranges[n,1]:    
                mask[a] = 0 
                
            else:
                 mask[a] = 1
                   
        else mask[a] = 1

    return mask


    
