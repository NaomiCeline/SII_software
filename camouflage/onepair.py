from config import uvw
from binorb import posvel
from multistar import sig_multistar

def signal(u,v,mea,e,aper,one,two,a,inc,lasc):
    lam = 442
    mas = 4.848 # nanorad                                                      
    a *= mas
    x,y,vz = posvel(e,inc,lasc,aper,mea)
    x,y = a*x,a*y
    diam1 = one * mas
    diam2 = two * mas
    relb = 1/6.5
    return sig_multistar(u/lam,v/lam,diam1,[(relb,diam2,x,y)])    

def model(h,mea,e,aper,one,two,a,inc,lasc):
    u,v,w = uvw(h)
    return signal(u,v,mea,e,aper,one,two,a,inc,lasc)

