from kivy.config import Config
WIDTH  = int(720 * 0.5)
HEIGHT = int(1400 * 0.5)
Config.set('graphics', 'width', WIDTH)
Config.set('graphics', 'height', HEIGHT)
Config.set('graphics', 'resizable', False)
Config.write()

from android.permissions import request_permissions, Permission
request_permissions([Permission.INTERNET])

import os
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.label import Label
from database import DatabaseHandler

class MainApp(App):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		# Connect the database
		self.dbhandler = DatabaseHandler(
		  host     = "jdm-master-15017.7tt.aws-us-east-1.cockroachlabs.cloud",
		  username = "jdm",
		  password = "bmKyHDrpbE6nP2qTiCc0nA",
		  port     = "26257"
		)
		self.dbhandler.connect()

	def build(self):
		return Label(text=str(self.dbhandler.is_connected()))

if __name__ == "__main__":
	MainApp().run()
