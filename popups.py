#STL
import random

#3rd party

#Kivy
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty

#Custom

"""
    This popup is only used when the app is used for the first time
"""
class UIDCheckerPopup(Popup):
    app = ObjectProperty()
    def __init__(self, app, *args, **kwargs):
        super(UIDCheckerPopup, self).__init__(*args, **kwargs)
        self.app = app

    def save_uid(self):
        uid = generate_uid()
        user_name = str(self.ids.user_name.text)
        if len(user_name):
            self.app.user_uid = uid
            self.app.user_name = user_name
            self.app.save_uid()
            self.dismiss()


def generate_uid():
    a = ""
    for _ in xrange(6):
        a += str(random.randint(0, 9))
    return a



class OfflinePopup(Popup):
    pass
