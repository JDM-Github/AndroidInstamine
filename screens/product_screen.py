import threading
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView

from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex as GetColor
from kivy.graphics import Rectangle, RoundedRectangle, Color, Line
from kivy.uix.screenmanager import SlideTransition, FadeTransition, WipeTransition, SwapTransition

from widgets import CircleImage, RoundedTextInput, CustomButton, LoadingPopup, BackButton, Utility, ThemedPopup
from handle_requests import RequestHandler


class CustomImage(Image):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.bind(size=self._update, pos=self._update)

	def _update(self, *_):
		self.canvas.after.clear()
		with self.canvas.after:
			Color(rgb=GetColor("#aaaaaa"))
			Line(rectangle=(self.x, self.y, self.width, self.height), width=1)

class ProductScreen(Screen):

	def update_product(self, product_id):
		self.layout.clear_widgets()
		image = Image(source="assets/test_product.jpg", size_hint=(1, None), height=Window.height*0.4, fit_mode="fill")
		scroll_view = ScrollView(
			size_hint=(0.95, None),
			pos_hint={'center_x': 0.5},
			height=dp(60), 
			do_scroll_x=True, 
			do_scroll_y=False
		)
		other_images = BoxLayout(
			size_hint_x=None,
			height=dp(50), 
			spacing=dp(5),
		)
		other_images.bind(minimum_width=other_images.setter('width'))
		other_images = BoxLayout(size_hint=(0.95, None), height=dp(50), pos_hint={'center_x': 0.5}, spacing=dp(5))
		other_images.add_widget(CustomImage(source="assets/test_product.jpg", size_hint_x=None, width=dp(50)))
		other_images.add_widget(CustomImage(source="assets/test_product.jpg", size_hint_x=None, width=dp(50)))
		other_images.add_widget(CustomImage(source="assets/test_product.jpg", size_hint_x=None, width=dp(50)))
		other_images.add_widget(CustomImage(source="assets/test_product.jpg", size_hint_x=None, width=dp(50)))
		other_images.add_widget(CustomImage(source="assets/test_product.jpg", size_hint_x=None, width=dp(50)))
		scroll_view.add_widget(other_images)

		bottom_layout = BoxLayout()
		self.layout.add_widget(image)
		self.layout.add_widget(scroll_view)
		self.layout.add_widget(bottom_layout)

	def display_design(self):
		self.size = self.manager.size
		with self.canvas.before:
			Color(rgba=GetColor(self.manager.theme.main_color))
			Rectangle(size=self.size)
			Color(rgba=GetColor("#ffffff"))
			RoundedRectangle(
				size=(self.width, Utility.get_value_percentage(self.height, 0.5)),
				radius=[dp(10), dp(10), 0, 0])

		self.display_widget()

	def display_widget(self):
		self.clear_widgets()
		widget = Widget(size=self.manager.size, pos=(0, 0))

		layout_scroll = ScrollView(size=self.manager.size, do_scroll_y=True, do_scroll_x=False)
		self.layout = BoxLayout(orientation='vertical', size_hint=(1, None),
			spacing=Utility.get_value_percentage(self.height, 0.01), size=self.manager.size)
		# self.layout.bind(minimum_height=self.layout.setter('height'))
		
		layout_scroll.add_widget(self.layout)
		widget.add_widget(layout_scroll)
		self.add_widget(widget)

	def layout_on_ref_press(self, *args):
		pass

