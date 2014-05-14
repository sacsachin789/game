"""
    Description
"""
#STL
import os, sys, inspect, json, random



# Adding parent directory to sys.path 
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

#3rd party
import cymunk as cy

#kivy
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, BooleanProperty
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.animation import Animation

#Custom


X, Y = Window.size
FRAMES = 30.0

class Play(Image):
    def __init__(self, *args, **kwargs):
        super(Play, self).__init__(*args, **kwargs)
        self.size_hint = [None, None] 
        self.size = [X/3., Y/3.]
        self.pos = [X*(-0.35), Y*0.1]
        self.allow_stretch = True
        self.keep_ratio = True
        self.source = "static/play_300.png"

    def animate(self):
        anim = Animation(x=X*0.1, t="in_quint", d=1)
        anim.start(self)

class Help(Image):
    def __init__(self, *args, **kwargs):
        super(Help, self).__init__(*args, **kwargs)
        self.size_hint = [None, None] 
        self.size = [X/3., Y/3.]
        self.pos = [X*1.1, Y*0.55]
        self.allow_stretch = True
        self.keep_ratio = True
        self.source = "static/help_300.png"

    def animate(self):
        anim = Animation(x=X*0.55, t="in_quint", d=1)
        anim.start(self)

class ScreenMenu(Screen):
    play_wdg = ObjectProperty()
    help_wdg = ObjectProperty()
    app = ObjectProperty()
    r = NumericProperty(random.randrange(0, 255))
    g = NumericProperty(random.randrange(0, 255))
    b = NumericProperty(random.randrange(0, 255))
    r_up = BooleanProperty(0)
    g_up = BooleanProperty(0)
    b_up = BooleanProperty(0)

    def __init__(self, app, *args, **kwargs):
        super(ScreenMenu, self).__init__(*args, **kwargs)
        self.app = app
        self.play_wdg = Play()
        self.help_wdg = Help()
        self.add_widget(self.play_wdg)
        self.add_widget(self.help_wdg)
        self.animate()
        Clock.schedule_interval(self.animate, 1/40.)

    def on_touch_down(self, touch):
        if self.play_wdg.collide_point(*touch.pos):
            self.app.switch_screen("one")
        elif self.help_wdg.collide_point(*touch.pos):
            self.app.switch_screen("help")

    def animate(self, *args):
        if self.r >= 255:
            self.r_up = 0
        elif self.r <= 0:
            self.r_up = 1
        if self.g >= 255:
            self.g_up = 0
        elif self.g <= 0:
            self.g_up = 1
        if self.b >= 255:
            self.b_up = 0
        elif self.b <= 0:
            self.b_up = 1
        if self.r_up:
            self.r += 1
        else:
            self.r -= 1
        if self.g_up:
            self.g += 1
        else:
            self.g -= 1
        if self.b_up:
            self.b += 1
        else:
            self.b -= 1

    def on_enter(self, *args):
        self.play_wdg.animate()
        self.help_wdg.animate()
