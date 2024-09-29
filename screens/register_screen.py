import threading
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock

from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex as GetColor
from kivy.graphics import Rectangle, RoundedRectangle, Color
from kivy.uix.screenmanager import SlideTransition

from widgets import RoundedTextInput, CustomButton, LoadingPopup, Utility, ThemedPopup
from handle_requests import RequestHandler

class TermsAgreement(Widget):

	def __init__(self, manager, **kwargs):
		super().__init__(**kwargs)
		self.manager = manager
		self.size_hint_x = 0.7
		self.size_hint_y = None
		self.height = dp(40)
		self.pos_hint = {"center_x": 0.5}

		self.layout   = BoxLayout(orientation='horizontal')
		self.checkbox = CheckBox(size_hint=(None, 1), width=dp(20))
		terms_policy_label = Label(
			font_size=sp(14),
			text="I agree to the [ref=terms][b]Terms[/b][/ref] and [ref=policy][b]Policy[/b][/ref].",
			markup=True,
			color=GetColor(manager.theme.main_color)
		)

		self.layout.add_widget(self.checkbox)
		self.layout.add_widget(terms_policy_label)

		self.add_widget(self.layout)
		self.bind(pos=self.update_pos, size=self.update_pos)
		terms_policy_label.bind(on_ref_press=self._on_ref_press)

	def update_pos(self, *_):
		self.layout.pos  = self.pos
		self.layout.size = self.size

	def _on_ref_press(self, *args):
		if args[1] == "terms":
			popup = ThemedPopup(
				self.manager,
				title='Instamine Terms',
				message=self.manager.main_config['terms'])
			popup.open()

		elif args[1] == "policy":
			popup = ThemedPopup(
				self.manager,
				title='Instamine Policy',
				message=self.manager.main_config['policy'])
			popup.open()





class RegisterScreen(Screen):

	def display_design(self):
		self.size = self.manager.size
		with self.canvas.before:
			Color(rgba=GetColor("#ffffff"))
			Rectangle(size=self.size)

			Color(rgba=GetColor(self.manager.theme.main_color))
			height = Utility.get_value_percentage(self.height, 0.25)
			RoundedRectangle(pos=(self.x, self.height-height), size=(self.width, height), radius=[0, 0, dp(30), dp(30)])

		self.display_widget()



	def display_widget(self):
		self.clear_widgets()
	
		widget    = Widget(size=self.manager.size, pos=(0, 0))
		spacepadd = Utility.get_value_percentage(self.height, 0.015)
		layout    = BoxLayout(size=self.manager.size, orientation='vertical', padding=spacepadd, spacing=spacepadd)
	
		main_color     = self.manager.theme.main_color
		main_color_88  = self.manager.theme.main_color_88

		common_kwargs = {
			'line_color': main_color,
			'fg_color': main_color,
			'hint_color': main_color_88,
			'size_hint_y': None,
			'height': dp(40)
		}
		
		self.username    = RoundedTextInput(icon_source='assets/user.png', hint_text="Username", **common_kwargs)
		self.name_layout = BoxLayout       (pos_hint={"center_x": 0.5}, size_hint=(0.8, None), height=dp(60), spacing=dp(10))
		self.first_name  = RoundedTextInput(hint_text="First Name", size_hint_x=0.5, **common_kwargs)
		self.last_name   = RoundedTextInput(hint_text="Last Name", size_hint_x=0.5, **common_kwargs)
		self.birthday    = RoundedTextInput(icon_source='assets/birthday.png', hint_text="MM/DD/YYYY", **common_kwargs)
		self.email       = RoundedTextInput(icon_source='assets/email.png', hint_text="Email", **common_kwargs)
		self.password    = RoundedTextInput(icon_source='assets/pass.png', hint_text="Password", eye_icon_source='assets/close.png', password=True, **common_kwargs)
		self.cpassword   = RoundedTextInput(icon_source='assets/pass.png', hint_text="Confirm Password", eye_icon_source='assets/close.png', password=True, **common_kwargs)


		register_btn = CustomButton(self.manager, text="Sign Up", on_press=self.register)
		self.name_layout.add_widget(self.first_name)
		self.name_layout.add_widget(self.last_name)
		self.terms_agreement = TermsAgreement(self.manager)

		layout.add_widget(self.name_layout)
		layout.add_widget(self.username)
		layout.add_widget(self.birthday)

		layout.add_widget(self.email)
		layout.add_widget(self.password)
		layout.add_widget(self.cpassword)
	
		layout.add_widget(Widget(size_hint_y=None, height=dp(10)))
		layout.add_widget(self.terms_agreement)
		layout.add_widget(register_btn)

		layout.add_widget(Widget(size_hint_y=None, height=dp(10)))
		ref_login = Label(
			color=GetColor(self.manager.theme.main_color),
			font_size=sp(14),
			text="Have an account? [ref=login][b]Sign in[/b][/ref]",
			markup=True, size_hint_y=None, height=dp(20))

		ref_login.bind(on_ref_press=self.layout_on_ref_press)
		layout.add_widget(ref_login)

		widget.add_widget(layout)
		self.add_widget(widget)

	def layout_on_ref_press(self, *args):
		if args[1] == "login":
			self.go_to_login()




	def register(self):
		self.loading = LoadingPopup(self.manager)
		self.add_widget(self.loading)

		success_color = GetColor(self.manager.theme.main_color)
		error_color = GetColor(self.manager.theme.main_error_color)

		if not Utility.validate_not_empty(self.first_name, "First Name", "First name cannot be empty.", error_color, success_color, self._on_error):
			return
		if not Utility.validate_not_empty(self.last_name, "Last Name", "Last name cannot be empty.", error_color, success_color, self._on_error):
			return
		if not Utility.validate_not_empty(self.username, "Username", "Username cannot be empty.", error_color, success_color, self._on_error):
			return
		if not Utility.validate_birthday(self.birthday, error_color, success_color, self.manager.main_config['at_least_years_user'], self._on_error):
			return
			
		email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
		if not Utility.validate_email(self.email, email_pattern, error_color, success_color, self._on_error):
			return

		if not Utility.validate_password(self.password, self.cpassword, error_color, success_color, self._on_error, check_strength=True):
			return

		if not self.terms_agreement.checkbox.active:
			self._on_error('', "User did not accept user terms and agreement.")
			return

		threading.Thread(target=self._register).start()

	
	def show_error_popup(self, message):
		popup = ThemedPopup(
			self.manager,
			title='Registration Failed',
			message=message)
		popup.open()

	def go_to_login(self):
		self.manager.transition = SlideTransition(direction='right', duration=0.5)
		self.manager.current = 'login'





	def _register(self):
		result, message = RequestHandler.create_request(
			link="register",
			data={
				'username': self.username.input.text,
				'email'   : self.email.input.text,
				'password': self.password.input.text
			}
		)
		if result:
			self.on_success(message)
		else:
			self.on_error(message)


	def on_success(self, result):
		Clock.schedule_once(lambda dt: self._on_success(result))

	def on_error(self, error):
		Clock.schedule_once(lambda dt: self._on_error(error))

	def _on_success(self, result):
		self.remove_widget(self.loading)
		# self.manager.get_screen('verify').to_verify = result['otp']
		self.manager.current = 'login'

	def _on_error(self, error, error_message="Error occurred while processing the request."):
		self.remove_widget(self.loading)
		print(f"Error: {error}")
		self.show_error_popup(error_message)
