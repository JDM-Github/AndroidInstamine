from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from widgets import Product

from handle_requests import RequestHandler
from widgets.product_ordered import ProductOrdered

class BaseSection(FloatLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.size_hint = (1, 1)
		self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

class OrderedProductListSection(BaseSection):
	manager = ObjectProperty(None)
	product_grid = ObjectProperty(GridLayout())

	def __init__(self, manager, link, pay=False, ship=False, receive=False, complete=False, order=False, **kwargs):
		super().__init__(**kwargs)
		self.manager = manager
		self.link = link

		self.is_to_pay = pay
		self.is_to_ship = ship
		self.is_to_receive = receive
		self.is_complete = complete
		self.is_order = order
		self.get_all_products()

	def get_all_products(self):
		RequestHandler.request_loader(self.manager.home, self.manager,
			lambda: RequestHandler.create_req_suc_error("get", self.link, {}, self.on_sucess, self.on_error))

	def on_sucess(self, response):
		self.all_product = None
		self.product_grid.clear_widgets()

		id = self.manager.main_state['user']['id']
		if response.get('success'):
			for order in response['order']:
				product = order['Product']
				product_widget = ProductOrdered(
					self.manager,
					order['id'],
					product['Users']['id'] == id, 
					product['name'],
					product['product_image'],
					float(product['price']),
					int(product['number_of_sold']),
					int(order['numberOfProduct']),
					product
				)
				product_widget.is_to_pay = self.is_to_pay
				product_widget.is_to_ship = self.is_to_ship
				product_widget.is_to_receive = self.is_to_receive
				product_widget.is_complete = self.is_complete
				product_widget.is_order = self.is_order
				self.product_grid.add_widget(product_widget)
		else:
			RequestHandler.show_error_popup(self.manager, "Loading Product", "No products available.")

	def on_error(self, error):
		RequestHandler.show_error_popup(self.manager, "Loading Product", "Error Loading Product: " + error.get('message'))

class ProductListSection(BaseSection):
	manager = ObjectProperty(None)
	product_grid = ObjectProperty(GridLayout())

	def __init__(self, manager, link, **kwargs):
		super().__init__(**kwargs)
		self.manager = manager
		self.link = link
		self.get_all_products()

	def get_all_products(self):
		RequestHandler.request_loader(self.manager.home, self.manager,
			lambda: RequestHandler.create_req_suc_error("get", self.link, {}, self.on_sucess, self.on_error))

	def on_sucess(self, response):
		self.all_product = None
		self.product_grid.clear_widgets()

		id = self.manager.main_state['user']['id']
		if response.get('success') and 'products' in response:
			self.all_product = response['products']
			for product in self.all_product:
				product_widget = Product(
					self.manager,
					product['Users']['id'] == id, 
					product['name'],
					product['product_image'],
					float(product['price']),
					int(product['number_of_sold']),
					product
				)
				self.product_grid.add_widget(product_widget)
		else:
			RequestHandler.show_error_popup(self.manager, "Loading Product", "No products available.")

	def on_error(self, error):
		RequestHandler.show_error_popup(self.manager, "Loading Product", "Error Loading Product: " + error.get('message'))