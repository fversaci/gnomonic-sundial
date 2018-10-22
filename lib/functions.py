#!/usr/bin/python3

from math import *

eps = 1e-9

def dsin(x) :
  y = radians(x)
  return(sin(y))

def dcos(x) :
  y = radians(x)
  return(cos(y))

def dtan(x) :
  y = radians(x)
  return(tan(y))

def adtan(x) :
  y = atan(x)
  return(degrees(y))

def adtan2(y, x) :
  if (abs(x)<eps):
    if ((x>0 and y>0) or (x<0 and y<0)) : return(90)
    return(-90)
  r = adtan(y/x)
  if (x>0) : return(r)
  if (r>0) : return(r - 180)
  return(r + 180)

def adcos(x) :
  y = acos(x)
  return(degrees(y))

def sunset(l, d) :
  tl = dtan(l)
  td = dtan(d)
  return(adcos(-tl*td))

def rot_lat(a, w, lat) :
  t = 90 - lat
  z = dcos(t+w)*dcos(a) + dcos(t)*dcos(w)*(1-dcos(a))
  return(90 - adcos(z))

def rot_lon(a, w, lon, lat) :
  # scale = 30
  t = 90 - lat
  x = dsin(t+w)*dcos(lon)*dcos(a) - dsin(lon)*dsin(w)*dsin(a) + dsin(t)*dcos(lon)*dcos(w)*(1-dcos(a))
  y = dsin(t+w)*dsin(lon)*dcos(a) + dcos(lon)*dsin(w)*dsin(a) + dsin(t)*dsin(lon)*dcos(w)*(1-dcos(a))
  if (abs(x)<eps and abs(y)<eps) : return(lon - 90)
  return(adtan2(y,x))

def pol_ang(a, w, lat) :
  g = adtan2(dtan(lat), dcos(a))
  t = dcos(lat)*dsin(-a)
  s = sqrt(1-t*t)*dcos(g-w)
  r = adtan2(t, s)
  return(r - 180)

def radius_lat(lat) :
  if (lat>0) : return(lat - 45)
  return(lat + 45)

