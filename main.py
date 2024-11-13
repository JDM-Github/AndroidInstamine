import re
import json

from kivy.config import Config

from screens.live_screen import LiveScreen
from screens.seller_product import SellerProductScreen
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

# from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from screens import LoginScreen, RegisterScreen, HomeScreen, ProductScreen, VerifyScreen, CheckoutScreen
from theme import OriginalColor
from kivy.properties import ObjectProperty

import yt_dlp
import socketio

from kivy.lang import Builder
Builder.load_file('widgets/widgets.kv')
Builder.load_file('screens/screens.kv')
Builder.load_file('screens/product_screen.kv')
Builder.load_file('screens/checkout_screen.kv')
Builder.load_file('screens/live_screen.kv')
Builder.load_file('popup/start_stream.kv')
Builder.load_file('popup/add_product.kv')
Builder.load_file('popup/chat_popup.kv')
Builder.load_file('popup/edit_profile.kv')
Builder.load_file('popup/payment.kv')

# ETO UNG MANAGER, SYA LAHAT NG MAMANAGE NG LAHAT
class Manager(ScreenManager):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.size = Window.size
		self.transition = FadeTransition(duration=0.1)

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
			self.home.update_button_active('home')

		self.sio = socketio.Client()

	def add_all_screen(self):
		self.home     = HomeScreen(name="home")
		self.login    = LoginScreen(name='login')
		self.register = RegisterScreen(name='register')
		self.product  = ProductScreen(name='product')
		self.verify   = VerifyScreen(name="verify")
		self.checkout = CheckoutScreen(name="checkout")
		self.live     = LiveScreen(name="live")

		self.seller_product  = SellerProductScreen(name='seller-product')

		self.add_widget(self.login)
		self.add_widget(self.register)
		self.add_widget(self.home)
		self.add_widget(self.product)
		self.add_widget(self.verify)
		self.add_widget(self.checkout)
		self.add_widget(self.seller_product)
		self.add_widget(self.live)

		self.display_all_screen()

	def display_all_screen(self):
		self.login   .display_design()
		self.register.display_design()
		self.home    .display_design()
		self.product .display_design()
		self.verify  .display_design()
		self.checkout.display_design()
		self.live    .display_design()
		self.seller_product.display_design()

	def change_product(self, is_my_product, product_id):
		self.transition = FadeTransition(duration=0.2)

		if is_my_product:
			self.seller_product.update_product(product_id)
			self.current = "seller-product"
		else:
			self.product.update_product(product_id)
			self.current = "product"
	
	def change_screen(self, screen):
		self.current = screen

	# LOAD CONFIG UTILITY
	def load_json_config(self, filepath):
		with open(filepath, 'r', encoding='utf-8') as file:
			content = file.read()

		# USED TO ALLOW COMMENT IN JSON
		content = re.sub(r'//.*', '', content)
		content = re.sub(r'/\*[\s\S]*?\*/', '', content)
		return json.loads(content)

	# SAVE JSON
	def save_json_config(self, filepath, data):
		with open(filepath, 'w') as file:
			json.dump(data, file, indent=4)
	
	def get_stream_url(self, yt_url):
		ydl_opts = {'format': 'best'}
		with yt_dlp.YoutubeDL(ydl_opts) as ydl:
			try:
				info_dict = ydl.extract_info(yt_url, download=False)
				formats = info_dict.get('formats', None)		
				for f in formats:
					if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
						return f['url']
			except Exception as e:
				print(e)
				return None



class InstaminApp(MDApp):
	sm = ObjectProperty(Manager())

	def build(self):
		return self.sm

	def on_start(self):
		try:
			self.sm.sio.connect('http://localhost:3000')
		except:
			print("NO")
		pass
		# yt_url = "https://www.youtube.com/live/1Xjn_qRCOtc"
		# stream_url = self.sm.get_stream_url(yt_url)
		# self.sm.sio.emit('start_stream', stream_url)

if __name__ == '__main__':
	InstaminApp().run()
