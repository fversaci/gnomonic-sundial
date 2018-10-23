# List of examples

## cagliari.60.-30

Sundial for Cagliari, Italy. Wall facing south-west-ish (30 degrees
from south towards west) and not vertical (60 degrees, instead of 90).
You can see the Italic hours in green (sunset is the horizontal one,
and then we have -1, -2, .., -6) and Babylonian hours in blue. The
analemma is set on the UTC+1 meridian. A red dashed line gives the
measure for a vertical gnomon to be placed at the center of the disk
(marked by an x).

Obtained with

```
wall_incl = 60
wall_decl = -30
```


## cagliari.equatorial

Equatorial sundial for Cagliari, Italy. Obtained with

```
wall_incl = 90 - %(lat)s
wall_decl = 180
```

That's the side of the disk facing up, which is illuminated in spring
and summer. To get the other side, which is illuminated in autumn and
winter, use

```
wall_incl = 90 + %(lat)s
wall_decl = 0
```

## cagliari.polar

Polar sundial for Cagliari, Italy, facing south. Obtained with

```
wall_incl = %(lat)s
wall_decl = 0
```

## perth.horizontal

Horizontal sundial for Perth, Australia. Obtained with

```
wall_incl = 0
wall_decl = 180
```

## perth.vertical

Vertical sundial for Perth, Australia. Wall facing north. Obtained with

```
wall_incl = 90
wall_decl = 180
```