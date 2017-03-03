import numpy as np
from scipy import stats 

def kde_contours(m1, 
                 m2, 
                 ax, 
                 kwargs_contour={},
                 kwargs_plot={},
                 color='black',
                 lims=None):

    """
    Plot contours using gaussian KDE
    and scatter points below threshold

    lims: (xmin, xmax, ymin, ymax) or None. 
    if None then use min and max of data  

    To do: Implement scikit-learn KDE
    """

    if lims is None:

        xmin = m1.min()
        xmax = m1.max()
        ymin = m2.min()
        ymax = m2.max()
    
    else:

        xmin, xmax, ymin, ymax = lims  

    X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    positions = np.vstack([X.ravel(), Y.ravel()])
    values = np.vstack([m1, m2])
    kernel = stats.gaussian_kde(values)
    Z = np.reshape(kernel(positions).T, X.shape)
    
    CS = ax.contour(X, 
                    Y, 
                    Z, 
                    colors=(color,),
                    **kwargs_contour)
    
    threshold = CS.levels[0]
    
    z = kernel(values)
    
    # mask points above density threshold
    x = np.ma.masked_where(z > threshold, m1)
    y = np.ma.masked_where(z > threshold, m2)
    
    # plot unmasked points
    ax.plot(x, 
            y, 
            markerfacecolor=color, 
            markeredgecolor='None', 
            linestyle='', 
            marker='o', 
            markersize=2,
            **kwargs_plot)

    return None 