from numpy import *
import unittest
import scipy.optimize as opt
import copy as cp
import matplotlib.pyplot as plt
from matplotlib import scale as mscale
from matplotlib import transforms as mtransforms
import matplotlib.figure as fig
import matplotlib.axes as maxes
from pylab import *

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
        self.masked = None


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


    #################################################
    #
    # SasTrim Routines for Trimming and Masking SasData
    #
    #################################################

    def make_mask(self, mask_ranges):
        """Generates a mask list of 0's and 1's to remove data in mask_ranges

        Takes a SasData object and creates a list with a 1 to 1 mapping with
        SasData.q containing only zeros and ones based on the q-values in
        mask_ranges. Mask_ranges takes the form of a list of length N of
        lists of length two containing data to exclude. May expand in the future
        to allow both positive and negative mask generation.
        """

    # need to make an assertion that mask ranges is a N x 2 set of lists
    # not immediately sure how to do this at the moment

    # make a copy of the q list because we are going to change it
        mask = cp.deepcopy(self.q)
        
        for j in range(0, len(mask)):

            #for each pair of values in mask_ranges
            for low, high in mask_ranges:
                # check whether q values are within mask_ranges
                if self.q[j] >= low and self.q[j] <= high:
                    mask[j] = 0
                    break
                else:
                    mask[j] = 1

        self.mask_list = mask

    def mask(self):
        """Applies a pre-calculated mask to a SasData object.

        Takes the pre-calculated mask from make_mask and creates a new
        SasData object with the masked data points (those corresponding
        to zeros in the mask) removed. The new object is then placed in
        self.masked. In principle this should allow nested masking operations.
        Whether this is a good idea remains to be seen.
        """

        assert type(self.mask_list) is list, 'Mask needs to be a list'
        assert self.mask_list != None, 'Mask appears not to have been setup'
        assert len(self.mask_list) != 0, 'Mask is zero length?'
        assert len(self.mask_list
                     ) == len(self.q), 'Mask not same length as data?'

        q_masked = extract(self.mask, self.q)
        i_masked = extract(self.mask, self.i)

        self.masked = SasData(q_masked, i_masked)
        return self.masked


##################################################
#
# Loaders for various SAS data formats to SasData objects
#
##################################################

def loadi22(file):
    """Loader for i22 two column data files.

    i22 files currently have two columns with three lines of text
    at the top. This just does a quick and dirty load of a the file
    into a SasData object. Currently setup to be called in the form
    data = loadi22('file')
    """

    data = np.loadtext(file, skiprows = 3)
    data_q = data[:,0]
    data_i = data[:,1]
    return SasData(data_q, data_i)
    

###################################################
#
# Definition of plotting routines
#
###################################################

class SasPlot(fig.Figure):
    """Class for generating and handling data plots.

    Uses the pylab module of matplotlib to generate and
    manipulate plots and provide some easy routines for
    modifying them, adding data, etc.
    """

    def __init__(self, data, format='ro'):
        """__init__ routine creates a plot with default features.

        """

        plt.plot(data.q, data.i, format)
        plt.ylabel('I')
        plt.xlabel('Q')
        # plt.title(name of data_to_plot) - how do I do this?
        plt.draw()

        # setup a list for holding the data for this plot
        # self.data.append(name of data_to_plot)

        # a place to hold the figure and plot number
        self.figure = plt.gcf()
        self.axes = plt.gca()
    

    def guinier_plot(self):
        """Routine to convert to a Guinier plot.

        Converts plot to show data on the coordinates of ln(I)
        versus Q^2. First we need to get the correct figure
        number and then change the axes. The routine sets the axes
        to base e log and a squared scale on y and x axes respectively.
        """

        self.axes.set_yscale('log', basey=e)
        self.axes.set_xscale('q_squared')
        plt.draw()


class SquaredScale(mscale.ScaleBase):
    """ScaleBase class for generating x axis of Guinier plots.

    Uses the built in scalebase to generate a transformed axis type
    called SquaredScale which can be called using ax.set_xscale('q_squared').
    Currently uses the default ticker and scale setup which will need
    to be changed in the future.

    The class requires the import of pylab (AutoLocator, ScalarFormatter
    NullLocator and NullFormatter) matplotlib.transforms (imported as
    mtransforms, required for the mtransforms.Transform class) and
    matplotlib.scale (imported as mscale, required for the mscale.ScaleBase
    class for inheritance of the scale).
    """

    name = 'q_squared'

    def __init__(self, axis, **kwargs):
        mscale.ScaleBase.__init__(self) # what does this do?


    def set_default_locators_and_formatters(self, axis):
        """
        Set the locators and formatters to reasonable defaults for
        scaling. Not really too sure what these do at the moment.
        """
        axis.set_major_locator(AutoLocator())
        axis.set_major_formatter(ScalarFormatter())
        axis.set_minor_locator(NullLocator())
        axis.set_minor_formatter(NullFormatter())

    class SquaredTransform(mtransforms.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def transform(self, a): return a**2

        def inverted(self):
            return SquaredScale.InvertedSquaredTransform()

    class InvertedSquaredTransform(mtransforms.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def transform(self, a): return a**0.5

        def inverted(self):
            return SquaredScale.SquaredTransform()

    def get_transform(self):
        """Set the actual transform for the axis coordinates.

        """
        return self.SquaredTransform()

mscale.register_scale(SquaredScale)

        

              

###################################################
#
# Definition of data fitting models
#
###################################################

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

########################################
#
# Unit tests
#
########################################

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

    def test_masking(self):
        """Tests for make_mask and mask."""

        test_mask_1 = [[0.,0.01],[0.05,0.1],[1,2.]]
        test_mask_2 = [[-2,-1],[10,20]]

        #self.assertRaises(make_mask(test_data_ranges, []))
        test_data = SasData((arange(0,3,0.001)), 
                (arange(4,1, -0.001)))

        test_data.make_mask(test_mask_1)
        self.assertTrue(test_data.mask_list != None)
        self.assertEqual(len(test_data.q), len(test_data.mask_list))
        self.assertEqual(test_data.mask_list[0], 0)
        print test_data.mask_list
        self.assertEqual(test_data.mask_list[-1], 1)

        test_data.make_mask(test_mask_2)
        self.assertTrue(test_data.mask_list != None)
        self.assertEqual(len(test_data.q), len(test_data.mask_list))
        self.assertEqual(test_data.mask_list[0], 1)
        self.assertEqual(test_data.mask_list[-1], 1)

        test_data.mask_list = None
        self.assertRaises(AssertionError, test_data.mask)
        test_data.mask_list = 'string'
        self.assertRaises(AssertionError, test_data.mask,)
        test_data.mask_list = []
        self.assertRaises(AssertionError, test_data.mask,)

        test_data.make_mask(test_mask_1)
        test_data.mask


class TestAnalysis(unittest.TestCase):

    def test_guinier(self):
        test_data = SasData((arange(0,3,0.001)), 
                (arange(4,1,-0.001)))

        i0 = 5.
        Rg= 20.
        background = 2.
        test_params = [i0, Rg, background]
        test_guinier = []

        # use guinier to make list to test
        test_guinier = guinier(test_data.q, test_params)

        # test that the lists are all the right length
        self.assertEqual(len(test_guinier), len(test_data))

        # test that guinier is returning the right numbers at extremes
        self.assertEqual(test_guinier[0], (i0+background))
        self.assertEqual(test_guinier[-1], background)

        self.assertRaises(AssertionError, guinier, test_data.q, [])
        self.assertRaises(AssertionError, guinier, [], test_params)

        # now test the residuals function
        test_zeros = [0] * 3000
        test_residuals = guinier_residuals(
                        test_params, test_guinier, test_data.q)
        self.assertTrue(allclose(test_residuals, test_zeros))

        test_residuals = []
        test_residuals = guinier_residuals(
                        test_params, test_zeros, test_data.q)
        self.assertTrue(allclose(test_residuals, (-(test_guinier))))

        # testing the fitting function to some faked data
        test_fit = SasData(test_data.q, test_guinier)

        test_outs = fit_guinier(test_fit)
        self.assertEqual(test_outs[0][0],i0)
        self.assertEqual(test_outs[0][1],Rg)
        self.assertEqual(test_outs[0][2], background)



if __name__ == '__main__':
    unittest.main()



	
        
    
    
