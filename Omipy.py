from tikz import * 
import math


class Coordinates:
    def __init__(self):
        self.x = {"name" : "x", "units": "nm", "show_units": True, "show_name": False, "scale": 1}
        self.y = {"name" : "y", "units": "nm", "show_units": True, "show_name": False, "scale": 1}

class Omipy:
    def __init__(self, width = 10, height = 10):
        self.pic = Picture()
        self.coord = Coordinates()
        self.scope = self.pic.scope()
        self.width = width
        self.height = height
        self.pic.usetikzlibrary('decorations.markings')

    def draw_coord(self):
        # background
        self.scope.draw((-1, -1), rectangle((self.width+1, self.height+1)), opt='fill=white')

        # horizontal axis and label
        self.scope.draw((0, 0), lineto((self.width*self.coord.x['scale'], 0)), node('$'+self.coord.x['name']+'$', right=True), coordinate(name=self.coord.x['name']),opt='->')
        # vertical axis and label
        self.scope.draw((0, 0), lineto((0, self.height*self.coord.x['scale'])), node('$'+self.coord.y['name']+'$', above=True), coordinate(name=self.coord.y['name']),opt='->')

        for x in range(1, self.width):
            self.scope.draw('(0pt,1pt)', lineto('(0pt,-1pt)'), node(f'${x}$', below=True, fill='white'),xshift=f'{x} cm')

        # ticks and tick labels on vertical axis
        for y in range(1, self.height):
            self.scope.draw('(1pt,0pt)', lineto('(-1pt,0pt)'), node(f'${y}$', left=True, fill='white'), yshift=f'{y} cm')

    def draw_fix(self, x = 1, y = 1, radius=0.25, time = ''):
        self.pic.draw((x, y), circle(radius=radius))
        self.pic.draw((x, y), circle(radius=0.03), fill='black')
        if time != '':
            self.pic.draw((x + radius*0.8, y + radius*0.8), node(r'\tiny ' + time, anchor='base west'))

    def draw_estimated_position(self, x = 1, y = 1, radius=0.3, time = ''):
        self.pic.draw((x - radius*math.cos(math.pi/6), y - radius*math.sin(math.pi/6)), lineto((x, y+radius)))
        self.pic.draw((x - radius*math.cos(math.pi/6), y - radius*math.sin(math.pi/6)), lineto((x + radius*math.cos(math.pi/6), y - radius*math.sin(math.pi/6))))
        self.pic.draw((x + radius*math.cos(math.pi/6), y - radius*math.sin(math.pi/6)), lineto((x, y+radius)))
        self.pic.draw((x, y), circle(radius=0.03), fill='black')
        if time != '':
            self.pic.draw((x + radius*0.7, y + radius*0.7), node(r'\tiny ' + time, anchor='base west'))
        
    def compute_dydx(self, c, s, t):
        dx = s*math.cos(2*math.pi / 360 * (-c+90)) * t
        dy = s*math.sin(2*math.pi / 360 * (-c+90)) * t
        return [dy, dx]
    
    def draw_generic(self, x, y, c, s, t, numarrows):
        if numarrows == 1:
            arr = ">"
        elif numarrows == 2:
            arr = ">>"
        else: 
            arr = ">>>"
        dy, dx = self.compute_dydx(c, s, t)
        this_scope = self.pic.scope('thick,decoration={markings, mark=at position 0.8 with {\\arrow{'+arr+'}}}') 
        this_scope.draw((x, y), lineto((x + dx, y + dy)), node('\\tiny $'+str("{:03d}".format(c))+'^{\circ}$', above=True, midway=True, rotate=-c+90), node('\\tiny $'+str("{:.1f}".format(s))+'$', below=True, midway=True, rotate=-c+90), opt='postaction={decorate}')
    
    def draw_course(self, x=1, y=1, c=45, s=5, t = 1):
        self.course = {'c':c, 's':s, 't':t, 'x':x, 'y':y}
        self.draw_generic(x, y, c, s, t, 1)
        
    def draw_track(self, x = 1, y =1, cog=45, sog=5, t = 1):
        self.track = {'c':cog, 's':sog, 't':t, 'x':x, 'y':y}
        self.draw_generic(x, y, cog, sog, t, 2)
        
    def draw_current(self, x=1, y=1, set=45, drift=5, t = 1):
        self.current = {'c':set, 's':drift, 't':t, 'x':x, 'y':y}
        self.draw_generic(x, y, set, drift, t, 3)
    
    def solve_track(self, time):
        dy1, dx1 = self.compute_dydx(self.course['c'], self.course['s'], self.course['t'])
        dy2, dx2 = self.compute_dydx(self.current['c'], self.current['s'], self.current['t'])
        sog = pow((dy1 + dy2)**2 + (dx1+dx2)**2, 0.5)
        sog = round(sog, 1)
        cog = math.atan((dy1 + dy2)/dx1+dx2)/(2*math.pi)*360
        cog = int(round(cog, 0))
        cog = -cog + 90
        x = self.course['x'] 
        y = self.course['y']
        self.draw_generic(x, y, cog, sog, self.current['t'], 2)
        self.draw_estimated_position(x + + dx1 + dx2,y + dy1 + dy2, radius = 0.3, time=time)
        
    def solve_course(self, time):
        dy1, dx1 = self.compute_dydx(self.track['c'], self.track['s'], self.track['t'])
        dy2, dx2 = self.compute_dydx(self.current['c'], self.current['s'], self.current['t'])
        s = pow((-dy1 + dy2)**2 + (-dx1+dx2)**2, 0.5)
        s = round(s, 1)
        c = math.atan((dy1 + dy2)/dx1+dx2)/(2*math.pi)*360
        c = int(round(c, 0))
        c = -c + 90
        x = self.current['x']
        y = self.current['y']
        self.draw_generic(x, y, c, s, self.current['t'], 1)
        
    def draw_LOP(self, x = 1, y = 1, a = 0, l = 1, time=''):
        dy, dx = self.compute_dydx(a, l, 1)
        self.scope.draw((x,y), lineto((x+dx, y + dy)), node('\\tiny' + time, above=True, opt='near start'), opt='->')
    
    def draw_LOP_transfered(self, x = 1, y = 1, a = 0, l = 1, time='', time_t = ''):
        dy, dx = self.compute_dydx(a, l, 1)
        self.scope.draw((x,y), lineto((x+dx, y + dy)), node(time, above=True, opt='near start'), node('\tiny' + time_t, above=True, opt='near end'), opt='<<->>')
    
    def print_file(self, name, dpi):
        self.pic.write_image(name, dpi)
