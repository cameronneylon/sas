from numpy import *
import unittest
import scipy.optimize as opt

class SasData(object):
    """A data object for holding 1-d Q versus I SAS data.

    Class has a series of methods for initialising and
    doing basic operations on SAS data. The root class
    is very simple and only contains the Q and I lists
    providing simple addition, multiplication, length
    and string operations.
    """

    def __init__(self, q_vals, i_vals):
        """Initializing the SasData object.

        Just passes two lists to the initializing object which
        are then stored internally. Possibly an argument for 
        including the units of Q in the root object
        """

        assert type(q_vals) == list or type(q_vals) == ndarray
        assert type(i_vals) == list or type(i_vals) == ndarray
        assert len(q_vals) == len(i_vals), 'q and i not the same length'
        self.q = q_vals
        self.i = i_vals


    def __len__(self):
        return len(self.q)


    def __add__(self, other):
        """Test whether other is SasData or float/int and add together.

        The basic add operation covers two specific cases. The first is
        where two SasData objects are added together where the wish is
        for the intensities of both to be combined. The second cases is
        when adding (or more likely subtracting) a numeric value (float 
        or int) which is handled separately. Probably both of these could
        be written neater and faster.

        Inputs must required are a SasData object and either a SasData object or
        an int or float. Returns a new SasData object.
        """

        assert isinstance(self, SasData)
        assert (type(other) is int or type(other)
                is float or isinstance(other, SasData))

        # addition of two SasData objects
        if isinstance(other, SasData):
            assert len(self) == len(other), 'datasets not the same length'
	    assert self.q == other.q, 'q values not the same'

            # initialize a SasData object with zero for all intensities
	    out = SasData(self.q, ([0] * len(self)))
	    for j in range(len(self)):
                out.i[j] = self.i[j] + other.i[j]

	    return out

        # addition of a float or int to  SasData objects
        elif type(other) is int or type(other) is float:
            out = SasData(self.q, ([0]*len(self)))
	    for j in range(len(self)):
	        out.i[j] = self.i[j] + other

	    return out


    def __mul__(self, other):
        """Basic mutplication function for SasData objects.

        Requires a SasData object and an int or a float. Returns a new
        SasData object.
        """

        assert isinstance(self, SasData) 
        assert type(other) is int or type(other) is float
 
        # initialize a SasData object with zero for all intensities 
        out = SasData(self.q, (([0] * len(self)))) 
        for j in range(len(self)):
            out.i[j] = self.i[j] * other
	return out
#definition of the Guinier model for a sphere with a flat background
def guinier(q,param):
    """Function that returns a Guinier model

    The parameter set list should contain i0, Rg, and background in that
    order. There is currently no option to hold any parameter.
    """

    assert len(param) == 3, 'Guinier fit requires three parameters'
    assert len(q) != 0, 'No Q values to evaluate'
      
    return param[0]*exp((-1/3)*(param[1]**2)*(q**2)) + param[2]

#calculate the residuals for a fit
def guinier_residuals(param, i, q):

    err = i-guinier(q, param)
    return err

#Least squares fitting routine for Guinier
def fit_guinier(data):
    """Function for calling to get a Guinier fit to a dataset

    This currently takes a dataset and sets some plausible initial values
    for a Guinier fit before calling guinier_residuals using leastsq.
    """

    assert isinstance(data, SasData) 

    param_0 = [1.,1.,0.] # Set reasonable initial values for Guinier fit
           
    least_squares_fit = opt.leastsq(
            guinier_residuals, param_0, args=(data.i, data.q))

    return least_squares_fit

class TestSasData(unittest.TestCase):

    def setUp(self):
        self.zero_to_nine = range(10)
	self.test_string = 'a string'
	self.nine_to_zero = range(9,-1,-1)
	self.test_zero = [0]
	self.zero_to_twenty = range(20)
        self.eighteen_to_zero = range(18,-2,-2)
	self.thirteen_to_four = range(13,3,-1)
        self.test_floats = [(9.*0.25), 2., (7.*0.25), 1.5, 1.25, 1., 3.*0.25,
                            0.5, 0.25, 0.]

	self.test_data_ranges = SasData(self.zero_to_nine, self.nine_to_zero)
	self.test_data_zeros = SasData(self.test_zero, self.test_zero)

    def tearDown(self):
        self.test_data_ranges = SasData([],[])
        self.test_data_zeros = SasData([],[])
	test_add = SasData([],[])


    def test_init(self):
	self.assertEqual(self.test_data_ranges.q, self.zero_to_nine)
	self.assertEqual(self.test_data_ranges.i, self.nine_to_zero)

	self.assertRaises(
                AssertionError, SasData, self.test_string, self.test_zero)
        self.assertRaises(
                AssertionError, SasData, self.test_zero, self.zero_to_twenty)


    def test_len(self):        	
        self.assertTrue(len(self.test_data_ranges) == 10)

	self.assertTrue(len(self.test_data_zeros) == 1)

	test_data = SasData([],[])
	self.assertTrue(len(test_data) == 0)

    def test_add(self):    

        test_add = SasData(self.zero_to_nine, self.nine_to_zero)
	test_add = self.test_data_ranges + self.test_data_ranges
	self.assertEqual(self.eighteen_to_zero, test_add.i)
	self.assertEqual(self.zero_to_nine, test_add.q)

        test_add = SasData(self.zero_to_nine, self.nine_to_zero)
	test_add = self.test_data_ranges + 4
	self.assertEqual(self.thirteen_to_four, test_add.i)
	self.assertEqual(self.zero_to_nine, test_add.q)

	self.assertRaises(AssertionError,
            self.test_data_ranges.__add__, self.test_string)
        
    def test_mul(self):

        # test simple multiplication
        test_mul = self.test_data_ranges * 2
        self.assertEqual(self.eighteen_to_zero, test_mul.i)
        self.assertEqual(self.zero_to_nine, test_mul.q)

        # test multiplication by zero
        test_mul = self.test_data_ranges * 0
        self.assertEqual([0] * len(self.test_data_ranges), test_mul.i)
        self.assertEqual(self.zero_to_nine, test_mul.q)

        # test multiplication by a float
        test_mul = self.test_data_ranges * 0.25
        self.assertEqual(self.test_floats, test_mul.i)
        self.assertEqual(self.zero_to_nine, test_mul.q)


class TestAnalysis(unittest.TestCase):

    def test_guinier(self):
        test_data = SasData((arange(0,3,0.001)), 
                (arange(4,1,-0.001)))

        test_params = [5., 20., 2.]
        test_guinier = []

        # use guinier to make list to test
        test_guinier = guinier(test_data.q, test_params)

        # test that the lists are all the right length
        self.assertEqual(len(test_guinier), len(test_data))

        # test that guinier is returning the right numbers at extremes
        self.assertEqual(test_guinier[0], 7)
        self.assertEqual(test_guinier[-1], 2)

        self.assertRaises(AssertionError, guinier, test_data.q, [])
        self.assertRaises(AssertionError, guinier, [], test_params)

        # now test the residuals function
        test_zeros = [0] * 3000
        test_residuals = guinier_residuals(
                        test_params, test_guinier, test_data.q)
        self.assertEqual(test_residuals[25], test_zeros[25])

        test_residuals = []
        test_residuals = guinier_residuals(
                        test_params, test_zeros, test_data.q)
        self.assertEqual(test_residuals[46], (-1*(test_guinier[46])))



if __name__ == '__main__':
    unittest.main()



	
        
    
    
