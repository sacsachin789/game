#STL
import random

#3rd Party
import cymunk as cy

#Kivy
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.properties import ListProperty, StringProperty, NumericProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.clock import Clock
from kivy.core.image import Image
from kivy.core.window import Window

#Custom
FRAMES = 60.0
MIN_IMPULSE = -30000
MAX_IMPULSE =  30000

class CircleObject(Widget):
    radius = NumericProperty()
    cy_body = ObjectProperty()
    cy_circle = ObjectProperty()
    initial_color = ListProperty()
    touch_color = ListProperty()
    def __init__(self, pos, radius, space, *args, **kwargs):
        super(CircleObject, self).__init__(*args, **kwargs)
        self.cy_body = cy.Body(100, 1e9)
        self.cy_body.position = pos[0], pos[1]
        self.cy_circle = cy.Circle(self.cy_body, radius)
        self.cy_circle.elasticity = 1
        self.cy_circle.collision_type = 1
        space.add(self.cy_body, self.cy_circle)
        self.size_hint = None, None
        self.size = radius*2, radius*2
        self.pos = pos[0] - radius, pos[1] - radius
        self.radius = radius
        self.initial_color = [1, 0, 128/255.]
        self.touch_color = [0, 1, 127/255.]

    def increase_radius(self):
        self.radius += 5

class ScreenTwo(Screen):
    no_of_widgets = NumericProperty(0)
    all_widgets = ListProperty()
    space = ObjectProperty()
    widget_to_increase = ObjectProperty()
    app = ObjectProperty()
    score = NumericProperty(0)

    def __init__(self, app, *args, **kwargs):
        super(ScreenTwo, self).__init__(*args, **kwargs)
        self.app = app
        self.init_physics() 
        Clock.schedule_interval(self.step, 1/FRAMES)

    def step(self, *args):
        self.space.step(1/FRAMES)
        self.update_objects()
        self.ids.label.text = "Score: " + str(int(self.score))

    def on_leave(self, *args):
        Clock.unschedule(self.step)

    def on_touch_down(self, touch, *args):
        if self.ids.back_button.collide_point(*touch.pos):
            self.app.switch_screen("one")
            return
        if self.ids.forward_button.collide_point(*touch.pos):
            self.app.switch_screen("three")
            return
        for item in self.all_widgets:
            if item.collide_point(*touch.pos):
                self.widget_to_increase = item
                return True


    def create_objects(self):
        for item in xrange(5):
            pos = [random.randint(0, Window.size[0]), random.randint(0, Window.size[1])]
            obj = CircleObject(pos=pos, radius=50, space=self.space)
            obj.cy_body.apply_impulse([random.randint(MIN_IMPULSE, MAX_IMPULSE), random.randint(MIN_IMPULSE, MAX_IMPULSE)])
            self.add_widget(obj)
            self.all_widgets.append(obj)
            self.no_of_widgets += 1

    def on_touch_up(self, *args):
        try:
            widg = self.widget_to_increase
            widg.canvas.children[0].rgb = widg.initial_color
        except Exception, e:
            print e
        self.widget_to_increase = 0

    def update_objects(self):
        score = 0
        for item in self.all_widgets:
            score += (item.radius * item.radius)
            if item == self.widget_to_increase:
                item.canvas.children[0].rgb = item.touch_color
                item.increase_radius()
                position = item.cy_body.position
                velocity = item.cy_body.velocity
                self.space.remove(item.cy_body)
                self.space.remove(item.cy_circle)
                radius = item.radius
                item.cy_body = cy.Body(100, 1e9)
                item.cy_body.position = position
                item.cy_body.velocity = velocity
                item.cy_circle = cy.Circle(item.cy_body, item.radius)
                item.cy_circle.elasticity = 1
                item.cy_circle.collision_type = 1
                self.space.add(item.cy_body, item.cy_circle)
            p = item.cy_body.position
            radius = item.radius
            item.size = radius * 2, radius * 2
            item.pos = p.x - radius, p.y - radius
        self.score = ((3.14 * score) / (Window.size[0] * Window.size[1])) * 100 * (1000/65.)
        self.score /= 10.
        if self.score >= 100 :
            self.on_leave()


    def init_physics(self, *args):
        self.space = cy.Space()
        self.space.gravity = 0, 0
        self.space.iterations = FRAMES
        #self.space.sleep_time_threshold = .5
        #self.space.collision_slop = 0 
        self.create_objects()
        self.set_boundary()
        self.arbiter = cy.Arbiter(self.space)
        self.space.add_collision_handler(1, 1, begin = self.collision_between_balls)

    
    def collision_between_balls(self, space, arbiter, *args, **kwargs):
        widg = self.widget_to_increase
        if widg:
            if widg.cy_circle in arbiter.shapes:
                pass
                #self.on_leave()
                #self.lose_popup.open()
        return True

    def set_boundary(self):
        x0, y0 = 0, 0
        x1, y1 = Window.size
        a = cy.Segment(self.space.static_body, cy.Vec2d(0, 0), cy.Vec2d(0, 0), 0)
        a.elasticity = 1
        b = cy.Segment(self.space.static_body, cy.Vec2d(0, 0), cy.Vec2d(0, 0), 0)
        b.elasticity = 1
        c = cy.Segment(self.space.static_body, cy.Vec2d(0, 0), cy.Vec2d(0, 0), 0)
        c.elasticity = 1
        d = cy.Segment(self.space.static_body, cy.Vec2d(0, 0), cy.Vec2d(0, 0), 0)
        d.elasticity = 1
        a.a = (x0, y0)
        a.b = (x1, y0)
        b.a = (x1, y0)
        b.b = (x1, y1)
        c.a = (x1, y1)
        c.b = (x0, y1)
        d.a = (x0, y1)
        d.b = (x0, y0)
        self.space.add(a)
        self.space.add(b)
        self.space.add(c)
        self.space.add(d)
