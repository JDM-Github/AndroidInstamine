from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.network.urlrequest import UrlRequest

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
		UrlRequest(
			'https://test888.netlify.app/.netlify/functions/api/login',
			req_body=str(data), on_success=self.on_success, on_failure=self.on_failure, on_error=self.on_error)


	def on_success(self, request, result):
		print(result['otp'])

		self.manager.get_screen('verify').to_verify = result['otp']
		self.manager.current = 'verify'

	def on_failure(self, request, result):
		print("Login failed.")
		print(result)

	def on_error(self, request, error):
		print(f"Error: {error}")

	def go_to_register(self, instance):
		self.manager.current = 'register'
