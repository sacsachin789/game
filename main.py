__author__ = "Sachin Railhan"
__version__ = "1.0"

#STD Library Imports
from functools import partial
import os
os.environ["KIVY_AUDIO"] = "pygame"
#3rd Party Imports


#Kivy Imports
from kivy.config import Config

Config.set("graphics", "fullscreen", "auto")
from kivy.app import App
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen, FallOutTransition
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.clock import Clock


#Custom Imports
from screens.menu import ScreenMenu
from screens.temp import ScreenTemp
from screens.one import ScreenOne
from screens.two import ScreenTwo
from screens.three import ScreenThree
from screens.four import ScreenFour
from screens.five import ScreenFive
from screens.six import ScreenSix
from screens.seven import ScreenSeven
from screens.eight import ScreenEight
from screens.nine import ScreenNine
from screens.help import ScreenHelp


class LogoScreen(Screen):
    app = ObjectProperty()
    def __init__(self, app, *args, **kwargs):
        super(LogoScreen, self).__init__(*args, **kwargs)
        self.app = app
        self.img = Image(source = "static/logo.png")
        self.img.pos = [0, 500]
        self.add_widget(self.img)

    def on_enter(self):
        anim = Animation(y = 0, t = "out_bounce")
        anim.start(self.img)
        Clock.schedule_once(partial(self.app.switch_screen, "menu"), 3)




class GameApp(App):
    sm = ObjectProperty()
    screen = ObjectProperty()
    score = NumericProperty(0)
    is_touch = BooleanProperty()
    music = ObjectProperty()

    def build(self):
        self.sm = ScreenManager(transition = FallOutTransition(duration = 0.3))
        self.switch_screen("logo")
        try:
            import android
            self.is_touch = 1
        except ImportError:
            self.is_touch = 0
        return self.sm

    def switch_screen(self, screen_name, *args):
        if screen_name == "logo":
            self.screen = LogoScreen(name="logo", app=self)
        elif screen_name == "menu":
            self.screen = ScreenMenu(name="menu", app=self)
        elif screen_name == "one":
            self.screen = ScreenOne(name="one", app=self)
        elif screen_name == "two":
            self.screen = ScreenTwo(name="two", app=self)
        elif screen_name == "three":
            self.screen = ScreenThree(name="three", app=self)
        elif screen_name == "four":
            self.screen = ScreenFour(name="four", app=self)
        elif screen_name == "temp":
            self.screen = ScreenTemp(name="temp", app=self)
        elif screen_name == "five":
            self.screen = ScreenFive(name="five", app=self)
        elif screen_name == "six":
            self.screen = ScreenSix(name="six", app=self)
        elif screen_name == "seven":
            self.screen = ScreenSeven(name="seven", app=self)
        elif screen_name == "eight":
            self.screen = ScreenEight(name="eight", app=self)
        elif screen_name == "nine":
            self.screen = ScreenNine(name="nine", app=self)
        elif screen_name == "help":
            self.screen = ScreenHelp(name="help", app=self)
        self.sm.clear_widgets()
        self.sm.add_widget(self.screen)
        self.sm.current = self.screen.name

GameApp().run()
