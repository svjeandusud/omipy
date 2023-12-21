# Omipy : Creating Coastal Navigation Figures With Python
This short class is a wrapper around [pytikz](https://github.com/allefeld/pytikz) to generate coastal navigation figures. Fixes, lines of positions, course, track, current, etc. 

## Installation
A python interpreter must be installed on your computer. This is installed by default on Apple Computers, on Linux Operating Systems ... but me installed on Windows Computer. The standard installation instructions can be found [here](https://www.python.org/downloads/windows/), but a troubleless installation is perhaps more likely to happen by installing the [Anaconda suite](https://www.anaconda.com/download).

The [pytikz](https://github.com/allefeld/pytikz) package must also be installed. This can be done with the simple pip command: 
```
pip install git+https://github.com/allefeld/pytikz.git
``` 
If you have no idea what this means, you can [read the documentation](https://packaging.python.org/en/latest/tutorials/installing-packages/) or google it. 

## Examples
### Basic Usage
Drawing a Figure manually. 
```
from omipy import Omipy

figure = Omipy(10, 10, draw_coord = True)
figure.draw_fix(x = 1, y = 1, time='1000')
figure.set_current(set = 0, drift = 5, x=6, y=1)
figure.set_course(s = 5, c = 90, x = 1, y = 1)
figure.set_track(cog = 45, sog = 7.1, x=1, y=1)
figure.make_diagram(time="1100")
figure.print_file('myfigure-1.png', dpi=500)
```
![](example-1-1.png)

### Solving for Course Over the Ground
When the navigation is performed without anticipation of the current. The current and course vectors are known. The resulting track (COG, SOG) is calculated. 
```
from omipy import Omipy

figure = Omipy(10, 10, draw_coord = True)
figure.draw_fix(x = 1, y = 1, time='1000')
figure.set_current(set = 0, drift = 5, x=6, y=1)
figure.set_course(s = 5, c = 90, x = 1, y = 1)
figure.solve_track("1100")
figure.print_file('myfigure-2.png', dpi=500)
```
![](example-2-2.png)

### Solving for Course to Steer
When the navigation anticipates the impact of the current. The current vector, the course over the ground (COG) and the surface speed are known. The speed over the ground and course are calculated. 
```
from omipy import Omipy

figure = Omipy(10, 10, draw_coord = True)
figure.draw_fix(x = 4, y = 8, time='1000')
figure.set_track(cog = 45+90, x=4, y = 8)
figure.set_current(set = 220, drift = 2, x = 4, y = 8)
figure.solve_course(s = 5.0, time = "1100")
figure.print_file('myfigure-3.png', dpi=500)
```
![](example-3.png)



