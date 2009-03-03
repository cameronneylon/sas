from numpy import *
import sas

test = loadtxt('data.DAT', skiprows=3)

test_i = test[:,1]
test_q = test[:,0]

i0 = sas.ModelParameter(10)
Rg = sas.ModelParameter(5)
background = sas.ModelParameter(0)

params = [i0, Rg, background]

globalvars = globals()
print globalvars.has_key(i0)

def guinier_test(q): return i0() * exp((-1/3)*(Rg()**2)*(q**2)) + background()

sas.fit(guinier_test, [i0, Rg, background], test_q, test_i)
print i0(), Rg(), background()

sas.fit(sas.guinier, [i0, Rg, background], test_q, test_i)
print i0(), Rg(), background()
