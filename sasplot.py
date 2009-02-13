# sasplot.py
# some simple plotting routines for standard sas plots

from scipy import *
from scipy.optimize import *
from scipy.io import read_array
import matplotlib.pyplot as plt

def plot_guinier(plot_data):

    q_plot = plot_data[:,0]
    i_plot = plot_data[:,1]

    q_plot_sq = q_plot**2
    log_i_plot = log(i_plot)

    plt.plot(q_plot_sq, log_i_plot, 'ro')
    plt.ylabel('log(I)')
    plt.xlabel('$Q^2$')
    plt.show()

def plot_loglog(plot_data):

    q_plot = plot_data[:,0]
    i_plot = plot_data[:,1]

    plt.loglog(q_plot, i_plot, 'ro')
    plt.ylabel('I')
    plt.xlabel('Q')
    plt.show()



