"""
    Description
"""
#STL
import os, sys, inspect, random



# Adding parent directory to sys.path 
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

#3rd party

#kivy
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, BooleanProperty
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.label import Label

#Custom


X, Y = Window.size
FRAMES = 30.0

class BackImage(Image):
    def __init__(self, source, *args, **kwargs):
        super(BackImage, self).__init__(*args, **kwargs)
        self.size_hint = [None, None] 
        self.size = [X*0.8, Y*0.7]
        self.pos = [X*0.1, Y*0.2]
        self.allow_stretch = True
        self.keep_ratio = True
        self.source = str(source)

    def animate(self):
        anim = Animation(x=X*0.1, t="in_quint", d=1)
        anim.start(self)

    def change_source(self, source):
        self.source = str(source)

class ScreenHelp(Screen):
    back_img = ObjectProperty()
    app = ObjectProperty()
    index = NumericProperty(1)
    label = ObjectProperty()
    label_list = ListProperty()

    def __init__(self, app, *args, **kwargs):
        super(ScreenHelp, self).__init__(*args, **kwargs)
        self.app = app
        self.label_list = ["According to question only one of the options is correct.Touch the correct one.", "Touch the circles to increase their size.Note while increasing size, circle should not come in contact with other circles.", "These stages test your problem solving techniques.", "Use arrow keys or wasd to play.", "Hint for next stage is given when you successfully pass the current stage", "I hope the stages are self explanatory.If not use your brain.", "Hope you like this game.", "Made by @sacsachin789 and @nitinsaroha (Github) for kivy contest 2014 at New Delhi, India"]
        self.label = Label( pos = [0,  Y*0.05],
                size_hint = [1, 0.1],
                font_name = "static/cartoon.ttf",
                font_size = Y/15.,
                text_size = [X, None],
                halign = "center",
                )
        self.add_widget(self.label)
        self.back_img = BackImage("static/help/{0}.png".format(self.index))
        self.add_widget(self.back_img)
        self.animate()

    def animate(self, *args):
        if self.index == 8:
            self.app.switch_screen("menu")
            return
        self.label.text = self.label_list[self.index-1]
        self.back_img.change_source("static/help/{0}.png".format(self.index))
        self.index += 1
        Clock.schedule_once(self.animate, 4)

    def on_pre_leave(self, *args):
        Clock.unschedule(self.animate)
