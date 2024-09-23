from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Rectangle, RoundedRectangle, Color
from kivy.utils import get_color_from_hex as GetColor
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.metrics import dp, sp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from widgets import Utility, CustomImageButton, RoundedTextInput

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Ellipse, Color
from kivy.utils import get_color_from_hex as GetColor
from kivy.core.window import Window

class BaseSection(FloatLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.size_hint = (1, 1)
		self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

class ProductSection(BaseSection):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.display_products()

	def display_products(self):
		scroll_view = ScrollView(size_hint=(0.95, 0.95), pos_hint = {"center_x": 0.5, "center_y": 0.5})
		product_grid = GridLayout(cols=2, spacing=Utility.get_value_percentage(Window.height, 0.01), size_hint_y=None)
		product_grid.bind(minimum_height=product_grid.setter('height'))

		for i in range(10):
			product_grid.add_widget(self.create_product_widget(f"Product {i + 1}", "assets/test_product.jpg", 99, 10))

		scroll_view.add_widget(product_grid)
		self.add_widget(scroll_view)

	def create_product_widget(self, product_name, product_image, product_price, product_sold):
		product_widget = FloatLayout(size_hint_y=None, height=Utility.get_value_percentage(Window.height, 0.3))
		product_widget.bind(pos=self.update_product_bind, size=self.update_product_bind)

		box_layout = BoxLayout(pos_hint={"center_x": 0.5, "center_y": 0.5}, orientation='vertical', padding=dp(5), spacing=dp(5))
		image = Image(source=product_image, size_hint_y=0.7)
		
		title = Label(
			text=product_name[:20] + ("..." if len(product_name) >= 20 else ""), 
			size_hint_y=None, 
			height=dp(20), 
			halign='left', 
			valign='middle', 
			color=(0, 0, 0, 1),
			font_size=sp(12)
		)
		title.bind(size=title.setter('text_size'))
		
		bottom_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(20), spacing=dp(5))		
		price = Label(
			text=f"${product_price}", 
			size_hint_x=0.5, 
			halign='left', 
			valign='middle', 
			color=(1, 0, 0, 1),
			font_size=sp(12)
		)
		price.bind(size=price.setter('text_size'))
		
		sold_label = Label(
			text=f"Sold: {product_sold}",
			size_hint_x=0.5,
			halign='right',
			valign='middle',
			color=(0, 0, 0, 0.6),
			font_size=sp(12)
		)
		sold_label.bind(size=sold_label.setter('text_size'))
		
		bottom_layout.add_widget(price)
		bottom_layout.add_widget(sold_label)
		
		box_layout.add_widget(image)
		box_layout.add_widget(title)
		box_layout.add_widget(bottom_layout)
		product_widget.add_widget(box_layout)

		return product_widget

	def update_product_bind(self, instance, _):
		instance.canvas.before.clear()
		with instance.canvas.before:
			Color(GetColor("#ffffff"))
			RoundedRectangle(size=instance.size, pos=instance.pos, radius=[dp(5)])

class MallSection(BaseSection):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)


class LiveSection(BaseSection):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)


class NotificationSection(BaseSection):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)


class ProfileSection(BaseSection):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

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
		self.is_in_profile = False

	def display_design(self):
		self.size = self.manager.size
		with self.canvas.before:
			Color(rgba=GetColor("#eaeaea"))
			Rectangle(size=self.size)

			height = Utility.get_value_percentage(self.height, 0.08)
			Color(rgba=GetColor(self.manager.theme.main_color))
			RoundedRectangle(
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

		self.main_layout = BoxLayout(orientation='vertical', padding=spacepadd, spacing=spacepadd)
		self.top_bar_layout = BoxLayout(orientation='horizontal', size_hint=(1, None),
			height=Utility.get_value_percentage(self.height, 0.05), spacing=dp(10))

		search_bar = RoundedTextInput(icon_source='assets/pass.png', hint_text="Search...", size_hint=(0.65, 1))
		cart_icon = Image(source='assets/cart.png', size_hint=(0.125, 1))
		message_button = Image(source='assets/chats.png', size_hint=(0.125, 1))

		self.top_bar_layout.add_widget(search_bar)
		self.top_bar_layout.add_widget(cart_icon)
		self.top_bar_layout.add_widget(message_button)

		self.middle_section = FloatLayout(size_hint=(1, 1))
		self.all_middle_section['home'] = ProductSection()
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
		self.middle_section.clear_widgets()

		if self.is_in_profile:
			self.main_layout.clear_widgets()
			self.main_layout.add_widget(self.top_bar_layout)
			self.main_layout.add_widget(self.middle_section)
			self.main_layout.add_widget(self.bottom_nav_layout)

		sect = self.all_middle_section.get(section, None)
		if not sect:
			if section == 'home':
				sect = self.all_middle_section.get('home', ProductSection())
				self.is_in_profile = False
			elif section == 'mall':
				sect = self.all_middle_section.get('mall', MallSection())
				self.is_in_profile = False
			elif section == 'live':
				sect = self.all_middle_section.get('live', LiveSection())
				self.is_in_profile = False
			elif section == 'notif':
				sect = self.all_middle_section.get('notif', NotificationSection())
				self.is_in_profile = False
			elif section == 'profile':
				self.is_in_profile = True
				self.main_layout.clear_widgets()
				self.main_layout.add_widget(self.middle_section)
				self.main_layout.add_widget(self.bottom_nav_layout)
				sect = self.all_middle_section.get('profile', ProfileSection())

		self.middle_section.add_widget(sect)
