from scipy import optimize
from numpy import *
 
class Parameter:
    def __init__(self, value):
         self.value = value
   
    def set(self, value):
         self.value = value

    def __call__(self):
         return self.value


def fit(function, parameters, y, x = None):
    def f(params):
        i = 0
        for p in parameters:
            p.set(params[i])
            i += 1
        return y - function(x)

    if x is None: x = arange(y.shape[0])
    p = [param() for param in parameters]
    optimize.leastsq(f, p)

    for i in parameters:
        print parameters[i]

data = loadtxt('data.DAT', skiprows=3)
data_x = data[:,0]
data_y = data[:,1]

# giving initial parameters
mu = Parameter(7)
sigma = Parameter(3)
height = Parameter(5)
 
# define your function:
def f(x): return mu() * exp((-1/3)*(sigma()**2)*(x**2)) + height()

# fit! (given that data is an array with the data to fit)
fit(f, [mu, sigma, height], data_y, data_x)
