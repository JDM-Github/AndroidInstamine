import json
import requests  # Import the requests library
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

class LoginScreen(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		layout = BoxLayout(orientation='vertical', padding=10)

		self.username = TextInput(hint_text="Username", multiline=False)
		self.password = TextInput(hint_text="Password", multiline=False, password=True)
		
		login_btn = Button(text="Login", on_press=self.login)
		register_btn = Button(text="Go to Register", on_press=self.go_to_register)
		
		layout.add_widget(Label(text="Login"))
		layout.add_widget(self.username)
		layout.add_widget(self.password)
		layout.add_widget(login_btn)
		layout.add_widget(register_btn)
		
		self.add_widget(layout)

	def login(self, instance):
		data = {
			'username': self.username.text,
			'password': self.password.text
		}
		# Use requests to make a POST request
		try:
			response = requests.post(
				f'{self.manager.url_link}/.netlify/functions/api/login',
				headers={'Content-Type': 'application/json'},
				data=json.dumps(data)
			)
			response.raise_for_status()  # Raise an error for bad responses
			result = response.json()  # Parse JSON response
			self.on_success(None, result)
		except requests.RequestException as e:
			self.on_error(None, e)

	def on_success(self, request, result):
		if result.get('success'):  # Check if login was successful
			self.manager.current = 'success'
		else:
			self.show_error_popup(result.get('message', 'Login failed.'))

	def on_failure(self, request, result):
		print("Login failed.")
		print(result)
		self.show_error_popup('Login failed.')

	def on_error(self, request, error):
		print(f"Error: {error}")
		self.show_error_popup('Error occurred while processing the request.')

	def go_to_register(self, instance):
		self.manager.current = 'register'

	def show_error_popup(self, message):
		popup = Popup(title='Login Failed',
					  content=Label(text=message),
					  size_hint=(0.8, 0.4))
		popup.open()
