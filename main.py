import re
import json


# setup the graphics

from kivy.config import Config
WIDTH  = int(750  * 0.5) 
HEIGHT = int(1400 * 0.5) 
Config.set('graphics', 'width', WIDTH)
Config.set('graphics', 'height', HEIGHT)
Config.set('graphics', 'resizable', 0)
Config.write()

from kivy.utils import platform
from kivy.core.window import Window


if platform == "win":
	Window.size  = (WIDTH, HEIGHT)
	Window.top   = 30
	Window.left  = 1

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens import LoginScreen, RegisterScreen, HomeScreen
from theme import OriginalColor



class Manager(ScreenManager):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.size = Window.size

		self.theme = OriginalColor()
		self.main_config = self.load_json_config("config.json")
		self.main_state = self.load_json_config("state.json")



	def load_json_config(self, filepath):
		with open(filepath, 'r') as file:
			content = file.read()

		content = re.sub(r'//.*', '', content)
		content = re.sub(r'/\*[\s\S]*?\*/', '', content)
		return json.loads(content)



	def save_json_config(self, filepath, data):
		with open(filepath, 'w') as file:
			json.dump(data, file, indent=4)


class MyApp(App):

	def build(self):

		sm       = Manager()

		home     = HomeScreen(name="home")
		login    = LoginScreen(name='login')
		register = RegisterScreen(name='register')
		# verify   = VerificationScreen(name='verify')

		sm.add_widget(login)
		sm.add_widget(register)
		# sm.add_widget(verify)
		sm.add_widget(home)

		login   .display_design()
		register.display_design()
		# verify  .display_design()
		home    .display_design()

		if not sm.main_state['already_login']:
			sm.current = "login"
		else:
			sm.current = "home"

		return sm

if __name__ == '__main__':
	MyApp().run()
