import matplotlib.pyplot as plt 
from plot_setup import figsize, set_plot_properties

def tls_scatter(trace):


    # Configure style of plot 
    set_plot_properties() 

    # Change color map 
    cs = palettable.colorbrewer.qualitative.Set1_3.mpl_colors

    fig, ax = plt.subplots(figsize=figsize(0.75, vscale=0.9))

    df = pd.read_csv('/home/lc585/Dropbox/IoA/nirspec/tables/masterlist_liam.csv', index_col=0)
    
    df = df[df.WARN_Ha == 0]
    df = df[df.WARN_Hb == 0]

    xi = df.FWHM_Broad_Ha.apply(np.log10)
    dxi = df.FWHM_Broad_Ha_Err / df.FWHM_Broad_Ha / np.log(10)  
    yi = df.FWHM_Broad_Hb.apply(np.log10)
    dyi = df.FWHM_Broad_Hb_Err / df.FWHM_Broad_Hb / np.log(10)  


    ax.errorbar(xi, yi, xerr=dxi, yerr=dyi, linestyle='', color='grey', alpha=0.4, zorder=2)
    ax.scatter(xi, yi, color=cs[1], s=8, zorder=3)

    logx = np.linspace(3.2, 4, 50)
    logy = np.log10(1.07) - 0.09 + 1.03*logx
    ax.plot(logx, logy, c='black', label='Green \& Ho', linestyle='--')

    #----------------Plot fit--------------------------------

    trace = np.load('/data/lc585/BHMassPaper2_MCMC_Traces/trace_ha_hb_relation.npy')
   
    m, b = trace[:2]
    # xfit = np.linspace(xdata.min(), xdata.max(), 10)
    yfit = b[:, None] + m[:, None] * (logx - 3.0) # 3 because divided x by 10**3 in model
    mu = yfit.mean(0)
    sig = 2 * yfit.std(0)

    ax.plot(logx, mu, 'k', linestyle='-', zorder=5, label='This paper')
    ax.fill_between(logx, mu - sig, mu + sig, color=palettable.colorbrewer.qualitative.Pastel1_6.mpl_colors[1], zorder=1)

    #--------------------------------------------------------

    plt.legend(loc='lower right', handlelength=2.5, frameon=False)

    ax.set_xlim(3.3, 4)
    ax.set_ylim(ax.get_xlim())

    ax.set_xlabel(r'log FWHM H$\alpha$ [km~$\rm{s}^{-1}$]')
    ax.set_ylabel(r'log FWHM H$\beta$ [km~$\rm{s}^{-1}$]')

    fig.tight_layout()

    fig.savefig('ha_hb_width_comparison.pdf')

    print np.mean(trace[0, :]), np.median(trace[0, :]), np.std(trace[0, :])
    print np.mean(trace[1, :]), np.median(trace[1, :]), np.std(trace[1, :]) 


    plt.show()

    return None 
