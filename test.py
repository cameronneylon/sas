from sas import *
import matplotlib.pyplot as plt

test = loadsasxml('xmltest.xml')

plot = SasPlot(test)

ranges = [[0,0.03],[0.11,5]]

test.make_mask(ranges)

test.apply_mask()
print test.masked.q

plt.plot(test.masked.q, test.masked.i, '-')
plt.draw()

raw_input('waiting')



