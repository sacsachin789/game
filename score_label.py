from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.core.window import Window

X, Y = Window.size


class ScoreLabel(Label):
    app = ObjectProperty()
    def __init__(self, app, *args, **kwargs):
        super(ScoreLabel, self).__init__(*args, **kwargs)
        self.pos = [0,  0]
        self.size_hint = [1, 0.1]
        self.font_name = "static/cartoon.ttf"
        self.font_size = Y/15.
        self.text_size = [X, None]
        self.halign = "center"
