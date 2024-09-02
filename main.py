from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens import LoginScreen, RegisterScreen, VerificationScreen, SuccessScreen

DEVELOPMENT = True
class Manager(ScreenManager):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.url_link = "http://localhost:8888"

		if not DEVELOPMENT:
			self.url_link = "https://test888.netlify.app"

class MyApp(App):
	def build(self):
		sm = Manager()
		sm.add_widget(LoginScreen(name='login'))
		sm.add_widget(RegisterScreen(name='register'))
		sm.add_widget(VerificationScreen(name='verify'))
		sm.add_widget(SuccessScreen(name='success'))
		return sm

if __name__ == '__main__':
	MyApp().run()
