"""
"""

#STL
import os, inspect, sys
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


#kivy
from kivy.properties import NumericProperty, ObjectProperty, ListProperty, BooleanProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics.vertex_instructions import Line
from kivy.graphics import Color
from kivy.uix.button import Button


#3rd party
import cymunk as cy


#Custom import
from popups import WinPopup

FRAMES = 30.0

class CircleObject(Widget):
    radius = NumericProperty()
    cy_body = ObjectProperty()
    cy_circle = ObjectProperty()

    def __init__(self, pos, radius, space, *args, **kwargs):
        super(CircleObject, self).__init__(*args, **kwargs)
        self.cy_body = cy.Body(1, 100)
        self.cy_body.position = pos[0], pos[1]
        #self.cy_body.velocity_limit = 10
        self.cy_circle = cy.Circle(self.cy_body, radius)
        self.cy_circle.elasticity = 1
        self.cy_circle.collision_type = 1
        #self.cy_circle.friction = 1
        space.add(self.cy_body, self.cy_circle)
        self.size_hint = None, None
        self.size = radius*2, radius*2
        self.pos = pos[0] - radius, pos[1] - radius
        self.radius = radius


    def update(self):
        p = self.cy_body.position
        self.pos = p.x - self.radius, p.y - self.radius

class WallObject(Widget):
    cy_body = ObjectProperty()
    cy_poly = ObjectProperty()

    def __init__(self, pos, size, space, *args, **kwargs):
        super(WallObject, self).__init__(*args, **kwargs)
        self.cy_body = cy.Body(None, None)
        self.cy_body.position = pos[0], pos[1]
        self.cy_poly = cy.Poly.create_box(self.cy_body, size=size, offset=(0,0), radius=0)
        self.cy_poly.elasticity = 0.2
        space.add_static(self.cy_poly)
        self.cy_poly.collision_type = 2
        self.size_hint = None, None
        self.size = size
        self.pos = pos[0] - size[0]/2, pos[1] - size[1]/2

class WinObject(Widget):
    cy_body = ObjectProperty()
    cy_poly = ObjectProperty()

    def __init__(self, pos, size, space, *args, **kwargs):
        super(WinObject, self).__init__(*args, **kwargs)
        self.cy_body = cy.Body(None, None)
        self.cy_body.position = pos[0], pos[1]
        self.cy_poly = cy.Poly.create_box(self.cy_body, size=size, offset=(0,0), radius=0)
        self.cy_poly.elasticity = 0.2
        space.add_static(self.cy_poly)
        self.cy_poly.collision_type = 3
        self.size_hint = None, None
        self.size = size
        self.pos = pos[0] - size[0]/2, pos[1] - size[1]/2



class ScreenThree(Screen):
    space = ObjectProperty()
    ball = ObjectProperty()
    walls = ListProperty()
    up = BooleanProperty(0)
    left = BooleanProperty(0)
    right = BooleanProperty(0)
    down = BooleanProperty(0)
    win_objects = ListProperty()
    win_popup = ObjectProperty()



    def __init__(self, app, *args, **kwargs):
        super(ScreenThree, self).__init__(*args, **kwargs)
        self.app = app
        self.win_popup = WinPopup(app, "You won the game", "score", "four")
        self.box_size = [Window.size[0] / 16., Window.size[1] / 10.]
        self.init_physics()
        self.keyboard = Window.request_keyboard(self.keyboard_closed, self, 'text')
        self.keyboard.bind(on_key_down=self.on_keyboard_down)
        self.keyboard.bind(on_key_up=self.on_keyboard_up)
        Clock.schedule_interval(self.step, 1/FRAMES)
        #Adding the lines
        for i in xrange(16):
            with self.canvas:
                Color(0, 0, 0, 0.3)
                Line(points=[self.box_size[0]*i, 0, self.box_size[0]*i, Window.size[1]], width=0.3)
        for i in xrange(10):
            with self.canvas:
                Line(points=[0, self.box_size[1]*i, Window.size[0], self.box_size[1]*i], width=0.3)
        #Adding back and forward buttons
        back_button = Button(text="<", pos=[Window.size[0]*0.025, Window.size[1]*0.925], size_hint = [0.05, 0.05])
        back_button.bind(on_press=self.back_btn_pressed)
        forward_button = Button(text=">", pos=[Window.size[0]*0.925, Window.size[1]*0.925], size_hint = [0.05, 0.05])
        forward_button.bind(on_press=self.forward_btn_pressed)
        self.add_widget(back_button)
        self.add_widget(forward_button)

    def back_btn_pressed(self, *args):
        self.app.switch_screen("two")

    def forward_btn_pressed(self, *args):
        self.app.switch_screen("four")

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        direction = keycode[1]
        vec2d = cy.vec2d.Vec2d
        if direction == "left" or direction == "a":
            self.left = True
        if direction == "right" or direction == "d":
            self.right = True
        if direction == "up" or direction == "w":
            self.up = True
        if direction == "down" or direction == "s":
            self.down = True

    def on_keyboard_up(self, keyboard, keycode, *args):
        direction = keycode[1]
        if direction == "left" or direction == "a":
            self.left = False
        if direction == "right" or direction == "d":
            self.right = False
        if direction == "up" or direction == "w":
            self.up = False
        if direction == "down" or direction == "s":
            self.down = False


    def keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self.on_keyboard_down)

    def init_physics(self):
        self.space = cy.Space()
        self.arbiter = cy.Arbiter(self.space)
        self.space.damping = 0.035
        self.space.collision_slop = 0
        for i in xrange(16):
            self.walls.append([i,0])
            self.walls.append([i,9])
        for i in xrange(1,9):
            self.walls.append([0,i])
            self.walls.append([15,i])
        self.win_objects.append([14, 8])
        self.add_ball()
        self.add_walls()
        self.add_win_objects()
        self.space.add_collision_handler(1, 3, begin = self.collision_between_balls)

    def collision_between_balls(self, space, arbiter, *args, **kwargs):
        print "[" + str(self.ball.cy_body.position.x) + "," +str(self.ball.cy_body.position.y) + "]", self.ball.pos
        #print self.ball.cy_body.local_to_world()
        self.win_popup.open()
        print "Contact"
        return True


    def add_ball(self):
        radius = min(self.box_size[0], self.box_size[1]) * 0.4
        pos = self.box_size[0] + (radius * 1.1), self.box_size[1] + (radius * 1.1)
        self.ball = CircleObject(pos, radius, self.space)
        self.add_widget(self.ball)

    def add_walls(self):
        for x,y in self.walls:
            pos = (x * self.box_size[0]) + (self.box_size[0]/2.), (y * self.box_size[1]) + (self.box_size[1]/2.)
            size = self.box_size[0], self.box_size[1]
            wall = WallObject(pos, size, self.space)
            self.add_widget(wall)

    def add_win_objects(self):
        for x, y in self.win_objects:
            pos = (x * self.box_size[0]) + (self.box_size[0]/2.), (y * self.box_size[1]) + (self.box_size[1]/2.)
            size = self.box_size[0], self.box_size[1]
            win = WinObject(pos, size, self.space)
            self.add_widget(win)


    def step(self, *args):
        self.space.step(1/FRAMES)
        imp = 80
        if self.left:
            self.ball.cy_body.apply_impulse([-1 * imp, 0])
        if self.right:
            self.ball.cy_body.apply_impulse([1 * imp, 0])
        if self.up:
            self.ball.cy_body.apply_impulse([0, 1 * imp])
        if self.down:
            self.ball.cy_body.apply_impulse([0, -1 * imp])
        self.update_objects()
    
    def update_objects(self):
        self.ball.update()

    def on_leave(self):
        Clock.unschedule(self.step)
        self.keyboard_closed()
