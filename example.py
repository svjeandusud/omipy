from omipy import Omipy

#Basic example
figure = Omipy(10, 10)
figure.draw_coord()
figure.draw_fix(x = 1, y = 1, time='1000')
figure.draw_current(x=6, y=1, set = 0, drift = 5)
figure.draw_course(x=1, y=1, c = 90, s = 5)
figure.draw_track(x = 1, y = 1,  cog = 45, sog = 7.1)
figure.draw_estimated_position(x = 6, y = 6, time='1100')
figure.print_file('myfigure.png', dpi=500)
