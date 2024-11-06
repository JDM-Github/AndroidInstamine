from kivy.uix.boxlayout import BoxLayout

from kivy.graphics import Rectangle, RoundedRectangle, Color
from kivy.utils import get_color_from_hex as GetColor
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.metrics import dp

from screens.sections.cart_section import CartSection
from screens.sections.chat_section import ChatSection
from screens.sections.checkUserProduct import CheckUserProducts
from screens.sections.is_complete import IsComplete
from screens.sections.recently_viewed import RecentlyViewed
from screens.sections.to_pay import ToPay
from screens.sections.to_receive import ToReceive
from screens.sections.to_ship import ToShip
from screens.sections.who_orders import WhoOrder
from widgets import Utility, CustomImageButton, RoundedTextInput

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color
from kivy.utils import get_color_from_hex as GetColor

from .sections import ProductSection, MallSection, LiveSection, NotificationSection, ProfileSection, MyLikes, MyProducts
from kivy.lang import Builder

Builder.load_file('screens/sections/section.kv')

class TopLayout(Label):
	pass

class HomeScreen(Screen):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.old_section = "home"

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
			self.top_color = Color(rgba=GetColor(self.manager.theme.main_color))
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
		self.cart_icon      = CustomImageButton(self.manager, src='assets/cart.png', size_hint=(0.1, 1))
		self.cart_icon.on_press = lambda: self.update_button_active("cart")

		self.message_button = CustomImageButton(self.manager, src='assets/chats.png', size_hint=(0.1, 1))
		self.message_button.on_press = lambda: self.update_button_active("chats")

		self.back_button = CustomImageButton(self.manager, src='assets/back.png', size_hint=(0.1, 1))
		self.back_button.on_press = lambda: self.update_button_active("home")

		self.top_bar_layout.add_widget(self.search_bar)
		self.top_bar_layout.add_widget(self.cart_icon)
		self.top_bar_layout.add_widget(self.message_button)

		self.middle_section = FloatLayout(size_hint=(1, 1))
		self.bottom_nav_layout = BoxLayout(orientation='horizontal', size_hint=(1, None),
			height=Utility.get_value_percentage(self.height, 0.05), spacing=dp(5))

		for button in self.buttons:
			nav_button = CustomImageButton(
				self.manager,
				src=button['icon'],
				active=True,
				is_active=button['active'],
				on_press=lambda section=button['section']: self.update_button_active(section),
				section=button['section']
			)
			self.bottom_nav_layout.add_widget(nav_button)

		self.main_layout.add_widget(self.top_bar_layout)
		self.main_layout.add_widget(self.middle_section)
		self.main_layout.add_widget(self.bottom_nav_layout)

		self.add_widget(self.main_layout)


	def update_button_active(self, section, add={}):
		for child in self.bottom_nav_layout.children:
			if child.section == section:
				child.is_active = True
				child.color.rgba = GetColor(self.manager.theme.main_hover_color)
				continue
			child.is_active = False
			child.color.rgba = GetColor(self.manager.theme.main_color)

		self.select_middle_section(section, add)

	def select_middle_section(self, section, add={}):
		self.top_bar_layout.clear_widgets()
		self.middle_section.clear_widgets()
		self.bg_color.rgba = GetColor(self.manager.theme.white_bg)
		self.top_color.rgba = GetColor(self.manager.theme.main_color)

		if self.reset_next:
			self.main_layout.clear_widgets()
			self.main_layout.add_widget(self.top_bar_layout)
			self.main_layout.add_widget(self.middle_section)
			self.main_layout.add_widget(self.bottom_nav_layout)		

		if section == 'home':
			self.top_bar_layout.add_widget(self.search_bar)
			sect = self.all_middle_section.get('home', None)
			if sect is None:
				sect = ProductSection(self.manager)
				self.all_middle_section['home'] = sect

			self.reset_next = False

		elif section == 'mall':
			self.top_bar_layout.add_widget(self.search_bar)
			sect = self.all_middle_section.get('mall', None)

			if sect is None:
				sect = MallSection(self.manager)
				self.all_middle_section['mall'] = sect

			self.reset_next = False

		elif section == 'live':
			if self.manager.main_state['user']['isStreaming']:
				# self.manager.live.set_live(self.manager.main_state['user']['id'])
				self.manager.current = "live"
				return

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
			self.top_bar_layout.add_widget(TopLayout(text="Notification"), 2)
			sect = self.all_middle_section.get('notif', None)
			if sect is None:
				sect = NotificationSection()
				self.all_middle_section['notif'] = sect

			self.reset_next = False

		elif section == 'profile':
			self.top_bar_layout.add_widget(TopLayout(text="Profile"), 2)
			sect = self.all_middle_section.get('profile', None)
			if sect is None:
				sect = ProfileSection(self.manager)
				self.all_middle_section['profile'] = sect
		elif section == 'chats':
			self.default_change('chats', "Chats", ChatSection, self.manager)
			return
		elif section == 'cart':
			self.default_change('cart', "Cart", CartSection, self.manager)
			return
		elif section == 'mylikes':
			self.default_change('mylikes', "My Likes", MyLikes, self.manager)
			return
		elif section == 'myproduct':
			self.default_change('myproduct', "My Products", MyProducts, self.manager,
				self.manager.main_state['user']['email'])
			return
		elif section == 'recentlyViewed':
			self.default_change('recentlyViewed', "Recently Viewed", RecentlyViewed, self.manager)
			return
		elif section == 'sellerProducts':
			self.default_change('sellerProducts', add.get('user') + "'s Products", CheckUserProducts, self.manager, add.get('email'))
			return
		elif section == 'whoOrder':
			self.default_change('whoOrder', "Who Order Your Products", WhoOrder, self.manager, self.manager.main_state['user']['id'])
			return
		elif section == 'toPay':
			self.default_change('toPay', "To Pay Products", ToPay, self.manager, self.manager.main_state['user']['id'])
			return
		elif section == 'toShip':
			self.default_change('toShip', "To Ship Products", ToShip, self.manager, self.manager.main_state['user']['id'])
			return
		elif section == 'toReceive':
			self.default_change('toReceive', "To Receive Products", ToReceive, self.manager, self.manager.main_state['user']['id'])
			return
		elif section == 'isComplete':
			self.default_change('isComplete', "Completed Orders", IsComplete, self.manager, self.manager.main_state['user']['id'])
			return

		self.back_button.on_press = lambda: self.update_button_active(self.old_section)
		self.old_section = section

		self.top_bar_layout.add_widget(self.cart_icon)
		self.top_bar_layout.add_widget(self.message_button)
		self.middle_section.add_widget(sect)
	
	def default_change(self, section, new_text, widget, *args):
		self.top_bar_layout.add_widget(TopLayout(text=new_text), 2)
		sect = self.all_middle_section.get(section, None)
		if sect is None:
			sect = widget(*args)
			self.all_middle_section[section] = sect

		self.top_bar_layout.add_widget(self.cart_icon)
		self.top_bar_layout.add_widget(self.back_button)
		self.middle_section.add_widget(sect)
