from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Rectangle, RoundedRectangle, Color, Ellipse
from kivy.utils import get_color_from_hex as GetColor
from kivy.uix.image import Image
from kivy.metrics import dp, sp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from widgets import Utility, CustomImageButton, RoundedTextInput

from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

from .base_section import BaseSection

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

