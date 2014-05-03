#STL
import random

#3rd party

#Kivy
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty

#Custom

"""
    Popup when a screen is successfully passed.
"""
class WinPopup(Popup):
    app = ObjectProperty()
    next_screen = StringProperty()
    title = StringProperty()
    label_text = StringProperty()


    def __init__(self, app, title, label_text, next_screen, *args, **kwargs):
        super(WinPopup, self).__init__(*args, **kwargs)
        self.app = app
        self.title = title
        self.label_text = label_text
        self.next_screen = next_screen

    def on_dismiss(self, *args):
        self.app.switch_screen(self.next_screen)
