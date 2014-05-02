"""
    Description
"""
#STL
import os, sys, inspect, json



# Adding parent directory to sys.path 
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

#3rd party

#kivy
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

#Custom

class MenuScreen(Screen):
    app = ObjectProperty()
    def __init__(self, app, *args, **kwargs):
        super(MenuScreen, self).__init__(*args, **kwargs)
        self.app = app

