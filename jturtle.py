# jupyter上でタートルグラフィクスもどきを
# インラインで表示する
import math
import time
from PIL import Image, ImageDraw
from IPython.display import display, clear_output

class JTurtle:
    def __init__(self):
        self.reset()
        self.show()

    def reset(self):
        self.wh = (800, 600)        
        self.bg_fill = (240, 240, 240)
        self.im = Image.new("RGB", self.wh, self.bg_fill)
        self.draw = ImageDraw.Draw(self.im)
        self.angle = 0
        self.x = self.wh[0]/2
        self.y = self.wh[1]/2
        self.is_pen_up = False        
        self.fill = (0, 0, 0)
        self.speed = 2 
        
    def show(self):
        clear_output(wait=True)
        display(self.im)
        time.sleep(0.01)
        
    def fd(self, r):
        for i in range(round(r/self.speed)):
            nx = self.x + self.speed * math.cos(math.radians(self.angle))
            ny = self.y + self.speed * math.sin(math.radians(self.angle))            

            if self.is_pen_up == False:
                self.draw.line((self.x, self.y, nx, ny), fill=self.fill, width=2)
                self.show()

            self.x = nx
            self.y = ny
    
    def circle(self, r):
        if self.is_pen_up == False:
            self.draw.ellipse((self.x-r, self.y-(2*r), self.x+r, self.y), fill=None, outline=self.fill, width=2)
            self.show()

    def ellipse(self, w, h):
        if self.is_pen_up == False:
            self.draw.ellipse((self.x-w/2, self.y-h, self.x+w/2, self.y), fill=None, outline=self.fill, width=2)
            self.show()

    def pu(self):
        self.is_pen_up = True
    
    def pd(self):       
        self.is_pen_up = False

    def lt(self, angle):
        self.angle -= angle

    def rt(self, angle):
        self.angle += angle
    
    def goto(self, x, y):
        if self.is_pen_up == False:
            self.draw.line((self.x, self.y, x, y), fill=self.fill, width=2)
            self.show()
        self.x = x
        self.y = y
                
    def seth(self, angle):
        self.angle = -angle
        
    def color(self, r, g, b):
        self.fill = (r, g, b)
        
    def done(self):
        self.reset()

_jturtle = JTurtle()
fd = _jturtle.fd
lt = _jturtle.lt
rt = _jturtle.rt
pu = _jturtle.pu
pd = _jturtle.pd
seth = _jturtle.seth
goto = _jturtle.goto
color = _jturtle.color
circle = _jturtle.circle
ellipse = _jturtle.ellipse
done = _jturtle.done
forward = fd
left = lt
right = rt
penup = pu
pendown = pd
setheading = seth
mainloop = done
