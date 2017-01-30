"""
Set up plot with correct options for publication in journal 
"""

import numpy as np 
import matplotlib as mpl 

"""
Set up for a MNRAS paper
"""

def figsize(hscale, 
            vscale=(np.sqrt(5.0)-1.0)/2.0,
            fig_width_pt = 504.0):
   

    """
    Get the fig_width_pt by inserting \the\textwidth into LaTeX document.

    hscale is fraction of text width you want.

    vscale is fraction of hscale (defaults to golden ratio)  
    """
   
    inches_per_pt = 1.0/72.27                       # Convert pt to inch
    fig_width = fig_width_pt*inches_per_pt*hscale   # width in inches
    fig_height = fig_width*vscale                   # height in inches
    fig_size = [fig_width,fig_height]

    return fig_size

def set_plot_properties():

    pgf_with_latex = {                       # setup matplotlib to use latex for output
        "pgf.texsystem": "pdflatex",         # change this if using xetex or lautex
        "text.usetex": True,                 # use LaTeX to write all text
        "font.family": "serif", 
        "font.serif": [],                    # blank entries should cause plots to inherit fonts from the document
        "font.sans-serif": [], 
        "font.monospace": [], 
        "axes.labelsize": 11,                # LaTeX default is 10pt font.
        "text.fontsize": 11, 
        "legend.fontsize": 10,               # Make the legend/label fonts a little smaller
        "xtick.labelsize": 10, 
        "ytick.labelsize": 10, 
        "figure.figsize": figsize(0.9),      # default fig size of 0.9 textwidth
        "pgf.preamble": [ 
            r"\usepackage[utf8x]{inputenc}", # use utf8 fonts
            r"\usepackage[T1]{fontenc}",     # plots will be generated using this preamble
            ]
        }
        
    mpl.rcParams.update(pgf_with_latex)

    

