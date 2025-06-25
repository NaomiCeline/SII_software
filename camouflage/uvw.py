import numpy as np

from astropy.time import Time
from astropy.coordinates import Angle
from astropy import units

def rotx(x,y,z,a):
    cs,sn = np.cos(a), np.sin(a)
    return x, cs*y - sn*z, sn*y + cs*z

def roty(x,y,z,a):
    cs,sn = np.cos(a), np.sin(a)
    return cs*x + sn*z, y, -sn*x + cs*z

def enup(lat,lon):
    lat *= np.pi/180
    lon *= np.pi/180
    Re = 6378100
    x = Re*np.cos(lat)*np.cos(lon)
    y = Re*np.cos(lat)*np.sin(lon)
    z = Re*np.sin(lat)
    return x,y,z

def radians(lat,lon,ra,dec,jd):
    lat = Angle(lat).radian
    lon = Angle(lon).radian
    ra = Angle(ra).radian
    dec = Angle(dec).radian
    t = Time(jd,format='jd')
    lst = t.sidereal_time('mean',longitude=lon*units.radian)
    lst = lst.to(units.radian).value
    return lat,lon,ra,dec,lst

def baseline(lat1,lon1,lat2,lon2):
    Re = 6378100
    lat1 *= np.pi/180
    lon1 *= np.pi/180
    lat2 *= np.pi/180
    lon2 *= np.pi/180
    north = Re * (lat1-lat2)
    east = Re * np.cos(lat1) * (lon1-lon2)
    return east,north

def get_ha(latlon,radec,jd):
    lat,lon,ra,dec,sid = radians(latlon[0],latlon[1],radec[0],radec[1],jd)
    ha = sid - ra
    return ha

def ha2uvw(latlon,radec,bline,ha):
    lat,lon,ra,dec,sid = radians(latlon[0],latlon[1],radec[0],radec[1],0)
    dx,dy,dz = rotx(bline[0],bline[1],bline[2],-lat)
    dx,dy,dz = roty(dx,dy,dz,ha)
    u,v,w = rotx(dx,dy,dz,dec)
    return u,v,w

def get_uvw(latlon,radec,bline,jd):
    lat,lon,ra,dec,sid = radians(latlon[0],latlon[1],radec[0],radec[1],jd)
    ha = sid - ra
    dx,dy,dz = rotx(bline[0],bline[1],bline[2],-lat)
    dx,dy,dz = roty(dx,dy,dz,ha)
    u,v,w = rotx(dx,dy,dz,dec)
    return u,v,w

def funs(latlon,radec,bline):
    lat = Angle(latlon[0]).radian
    lon = Angle(latlon[1]).radian
    ra = Angle(radec[0]).radian
    dec = Angle(radec[1]).radian
    def ha(jd):
        t = Time(jd,format='jd')
        lst = t.sidereal_time('mean',longitude=lon*units.radian)
        lst = lst.to(units.radian).value
        h = lst - ra
        return h
    def uvw(ha):
        dx,dy,dz = rotx(bline[0],bline[1],bline[2],-lat)
        dx,dy,dz = roty(dx,dy,dz,ha)
        u,v,w = rotx(dx,dy,dz,dec)
        return u,v,w
    return ha, uvw

