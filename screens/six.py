"""
"""

#STL
import os, inspect, sys, math
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
from popups import WinPopup, LosePopup

FRAMES = 30.0


class DangerObject(Widget):
    cy_body = ObjectProperty()
    cy_poly = ObjectProperty()

    def __init__(self, pos, size, space, *args, **kwargs):
        super(DangerObject, self).__init__(*args, **kwargs)
        self.cy_body = cy.Body(None, None)
        self.cy_body.position = pos[0], pos[1]
        self.cy_poly = cy.Poly.create_box(self.cy_body, size=size, offset=(0,0), radius=0)
        self.cy_poly.elasticity = 0.2
        space.add_static(self.cy_poly)
        self.cy_poly.collision_type = 4
        self.size_hint = None, None
        self.size = size
        self.pos = pos[0] - size[0]/2, pos[1] - size[1]/2


class DangerCircleObject(Widget):
    radius = NumericProperty()
    cy_body = ObjectProperty()
    cy_circle = ObjectProperty()

    def __init__(self, pos, radius, space, *args, **kwargs):
        super(DangerCircleObject, self).__init__(*args, **kwargs)
        self.cy_body = cy.Body(1, 100)
        self.cy_body.position = pos[0], pos[1]
        #self.cy_body.velocity_limit = 10
        self.cy_circle = cy.Circle(self.cy_body, radius)
        self.cy_circle.elasticity = 1
        self.cy_circle.collision_type = 6
        #self.cy_circle.friction = 1
        space.add(self.cy_body, self.cy_circle)
        self.size_hint = None, None
        self.size = radius*2, radius*2
        self.pos = pos[0] - radius, pos[1] - radius
        self.radius = radius

    def update(self):
        p = self.cy_body.position
        self.pos = p.x - self.radius, p.y - self.radius

class DragCircleObject(Widget):
    radius = NumericProperty()
    cy_body = ObjectProperty()
    cy_circle = ObjectProperty()

    def __init__(self, pos, radius, space, *args, **kwargs):
        super(DragCircleObject, self).__init__(*args, **kwargs)
        self.cy_body = cy.Body(1, 100)
        self.cy_body.position = pos[0], pos[1]
        #self.cy_body.velocity_limit = 10
        self.cy_circle = cy.Circle(self.cy_body, radius)
        self.cy_circle.elasticity = 1
        self.cy_circle.collision_type = 5
        #self.cy_circle.friction = 1
        space.add(self.cy_body, self.cy_circle)
        self.size_hint = None, None
        self.size = radius*2, radius*2
        self.pos = pos[0] - radius, pos[1] - radius
        self.radius = radius

    def update(self):
        p = self.cy_body.position
        self.pos = p.x - self.radius, p.y - self.radius

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



class ScreenSix(Screen):
    space = ObjectProperty()
    ball = ObjectProperty()
    walls = ListProperty()
    up = BooleanProperty(0)
    left = BooleanProperty(0)
    right = BooleanProperty(0)
    down = BooleanProperty(0)
    win_objects = ListProperty()
    danger_objects = ListProperty()
    drag_circle_objects = ListProperty()
    danger_circle_objects = ListProperty()
    real_drag_circle_objects = ListProperty()
    real_danger_circle_objects = ListProperty()
    win_popup = ObjectProperty()
    lose_popup = ObjectProperty()
    counter = NumericProperty(0)

    def __init__(self, app, *args, **kwargs):
        super(ScreenSix, self).__init__(*args, **kwargs)
        self.app = app
        self.win_popup = WinPopup(app, "You won the game", "31613616317682335123%22", "seven")
        self.win_popup.bind(on_dismiss=self.on_pre_leave)
        self.lose_popup = LosePopup(app, "Sorry you lost the game", "Try again", "six")
        self.box_size = [Window.size[0] / 16., Window.size[1] / 10.]
        self.lose_popup.bind(on_dismiss=self.on_pre_leave)
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
        self.app.switch_screen("five")

    def forward_btn_pressed(self, *args):
        self.app.switch_screen("seven")

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        direction = keycode[1]
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
        self.space.damping = 0.005
        self.space.collision_slop = 0
        for i in xrange(16):
            self.walls.append([i,0])
            self.walls.append([i,9])
        for i in xrange(1,9):
            self.walls.append([0,i])
            self.walls.append([15,i])
        self.walls.append((12, 2))
        self.walls.append((12, 3))
        self.walls.append((12, 4))
        self.walls.append((12, 5))
        self.walls.append((12, 6))
        self.walls.append((12, 7))
        self.walls.append((12, 8))
        self.win_objects.append([14, 8])
        self.danger_circle_objects = [(14, 1), (14, 2), (14, 3), (14, 4), (14, 5), (10, 6), (10, 7), (13, 1), (13, 2), (13, 3), (13, 4), (13, 5), (11, 6), (11, 7), (11, 8), (8, 6), (8, 7), (8, 8), (5, 6), (4, 6), (5, 8)]
        """
        for i in xrange(2, 16, 2):
            for j in xrange(1, 8):
                if i%4:
                    self.danger_objects.append((i, j))
                else:
                    self.danger_objects.append((i, j+1))
        """
        self.add_ball()
        self.add_walls()
        self.add_win_objects()
        self.add_danger_objects()
        self.add_drag_circle_objects()
        self.add_danger_circle_objects()
        self.space.add_collision_handler(1, 3, begin = self.collision_with_end)
        self.space.add_collision_handler(1, 6, begin = self.collision_with_danger)

    def collision_with_end(self, space, arbiter, *args, **kwargs):
        Clock.unschedule(self.step)
        self.on_pre_leave()
        self.win_popup.open()
        return True

    def collision_with_danger(self, space, arbiter, *args, **kwargs):
        Clock.unschedule(self.step)
        self.lose_popup.open()
        self.on_pre_leave()
        return True

    def add_ball(self):
        radius = min(self.box_size[0], self.box_size[1]) * 0.3
        pos = self.box_size[0] + (radius * 1.1), self.box_size[1] + (radius * 1.1)
        self.ball = CircleObject(pos, radius, self.space)
        self.add_widget(self.ball)

    def add_danger_circle_objects(self):
        for x, y in self.danger_circle_objects:
            radius = min(self.box_size[0], self.box_size[1]) * 0.3
            pos = (x * self.box_size[0]) + (radius * 1.1), (y * self.box_size[1]) + (radius * 1.1)
            danger_ball = DangerCircleObject(pos, radius, self.space)
            self.add_widget(danger_ball)
            self.real_danger_circle_objects.append(danger_ball)

    def add_drag_circle_objects(self):
        for x, y in self.drag_circle_objects:
            radius = min(self.box_size[0], self.box_size[1]) * 0.3
            pos = (x * self.box_size[0]) + (radius * 1.1), (y * self.box_size[1]) + (radius * 1.1)
            drag_ball = DragCircleObject(pos, radius, self.space)
            self.add_widget(drag_ball)
            self.real_drag_circle_objects.append(drag_ball)

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

    def add_danger_objects(self):
        for x, y in self.danger_objects:
            pos = (x * self.box_size[0]) + (self.box_size[0]/2.), (y * self.box_size[1]) + (self.box_size[1]/2.)
            size = self.box_size[0], self.box_size[1]
            danger = DangerObject(pos, size, self.space)
            self.add_widget(danger)

    def step(self, *args):
        self.space.step(1/FRAMES)
        imp = 50
        if self.left:
            self.ball.cy_body.apply_impulse([-1 * imp, 0])
        if self.right:
            self.ball.cy_body.apply_impulse([1 * imp, 0])
        if self.up:
            self.ball.cy_body.apply_impulse([0, 1 * imp])
        if self.down:
            self.ball.cy_body.apply_impulse([0, -1 * imp])
        for item in self.real_danger_circle_objects:
            pos_y = self.ball.pos[1] - item.pos[1]
            pos_x = self.ball.pos[0] - item.pos[0]
            tan_inv = math.atan2(pos_y, pos_x)
            temp_imp = imp * math.cos(tan_inv) * 0.9, imp * math.sin(tan_inv) * 0.9
            item.cy_body.apply_impulse(temp_imp)
        self.update_objects()
    
    def update_objects(self):
        self.ball.update()
        for item in self.real_drag_circle_objects:
            item.update()
        for item in self.real_danger_circle_objects:
            item.update()

    def on_pre_leave(self, *args):
        Clock.unschedule(self.step)
        self.keyboard_closed()
