__author__ = "Sachin Railhan"
__version__ = "1.0"

#STD Library Imports
import json
from functools import partial
import os
os.environ["KIVY_AUDIO"] = "pygame"
#3rd Party Imports


#Kivy Imports
from kivy.config import Config

#Config.set("graphics", "fullscreen", "auto")
from kivy.app import App
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen, FallOutTransition
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.clock import Clock


#Custom Imports
from screens.menu import MenuScreen
from screens.one import ScreenOne
from screens.two import ScreenTwo
from screens.three import ScreenThree


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
        Clock.schedule_once(partial(self.app.switch_screen, "menu"), 1.5)




class GameApp(App):
    sm = ObjectProperty()
    screen = ObjectProperty()
    user_online = BooleanProperty()
    user_name = StringProperty()
    user_uid = StringProperty()
    score = NumericProperty(0)
    opponent_score = NumericProperty(0)

    def build(self):
        self.sm = ScreenManager(transition = FallOutTransition(duration = 0.3))
        self.switch_screen("logo")
        return self.sm

    def switch_screen(self, screen_name, *args):
        if screen_name == "logo":
            self.screen = LogoScreen(name="logo", app=self)
        elif screen_name == "menu":
            self.screen = MenuScreen(name="menu", app=self)
        elif screen_name == "one":
            self.screen = ScreenOne(name="one", app=self)
        elif screen_name == "two":
            self.screen = ScreenTwo(name="two", app=self)
        elif screen_name == "three":
            self.screen = ScreenThree(name="three", app=self)
        self.sm.clear_widgets()
        self.sm.add_widget(self.screen)
        self.sm.current = self.screen.name

    def save_uid(self):
        with open("data/uid.json", "w+") as f:
            data = {}
            data["uid"] = self.user_uid
            data["uname"] = self.user_name
            json.dump(data, f)

        

if __name__ == "__main__":
    DEVID = "MAIN"
    game = GameApp()
    game.run()
