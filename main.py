from fitting import *

# load some data
test_data = loadi22('A33001.DAT')

# convert 2d array to 1d
i_plot = test_data[:,1]
q_plot = test_data[:,0]

param_fit = least_sq_fit(test_data)
fit_i = guinier(q_plot, param_fit[0])


plt.plot(q_plot, i_plot, 'rD', q_plot, fit_i, 'k-')
plt.show()
