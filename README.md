# Omipy : Creating Coastal Navigation Figures With Python
This short class is a wrapper around pytikz to generate coastal navigation figures. Fixes, lines of positions, course, track, current, etc. 

## Basic usage
```
from omipy import Omipy

figure = Omipy(10, 10)
figure.draw_coord()
figure.draw_fix(x = 1, y = 1, time='1000')
figure.draw_current(x=6, y=1, set = 0, drift = 5)
figure.draw_course(x=1, y=1, c = 90, s = 5)
figure.draw_track(x = 1, y = 1,  cog = 45, sog = 7.1)
figure.draw_estimated_position(x = 6, y = 6, time='1100')
figure.print_file('myfigure.png', dpi=500)
```
![](myfigure.png)

## Solving for track
```
from omipy import Omipy

figure = Omipy(10, 10)
figure.draw_coord()
figure.draw_fix(x = 1, y = 1, time='1000')
figure.draw_current(x=6, y=1, set = 0, drift = 5)
figure.draw_course(x=1, y=1, c = 90, s = 5)
figure.solve_track(time='1100')
figure.print_file('myfigure-1.png', dpi=500)
```
![](myfigure-1.png)
