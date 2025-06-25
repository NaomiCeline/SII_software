import numpy as np
from numpy import pi, cos, sin

def kepsol(e,M):
    E = M
    for i in range(4):
        f = E-e*np.sin(E)-M
        df = 1 - e*np.cos(E)
        E = E - f/df
    return E

def posvel(e,I,Omega,omega,mea):
    ''' Keplerian x,y '''
    psi = kepsol(e,mea)
    # then find x,y,vx,vy in orbital plane
    ec = (1-e*e)**.5
    x,y = cos(psi)-e, ec*sin(psi)
    denom = 1 - e*cos(psi)
    vx,vy = -sin(psi)/denom, ec*cos(psi)/denom
    # next rotate by omega
    f = omega*pi/180
    cs, sn = cos(f), sin(f)
    x,y = x*cs - y*sn, x*sn + y*cs
    vy = vx*sn + vy*cs
    # then inclination
    f = I*pi/180
    x,y = x, y*cos(f)
    vz = vy*sin(f)
    # and finally rotate by Omega
    f = (Omega+90)*pi/180   # North is up convention
    cs,sn = cos(f), sin(f)
    x,y = x*cs - y*sn, x*sn + y*cs
    vx,vy = vx*cs - vy*sn, vx*sn + vy*cs
    return x,y,vz  # East, North, los

    
