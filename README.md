# Omipy : Creating Coastal Navigation Figures With Python
This short class is a wrapper around pytikz to generate coastal navigation figures. Fixes, lines of positions, course, track, current, etc. 

## Basic usage
```
figure = Omipy(10, 10)
figure.draw_coord()
figure.draw_current(x=1, y=1, set = 0, drift = 5)
figure.draw_course(x=1, y=3, c = 90, s = 5)
figure.draw_track(x = 1, y = 1,  cog = 45, sog = 7.1)
figure.print_file('myfigure.png', dpi=500)
```
