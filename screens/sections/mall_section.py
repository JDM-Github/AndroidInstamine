from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Rectangle, RoundedRectangle, Color, Ellipse
from kivy.utils import get_color_from_hex as GetColor
from kivy.uix.image import Image
from kivy.metrics import dp, sp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.effects.scroll import ScrollEffect

from widgets import Utility, CustomImageButton, RoundedTextInput, Product

from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from .base_section import BaseSection


class MallSection(BaseSection):
	def __init__(self, manager, **kwargs):
		super().__init__(**kwargs)
		self.manager = manager
		self.display_products()

	def display_products(self):
		scroll_view = ScrollView(size_hint=(0.95, 0.95), pos_hint = {"center_x": 0.5, "center_y": 0.5}, effect_cls=ScrollEffect)
		product_grid = GridLayout(cols=2, spacing=Utility.get_value_percentage(Window.height, 0.01), size_hint_y=None)
		product_grid.bind(minimum_height=product_grid.setter('height'))

		for i in range(10):
			product_grid.add_widget(Product(self.manager, f"Product {i + 1}", "assets/test_product.jpg", 99, 10))

		scroll_view.add_widget(product_grid)
		self.add_widget(scroll_view)
