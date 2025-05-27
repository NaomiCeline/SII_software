import matplotlib.pyplot as pl
import numpy as np
import csv

from utils import reel, colorof

pl.rcParams.update({'font.size': 18})
pl.style.use('dark_background')

def setup(a,b,c,d,fname='limits.txt'):
    global fig,bbox
    xmin,xmax,ymin,ymax = a,b,c,d
    wd = 9
    ht = np.log(ymax/ymin)/np.log(xmax/xmin) * wd
    fig, ax = pl.subplots(figsize=(wd, ht))
    pl.xscale('log')
    pl.yscale('log')
    pl.ylim(ymin,ymax)
    pl.xlim(xmin,xmax)
    pl.gca().set_aspect('equal')
    pl.ylabel('Distance (pc)')
    pl.xlabel('Size ($R_\\odot$)')
    bbox = ax.get_position()

def nopic(s,x,y):
    pl.text(x,y,s,horizontalalignment='center',verticalalignment='center')
    
mas = 4.8e-9
dsol = 4.6
pc = 1e8

xmin = 3e-2
xmax = 6e3
ymin = 0.5e8
ymax = 1e12

setup(xmin/dsol,xmax/dsol,ymin/pc,ymax/pc)

y = np.array((ymin,ymax*1000)) / pc
ylo = 1e-6*y
tcol = "#bcd4d6"
tcol = 'turquoise'

x = y * pc/dsol * 1e-7
pl.fill_between(x, y1=ylo, y2=y, color="gray", alpha=0.3)
pl.text(x[-1]/45000,y[-1]/30000, "JWST", rotation=45, color=tcol)

x = y * pc/dsol * 4e-9
pl.fill_between(x, y1=ylo, y2=y, color="gray", alpha=0.3)
pl.text(x[-1]/51000,y[-1]/34000, "VERITAS/MAGIC/HESS", rotation=45, color=tcol)

x = y * pc/dsol * 1e-9
pl.fill_between(x, y1=ylo, y2=y, color="gray", alpha=0.3)
pl.text(x[-1]/6000,y[-1]/4000, "CHARA", rotation=45, color=tcol)

x = y * pc/dsol * 2e-10
pl.fill_between(x, y1=ylo, y2=y, color="gray", alpha=0.3)
pl.text(x[-1]/6000,y[-1]/4000, "CTAO-S", rotation=45, color=tcol)


def star(s):
    name,M,R,T,g,dis,dx,dy = reel(s)
    x,y = 2*R,dis
    pl.plot(x/dsol,y/pc,'o',color=colorof(T))
    nopic(name,x*dx/dsol,y*dy/pc)
    
pl.rcParams.update({'font.size': 14})

fil = open('starsizes.txt')
while True:
    s = fil.readline()
    if not s:
        break
    star(s)
    

with open('filtered_stars.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    all = list(reader)
ixdist = all[0].index('Distance')
ixtemp = all[0].index('Temp')
ixU = all[0].index('Diameter_U')
ixB = all[0].index('Diameter_B')
ixV = all[0].index('Diameter_V')
for s in all[1:]:
    a,b,c = s[ixU],s[ixB],s[ixV]
    if len(a)==0 or len(b)==0 or len(c)==0:
        continue
    diams = float(a),float(b),float(c)
    diam = np.mean(diams)
    sigdiam = np.std(diams)
    if sigdiam < 0.5*diam and diam < 0.2:
        dist = float(s[ixdist])
        diam *= mas * dist * pc / dsol
        T = float(s[ixtemp])
        pl.plot(diam,dist,'o',color=colorof(T),alpha=0.5)
    

pl.savefig('si-resol.png')
pl.show()
