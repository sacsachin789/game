"""
"""

#STL


#kivy
from kivy.properties import NumericProperty, ObjectProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen

#3rd party
import cymunk as cy


#Custom import


class CircleObject(Widget):
    radius = NumericProperty()
    cy_body = ObjectProperty()
    cy_circle = ObjectProperty()
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


class ScreenThree(Screen):
    space = ObjectProperty()
    ball = ObjectProperty()


    def __init__(self, app, *args, **kwargs):
        super(ScreenThree, self).__init__(*args, **kwargs)
        self.app = app
