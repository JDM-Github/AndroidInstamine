from kivy.config import Config
WIDTH  = int(750  * 0.5) 
HEIGHT = int(1400 * 0.5) 
Config.set('graphics', 'width', WIDTH)
Config.set('graphics', 'height', HEIGHT)
Config.set('graphics', 'resizable', 0)
Config.write()

from kivy.utils import platform
from kivy.core.window import Window

if platform != "Android":
	Window.size  = (WIDTH, HEIGHT)
	Window.top   = 30
	Window.left  = 1

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens import LoginScreen, RegisterScreen, VerificationScreen, SuccessScreen
from theme import OriginalColor

DEVELOPMENT = False
class Manager(ScreenManager):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		if platform != "Android":
			self.size = (WIDTH, HEIGHT)

		self.theme = OriginalColor()
		self.url_link = "http://localhost:8888"


		if not DEVELOPMENT:
			self.url_link = "https://test888.netlify.app"

class MyApp(App):
	def build(self):
		sm = Manager()
		login    = LoginScreen(name='login')
		register = RegisterScreen(name='register')
		verify   = VerificationScreen(name='verify')
		success  = SuccessScreen(name='success')
		sm.add_widget(login)
		sm.add_widget(register)
		sm.add_widget(verify)
		sm.add_widget(success)

		login.display_design()
		register.display_design()
		verify.display_design()
		success.display_design()


		return sm

if __name__ == '__main__':
	MyApp().run()
