import turtle
import math
import weakref
import threading
import sys

from common import *
from ide import add_command, get_canvas, get_scroller

class Turtle:

    _all_turtles = []
    _turtle_count = 1

    def __init__(self):
        self.pen = turtle.RawPen(get_canvas())
        self.pen.degrees()
        self._all_turtles.append(weakref.ref(self))
        self._count = self._turtle_count
        self.__class__._turtle_count += 1

    def __repr__(self):
        return '<%s %i>' % (self.__class__.__name__,
                            self._count)

    @logofunc()
    def turtle(self):
        return self

    @logofunc(aliases=['fd'])
    def forward(self, v):
        add_command(self.pen.forward, v)
        add_command(get_canvas().update)
        add_command(get_scroller().resizescrollregion)

    @logofunc(aliases=['back', 'bk'])
    def backward(self, v):
        add_command(self.pen.backward,v)
        add_command(get_canvas().update)
        add_command(get_scroller().resizescrollregion)

    @logofunc(aliases=['lt'])
    def left(self, v):
        add_command(self.pen.left, v)

    @logofunc(aliases=['rt'])
    def right(self, v):
        add_command(self.pen.right, v)

    @logofunc(aliases=['pu'])
    def penup(self):
        add_command(self.pen.up)

    @logofunc(aliases=['pd'])
    def pendown(self):
        add_command(self.pen.down)

    @logofunc(aliases=['pw'],arity=1)
    def penwidth(self, v):
        add_command(self.pen.width, v)

    @logofunc(aliases=['pc', 'color'],
              arity=1)
    def pencolor(self, *args):
        add_command(self.pen.color, *args)

    @logofunc(aliases=['pc3', 'color3'],
              arity=3)
    def pencolor3(self, *args):
        add_command(self.pen.color, *args)
    @logofunc(aliases=['ht'])
    def hideturtle(self):
        add_command(self.pen.tracer, 0)

    @logofunc(aliases=['st'])
    def showturtle(self):
        add_command(self.pen.tracer, 1)

    @logofunc(aliases=['turtleprint', 'turtlepr'], arity=1)
    def turtlewrite(self, text, move=False):
        if isinstance(text, list):
            text = ' '.join(map(str, text))
        else:
            text = str(text)
        add_command(self.pen.write, text, move)
        add_command(get_canvas().update)
        add_command(get_scroller().resizescrollregion)

    @logofunc()
    def startfill(self):
        add_command(self.pen.fill, 1)

    @logofunc()
    def endfill(self):
        add_command(self.pen.fill, 0)
        add_command(get_canvas().update)
        add_command(get_scroller().resizescrollregion)

    @logofunc()
    def setxy(self, x, y):
        add_command(self.pen.goto, x, y)
        add_command(get_canvas().update)
        add_command(get_scroller().resizescrollregion)

    @logofunc()
    def setx(self, x):
        add_command(self.pen.setx,x)
        add_command(get_canvas().update)
        add_command(get_scroller().resizescrollregion)

    @logofunc()
    def sety(self, y):
        add_command(self.pen.sety, y)
        add_command(get_canvas().update)
        add_command(get_scroller().resizescrollregion)

    @logofunc()
    def posx(self):
        return self.pen.position()[0]

    @logofunc()
    def posy(self):
        return self.pen.position()[1]

    @logofunc()
    def heading(self):
        return self.pen.heading()

    @logofunc()
    def setheading(self, v):
        add_command(self.pen.setheading, v)

    @logofunc()
    def home(self):
        add_command(self.pen.setheading, 0)
        add_command(self.pen.goto, 0, 0)
        add_command(get_canvas().update)
        add_command(get_scroller().resizescrollregion)

    @logofunc(arity=1)
    def speed(self, x):
        add_command(self.pen.speed,x)
        
    @logofunc(arity=1)
    def delay(self, x):
        add_command(self.pen.delay,x)

    @logofunc(aliases=['cs', 'clearscreen'])
    def clear(self):
        self.home()
        add_command(self.pen.clear)
        add_command(get_canvas().update)
        add_command(get_scroller().resizescrollregion)

    @logofunc(arity=1)
    def distance(self, other, orig=None):
        if orig is None:
            orig = self.pen
        return math.sqrt((orig.position()[0]-other.position()[0])**2 +
                         (orig.position()[1]-other.position()[1])**2)

    @logofunc(aware=True)
    def clone(self, interp):
        new = self.__class__()

@logofunc()
def allturtles():
    return [t() for t in Turtle._all_turtles if t()]

@logofunc(aware=True)
def createturtle(interp):
    t = Turtle()
    interp.push_actor(t)
