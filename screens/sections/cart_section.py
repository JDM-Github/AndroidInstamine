from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, NumericProperty
from widgets import Product
from widgets.product import ProductItem
from .base_section import BaseSection

from handle_requests import RequestHandler
from widgets.product_ordered import ProductOrdered

class CartSection(BaseSection):
    manager = ObjectProperty(None)
    product_grid = ObjectProperty(GridLayout())

    total_product = NumericProperty(0)

    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager
        self.link = "cart/getAllCartById?userId="+self.manager.main_state['user']['id']
        self.get_all_products()

    def get_all_products(self):
        RequestHandler.request_loader(self.manager.home, self.manager,
            lambda: RequestHandler.create_req_suc_error("get", self.link, {}, self.on_sucess, self.on_error))

    def on_sucess(self, response):
        self.all_product = []

        if response.get('success') and 'cart' in response:
            all_product = response['cart']
            for product in all_product:
                product_widget = ProductItem(
                    product_id = product['Product']['id'],
                    seller_id = product['Product']['userId'],
                    seller_name = product['Product']['Users']['firstName'] + " " + product['Product']['Users']['lastName'],
                    product_image = product['Product']['product_image'],
                    product_name = product['Product']['name'],
                    product_price = float(product['Product']['price'])
                )
                self.all_product.append(product_widget)
                product_widget.bind(product_qty=self.update_total)
                self.product_grid.add_widget(product_widget)
        self.update_total()

    def on_error(self, error):
        RequestHandler.show_error_popup(self.manager, "Loading Cart", "Error Loading Cart: " + error.get('message'))
    
    def update_total(self, *args):
        total = 0
        for product_widget in self.product_grid.children:
            if isinstance(product_widget, ProductItem):
                total += product_widget.product_price * product_widget.product_qty
        self.total_product = total

    def buy_now_product(self, *_):
        if self.manager.main_state['user']['location'] == "" and \
            self.manager.main_state['user']['phoneNumber'] == "":
            RequestHandler.show_error_popup(self.manager, "Order Error", "Please setup your account information.")
        else:
            self.manager.checkout.update_checkout(products=self.all_product)
            self.manager.current = "checkout"
