from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens import LoginScreen, RegisterScreen, VerificationScreen, SuccessScreen

class MyApp(App):
	def build(self):
		sm = ScreenManager()
		sm.add_widget(LoginScreen(name='login'))
		sm.add_widget(RegisterScreen(name='register'))
		sm.add_widget(VerificationScreen(name='verify'))
		sm.add_widget(SuccessScreen(name='success'))
		return sm

if __name__ == '__main__':
	MyApp().run()
