set term postscript enhanced color
set output "timeofday.ps"

i = 0.0698132

f(x,y) =  21.0 / 4.0  * acos( - tan(y)* tan( asin( cos(x) * sin(i))))

set isosample 250,250

set xrange [0:2*pi]
set yrange [-pi/2:pi/2]


set cntrparam levels incremental 5, 0.1, 18

#set pm3d interpolate 20,20

set palette model RGB defined (10 "black", 11 "blue", 12 "cyan", 13 "green", 14 "yellow", 15 "red", 21 "purple")



set contour base
unset surface

set view map

unset key
unset table




splot f(x,y) palette
