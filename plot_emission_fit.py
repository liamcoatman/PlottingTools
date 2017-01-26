"""
Plotting routines for emission line fits 
"""


def plot_spectra(name, line, ax, offset):

    from lmfit import Model

    cs = palettable.colorbrewer.qualitative.Set1_9.mpl_colors
    cs_light = palettable.colorbrewer.qualitative.Pastel1_9.mpl_colors

    df = pd.read_csv('/home/lc585/Dropbox/IoA/nirspec/tables/masterlist_liam.csv', index_col=0)  
    instr = df.ix[name, 'INSTR']

    import sys
    sys.path.insert(1, '/home/lc585/Dropbox/IoA/nirspec/python_code')
    
    if instr == 'FIRE': from fit_properties_fire import get_line_fit_props
    if instr == 'GNIRS': from fit_properties_gnirs import get_line_fit_props
    if instr == 'ISAAC': from fit_properties_isaac import get_line_fit_props
    if instr == 'LIRIS': from fit_properties_liris import get_line_fit_props
    if instr == 'NIRI': from fit_properties_niri import get_line_fit_props
    if instr == 'NIRSPEC': from fit_properties_nirspec import get_line_fit_props
    if instr == 'SOFI_JH': from fit_properties_sofi_jh import get_line_fit_props
    if instr == 'SOFI_LC': from fit_properties_sofi_lc import get_line_fit_props
    if instr == 'TRIPLE': from fit_properties_triple import get_line_fit_props
    if instr == 'TRIPLE_S15': from fit_properties_triple_shen15 import get_line_fit_props
    if instr == 'XSHOOT': from fit_properties_xshooter import get_line_fit_props
    if instr == 'SINF': from fit_properties_sinfoni import get_line_fit_props
    if instr == 'SINF_KK': from fit_properties_sinfoni_kurk import get_line_fit_props
    
    q = get_line_fit_props().all_quasars()
    p = q[df.ix[name, 'NUM']]

    if line == 'Ha': w0 = 6564.89*u.AA
    if line == 'Hb': w0 = 4862.721*u.AA
    if (line == 'CIV') | (line == 'CIV_XSHOOTER'): w0 = np.mean([1548.202,1550.774])*u.AA
    
    xs, step = np.linspace(-20000,
                            20000,
                            1000,
                           retstep=True)

    save_dir = os.path.join('/data/lc585/nearIR_spectra/linefits/', name, line)


    parfile = open(os.path.join(save_dir,'my_params.txt'), 'r')
    params = Parameters()
    params.load(parfile)
    parfile.close()

    wav_file = os.path.join(save_dir, 'wav.txt')
    parfile = open(wav_file, 'rb')
    wav = pickle.load(parfile)
    parfile.close()

    flx_file = os.path.join(save_dir, 'flx.txt')
    parfile = open(flx_file, 'rb')
    flx = pickle.load(parfile)
    parfile.close()

    err_file = os.path.join(save_dir, 'err.txt')
    parfile = open(err_file, 'rb')
    err = pickle.load(parfile)
    parfile.close()

    sd_file = os.path.join(save_dir, 'sd.txt')
    parfile = open(sd_file, 'rb')
    sd = pickle.load(parfile)
    parfile.close()

    vdat = wave2doppler(wav, w0)

    if (line == 'Hb') & (p.hb_model == 'Hb'):

        mod = GaussianModel(prefix='oiii_4959_n_')
    
        mod += GaussianModel(prefix='oiii_5007_n_')
    
        mod += GaussianModel(prefix='oiii_4959_b_')
    
        mod += GaussianModel(prefix='oiii_5007_b_')
    
        if p.hb_narrow is True: 
            mod += GaussianModel(prefix='hb_n_')  
    
        for i in range(p.hb_nGaussians):
    
            mod += GaussianModel(prefix='hb_b_{}_'.format(i))  

         
        g1 = GaussianModel()
        p1 = g1.make_params()

        p1['center'].value = params['oiii_5007_n_center'].value
        p1['sigma'].value = params['oiii_5007_n_sigma'].value
        p1['amplitude'].value = params['oiii_5007_n_amplitude'].value

        ax.plot(np.sort(vdat.value) - offset, 
                g1.eval(p1, x=np.sort(vdat.value)),
                c=cs_light[4],
                linestyle='-')

        g1 = GaussianModel()
        p1 = g1.make_params()

        p1['center'].value = params['oiii_4959_n_center'].value
        p1['sigma'].value = params['oiii_4959_n_sigma'].value
        p1['amplitude'].value = params['oiii_4959_n_amplitude'].value

        ax.plot(np.sort(vdat.value) - offset, 
                g1.eval(p1, x=np.sort(vdat.value)),
                c=cs_light[4],
                linestyle='-')        

        g1 = GaussianModel()
        p1 = g1.make_params()

        p1['center'].value = params['oiii_5007_b_center'].value
        p1['sigma'].value = params['oiii_5007_b_sigma'].value
        p1['amplitude'].value = params['oiii_5007_b_amplitude'].value

        ax.plot(np.sort(vdat.value) - offset, 
                g1.eval(p1, x=np.sort(vdat.value)),
                c=cs_light[4],
                linestyle='-')       

        g1 = GaussianModel()
        p1 = g1.make_params()

        p1['center'].value = params['oiii_4959_b_center'].value
        p1['sigma'].value = params['oiii_4959_b_sigma'].value
        p1['amplitude'].value = params['oiii_4959_b_amplitude'].value   

        ax.plot(np.sort(vdat.value) - offset, 
                g1.eval(p1, x=np.sort(vdat.value)),
                c=cs_light[4],
                linestyle='-')             

        for i in range(p.hb_nGaussians):
    
            g1 = GaussianModel()
            p1 = g1.make_params()
    
            p1['center'].value = params['hb_b_{}_center'.format(i)].value
            p1['sigma'].value = params['hb_b_{}_sigma'.format(i)].value
            p1['amplitude'].value = params['hb_b_{}_amplitude'.format(i)].value  
        
            ax.plot(np.sort(vdat.value) - offset, 
                    g1.eval(p1, x=np.sort(vdat.value)),
                    c=cs_light[4])  
    
        if p.hb_narrow is True: 
    
            g1 = GaussianModel()
            p1 = g1.make_params()
        
            p1['center'] = params['hb_n_center']
            p1['sigma'] = params['hb_n_sigma']
            p1['amplitude'] = params['hb_n_amplitude']   
        
            ax.plot(np.sort(vdat.value) - offset, 
                    g1.eval(p1, x=np.sort(vdat.value)),
                    c=cs_light[4],
                    linestyle='-')                    

    if (line == 'Ha') & (p.ha_model == 'Ha'):

        mod = GaussianModel(prefix='ha_n_')  
        mod += GaussianModel(prefix='nii_6548_n_')
        mod += GaussianModel(prefix='nii_6584_n_')
        mod += GaussianModel(prefix='sii_6717_n_')
        mod += GaussianModel(prefix='sii_6731_n_')

        for i in range(p.ha_nGaussians):
            mod += GaussianModel(prefix='ha_b_{}_'.format(i))  

        g1 = GaussianModel()
        p1 = g1.make_params()

        p1['center'].value = params['ha_n_center'].value
        p1['sigma'].value = params['ha_n_sigma'].value
        p1['amplitude'].value = params['ha_n_amplitude'].value

        ax.plot(np.sort(vdat.value) - offset, 
                g1.eval(p1, x=np.sort(vdat.value)),
                c=cs_light[4],
                linestyle='-')

        g1 = GaussianModel()
        p1 = g1.make_params()

        p1['center'].value = params['nii_6548_n_center'].value
        p1['sigma'].value = params['nii_6548_n_sigma'].value
        p1['amplitude'].value = params['nii_6548_n_amplitude'].value

        ax.plot(np.sort(vdat.value) - offset, 
                g1.eval(p1, x=np.sort(vdat.value)),
                c=cs_light[4],
                linestyle='-')

        g1 = GaussianModel()
        p1 = g1.make_params()

        p1['center'].value = params['nii_6584_n_center'].value
        p1['sigma'].value = params['nii_6584_n_sigma'].value
        p1['amplitude'].value = params['nii_6584_n_amplitude'].value

        ax.plot(np.sort(vdat.value) - offset, 
                g1.eval(p1, x=np.sort(vdat.value)),
                c=cs_light[4],
                linestyle='-')

        g1 = GaussianModel()
        p1 = g1.make_params()

        p1['center'].value = params['sii_6717_n_center'].value
        p1['sigma'].value = params['sii_6717_n_sigma'].value
        p1['amplitude'].value = params['sii_6717_n_amplitude'].value

        ax.plot(np.sort(vdat.value) - offset, 
                g1.eval(p1, x=np.sort(vdat.value)),
                c=cs_light[4],
                linestyle='-')      
                 
        g1 = GaussianModel()
        p1 = g1.make_params()

        p1['center'].value = params['sii_6731_n_center'].value
        p1['sigma'].value = params['sii_6731_n_sigma'].value
        p1['amplitude'].value = params['sii_6731_n_amplitude'].value

        ax.plot(np.sort(vdat.value) - offset, 
                g1.eval(p1, x=np.sort(vdat.value)),
                c=cs_light[4],
                linestyle='-') 

        for i in range(p.ha_nGaussians):

            g1 = GaussianModel()
            p1 = g1.make_params()

            p1['center'].value = params['ha_b_{}_center'.format(i)].value
            p1['sigma'].value = params['ha_b_{}_sigma'.format(i)].value
            p1['amplitude'].value = params['ha_b_{}_amplitude'.format(i)].value  
    
            ax.plot(np.sort(vdat.value) - offset, 
                    g1.eval(p1, x=np.sort(vdat.value)),
                    c=cs_light[4])  


    if ((line == 'CIV') | (line == 'CIV_XSHOOTER')) & (p.civ_model == 'GaussHermite'):

        param_names = []

        for i in range(p.civ_gh_order + 1):
            
            param_names.append('amp{}'.format(i))
            param_names.append('sig{}'.format(i))
            param_names.append('cen{}'.format(i))

        if p.civ_gh_order == 0: 
 
            mod = Model(gausshermite_0, independent_vars=['x'], param_names=param_names) 
    
        if p.civ_gh_order == 1: 
 
            mod = Model(gausshermite_1, independent_vars=['x'], param_names=param_names) 
     
        if p.civ_gh_order == 2: 
 
            mod = Model(gausshermite_2, independent_vars=['x'], param_names=param_names) 
     
        if p.civ_gh_order == 3: 
 
            mod = Model(gausshermite_3, independent_vars=['x'], param_names=param_names) 
     
        if p.civ_gh_order == 4: 
 
            mod = Model(gausshermite_4, independent_vars=['x'], param_names=param_names) 
     
        if p.civ_gh_order == 5: 
 
            mod = Model(gausshermite_5, independent_vars=['x'], param_names=param_names) 

        if p.civ_gh_order == 6: 
 
            mod = Model(gausshermite_6, independent_vars=['x'], param_names=param_names) 

    if (line == 'Ha') & (p.ha_model == 'MultiGauss'):

        mod = ConstantModel()
        
        for i in range(p.ha_nGaussians):
            gmod = GaussianModel(prefix='g{}_'.format(i))
            mod += gmod

        for i in range(p.ha_nGaussians):

            g1 = GaussianModel()
            p1 = g1.make_params()

            p1['center'].value = params['g{}_center'.format(i)].value
            p1['sigma'].value = params['g{}_sigma'.format(i)].value
            p1['amplitude'].value = params['g{}_amplitude'.format(i)].value  
    
            ax.plot(np.sort(vdat.value) - offset, 
                    g1.eval(p1, x=np.sort(vdat.value)),
                    c=cs_light[4])  


    vdat = vdat.value
    
    ax.plot(vdat - offset,
            flx,
            linestyle='-',
            color='grey',
            lw=1,
            alpha=1,
            zorder=5)

    ax.plot(xs - offset,
            mod.eval(params=params, x=xs/sd) ,
            color='black',
            lw=1,
            zorder=6)

    ax.axhline(0.0, color='black', linestyle=':')

    return None 

def plot_residual(name, line, ax):

    from lmfit import Model

    cs = palettable.colorbrewer.qualitative.Set1_9.mpl_colors

    df = pd.read_csv('/home/lc585/Dropbox/IoA/nirspec/tables/masterlist_liam.csv', index_col=0)  
    instr = df.ix[name, 'INSTR']

    import sys
    sys.path.insert(1, '/home/lc585/Dropbox/IoA/nirspec/python_code')
    
    if instr == 'FIRE': from fit_properties_fire import get_line_fit_props
    if instr == 'GNIRS': from fit_properties_gnirs import get_line_fit_props
    if instr == 'ISAAC': from fit_properties_isaac import get_line_fit_props
    if instr == 'LIRIS': from fit_properties_liris import get_line_fit_props
    if instr == 'NIRI': from fit_properties_niri import get_line_fit_props
    if instr == 'NIRSPEC': from fit_properties_nirspec import get_line_fit_props
    if instr == 'SOFI_JH': from fit_properties_sofi_jh import get_line_fit_props
    if instr == 'SOFI_LC': from fit_properties_sofi_lc import get_line_fit_props
    if instr == 'TRIPLE': from fit_properties_triple import get_line_fit_props
    if instr == 'TRIPLE_S15': from fit_properties_triple_shen15 import get_line_fit_props
    if instr == 'XSHOOT': from fit_properties_xshooter import get_line_fit_props
    if instr == 'SINF': from fit_properties_sinfoni import get_line_fit_props
    if instr == 'SINF_KK': from fit_properties_sinfoni_kurk import get_line_fit_props
    
    q = get_line_fit_props().all_quasars()
    p = q[df.ix[name, 'NUM']]

    if line == 'Ha': w0 = 6564.89*u.AA
    if line == 'Hb': w0 = 4862.721*u.AA
    if (line == 'CIV') | (line == 'CIV_XSHOOTER'): w0 = np.mean([1548.202,1550.774])*u.AA

    save_dir = os.path.join('/data/lc585/nearIR_spectra/linefits/', name, line)

    parfile = open(os.path.join(save_dir,'my_params.txt'), 'r')
    params = Parameters()
    params.load(parfile)
    parfile.close()

    wav_file = os.path.join(save_dir, 'wav.txt')
    parfile = open(wav_file, 'rb')
    wav = pickle.load(parfile)
    parfile.close()

    flx_file = os.path.join(save_dir, 'flx.txt')
    parfile = open(flx_file, 'rb')
    flx = pickle.load(parfile)
    parfile.close()

    err_file = os.path.join(save_dir, 'err.txt')
    parfile = open(err_file, 'rb')
    err = pickle.load(parfile)
    parfile.close()

    sd_file = os.path.join(save_dir, 'sd.txt')
    parfile = open(sd_file, 'rb')
    sd = pickle.load(parfile)
    parfile.close()
  
    vdat = wave2doppler(wav, w0)

    if (line == 'Hb') & (p.hb_model == 'Hb'):

        mod = GaussianModel(prefix='oiii_4959_n_')
    
        mod += GaussianModel(prefix='oiii_5007_n_')
    
        mod += GaussianModel(prefix='oiii_4959_b_')
    
        mod += GaussianModel(prefix='oiii_5007_b_')
    
        if p.hb_narrow is True: 
            mod += GaussianModel(prefix='hb_n_')  
    
        for i in range(p.hb_nGaussians):
            mod += GaussianModel(prefix='hb_b_{}_'.format(i))  
         
      
    if (line == 'Ha') & (p.ha_model == 'Ha'):

        mod = GaussianModel(prefix='ha_n_')  
        mod += GaussianModel(prefix='nii_6548_n_')
        mod += GaussianModel(prefix='nii_6584_n_')
        mod += GaussianModel(prefix='sii_6717_n_')
        mod += GaussianModel(prefix='sii_6731_n_')

        for i in range(p.ha_nGaussians):
            mod += GaussianModel(prefix='ha_b_{}_'.format(i))  

        
    if ((line == 'CIV') | (line == 'CIV_XSHOOTER')) & (p.civ_model == 'GaussHermite'):

        param_names = []

        for i in range(p.civ_gh_order + 1):
            
            param_names.append('amp{}'.format(i))
            param_names.append('sig{}'.format(i))
            param_names.append('cen{}'.format(i))

        if p.civ_gh_order == 0: 
 
            mod = Model(gausshermite_0, independent_vars=['x'], param_names=param_names) 
    
        if p.civ_gh_order == 1: 
 
            mod = Model(gausshermite_1, independent_vars=['x'], param_names=param_names) 
     
        if p.civ_gh_order == 2: 
 
            mod = Model(gausshermite_2, independent_vars=['x'], param_names=param_names) 
     
        if p.civ_gh_order == 3: 
 
            mod = Model(gausshermite_3, independent_vars=['x'], param_names=param_names) 
     
        if p.civ_gh_order == 4: 
 
            mod = Model(gausshermite_4, independent_vars=['x'], param_names=param_names) 
     
        if p.civ_gh_order == 5: 
 
            mod = Model(gausshermite_5, independent_vars=['x'], param_names=param_names) 

        if p.civ_gh_order == 6: 
 
            mod = Model(gausshermite_6, independent_vars=['x'], param_names=param_names) 

    if (line == 'Ha') & (p.ha_model == 'MultiGauss'):

        mod = ConstantModel()
        
        for i in range(p.ha_nGaussians):
            gmod = GaussianModel(prefix='g{}_'.format(i))
            mod += gmod

    ax.plot(vdat,
            (flx - mod.eval(params=params, x=vdat.value/sd)) / err,
            color=cs[8],
            lw=1)


    ax.axhline(0.0, color='black', linestyle=':')


    return None 