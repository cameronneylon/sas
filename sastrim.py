# sastrim
# routines for trimming and processing scattering curves
        
import numpy as np
import copy as cp

def mask_data(data_to_mask, mask):
    q = data_to_mask[:,0]
    i = data_to_mask[:,1]

    q_masked = np.extract(mask, q)
    i_masked = np.extract(mask, i)

    masked_data = np.column_stack((q_masked,i_masked))

    return masked_data


def generate_mask(data_to_mask, mask_ranges):
    q_mask = data_to_mask[:,0]
    mask = cp.deepcopy(q_mask) # copy the q list because we will change it    

    for i in range(0,len(mask)):
        for low, high in mask_ranges:
            if q_mask[i] >= low and q_mask[i] <= high:
                mask[i] = 0
                break
            else:
                mask[i] = 1 

    return mask




    
