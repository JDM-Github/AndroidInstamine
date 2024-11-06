from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from widgets import Product

from .base_section import BaseSection

class MyLikes(BaseSection):
	manager = ObjectProperty(None)
	product_grid = ObjectProperty(GridLayout())

	def __init__(self, manager, **kwargs):
		super().__init__(**kwargs)
		self.manager = manager
		self.display_products()

	def display_products(self):
		for i in range(10):
			self.product_grid.add_widget(Product(self.manager, f"Product {i + 1}", "assets/test_product.jpg", 99, 10))
