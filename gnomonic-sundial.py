#!/usr/bin/python3

# Let r be the distance on the paper between (clon, clat) and (clon, lat+45)
# (drawn as a dashed, red line)
# let g = r / sin(clat)
# r is the length of a vertical gnomon standing at (clon, clat)
# g is the length of a polar gnomon, fixed at (0, 90) or (0, -90)
# see README.md for more info
# released under GNU GPLv3, see COPYING file

import subprocess
from datetime import date
from lib.functions import *
import configparser

tilt = 23.437 # earth's tilt angle, constant

config = configparser.ConfigParser()
config.read('gnomonic-sundial.ini')
conf = config['sundial']

lon = conf.getfloat('lon')
lat = conf.getfloat('lat')
map_range = conf.getfloat('map_range')
lemn_merid = conf.getfloat('lemn_merid')
filename = "/tmp/gnomonic-sundial.ps"
wall_incl = conf.getfloat('wall_incl')
wall_decl = conf.getfloat('wall_decl')
paper_size = conf['paper_size']
image_size = conf.getfloat('image_size')
dates = conf['starred_dates'].split(',')
starred_dates = map(lambda x : map(lambda y : int(y), x.split('/')),
                    dates)

clon = rot_lon(wall_decl, wall_incl, lon, lat)
clat = rot_lat(wall_decl, wall_incl, lat)
pol_ang = pol_ang(wall_decl, wall_incl, lat)

def open_file(outfile) :
  return(open(outfile, "w"))

outfile = open_file(filename)

def close_file(outfile) :
  outfile.close

def clear_variables() :
  subprocess.run(["gmt", "clear", "conf"], stderr = subprocess.DEVNULL)
  subprocess.run(["gmt", "clear", "history"], stderr = subprocess.DEVNULL)

def set_size(paper_size) :
  subprocess.run(["gmt", "set", "PS_MEDIA", paper_size])
  
def draw_basemap(clon, clat, map_range, image_size, pol_ang) :
  print("Center of the map: LON:{} LAT:{}".format(clon, clat))
  subprocess.run(["gmt", "psbasemap", "-P", "-Rg",
		  "-JF{}/{}/{}/{}c".format(clon, clat, map_range, image_size),
		  "-p{}+w{}/{}".format(pol_ang, clon, clat),
		  "-Bg15/", "-X1.5c", "-K"], stdout = outfile)
  subprocess.run(["gmt", "pscoast", "-R", "-J", "-B", "-Di",
                  "-Glightgray", "-N1/0.25p,-", "-W1/", "-O", "-K"], stdout = outfile)
  
def draw_parallels(tilt) :
  common_pars = ["gmt", "psxy", "-R", "-J", "-Ap", "-L", "-O", "-K"]
  subprocess.run(common_pars,
                 input = "0 0\n120 0\n240 0",
                 encoding='ascii',
                 stdout = outfile)
  subprocess.run(common_pars,
                 input = "0 {0}\n120 {0}\n240 {0}".format(tilt),
                 encoding='ascii',
                 stdout = outfile)
  subprocess.run(common_pars,
                 input = "0 {0}\n120 {0}\n240 {0}".format(-tilt),
                 encoding='ascii',
                 stdout = outfile)


def draw_analemma(lemn_merid, starred_dates) :
  # draw analemma
  time_shift = list(map(lambda x : float(x) + lemn_merid,
                        open("data/sun-time-shift.txt")))
  declination = list(map(float, open("data/sun-declination.txt")))
  analemma =  ['{} {}'.format(*i) for i in zip(time_shift, declination)]
  subprocess.run(["gmt", "psxy", "-R", "-L", "-J", "-O", "-K", "-W1,red"],
                 input = "\n".join(analemma),
                 encoding='ascii',
                 stdout = outfile)
  # add stars
  def day_of_year(day, month) :
    delta = date(2019, month, day) - date(2019, 1, 1)
    return delta.days
  def lon_lat(day_month) :
    (day, month) = day_month
    numday = day_of_year(day, month)
    return(analemma[numday])
  def star_date(ll) :
    subprocess.run(["gmt", "psxy", "-R", "-J", "-O", "-K", "-Sa.2", "-Gred"],
                   input = "{}".format(ll),
                   encoding='ascii',
                   stdout = outfile)
  for ll in map(lon_lat, starred_dates) :
    star_date(ll)

def draw_italic_hours(lon, lat) :
    da = sunset(lat, tilt)
    db = sunset(lat, -tilt)
    for d in range(0, 90 + 1, 15) :
      line = ("{} {}\n{} {}".format(d + lon - da, tilt, d + lon - db, -tilt))
      subprocess.run(["gmt", "psxy", "-R", "-J", "-O", "-K", "-W1,green,-"],
                     input = line,
                     encoding='ascii',
                     stdout = outfile)

def draw_babylonian_hours(lon, lat) :
    da = sunset(lat, tilt)
    db = sunset(lat, -tilt)
    for d in range(0, -(90 + 1), -15) :
      line = ("{} {}\n{} {}".format(d + lon + da, tilt, d + lon + db, -tilt))
      subprocess.run(["gmt", "psxy", "-R", "-J", "-O", "-K", "-W1,blue,-"],
                     input = line,
                     encoding='ascii',
                     stdout = outfile)

def mark_points(clon, clat, lon, lat) :
  radius=radius_lat(clat)
  common_pars = ["gmt", "psxy", "-R", "-J", "-O", "-K"]
  subprocess.run(common_pars + ["-Sx.2", "-Wred"],
                 input = "{} {}".format(clon, clat),
                 encoding='ascii',
                 stdout = outfile)
  subprocess.run(common_pars + ["-Sx.2", "-Wred"],
                 input = "{} {}".format(lon, lat),
                 encoding='ascii',
                 stdout = outfile)
  subprocess.run(common_pars + ["-S+.2", "-Wred"],
                 input = "{} {}".format(clon, radius),
                 encoding='ascii',
                 stdout = outfile)
  subprocess.run(common_pars + ["-W0.5,red,-"],
                 input = "{} {}\n{} {}".format(clon, clat, clon, radius),
                 encoding='ascii',
                 stdout = outfile)

def clean() :
  clear_variables()

########################################################################
# main
########################################################################
clear_variables()
set_size(paper_size)
draw_basemap(clon, clat, map_range, image_size, pol_ang)
draw_parallels(tilt)
draw_analemma(lemn_merid, starred_dates)
mark_points(clon, clat, lon, lat)
if (abs(lat) < 90 - tilt) :
  draw_italic_hours(lon, lat)
  draw_babylonian_hours(lon, lat)
close_file(outfile)
clean()
exit(0)

  
