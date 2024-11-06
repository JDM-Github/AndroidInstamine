from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from widgets import Product

from popup import AddProduct
from .base_section import BaseSection, ProductListSection

class MyProducts(ProductListSection):

	def __init__(self, manager, email, **kwargs):
		super().__init__(manager, "product/products?email="+email, **kwargs)
		self.manager = manager

	def add_product(self):
		popup = AddProduct()
		popup.open()

