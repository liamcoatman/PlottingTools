"""
Make scatter plot with contours in regions of high point density, and 1D histograms along the axes. 
We use a Gausssian Kernel Density estimator, which is slow for large numbers of points
"""

from astropy.table import Table
from scipy import stats 
import palettable
import matplotlib.pyplot as plt 
import numpy as np
from plot_setup import figsize, set_plot_properties
from matplotlib.ticker import NullFormatter

# configure style of plot 
set_plot_properties() 

# get color map 
cs = palettable.colorbrewer.qualitative.Set1_9.mpl_colors 

# definitions for the axes
left, width = 0.1, 0.65
bottom, height = 0.1, 0.65
bottom_h = left_h = left + width + 0.0

rect_scatter = [left, bottom, width, height]
rect_histx = [left, bottom_h, width, 0.2]
rect_histy = [left_h, bottom, 0.2, height]

fig = plt.figure(figsize=figsize(0.8, vscale=1.0))

axScatter = plt.axes(rect_scatter)
axHistx = plt.axes(rect_histx)
axHisty = plt.axes(rect_histy)

# no labels
nullfmt = NullFormatter() 
axHistx.xaxis.set_major_formatter(nullfmt)
axHistx.yaxis.set_major_formatter(nullfmt)
axHisty.xaxis.set_major_formatter(nullfmt)
axHisty.yaxis.set_major_formatter(nullfmt)

axHistx.set_xticks([])
axHistx.set_yticks([])
axHisty.set_xticks([])
axHisty.set_yticks([])

# Shen et al. (2011) SDSS catalogue 
t = Table.read('luminosity_z.fits')
t = t[t['LOGLBOL'] > 0.0]
t = t[t['Z_HW'] > 1.0]

m1, m2 = t['Z_HW'], t['LOGLBOL'] 

xmin = 1.0
xmax = 5.0
ymin = 44.0
ymax = 48.0

X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
positions = np.vstack([X.ravel(), Y.ravel()])
values = np.vstack([m1, m2])

kernel = stats.gaussian_kde(values)
  
Z = np.reshape(kernel(positions).T, X.shape)

CS = axScatter.contour(X, 
                       Y, 
                       Z, 
                       colors=[cs[-1]], 
                       levels=[0.02, 0.05, 0.13, 0.2, 0.4, 0.8, 1.2])

threshold = 0.02

z = kernel(values)

# mask points above density threshold
x = np.ma.masked_where(z > threshold, m1)
y = np.ma.masked_where(z > threshold, m2)

# plot unmasked points
axScatter.plot(x, 
               y, 
               markerfacecolor=cs[-1], 
               markeredgecolor='None', 
               linestyle='', 
               marker='o', 
               markersize=2, 
               label='SDSS DR7')

axScatter.set_xlabel(r'Redshift $z$')
axScatter.set_ylabel(r'log $L_{\mathrm{Bol}}$ [erg/s]')

legend = axScatter.legend(frameon=True, 
                          scatterpoints=1, 
                          numpoints=1, 
                          loc='lower right') 

axHistx.hist(m1, 
             bins=np.arange(1, 5.0, 0.25), 
             facecolor=cs[-1], 
             edgecolor='None', 
             alpha=0.4, 
             normed=True)

axHisty.hist(m2, 
             bins=np.arange(44, 49, 0.25), 
             facecolor=cs[-1], 
             edgecolor='None', 
             orientation='horizontal', 
             alpha=0.4, 
             normed=True)

axScatter.set_xlim(1.25, 4.5)
axScatter.set_ylim(45, 48.5)

axHistx.set_xlim(axScatter.get_xlim())
axHisty.set_ylim(axScatter.get_ylim())

axHistx.set_ylim(0, 1.5)
axHisty.set_xlim(0, 1.2)

plt.show() 
