"""
Set up plots for thesis 
"""

import numpy as np 
import matplotlib as mpl 

"""
Set up for thesis
"""

def figsize(hscale, 
            vscale=(np.sqrt(5.0)-1.0)/2.0,
            fig_width_pt = 336.0):
   

    """
    Get the fig_width_pt by inserting \the\textwidth into LaTeX document.

    hscale is fraction of text width you want.

    vscale is fraction of hscale (defaults to golden ratio)  
    """
   
    inches_per_pt = 1.0/72.27                       # Convert pt to inch
    fig_width = fig_width_pt*inches_per_pt*hscale   # width in inches
    fig_height = fig_width*vscale                   # height in inches
    fig_size = [fig_width, fig_height]

    return fig_size

def set_plot_properties():

    pars = {"axes.labelsize":10,
            "text.fontsize":10, 
            "legend.fontsize":10,             
            "xtick.labelsize":9, 
            "ytick.labelsize":9, 
            "figure.figsize":figsize(1.0),    
            "text.usetex":True,               
            "font.family":"serif",
            "font.serif":'Palatino'}

    mpl.rcParams.update(pars)

    return None 
