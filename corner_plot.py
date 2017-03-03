def corner_plot(chain, 
                axis_labels=None, 
                fname = None, 
                nbins=40, 
                figsize=(15.,15.), 
                filled=True, 
                gradient=False, 
                cmap="Blues", 
                fontsize=20, 
                tickfontsize=15, 
                nticks=4, 
                linewidth=1., 
                linecolor = 'k', 
                markercolor = 'k', 
                markersize = 10,
                wspace=0.5, 
                hspace=0.5 ):


    """
    Make a corner plot to show histograms / correlations
    """

   

    major_formatter = FuncFormatter(my_formatter)
        
    traces = chain.T

    if axis_labels is None:
        axis_labels = ['']*len(traces)

    num_samples = min([ len(trace) for trace in traces])
    n_traces = len(traces)

    #Set up the figure
    fig = plt.figure( num = None, figsize = figsize)

    fig.subplots_adjust(bottom=0.15)

    dim = 2*n_traces - 1

    gs = gridspec.GridSpec(dim+1,dim+1)
    gs.update(wspace=wspace,hspace=hspace)

    hist_2d_axes = {}

    #Create axes for 2D histograms
    for x_pos in xrange( n_traces - 1 ):
        for y_pos in range( n_traces - 1 - x_pos  ):
            x_var = x_pos
            y_var = n_traces - 1 - y_pos

            hist_2d_axes[(x_var, y_var)] = fig.add_subplot( \
                                           gs[ -1-(2*y_pos):-1-(2*y_pos), \
                                               2*x_pos:(2*x_pos+2) ] )
            hist_2d_axes[(x_var, y_var)].xaxis.set_major_formatter(major_formatter)
            hist_2d_axes[(x_var, y_var)].yaxis.set_major_formatter(major_formatter)

    #Create axes for 1D histograms
    hist_1d_axes = {}
    for var in xrange( n_traces -1 ):
        hist_1d_axes[var] = fig.add_subplot( gs[ (2*var):(2*var+2), 2*var:(2*var+2) ] )
        hist_1d_axes[var].xaxis.set_major_formatter(major_formatter)
        hist_1d_axes[var].yaxis.set_major_formatter(major_formatter)
    hist_1d_axes[n_traces-1] = fig.add_subplot( gs[-2:, -2:] )
    hist_1d_axes[n_traces-1].xaxis.set_major_formatter(major_formatter)
    hist_1d_axes[n_traces-1].yaxis.set_major_formatter(major_formatter)



    #Remove the ticks from the axes which don't need them
    for x_var in xrange( n_traces -1 ):
        for y_var in xrange( 1, n_traces - 1):
            try:
                hist_2d_axes[(x_var,y_var)].xaxis.set_visible(False)
            except KeyError:
                continue
    for var in xrange( n_traces - 1 ):
        hist_1d_axes[var].set_xticklabels([])
        hist_1d_axes[var].xaxis.set_major_locator(MaxNLocator(nticks))
        hist_1d_axes[var].yaxis.set_visible(False)

    for y_var in xrange( 1, n_traces ):
        for x_var in xrange( 1, n_traces - 1):
            try:
                hist_2d_axes[(x_var,y_var)].yaxis.set_visible(False)
            except KeyError:
                continue

    #Do the plotting
    #Firstly make the 1D histograms
    vals, walls = np.histogram(traces[-1][:num_samples], bins=nbins, normed = True)

    xplot = np.zeros( nbins*2 + 2 )
    yplot = np.zeros( nbins*2 + 2 )
    for i in xrange(1, nbins * 2 + 1 ):
        xplot[i] = walls[int((i-1)/2)]
        yplot[i] = vals[int((i-2)/2)]

    xplot[0] = walls[0]
    xplot[-1] = walls[-1]
    yplot[0] = yplot[1]
    yplot[-1] = yplot[-2]

    Cmap = colors.Colormap(cmap)
    cNorm = colors.Normalize(vmin=0.,vmax=1.)
    scalarMap = cm.ScalarMappable(norm=cNorm,cmap=cmap)
    cVal = scalarMap.to_rgba(0.65)

    #this one's special, so do it on it's own
    hist_1d_axes[n_traces - 1].plot(xplot, yplot, color = linecolor, lw=linewidth)
    if filled: hist_1d_axes[n_traces - 1].fill_between(xplot,yplot,color=cVal)
    hist_1d_axes[n_traces - 1].set_xlim( walls[0], walls[-1] )
    hist_1d_axes[n_traces - 1].set_xlabel(axis_labels[-1],fontsize=fontsize)
    hist_1d_axes[n_traces - 1].tick_params(labelsize=tickfontsize)
    hist_1d_axes[n_traces - 1].xaxis.set_major_locator(MaxNLocator(nticks))
    hist_1d_axes[n_traces - 1].yaxis.set_visible(False)
    plt.setp(hist_1d_axes[n_traces - 1].xaxis.get_majorticklabels(), rotation=45)
  
    #Now Make the 2D histograms
    for x_var in xrange( n_traces ):
        for y_var in xrange( n_traces):
            try:
                H, y_edges, x_edges = np.histogram2d(traces[y_var][:num_samples], 
                                                     traces[x_var][:num_samples],
                                                     bins=nbins)
                
                hist_2d_axes[(x_var,y_var)].scatter(traces[x_var][:num_samples],
                                                    traces[y_var][:num_samples],
                                                    edgecolor='None',
                                                    facecolor=cVal,
                                                    s=10)

                hist_2d_axes[(x_var,y_var)].set_xlim(x_edges.min(), x_edges.max())
                hist_2d_axes[(x_var,y_var)].set_ylim(y_edges.min(), y_edges.max())
              
            except KeyError:
                pass
        if x_var < n_traces - 1:
            vals, walls = np.histogram( traces[x_var][:num_samples], bins=nbins, normed = True )

            xplot = np.zeros( nbins*2 + 2 )
            yplot = np.zeros( nbins*2 + 2 )
            for i in xrange(1, nbins * 2 + 1 ):
                xplot[i] = walls[int((i-1)/2)]
                yplot[i] = vals[int((i-2)/2)]

            xplot[0] = walls[0]
            xplot[-1] = walls[-1]
            yplot[0] = yplot[1]
            yplot[-1] = yplot[-2]

            hist_1d_axes[x_var].plot(xplot, yplot, color = linecolor , lw=linewidth)
            if filled: hist_1d_axes[x_var].fill_between(xplot,yplot,color=cVal)
            hist_1d_axes[x_var].set_xlim( x_edges[0], x_edges[-1] )
           

    #Finally Add the Axis Labels
    for x_var in xrange(n_traces - 1):
        hist_2d_axes[(x_var, n_traces-1)].set_xlabel(axis_labels[x_var],fontsize=fontsize)
        hist_2d_axes[(x_var, n_traces-1)].tick_params(labelsize=tickfontsize)
        hist_2d_axes[(x_var, n_traces-1)].xaxis.set_major_locator(MaxNLocator(nticks))
        plt.setp(hist_2d_axes[(x_var, n_traces-1)].xaxis.get_majorticklabels(), rotation=45)
    for y_var in xrange(1, n_traces ):
        hist_2d_axes[(0,y_var)].set_ylabel(axis_labels[y_var],fontsize=fontsize)
        hist_2d_axes[(0,y_var)].tick_params(labelsize=tickfontsize)
        plt.setp(hist_2d_axes[(0,y_var)].yaxis.get_majorticklabels(), rotation=45)
        hist_2d_axes[(0,y_var)].yaxis.set_major_locator(MaxNLocator(nticks))

    hist_2d_axes[(1, 2)].xaxis.labelpad = 15
    hist_2d_axes[(0, 1)].yaxis.labelpad = 12

    if fname != None:
        if len(fname.split('.')) == 1:
            fname += '.pdf'
        plt.savefig(fname, transparent=True)

    return None