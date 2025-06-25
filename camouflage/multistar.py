import numpy as np
from scipy.special import j1

def sig_multistar(u,v,diam,compan=None):
    ''' u,v (dimensionless) can be a meshgrid
        diam (also dimensionless) is angular diameter of one star
        compan[relative_brightness,diam,pos_x,pos_y)] are further stars
    '''
    rho = (u*u+v*v)**(1/2)
    arg = np.pi*rho*diam + 1e-10
    V =  2*j1(arg)/arg
    denom = 1
    if compan:
        V = (1+0j) * V
        for star in compan:
            b = star[0]
            sdiam = star[1]
            x,y = star[2:]
            arg = np.pi*rho*sdiam + 1e-10
            V += b * 2*j1(arg)/arg * np.exp(2j*np.pi*(u*x+v*y))
            denom += b
    sig = abs(V*V) / denom**2
    return sig

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    # Example, which is realistic if
    # angular distances are in nanoradians
    # u,v are in Giga-wavelengths
    R = 0.3
    l = np.linspace(-R,R,128)
    u,v = np.meshgrid(l,l)
    sig = sig_multistar(u,v,5,[(1,5,10,5)]) # binary of two similar stars
    sig /= np.max(sig)
    ssig = sig**(1/4)  # stretching to show second peak
    plt.contourf(u,v,ssig,cmap='magma')
    plt.gca().set_aspect(1)
    plt.show()
    
