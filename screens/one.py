from string import lowercase
from functools import partial
import os, inspect, sys
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty, BooleanProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

class ScreenOne(Screen):
    app = ObjectProperty()
    question_content = ListProperty()
    content_marker = NumericProperty()
    label_content = StringProperty()
    music = ObjectProperty()
    score = NumericProperty(0)
    state = BooleanProperty(0)
    counter = NumericProperty(60)

    def __init__(self, app, *args, **kwargs):
        super(ScreenOne, self).__init__(*args, **kwargs)
        self.app = app
        self.init_game()
        self.keyboard = Window.request_keyboard(self.keyboard_closed, self, 'text')
        self.keyboard.bind(on_key_down=self.on_keyboard_down)
        self.music = SoundLoader.load('static/screen1_music.wav')
        self.music.loop = True

    def on_enter(self):
        self.music.play()

    def init_game(self):
        self.question_content = ['press start and type as i say hello my name is kivame',
         'i am a small kivy app',
         'i am very unique bcoz i m',
         'first multiplayer game created in kivy',
         'yes firzt but i am in prolbem today',
         'save my townz from the evil elze we alls zill die',
         'help pleaze az thee dere huh',
         'yes rhis is lazt menemy',
         'hang on yessssssssssss thank you',
         'remember i should win the kivy contest']
        self.marker = 0
        self.content_marker = 0
        self.label_content = self.question_content[self.marker]
        self.ids.label.text = self.label_content
        self.lowercase_set = set(lowercase)

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        text = str(text)
        if text in self.lowercase_set or text is ' ':
            self.button_pressed(text)

    def start_game(self):
        if self.state:
            return
        self.state = 1
        label = self.ids.time_label
        label.text = str(self.counter)
        Clock.schedule_once(self.change_counter, 1)

    def change_counter(self, *args):
        self.counter -= 1
        label = self.ids.time_label
        label.text = str(self.counter)
        if self.counter:
            Clock.schedule_once(self.change_counter, 1)
        else:
            self.state = 0

    def button_pressed(self, text):
        if not self.state:
            return
        label = self.ids.label
        if self.marker == 10:
            return
        item = self.label_content[0]
        if item == ' ':
            item2 = self.label_content[1]
        else:
            item2 = None
        text = str(text)
        if text == item:
            self.label_content = self.label_content[1:]
        elif text == item2:
            self.label_content = self.label_content[2:]
        if len(self.label_content) == 0:
            self.marker += 1
            self.score += 10
            if self.marker == 10:
                return
            self.label_content = self.question_content[self.marker]
        label.text = self.label_content

    def keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self.on_keyboard_down)

    def on_leave(self):
        self.music.stop()
        self.music.unload()
