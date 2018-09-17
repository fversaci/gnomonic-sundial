# How to create a complete geographic sundial using gmt

## Prerequisites

In order to run the script you will need a Linux system with
[gmt](http://gmt.soest.hawaii.edu/). To be able to draw the geographic
map within the sundial, be sure to also have the `gmt-gshhg` package
installed.

Apart from `gmt`, you will need the following (standard) Linux tools:

- bash
- date
- sed
- awk

## Overview of sundials

The literature on sundials is huge (and with some surprises even in
recent times, see bifilar sundials for example). The basic ideas
behind the gnomonic sundial, that we will present shortly here, are
thousands of years old, and can be understood with some basic
knowledge of the trigonometric functions. Nonetheless, the ability to
create them easily, automatically and complete with a full geographic
map is recent, thanks to current computers.

We will assume in the rest of this section that our location is in the
northern hemisphere and above the tropic of cancer.

A gnomonic sundial is, in its essence, a miniature reproduction of the
earth, projected onto a surface. Let's take a globe, orient its axis
along the earth's axis (i.e., pointing to Polaris star, i.e., north
with angle equal to the local latitude), and roll the globe so to have
your location facing upwards, to your zenith. You now have small copy
of the earth, with the same exact orientation w.r.t. to the sun. If we
assume the sun to be at infinite distance (since the distance
sun-earth is much larger than the earth's radius), we can use our globe
as an exact reproduction of the earth, to understand our local time.

We say that we are at (local-time) midday when the sun is exactly at
south, which means that it is at the zenith on some place on earth
which is south of us, between the tropics (on the summer solstice the
sun travels right above the tropic of Cancer, on the winter solstice
above the tropic of Capricorn, and on the two equinoxes above the
equator). Which point has the sun exactly at its zenith? If we assume
the earth to be spherical (which we will) then it's easy: it's just
the intersection between the line going from the sun to the center of
the earth and its spherical surface.

Now imagine to take our globe, make it semi-transparent and invert
each point on it with its antipode: in our new globe our current
location will be facing downward, looking at nadir. Lets make the
center point of our globe opaque, so that it casts a visible shadow on
the semi-transparent inverted globe: the point shown now on the
semi-transparent globe will be the one which originally had the sun at
its zenith, thus indicating the midday meridian.

Instead of having only the globe center opaque, we could have the
whole axis: in this way the shadow would cover the whole midday
meridian (but we would lose the exact position of the zenith point).

### Gnomonic projection

One can construct a sundial using the semi-transparent globe we
outlined above. This type of sundial is called equatorial, and it is
typically realized with the globe axis casting its shadow on a
circular stripe (or a disk) representing the equator.

What if we want to be able to see the same information on a flat
surface instead? Remember that we want to see which point on the
sphere is along the line from the sun to the globe's center. What we
can do is project, starting from the globe's center, every point on
the globe's surface until we reach the flat surface. This projection
is called
[gnomonic](https://en.wikipedia.org/wiki/Gnomonic_projection), and
dates back to Thales, in the 6th century BC. If we draw our map on a
flat surface using the gnomonic projection, then we can get rid of the
globe, leaving only its center or its axis (which will be the gnomon
of our sundial) and read the zenith location directly on the flat
surface.

Our program assumes the surface to be horizontal, but if you want to
build a vertical or oblique sundial, you just need to change the point
of the globe projection accordingly. Let take as an example Cagliari,
in Italy, which has coordinates LON = 9.133 and LAT = 39.248. In our
hypothetical, semi-transparent sphere our location will be facing
down, thus being the intersection point of an horizontal plane tangent
to the globe. Instead, if we want to project our globe to a vertical
plane facing south, the tangent point on the globe will have
coordinates LON = 9.133 and LAT = 39.248 - 90 = -50.752. If your wall
is not vertical and/or not facing south, you just need to compute the
tangent point of wall plane with the semi-transparent globe to
generate the correct sundial map.

### Reference meridian

Until the 19th century each city used its own local time, i.e., based
on the solar position: when the sun is exactly at south then it is
midday. Until transport and communication were slow, this was not a
problem, but when railways were more and more widespread the time
difference between cities started posing serious challenges to the
design and supervision of train schedules. E.g., traveling from Venice
to Turin required passengers and train personnel to adjust their
clocks by 18 minutes.

At the end of 19th century the world was divided in 24 time zones,
each large 15 degrees, to mitigate the effects of the different local
times and accumulate the differences in multiple of one hour.  E.g.,
Italy has adopted the time of the 15⁰ meridian, which goes roughly
through the mount Etna, so that there are no time differences when
using nation trains.

Adopting the reference time in the gnomonic sundial is quite simple,
you just consider it midday when the sun crosses your reference
meridian, instead of your local one.

### Mean day and the equation of time

Until now we have considered the days to be 24 hours long, but in
reality the solar days (i.e., time difference between local middays)
are quite variable throughout the year, with differences between
shortest and longest of about half an hour. This is due to both the
eccentricity of the earth's orbit and to the difference between the
axes of rotation and revolution (obliquity of the ecliptic).

A mean time of exactly 24 hours has been adopted, to avoid adjusting
clocks everyday. The difference in time between this mean time and the
real one is described by the [equation of
time](https://en.wikipedia.org/wiki/Equation_of_time).

Using the equation of time we can plot on our map, for each day, the
coordinates of the points which will have the sun at the zenith when
it's noon in our location. Because of the equation of time this curve
will not be a segment, but a 8 shaped curve, known as lemniscate. This
curve is the earth equivalent of the
[analemma](https://en.wikipedia.org/wiki/Analemma). Note, e.g., that
in November the difference between mean and real time reaches 16.5
minutes. Considering again Cagliari as our location, that means that
when the official time is noon, our local time is actually 11:20, off
by almost 40 minutes (23.5 minutes from the reference meridian + 16.5
minutes from the equation of time).

To consider also this correction to the local time, we draw the
analemma corresponding to the midday meridian (but we could also draw
one for each meridian) and we read the midday when the shadow touches
the lemniscate. Since the lemniscate has two intersection point with
almost all parallels, we need to know which one to consider when
reading. The analemma starts clockwise at the tropic of Capricorn on
winter solstice, crosses the equator (west of midday meridian) on
spring equinox and so on, changing season each time it touches a
tropic or the equator. E.g., if its winter we should consider the
western branch of the analemma, if its autumn the eastern one.

## How to use the sundial

TBD

## Program description

TBD

## Author

`gnomonic-sundial` is developed by
  * Francesco Versaci <francesco.versaci@gmail.com>


## License

This is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your
option) any later version.

See COPYING for further details.
