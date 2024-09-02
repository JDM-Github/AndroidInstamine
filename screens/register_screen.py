import json
import requests  # Import the requests library
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

class RegisterScreen(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		layout = BoxLayout(orientation='vertical', padding=10)
		
		self.username = TextInput(hint_text="Username", multiline=False)
		self.email    = TextInput(hint_text="Email", multiline=False)
		self.password = TextInput(hint_text="Password", multiline=False, password=True)
		
		register_btn      = Button(text="Register", on_press=self.register)
		back_to_login_btn = Button(text="Back to Login", on_press=self.go_to_login)
		
		layout.add_widget(Label(text="Register"))
		layout.add_widget(self.username)
		layout.add_widget(self.email)
		layout.add_widget(self.password)
		layout.add_widget(register_btn)
		layout.add_widget(back_to_login_btn)
		self.add_widget(layout)

	def register(self, instance):
		data = {
			'username': self.username.text,
			'email': self.email.text,
			'password': self.password.text
		}
		try:
			response = requests.post(
				f'{self.manager.url_link}/.netlify/functions/api/register',
				headers={'Content-Type': 'application/json'},
				data=json.dumps(data)
			)
			response.raise_for_status()  # Raise an error for bad responses
			result = response.json()
			self.on_success(None, result)
		except requests.RequestException as e:
			self.on_error(None, e)

	def on_success(self, request, result):
		print(result['otp'])
		self.manager.get_screen('verify').to_verify = result['otp']
		self.manager.current = 'verify'

	def on_failure(self, request, result):
		print("Registration failed.")
		print(result)
		self.show_error_popup(result['message'])

	def on_error(self, request, error):
		print(f"Error: {error}")
		self.show_error_popup('Failed to send request.')

	def go_to_login(self, instance):
		self.manager.current = 'login'

	def show_error_popup(self, message):
		popup = Popup(title='Register Failed',
					  content=Label(text=message),
					  size_hint=(0.8, 0.4))
		popup.open()
