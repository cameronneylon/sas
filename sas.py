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


class ModelParameter:
    """Parameter class for model fits.

    See scipy.org cookbook entry on least squares fitting
    """

    def __init__(self, value):
         self.value = value
   
    def set(self, value):
         self.value = value

    def __call__(self):
         return self.value

def guinier(q):
    """Returns the intensities according to Guinier model for a sphere

    Takes a q vector and three parameters (I(0), Rg and background) and 
    returns calculated values of I for each value of Q. Requires a simple 
    list of q values as an argument. Relies on i0, Rg, and background having 
    been previously defined as members of the ModelParameter class.
    """

    assert len(q) != 0, 'Zero length q vector'

    return i0()*exp((-1/3)*(Rg()**2)*(q**2)) + background()


def fit(function, parameters, q, i):
    """Fit function adapted from the scipy cookbook.

    I don't entirely understand how this works and it is not yet fully 
    tested but it worked ok on a test rig so will put it here for the
    moment. Parameters are taken as a list of instances of the 
    ModelParameter class. Calling the function therefore looks like e.g.

    >>> fit(guinier, [i0, Rg, background], q_data, i_data)

    It throws a bunch of deprecation warnings but these look to be
    quite deep in the library so I'm not going to fuss about them for the 
    moment. 
    """

    def f(params):
        j = 0
        for p in parameters:
            p.set(params[j])
            j += 1
        return i - function(q)

    p = [param() for param in parameters]
    optimize.leastsq(f, p)


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
        test_data = SasData((arange(0,3,0.001)), (arange(4,1,-0.001)))

        # testing with pre-set parameter values


        test_guinier = []
        test_guinier = guinier(test_data.q)
        self.assertEqual(len(test_guinier), len(test_data))
        self.assertEqual(test_guinier[0], 7)
        self.assertEqual(test_guinier[-1], 2)


if __name__ == '__main__':
    i0 = ModelParameter(5)
    Rg = ModelParameter(50)
    background = ModelParameter(2)
    unittest.main()



	
        
    
    
