from matplotlib.ticker import NullFormatter
import matplotlib.pyplot as plt

def scatter_hist(figsize=(6,4),
                 left=0.1, 
                 width=0.65,
                 bottom=0.1, 
                 height=0.65): 

    """
    Generates axes for use with scatter + hist plot 
    """

    # definitions for the axes
    bottom_h = left_h = left + width + 0.0
        
    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom_h, width, 0.2]
    rect_histy = [left_h, bottom, 0.2, height]
    
    # no labels
    nullfmt = NullFormatter() 
    
    fig = plt.figure(figsize=figsize)
    
    axScatter = plt.axes(rect_scatter)
    axHistx = plt.axes(rect_histx)
    axHisty = plt.axes(rect_histy)
    
    # no labels
    axHistx.xaxis.set_major_formatter(nullfmt)
    axHistx.yaxis.set_major_formatter(nullfmt)
    axHisty.xaxis.set_major_formatter(nullfmt)
    axHisty.yaxis.set_major_formatter(nullfmt)
    
    axHistx.set_xticks([])
    axHistx.set_yticks([])
    axHisty.set_xticks([])
    axHisty.set_yticks([])

    return fig, axScatter, axHistx, axHisty