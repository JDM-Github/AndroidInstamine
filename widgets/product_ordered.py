from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, NumericProperty, BooleanProperty

from kivy.core.window import Window
from handle_requests import RequestHandler
from widgets import Utility

class CustomFloatLayout(FloatLayout):

    def __init__(self, func, **kwargs):
        super().__init__(**kwargs)
        self.func = func
        self.size_hint_y = None
        self.height = Utility.get_value_percentage(Window.height, 0.2)

    # def on_touch_down(self, touch):
    #     if self.collide_point(*touch.pos):
    #         self.func()
    #     return super().on_touch_down(touch)

class ProductOrdered(CustomFloatLayout):

    order_id = StringProperty("")
    product_name = StringProperty("")
    product_image = StringProperty("")
    product_price = NumericProperty(0)
    product_sold = NumericProperty(0)
    product_num_ordered = NumericProperty(1)

    is_to_pay = BooleanProperty(False)
    is_to_ship = BooleanProperty(False)
    is_to_receive = BooleanProperty(False)
    is_complete = BooleanProperty(False)
    is_order = BooleanProperty(False)

    def __init__(self,
        manager=None, order_id='', is_my_product=False, product_name='', product_image='', product_price=0, product_sold=0,
        product_num_ordered=1, product=None, **kwargs):
        super().__init__(lambda: manager.change_product(is_my_product, product), **kwargs)

        self.manager = manager
        self.order_id = order_id
        self.product_name = product_name
        self.product_image = product_image
        self.product_price = product_price
        self.product_sold = product_sold
        self.product_num_ordered = product_num_ordered
    
    def none_func(self):
        pass

    def open_ship(self):
        RequestHandler.request_loader(self, self.manager,
            lambda: RequestHandler.create_req_suc_error("post", "orders/shipOrder",
            {
                'id': self.order_id,
            }, self.on_success_cancel_order, self.on_error_cancel_order))

    def cancel_order(self):
        RequestHandler.request_loader(self, self.manager,
            lambda: RequestHandler.create_req_suc_error("post", "orders/cancelOrder",
            {
                'id': self.order_id,
            }, self.on_success_cancel_order, self.on_error_cancel_order))

    def on_error_cancel_order(self, error):
        RequestHandler.show_error_popup(self.manager, "Cancel order error", str(error['message']))

    def on_success_cancel_order(self, result):
        RequestHandler.show_error_popup(self.manager, "Successful Cancel Order", "You successfully cancel the order.")
        self.manager.home.update_button_active("profile")
        self.manager.home.all_middle_section = {}
