# jupyter上でタートルグラフィクスもどきを
# インラインで表示する
import math
from PIL import Image, ImageDraw
from IPython.display import HTML, display, clear_output
import io
import base64
import random

class JTurtle:
    def __init__(self):
        self.reset()

    def reset(self):
        self.wh = (800, 600)        
        self.bg_fill = (240, 240, 240)
        self.im = Image.new('RGB', self.wh, self.bg_fill)
        self.draw = ImageDraw.Draw(self.im)
        self.angle = 0
        self.x = self.wh[0]/2
        self.y = self.wh[1]/2
        self.is_pen_up = False        
        self.pen_color = (0, 0, 0)
        self.filling_color = None
        self.tspeed = 2 
        self.images = []
        self.idx = 0
        self.is_filling = False
        self.points = []
        # self.images.append(self.im.copy())
        self.append_dummy_image()
        clear_output(wait=True)
        self.msg = ""
    
    # 数字が大きい方が速い．オリジナルは数字が小さいほうが速い．
    def speed(self, val=2):
        if val < 2:
            self.tspeed = 2
        else:
            self.tspeed = val

    def show_progress(self):
        print("making frames:", self.idx)
        self.idx += 1
        clear_output(wait=True)
    
    def show_msg(self, msg):
        print(msg)
        clear_output(wait=True)

    def append_image(self):
        self.images.append(self.im.copy())
        
    def fd(self, r):
        for i in range(int(r/self.tspeed)):
            nx = self.x + self.tspeed * math.cos(math.radians(self.angle))
            ny = self.y + self.tspeed * math.sin(math.radians(self.angle))            

            if self.is_pen_up == False:
                self.draw.line((self.x, self.y, nx, ny), fill=self.pen_color, width=2)
                self.append_image()
                self.show_progress()
                if self.is_filling:
                    self.points.append((nx, ny))

            self.x = nx
            self.y = ny

        # 端数の描画
        nokori = r % self.tspeed
        if nokori > 0:
            nx = self.x + nokori * math.cos(math.radians(self.angle))
            ny = self.y + nokori * math.sin(math.radians(self.angle))            
            if self.is_pen_up == False:
                self.draw.line((self.x, self.y, nx, ny), fill=self.pen_color, width=2)
                self.append_image()
                self.show_progress()
                if self.is_filling:
                    self.points.append((nx, ny))
            self.x = nx
            self.y = ny
            
    def circle(self, r):
        if self.is_pen_up == False:
            self.draw.ellipse((self.x-r, self.y-(2*r), self.x+r, self.y), fill=self.filling_color, outline=self.pen_color, width=2)
            self.append_image()
            self.show_progress()

    def ellipse(self, w, h):
        if self.is_pen_up == False:
            self.draw.ellipse((self.x-w/2, self.y-h, self.x+w/2, self.y), fill=self.filling_color, outline=self.pen_color, width=2)
            self.append_image()
            self.show_progress()

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
            self.draw.line((self.x, self.y, x, y), fill=self.pen_color, width=2)
            self.append_image()
            self.show_progress()
        self.x = x
        self.y = y
        if self.is_filling:
            self.points.append((x, y))
                
    def seth(self, angle):
        self.angle = -angle
        
    def color(self, r, g, b):
        self.pen_color = (r, g, b)
    
    def fillcolor(self, r=None, g=None, b=None):
        # begin_fill, end_fillは採用しない．塗りつぶさないときにはfillcolor(None)で
        if r is not None and g is not None and b is not None and r >= 0 and g >= 0 and b >= 0:
            self.filling_color = (r, g, b)
        else:
            self.filling_color = None

    def append_dummy_image(self):
        # 画像キャッシュ対策(最初のフレームに目立たない色で点を追加)
        rx = random.randrange(self.wh[0])
        ry = random.randrange(self.wh[1])
        self.draw.line((rx, ry, rx, ry), fill=(240, 240, 239), width=1)
        self.append_image()

    def done(self):
        buf = io.BytesIO()
        self.images[0].save(buf, format="PNG", save_all=True, append_images=self.images[1:], optimize=False, duration=20, loop=2) 
        buf.seek(0)
        # img_str = f"""<img src="data:image/png;base64,{base64.b64encode(buf.getvalue()).decode('ascii')}" />"""
        img_str = f"""<div>{self.msg}</div><img src="data:image/png;base64,{base64.b64encode(buf.getvalue()).decode('ascii')}" />"""
        buf.close()
        display(HTML(img_str))
        self.reset()
    
    # for debug
    def show_pos(self, text=None):
        if text is not None:
            self.msg += text + ":"
        self.msg += f"({int(self.x)}, {int(self.y)}), "
    
    def begin_fill(self):
        self.points = [(self.x, self.y)]
        self.is_filling = True
    
    def end_fill(self):
        if len(self.points) > 0 and self.is_filling:
            self.draw.polygon(self.points, fill=self.filling_color, outline=self.pen_color)
            self.is_filling = False


_jturtle = JTurtle()
fd = _jturtle.fd
lt = _jturtle.lt
rt = _jturtle.rt
pu = _jturtle.pu
pd = _jturtle.pd
seth = _jturtle.seth
goto = _jturtle.goto
color = _jturtle.color
fillcolor = _jturtle.fillcolor
circle = _jturtle.circle
ellipse = _jturtle.ellipse
done = _jturtle.done
speed = _jturtle.speed
begin_fill = _jturtle.begin_fill
end_fill = _jturtle.end_fill

forward = fd
left = lt
right = rt
penup = pu
pendown = pd
setheading = seth
mainloop = done

#for debug
show_pos = _jturtle.show_pos
