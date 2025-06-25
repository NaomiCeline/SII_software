from uvw import funs

latlon = ('31d57m30s','-111d35m48s') # Kitt Peak
radec = ('12h25m11.579s','-11d9m40.75s')   # Spica

pos = [ [135.48, -8.61, 12.23],
        [44.836, -49.601, 5.102],
        [29.335, 60.022, 10.636],
        [-35.885, 11.742, 6.417] ]

east = pos[1][0] - pos[0][0]
north = pos[1][1] - pos[0][1]

bline = (east,north,0)
print(bline)

ha,uvw = funs(latlon,radec,bline)

if __name__ == '__main__':

    import numpy as np
    import matplotlib.pyplot as pl
    
    jd0 = 2460781 - 180
    jd = jd0 + np.arange(12)/24
    u,v,w = uvw(ha(jd))

    ax = pl.gca()
    ax.invert_xaxis()
    ax.set_aspect('equal')
    #pl.plot(u,v,'.',color='black')
    pl.plot(u,v,'.',color='white')
    for i in range(len(jd)):
        pl.text(u[i],v[i],'%.2f' % (jd[i]-jd0),
                horizontalalignment='center', verticalalignment='center')
    pl.xlabel('$u$ in metres')
    pl.ylabel('$v$ in metres')
    pl.tight_layout()
    pl.show()

