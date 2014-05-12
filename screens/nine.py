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

class DarkObject(Widget):
    cy_body = ObjectProperty()
    cy_poly = ObjectProperty()

    def __init__(self, pos, size, space, *args, **kwargs):
        super(DarkObject, self).__init__(*args, **kwargs)
        size = size[0]/30., size[1]/30.
        self.cy_body = cy.Body(None, None)
        self.cy_body.position = pos[0], pos[1]
        self.cy_poly = cy.Poly.create_box(self.cy_body, size=size, offset=(0,0), radius=0)
        self.cy_poly.elasticity = 0.2
        space.add_static(self.cy_poly)
        self.cy_poly.collision_type = 9
        self.size_hint = None, None
        self.size = size
        self.pos = pos[0] - size[0]/2, pos[1] - size[1]/2



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


class GlowCircleObject(Widget):
    radius = NumericProperty()
    cy_body = ObjectProperty()
    cy_circle = ObjectProperty()

    def __init__(self, pos, radius, space, *args, **kwargs):
        super(GlowCircleObject, self).__init__(*args, **kwargs)
        self.cy_body = cy.Body(1, 100)
        self.cy_body.position = pos[0], pos[1]
        self.cy_circle = cy.Circle(self.cy_body, radius)
        self.cy_circle.elasticity = 1
        self.cy_circle.collision_type = 1
        space.add(self.cy_body, self.cy_circle)
        self.size_hint = None, None
        self.size = radius*2, radius*2
        self.pos = pos[0] - radius, pos[1] - radius
        self.radius = radius

    def update(self):
        p = self.cy_body.position
        self.pos = p.x - self.radius, p.y - self.radius

class FakeDoorObject(Widget):
    cy_body = ObjectProperty()
    cy_poly = ObjectProperty()

    def __init__(self, pos, size, space, *args, **kwargs):
        super(FakeDoorObject, self).__init__(*args, **kwargs)
        self.cy_body = cy.Body(None, None)
        self.cy_body.position = pos[0], pos[1]
        self.cy_poly = cy.Poly.create_box(self.cy_body, size=size, offset=(0,0), radius=0)
        self.cy_poly.elasticity = 0.2
        space.add_static(self.cy_poly)
        self.cy_poly.collision_type = 7
        self.size_hint = None, None
        self.size = size
        self.pos = pos[0] - size[0]/2, pos[1] - size[1]/2

class RealDoorObject(Widget):
    cy_body = ObjectProperty()
    cy_poly = ObjectProperty()

    def __init__(self, pos, size, space, *args, **kwargs):
        super(RealDoorObject, self).__init__(*args, **kwargs)
        self.cy_body = cy.Body(None, None)
        self.cy_body.position = pos[0], pos[1]
        self.cy_poly = cy.Poly.create_box(self.cy_body, size=size, offset=(0,0), radius=0)
        self.cy_poly.elasticity = 0.2
        space.add_static(self.cy_poly)
        self.cy_poly.collision_type = 8
        self.size_hint = None, None
        self.size = size
        self.pos = pos[0] - size[0]/2, pos[1] - size[1]/2

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

class ScreenNine(Screen):
    space = ObjectProperty()
    balls = ListProperty()
    real_balls = ListProperty()
    walls = ListProperty()
    up = BooleanProperty(0)
    left = BooleanProperty(0)
    right = BooleanProperty(0)
    down = BooleanProperty(0)
    fake = BooleanProperty(0)
    win_objects = ListProperty()
    danger_objects = ListProperty()
    drag_circle_objects = ListProperty()
    danger_circle_objects = ListProperty()
    real_drag_circle_objects = ListProperty()
    real_danger_circle_objects = ListProperty()
    real_door_objects = ListProperty()
    fake_door_objects = ListProperty()
    dark_objects = ListProperty()
    door_objects = ListProperty()
    win_popup = ObjectProperty()
    lose_popup = ObjectProperty()
    counter = NumericProperty(0)

    def __init__(self, app, *args, **kwargs):
        super(ScreenNine, self).__init__(*args, **kwargs)
        self.app = app
        self.win_popup = WinPopup(app, "You have played all the stages", "Taking you to menu screen", "menu")
        self.lose_popup = LosePopup(app, "Sorry you lost the game", "Try again", "nine")
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
        #forward_button = Button(text=">", pos=[Window.size[0]*0.925, Window.size[1]*0.925], size_hint = [0.05, 0.05])
        #forward_button.bind(on_press=self.forward_btn_pressed)
        self.add_widget(back_button)
        #self.add_widget(forward_button)

    def back_btn_pressed(self, *args):
        self.app.switch_screen("eight")

    def forward_btn_pressed(self, *args):
        self.app.switch_screen("ten")

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
        """
        for i in xrange(1, 11):
            self.fake_door_objects.append((i, 7))
        self.real_door_objects.append((11, 7))
        for i in xrange(12, 15):
            self.fake_door_objects.append((i, 7))
        """
        #self.danger_circle_objects = [(14, 1)]
        """
        self.walls.append((3, 3))
        self.walls.append((14, 6))
        self.walls.append((5, 3))
        """
        self.balls = [(1, 1)]
        self.dark_objects = [(2, 8)]
        #self.danger_objects = [(1, 8), (2, 6), (1, 4), (2, 2), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8), (10, 8), (11, 8), (12, 8), (5, 1), (5, 2), (5, 4), (5, 5), (5, 6), (7, 2), (8, 2), (6, 4), (7, 4), (7, 6), (8, 6), (9, 2), (10, 2), (11, 2), (13, 2), (14, 2), (9, 4), (10, 4), (11, 4), (12, 4), (14, 4), (3, 6), (10, 6), (12, 6), (3, 1), (3, 2), (3, 4), (3, 5), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (9, 3), (10, 3), (9, 1), (10, 1), (11, 1), (4, 6), (9, 6)]
        self.add_balls()
        self.add_walls()
        self.add_win_objects()
        self.add_danger_objects()
        self.add_drag_circle_objects()
        self.add_danger_circle_objects()
        self.add_fake_door_objects()
        self.add_real_door_objects()
        self.add_dark_objects()
        self.space.add_collision_handler(1, 9, begin = self.collision_with_end)
        self.space.add_collision_handler(1, 4, begin = self.collision_with_danger)

    def collision_with_end(self, space, arbiter, *args, **kwargs):
        self.win_popup.open()
        self.on_pre_leave()
        return True

    def collision_with_danger(self, space, arbiter, *args, **kwargs):
        self.lose_popup.open()
        self.on_pre_leave()
        return True

    def add_balls(self):
        radius = min(self.box_size[0], self.box_size[1]) * 0.3
        for x,y in self.balls:
            pos = (x * self.box_size[0]) + (radius * 1.1), (y * self.box_size[1]) + (radius * 1.1)
            ball = GlowCircleObject(pos, radius, self.space)
            self.add_widget(ball)
            self.real_balls.append(ball)

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

    def add_fake_door_objects(self):
        for x,y in self.fake_door_objects:
            pos = (x * self.box_size[0]) + (self.box_size[0]/2.), (y * self.box_size[1]) + (self.box_size[1]/2.)
            size = self.box_size[0], self.box_size[1]
            door = FakeDoorObject(pos, size, self.space)
            self.add_widget(door)

    def add_real_door_objects(self):
        for x,y in self.real_door_objects:
            pos = (x * self.box_size[0]) + (self.box_size[0]/2.), (y * self.box_size[1]) + (self.box_size[1]/2.)
            size = self.box_size[0], self.box_size[1]
            door = RealDoorObject(pos, size, self.space)
            self.add_widget(door)

    def add_win_objects(self):
        for x, y in self.win_objects:
            pos = (x * self.box_size[0]) + (self.box_size[0]/2.), (y * self.box_size[1]) + (self.box_size[1]/2.)
            size = self.box_size[0], self.box_size[1]
            win = WinObject(pos, size, self.space)
            self.add_widget(win)

    def add_dark_objects(self):
        for x, y in self.dark_objects:
            pos = (x * self.box_size[0]) + (self.box_size[0]/2.), (y * self.box_size[1]) + (self.box_size[1]/2.)
            size = self.box_size[0], self.box_size[1]
            dark = DarkObject(pos, size, self.space)
            self.add_widget(dark)

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
            for item in self.real_balls:
                item.cy_body.apply_impulse([-1 * imp, 0])
        if self.right:
            for item in self.real_balls:
                item.cy_body.apply_impulse([1 * imp, 0])
        if self.up:
            for item in self.real_balls:
                item.cy_body.apply_impulse([0, 1 * imp])
        if self.down:
            for item in self.real_balls:
                item.cy_body.apply_impulse([0, -1 * imp])
        self.update_objects()
    
    def update_objects(self):
        for item in self.real_balls: 
            item.update()
        for item in self.real_drag_circle_objects:
            item.update()
        for item in self.real_danger_circle_objects:
            item.update()

    def on_pre_leave(self, *args):
        Clock.unschedule(self.step)
        self.keyboard_closed()
