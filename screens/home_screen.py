from kivy.uix.boxlayout import BoxLayout

from kivy.graphics import Rectangle, RoundedRectangle, Color
from kivy.utils import get_color_from_hex as GetColor
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.metrics import dp

from widgets import Utility, CustomImageButton, RoundedTextInput

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color
from kivy.utils import get_color_from_hex as GetColor

from .sections import ProductSection, MallSection, LiveSection, NotificationSection, ProfileSection, TopNotification

class HomeScreen(Screen):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.buttons = [
			{'active': True,  "section": "home",    "icon": "assets/home.png"},
			{'active': False, "section": "mall",    "icon": "assets/mall.png"},
			{'active': False, "section": "live",    "icon": "assets/live.png"},
			{'active': False, "section": "notif",   "icon": "assets/notification.png"},
			{'active': False, "section": "profile", "icon": "assets/profile.png"},
		]

		self.all_middle_section = {}
		self.reset_next = False


	def display_design(self):
		self.size = self.manager.size
		with self.canvas.before:
			self.bg_color = Color(rgba=GetColor("#eaeaea"))
			Rectangle(size=self.size)

			height = Utility.get_value_percentage(self.height, 0.08)
			Color(rgba=GetColor(self.manager.theme.main_color))
			RoundedRectangle   (
				size=(self.width, height),
				radius=[dp(30), dp(30), 0, 0]
			)

			Rectangle(
				size=(self.width, height),
				pos=(0, self.height-height),
			)

		self.display_widget()


	def display_widget(self):
		self.clear_widgets()
		spacepadd = Utility.get_value_percentage(self.height, 0.015)
		self.main_layout    = BoxLayout(orientation='vertical', padding=spacepadd, spacing=spacepadd)

		self.top_bar_layout = BoxLayout(orientation='horizontal', size_hint=(1, None),
			height=Utility.get_value_percentage(self.height, 0.05), spacing=dp(10))

		self.search_bar     = RoundedTextInput(icon_source='assets/pass.png', hint_text="Search...", size_hint=(0.9, 1))
		self.cart_icon      = Image(source='assets/cart.png', size_hint=(0.1, 1))
		self.message_button = Image(source='assets/chats.png', size_hint=(0.1, 1))

		self.top_bar_layout.add_widget(self.search_bar)
		self.top_bar_layout.add_widget(self.cart_icon)
		self.top_bar_layout.add_widget(self.message_button)




		self.middle_section = FloatLayout(size_hint=(1, 1))
		self.all_middle_section['home'] = ProductSection(self.manager)
		self.middle_section.add_widget(self.all_middle_section['home'])

		self.bottom_nav_layout = BoxLayout(orientation='horizontal', size_hint=(1, None),
			height=Utility.get_value_percentage(self.height, 0.05), spacing=dp(5))

		for button in self.buttons:
			nav_button = CustomImageButton(
				self.manager,
				src=button['icon'],
				active=True,
				is_active=button['active'],
				on_press=lambda section=button['section']: self.update_button_active(section)
			)
			self.bottom_nav_layout.add_widget(nav_button)



		self.main_layout.add_widget(self.top_bar_layout)
		self.main_layout.add_widget(self.middle_section)
		self.main_layout.add_widget(self.bottom_nav_layout)

		self.add_widget(self.main_layout)


	def update_button_active(self, section):
		for child in self.bottom_nav_layout.children:
			child.is_active = False
			child.color.rgba = GetColor(self.manager.theme.main_color)

		self.select_middle_section(section)

	def select_middle_section(self, section):
		self.top_bar_layout.clear_widgets()
		self.middle_section.clear_widgets()
		self.bg_color.rgba = GetColor(self.manager.theme.white_bg)

		if self.reset_next:
			self.main_layout.clear_widgets()
			self.main_layout.add_widget(self.top_bar_layout)
			self.main_layout.add_widget(self.middle_section)
			self.main_layout.add_widget(self.bottom_nav_layout)

		# sect = self.all_middle_section.get(section, None)

		if section == 'home':
			self.top_bar_layout.add_widget(self.search_bar)
			sect = self.all_middle_section.get('home', None)
			if sect is None:
				sect = ProductSection(self.manager)
				self.all_middle_section['home'] = sect

			self.reset_next = False

		elif section == 'mall':
			sect = self.all_middle_section.get('mall', None)
			if sect is None:
				sect = MallSection(self.manager)
				self.all_middle_section['mall'] = sect

			self.reset_next = False

		elif section == 'live':
			self.reset_next = True
			self.main_layout.clear_widgets()
			self.main_layout.add_widget(self.middle_section)
			self.main_layout.add_widget(self.bottom_nav_layout)
			sect = self.all_middle_section.get('live', None)
			if sect is None:
				sect = LiveSection(self.manager)
				self.all_middle_section['live'] = sect

			self.bg_color.rgba = GetColor(self.manager.theme.main_color_88)

		elif section == 'notif':
			self.top_bar_layout.add_widget(TopNotification(), 2)
			sect = self.all_middle_section.get('notif', None)
			if sect is None:
				sect = NotificationSection()
				self.all_middle_section['notif'] = sect

			self.reset_next = False

		elif section == 'profile':
			self.reset_next = True
			self.main_layout.clear_widgets()
			self.main_layout.add_widget(self.middle_section)
			self.main_layout.add_widget(self.bottom_nav_layout)
			sect = self.all_middle_section.get('profile', None)
			if sect is None:
				sect = ProfileSection()
				self.all_middle_section['profile'] = sect

		self.top_bar_layout.add_widget(self.cart_icon)
		self.top_bar_layout.add_widget(self.message_button)
		self.middle_section.add_widget(sect)
