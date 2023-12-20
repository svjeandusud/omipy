from tikz import * 
import math

class Omipy:
    def __init__(self, width = 10, height = 10, draw_coord = False):
        self.vectors = {'course':{}, 'current':{}, 'track':{}}
        self.pic = Picture()
        self.pic.usetikzlibrary('decorations.markings')
        self.dims = (width, height)
        # background
        self.pic.draw((-1, -1), rectangle((self.dims[0]+1, self.dims[1]+1)), opt='fill=white')
        if draw_coord == True: 
            self.draw_coord()
    
    def update_vector(self, name):
        dy, dx = self.compute_dydx(name)
        self.vectors[name]['y1'] = self.vectors[name]['y0'] + dy
        self.vectors[name]['x1'] = self.vectors[name]['x0'] + dx

    def set_current(self, set = 45, drift = 2, x = 1, y = 1, t = 1):
        self.vectors['current'] = {'c':set, 's':drift, 't':t, 'x0':x, 'y0':y, 'x1': -1, 'y1': -1}
        self.update_vector('current')
    
    def set_track(self, cog = 45, sog = 20, x = 1, y = 1,  t = 1):
        self.vectors['track'] = {'c':cog, 's':sog, 't':t, 'x0':x, 'y0':y, 'x1': -1, 'y1': -1}
        self.update_vector('track')

    def set_course(self, c = 45, s = 20, x = 1, y = 1, t = 1):
        self.vectors['course'] = {'c':c, 's':s, 't':t, 'x0':x, 'y0':y, 'x1': -1, 'y1': -1}
        self.update_vector('course')

    def compute_dydx(self, vector_name):
        dx = self.vectors[vector_name]["s"] * math.cos(2 * math.pi / 360 * (- self.vectors[vector_name]["c"] + 90)) * self.vectors[vector_name]["t"]
        dy = self.vectors[vector_name]["s"] * math.sin(2 * math.pi / 360 * (- self.vectors[vector_name]["c"] + 90)) * self.vectors[vector_name]["t"]
        return [dy, dx]

    def solve_track(self, time):
        self.vectors['track'] = {'c':0, 's':0, 't':self.vectors['course']['t'], 'x0':self.vectors['course']['x0'], 'y0':self.vectors['course']['y0'], 'x1': -1, 'y1': -1}
        #Set the current at the end of the course
        self.vectors["current"]['x0'] = self.vectors["course"]['x1'] 
        self.vectors["current"]['y0'] = self.vectors["course"]['y1'] 
        self.update_vector("current")
        self.compute_track(update_cog = True)

        self.make_diagram(time)

    def compute_track(self, update_cog = False):
        dy_co, dx_co = self.compute_dydx("course")
        dy_cu, dx_cu = self.compute_dydx("current")
        sog = pow((dy_co + dy_cu) ** 2 + (dx_co + dx_cu) ** 2, 0.5) / self.vectors["course"]["t"]
        cog = -math.atan((dy_co + dy_cu)/(dx_co + dx_cu)) / (2 * math.pi) * 360 + 90
        self.vectors["track"]['s'] = sog
        if update_cog == True: 
            self.vectors["track"]['c'] = cog
        self.update_vector("track")
        dy_tr, dx_tr = self.compute_dydx("track")
        if abs(dy_tr - (dy_cu + dy_co)) > 0.1 or abs(dx_tr - (dx_cu + dx_co)) > 0.1:
            self.vectors["track"]["c"] = (self.vectors["track"]["c"] + 180) % 360
            self.update_vector("track")
    
    def draw_generic(self, vector_name, thick=True):
        if "course" in vector_name:
            arr = ">"
        elif "track" in vector_name:
            arr = ">>"
        elif "current" in vector_name: 
            arr = ">>>"
        else:
            arr = ''
        if thick == True:
            add = 'thick,'
        else:
            add = ''
        this_scope = self.pic.scope(add+'decoration={markings, mark=at position 0.8 with {\\arrow{'+arr+'}}}') 
        if self.vectors[vector_name]['c'] > 180 : 
            this_scope.draw((self.vectors[vector_name]['x0'], self.vectors[vector_name]['y0']), lineto((self.vectors[vector_name]['x1'], self.vectors[vector_name]['y1'])), node('\\tiny $'+str("{:03d}".format(int(round(self.vectors[vector_name]['c'],0))))+'$', above=True, midway=True, rotate=-self.vectors[vector_name]['c']+90-180), node('\\tiny $'+str("{:.1f}".format(self.vectors[vector_name]['s']))+'$', below=True, midway=True, rotate=-self.vectors[vector_name]['c']+90-180), opt='postaction={decorate}')
        else:
            this_scope.draw((self.vectors[vector_name]['x0'], self.vectors[vector_name]['y0']), lineto((self.vectors[vector_name]['x1'], self.vectors[vector_name]['y1'])), node('\\tiny $'+str("{:03d}".format(int(round(self.vectors[vector_name]['c'],0))))+'$', above=True, midway=True, rotate=-self.vectors[vector_name]['c']+90), node('\\tiny $'+str("{:.1f}".format(self.vectors[vector_name]['s']))+'$', below=True, midway=True, rotate=-self.vectors[vector_name]['c']+90), opt='postaction={decorate}')
    
    def make_diagram(self, time, draw_dr = True):
        for some_vector in ["course", "track", "current"]:
            self.update_vector(some_vector)
            self.draw_generic(some_vector)
        self.draw_estimated_position(self.vectors["track"]['x1'], self.vectors["track"]['y1'], radius = 0.3, time = time)
        if draw_dr == True: 
            self.draw_DR(self.vectors["course"]['x1'], self.vectors["course"]['y1'], a = self.vectors["course"]["c"], time = time)
    
    def make_cts_diagram(self, time):
        for some_vector in ["course", "track", "current"]:
            self.update_vector(some_vector)
        #Increase the length of the track vector by 1.1
        dy_tr, dx_tr = self.compute_dydx("track")
        self.pic.draw((self.vectors["track"]['x0'], self.vectors["track"]['y0']), lineto((self.vectors["track"]['x0'] + dx_tr * 1.2, self.vectors["track"]['y0']+ dy_tr * 1.2)), opt='thick')
        self.draw_generic("current", thick = False)
        self.draw_generic("course", thick = False)
        self.draw_generic("track", thick = True)
        self.draw_estimated_position(self.vectors["track"]['x1'], self.vectors["track"]['y1'], radius = 0.3, time = time)
        #Move course vector to the origin
        for dim in ['x0', 'y0']:
            self.vectors["course"][dim] = self.vectors["track"][dim]
        self.update_vector('course')
        self.draw_generic("course", thick = True)
        

    def solve_course(self, s, time):
        #Set the current at the origin of the track vector
        for dim in ['x0', 'y0']:
            self.vectors["current"][dim] = self.vectors["track"][dim]
        self.update_vector('current')
        #Set the course at the end of the current
        self.vectors['course'] = {'c':0, 's':s, 't':self.vectors['track']['t'], 'x0':self.vectors['current']['x1'], 'y0':self.vectors['current']['y1'], 'x1': -1, 'y1': -1}
        self.update_vector('course')
        #Lovely trig solution
        self.vectors['course']['c'] = -1 * 360 / (2*math.pi) * math.asin(self.vectors['current']['s']/self.vectors['course']['s'] * math.sin(math.pi*2/360*(self.vectors['current']['c'] - self.vectors['track']['c'])))+ self.vectors["track"]['c']
        self.update_vector('course')
        self.compute_track(update_cog = False)
        self.make_cts_diagram(time)
        
    def draw_estimated_position(self, x = 1, y = 1, radius=0.3, time = ''):
        self.pic.draw((x - radius*math.cos(math.pi/6), y - radius*math.sin(math.pi/6)), lineto((x, y+radius)))
        self.pic.draw((x - radius*math.cos(math.pi/6), y - radius*math.sin(math.pi/6)), lineto((x + radius*math.cos(math.pi/6), y - radius*math.sin(math.pi/6))))
        self.pic.draw((x + radius*math.cos(math.pi/6), y - radius*math.sin(math.pi/6)), lineto((x, y+radius)))
        self.pic.draw((x, y), circle(radius=0.03), fill='black')
        if time != '':
            self.pic.draw((x + radius*0.7, y + radius*0.7), node(r'\tiny ' + time, anchor='base west'))
    
    def draw_course(self):
        self.draw_generic("course")
        
    def draw_track(self):
        self.draw_generic("track")
        
    def draw_current(self):
        self.draw_generic("current")

    def draw_fix(self, x = 1, y = 1, radius=0.25, time = ''):
        self.pic.draw((x, y), circle(radius=radius))
        self.pic.draw((x, y), circle(radius=0.03), fill='black')
        if time != '':
            self.pic.draw((x + radius*0.8, y + radius*0.8), node(r'\tiny ' + time, anchor='base west'))

    def draw_coord(self):
        temp = self.pic.scope()
        temp.draw((0, 0), lineto((self.dims[0], 0)), node('$x$', right=True), coordinate('x'),opt='->')
        temp.draw((0, 0), lineto((0, self.dims[1])), node('$y$', above=True), coordinate('y'),opt='->')
        for x in range(1, self.dims[0]):
            temp.draw('(0pt,1pt)', lineto('(0pt,-1pt)'), node(f'${x}$', below=True, fill='white'),xshift=f'{x} cm')
        for y in range(1, self.dims[1]):
            temp.draw('(1pt,0pt)', lineto('(-1pt,0pt)'), node(f'${y}$', left=True, fill='white'), yshift=f'{y} cm')

    def draw_LOP(self, x = 1, y = 1, a = 0, l = 1, time=''):
        self.vectors["temp"] = {'c':a, 's':l, 't':0, 'x0':x, 'y0':y, 'x1': -1, 'y1': -1}
        dy, dx = self.compute_dydx("temp")
        self.pic.draw((x,y), lineto((x+dx, y + dy)), node('\\tiny' + time, above=True, opt='near start'), opt='->')
    
    def draw_LOP_transfered(self, x = 1, y = 1, a = 0, l = 1, time='', time_t = ''):
        self.vectors["temp"] = {'c':a, 's':l, 't':0, 'x0':x, 'y0':y, 'x1': -1, 'y1': -1}
        dy, dx = self.compute_dydx("temp")
        self.pic.draw((x,y), lineto((x+dx, y + dy)), node('\\tiny'+time, above=True, opt='near start'), node('\tiny' + time_t, above=True, opt='near end'), opt='<<->>')

    def draw_DR(self, x = 1, y = 1, a = 0, time = ''):
        self.vectors["temp"] = {'c':(a-90), 's':0.1, 't':self.vectors['course']['t'], 'x0':x, 'y0':y, 'x1': -1, 'y1': -1}
        dy, dx = self.compute_dydx("temp")
        self.pic.draw((x, y), lineto((x + dx, y + dy)), node('\\tiny'+time, above = True, right=True))
        self.vectors["temp"] = {'c':(a+90), 's':0.1, 't':self.vectors['course']['t'], 'x0':x, 'y0':y, 'x1': -1, 'y1': -1}
        dy, dx = self.compute_dydx("temp")
        self.pic.draw((x,y), lineto((x + dx, y + dy)))

    def print_file(self, name, dpi):
        self.pic.write_image(name, dpi)
