import numpy as np 
import math 

def gausshermite_component(x, amp, sig, cen, order):

    if order == 0:
        return (amp/(np.sqrt(2*math.pi)*sig)) * np.exp(-(x-cen)**2 /(2*sig**2))
    if order == 1:
        return np.sqrt(2.0) * x * (amp/(np.sqrt(2*math.pi)*sig)) * np.exp(-(x-cen)**2 /(2*sig**2))
    if order == 2:    
        return (2.0*x*x - 1.0) / np.sqrt(2.0) * (amp/(np.sqrt(2*math.pi)*sig)) * np.exp(-(x-cen)**2 /(2*sig**2))
    if order == 3:   
        return x * (2.0*x*x - 3.0) / np.sqrt(3.0) * (amp/(np.sqrt(2*math.pi)*sig)) * np.exp(-(x-cen)**2 /(2*sig**2))
    if order == 4:   
        return (x*x*(4.0*x*x-12.0)+3.0) / (2.0*np.sqrt(6.0)) * (amp/(np.sqrt(2*math.pi)*sig)) * np.exp(-(x-cen)**2 /(2*sig**2))
    if order == 5:    
        return (x*(x*x*(4.0*x*x-20.0) + 15.0)) / (2.0*np.sqrt(15.0)) * (amp/(np.sqrt(2*math.pi)*sig)) * np.exp(-(x-cen)**2 /(2*sig**2))
    if order == 6:    
        return (x*x*(x*x*(8.0*x*x-60.0) + 90.0) - 15.0) / (12.0*np.sqrt(5.0)) * (amp/(np.sqrt(2*math.pi)*sig)) * np.exp(-(x-cen)**2 /(2*sig**2))

def gausshermite_0(x, amp0, sig0, cen0):

    h0 = gausshermite_component(x, amp0, sig0, cen0, 0)

    return h0 

def gausshermite_1(x, 
                   amp0, 
                   sig0, 
                   cen0, 
                   amp1, 
                   sig1, 
                   cen1):

    h0 = gausshermite_component(x, amp0, sig0, cen0, 0)
    h1 = gausshermite_component(x, amp1, sig1, cen1, 1)

    return h0 + h1

def gausshermite_2(x, 
                   amp0, 
                   sig0, 
                   cen0, 
                   amp1, 
                   sig1, 
                   cen1, 
                   amp2, 
                   sig2, 
                   cen2):

    h0 = gausshermite_component(x, amp0, sig0, cen0, 0)
    h1 = gausshermite_component(x, amp1, sig1, cen1, 1)
    h2 = gausshermite_component(x, amp2, sig2, cen2, 2)

    return h0 + h1 + h2 

def gausshermite_3(x, 
                   amp0, 
                   sig0, 
                   cen0, 
                   amp1, 
                   sig1, 
                   cen1, 
                   amp2, 
                   sig2, 
                   cen2, 
                   amp3, 
                   sig3, 
                   cen3):   

    h0 = gausshermite_component(x, amp0, sig0, cen0, 0)
    h1 = gausshermite_component(x, amp1, sig1, cen1, 1)
    h2 = gausshermite_component(x, amp2, sig2, cen2, 2)
    h3 = gausshermite_component(x, amp3, sig3, cen3, 3)

    return h0 + h1 + h2 + h3 

def gausshermite_4(x, 
                   amp0, 
                   sig0, 
                   cen0, 
                   amp1, 
                   sig1, 
                   cen1, 
                   amp2, 
                   sig2, 
                   cen2, 
                   amp3, 
                   sig3, 
                   cen3, 
                   amp4, 
                   sig4, 
                   cen4):

    h0 = gausshermite_component(x, amp0, sig0, cen0, 0)
    h1 = gausshermite_component(x, amp1, sig1, cen1, 1)
    h2 = gausshermite_component(x, amp2, sig2, cen2, 2)
    h3 = gausshermite_component(x, amp3, sig3, cen3, 3)
    h4 = gausshermite_component(x, amp4, sig4, cen4, 4)

    return h0 + h1 + h2 + h3 + h4 

def gausshermite_5(x, 
                   amp0, 
                   sig0, 
                   cen0, 
                   amp1, 
                   sig1, 
                   cen1, 
                   amp2, 
                   sig2, 
                   cen2, 
                   amp3, 
                   sig3, 
                   cen3, 
                   amp4, 
                   sig4, 
                   cen4, 
                   amp5, 
                   sig5, 
                   cen5):   

    h0 = gausshermite_component(x, amp0, sig0, cen0, 0)
    h1 = gausshermite_component(x, amp1, sig1, cen1, 1)
    h2 = gausshermite_component(x, amp2, sig2, cen2, 2)
    h3 = gausshermite_component(x, amp3, sig3, cen3, 3)
    h4 = gausshermite_component(x, amp4, sig4, cen4, 4)
    h5 = gausshermite_component(x, amp5, sig5, cen5, 5)

    return h0 + h1 + h2 + h3 + h4 + h5 

def gausshermite_6(x, 
                   amp0, 
                   sig0, 
                   cen0, 
                   amp1, 
                   sig1, 
                   cen1, 
                   amp2, 
                   sig2, 
                   cen2, 
                   amp3, 
                   sig3, 
                   cen3, 
                   amp4, 
                   sig4, 
                   cen4, 
                   amp5, 
                   sig5, 
                   cen5, 
                   amp6, 
                   sig6, 
                   cen6):

    h0 = gausshermite_component(x, amp0, sig0, cen0, 0)
    h1 = gausshermite_component(x, amp1, sig1, cen1, 1)
    h2 = gausshermite_component(x, amp2, sig2, cen2, 2)
    h3 = gausshermite_component(x, amp3, sig3, cen3, 3)
    h4 = gausshermite_component(x, amp4, sig4, cen4, 4)
    h5 = gausshermite_component(x, amp5, sig5, cen5, 5)
    h6 = gausshermite_component(x, amp6, sig6, cen6, 6)

    return h0 + h1 + h2 + h3 + h4 + h5 + h6