# Omipy : Creating Coastal Navigation Figures With Python
This short class is a wrapper around pytikz to generate coastal navigation figures. Fixes, lines of positions, course, track, current, etc. 

## Basic usage

figure = Omipy(10, 10)
figure.draw_coord()
figure.draw_current(x=1, y=1, set = 0, drift = 2)
figure.draw_course(x=1, y=3, set = 0, drift = 2)
