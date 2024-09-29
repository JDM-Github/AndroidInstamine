import re
import json

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
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from screens import LoginScreen, RegisterScreen, HomeScreen, ProductScreen
from theme import OriginalColor


# ETO UNG MANAGER, SYA LAHAT NG MAMANAGE NG LAHAT
class Manager(ScreenManager):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.size = Window.size

		# THE THEME HANDLER
		self.theme = OriginalColor()

		# THE MAIN CONFIGURATION, EXAMPLE MGA MESSAGE
		self.main_config = self.load_json_config("config.json")

		# THE MAIN STATE, LIKE A SESSION
		self.main_state = self.load_json_config("state.json")

		# PAG ALREADY LOGIN NA, PUMUNTA SA HOME SCREEN
		self.add_all_screen()
		if not self.main_state['already_login']:
			self.current = "login"
		else:
			self.current = "home"

	def add_all_screen(self):
		self.home     = HomeScreen(name="home")
		self.login    = LoginScreen(name='login')
		self.register = RegisterScreen(name='register')
		self.product  = ProductScreen(name='product')

		self.add_widget(self.login)
		self.add_widget(self.register)
		self.add_widget(self.home)
		self.add_widget(self.product)

		self.display_all_screen()

	def display_all_screen(self):
		self.login   .display_design()
		self.register.display_design()
		self.home    .display_design()
		self.product .display_design()

	def change_product(self, product_id):
		self.transition = FadeTransition(duration=0.5)
		self.product.update_product(product_id)
		self.current = "product"

	# LOAD CONFIG UTILITY
	def load_json_config(self, filepath):
		with open(filepath, 'r') as file:
			content = file.read()

		# USED TO ALLOW COMMENT IN JSON
		content = re.sub(r'//.*', '', content)
		content = re.sub(r'/\*[\s\S]*?\*/', '', content)
		return json.loads(content)

	# SAVE JSON
	def save_json_config(self, filepath, data):
		with open(filepath, 'w') as file:
			json.dump(data, file, indent=4)



class MyApp(App):

	def build(self):
		return Manager()

if __name__ == '__main__':
	MyApp().run()
