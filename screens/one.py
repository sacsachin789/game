#STL
import random
from functools import partial



#kivy
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import ListProperty, ObjectProperty, NumericProperty, BooleanProperty
from kivy.core.audio import SoundLoader as SL


#3rd


#custom

X = Window.size[0]
Y = Window.size[1]
CLOUD_WIDTH = X/5.
CLOUD_HEIGHT = Y/5.
NO_WIDTH = X/15.
NO_HEIGHT = Y/15.


class Background(Image):
    def __init__(self):
        super(Background, self).__init__()
        self.size_hint = [None, None]
        self.size = [X, Y]
        self.source = "static/landscape.png"
        self.pos = [0, 0]
        self.allow_stretch = True
        self.keep_ratio = False

class No(Image):
    screen = ObjectProperty()
    cloud = ObjectProperty()
    index = NumericProperty()
    question = NumericProperty()
    answer = BooleanProperty()

    def __init__(self, index, question, answer, cloud, screen):
        super(No, self).__init__()
        self.cloud = cloud
        self.index = index
        self.size_hint = [None, None]
        self.size = [NO_WIDTH, NO_HEIGHT]
        if question == 2 or question == 6:
            self.source = "static/questions/question2/{1}.zip".format(question, index-1)
        else:
            self.source = "static/questions/question{0}/{1}.png".format(question, index-1)
        self.pos = [cloud.pos[0] + CLOUD_WIDTH/3., cloud.pos[1]]
        self.screen = screen
        self.answer = answer
        self.animate()

    def animate(self):
        anim = Animation(y = Y/10., t="out_bounce", d = 3)
        anim.start(self)


class Drop(Image):
    index = NumericProperty()

    def __init__(self, index):
        super(Drop, self).__init__()
        self.size_hint = [None, None]
        self.index = index
        self.size = [X/15., CLOUD_HEIGHT/15.]
        self.source = "static/drop.png"
        self.pos = [X*((index-1)*0.0125), Y*(random.uniform(1.1, 2.0))]
        self.animate()

    def repeat(self, *args):
        self.pos = [X*((self.index-1)*0.04), Y*(random.uniform(1.1, 1.35))]
        self.animate()

    def animate(self):
        anim = Animation(y = 0, d = random.uniform(2, 4))
        anim.start(self)
        anim.bind(on_complete = self.repeat)


class Cloud(Image):
    place = BooleanProperty(0)
    index = NumericProperty()

    def __init__(self, index):
        super(Cloud, self).__init__()
        self.size_hint = [None, None]
        self.index = index
        self.size = [CLOUD_WIDTH, CLOUD_HEIGHT]
        self.source = "static/cloud_{0}.png".format(index)
        self.pos = [X*((index-1)*0.3), Y*(0.9 - ((index-1)*0.05)) - self.size[1] ]
        self.animate()

    def animate(self, *args):
        d = random.uniform(2, 5)
        if self.place:
            anim = Animation(x = X*((self.index-1)*0.3), d = d)
            self.place = 0
        else:
            anim = Animation(x = (X*(self.index*0.3)) - self.size[0]/2., d = d)
            self.place = 1
        anim.start(self)
        anim.bind(on_complete = self.animate)

class ScreenOne(Screen):
    app = ObjectProperty()
    clouds = ListProperty()
    questions = ListProperty()
    answers = ListProperty()
    options = ListProperty()
    label = ObjectProperty()
    index = NumericProperty(0)
    r = NumericProperty(120)
    g = NumericProperty(133)
    b = NumericProperty(118)
    thunder = ObjectProperty()
    rain_music = ObjectProperty()
    
    def __init__(self, app, *args, **kwargs):
        super(ScreenOne, self).__init__(*args, **kwargs)
        self.app = app
        self.questions = ["44%6", "x*x = 4 so x is", "Largest Democracy in the World?", "When did World War 2 begin?", "Total no of kivy properties", "Planet with rings", "NYC", "Speed of light(km/s)"]
        self.answers = [1, 3, 3, 2, 3, 2, 1, 2]
        self.thunder = SL.load("static/lightning.wav")
        self.rain_music = SL.load("static/rain.wav")
        self.rain_music.loop = True
        assert len(self.questions) == len(self.answers)
        self.create_objects()
        self.update()
        Clock.schedule_interval(self.update, 4)

    def create_objects(self, *args):
        self.clear_widgets()
        self.add_widget(Background())
        self.create_rain()
        self.score_label = Label( pos = [0,  0],
                size_hint = [1, 0.1],
                font_name = "static/cartoon.ttf",
                font_size = Y/15.,
                text_size = [X, None],
                halign = "center",
                text = "Score: 0"
                )
        self.label = Label( pos = [0,  Y * 0.4],
                font_name = "static/cartoon.ttf",
                font_size = Y/15.,
                text_size = [X, None],
                halign = "center"
                )
        self.back_btn = Button(size_hint = [0.05, 0.05],
                pos = [X*0.025, Y*0.925],
                font_name = "static/cartoon.ttf",
                font_size = Y/15.,
                halign = "center",
                text = "<"
                )
        self.forward_btn = Button(size_hint = [0.05, 0.05],
                pos = [X*0.925, Y*0.925],
                font_name = "static/cartoon.ttf",
                font_size = Y/15.,
                halign = "center",
                text = ">"
                )
        self.add_widget(self.back_btn)
        self.add_widget(self.forward_btn)
        self.add_widget(self.label)
        self.add_widget(self.score_label)
        for i in xrange(3):
            cloud = Cloud(i+1)
            self.clouds.append(cloud)
            self.add_widget(cloud)

    def create_rain(self):
        for i in xrange(1, 81):
            drop = Drop(i)
            self.add_widget(drop)

    def go_to(self, screen):
        self.app.switch_screen(screen)

    def update(self, *args):
        if self.index >= 8:
            self.app.switch_screen("two")
            return True
        for i in self.options:
            self.remove_widget(i)
        self.options = []
        self.label.text = self.questions[self.index]
        self.label.texture_update()
        for i in xrange(3):
            item = No(i+1, self.index, i+1 == self.answers[self.index], self.clouds[i], self) 
            self.add_widget(item)
            self.options.append(item)
        self.index += 1

    def thunderstorm(self, start, *args):
        if start:
            self.r = 0
            self.g = 0
            self.b = 0
            Clock.schedule_once(partial(self.thunderstorm, 0), 0.2)
            return
        self.r = 120
        self.g = 133
        self.b = 118
        return

    def on_touch_down(self, touch, *args):
        if self.back_btn.collide_point(*touch.pos):
            self.go_to("menu")
            return 
        if self.forward_btn.collide_point(*touch.pos):
            self.go_to("two")
            return
        for item in self.options:
            if item.collide_point(*touch.pos):
                if not item.answer:
                    self.thunderstorm(1)
                    self.thunder.play()
                    Clock.unschedule(self.update)
                    self.update()
                    Clock.schedule_interval(self.update, 4)
                    self.app.score -= 5
                    self.score_label.text = "Score: {0}".format(self.app.score)
                else:
                    Clock.unschedule(self.update)
                    self.update()
                    Clock.schedule_interval(self.update, 4)
                    self.app.score += 5
                    self.score_label.text = "Score: {0}".format(self.app.score)



    def on_pre_leave(self, *args):
        Clock.unschedule(self.update)
        self.rain_music.unload()

    def on_enter(self, *args):
        if self.app.music:
            self.app.music.unload()
        self.rain_music.play()
