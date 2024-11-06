from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.metrics import dp

from kivy.core.window import Window
from widgets import Utility

class CustomFloatLayout(FloatLayout):

    def __init__(self, func, **kwargs):
        super().__init__(**kwargs)
        self.func = func
        self.size_hint_y = None
        self.height = Utility.get_value_percentage(Window.height, 0.3)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.func()
        return super().on_touch_down(touch)

class BindWidget(Widget):
    radius = ListProperty([dp(10), dp(10), dp(10), dp(10)])

class CustomBoxLayout(BoxLayout, BindWidget):
    pass

class ProductItem(CustomBoxLayout):
    product_id = StringProperty('')
    seller_id = StringProperty('')
    seller_name = StringProperty('')
    product_qty = NumericProperty(1)
    product_image = StringProperty('')
    product_name = StringProperty('')
    product_price = NumericProperty(0)

# class ProductItem
class Product(CustomFloatLayout):

    product_name = StringProperty("")
    product_image = StringProperty("")
    product_price = NumericProperty(0)
    product_sold = NumericProperty(0)

    def __init__(self,
              manager=None, is_my_product=False, product_name='', product_image='', product_price=0, product_sold=0, product=None, **kwargs):
        super().__init__(lambda: manager.change_product(is_my_product, product), **kwargs)

        self.manager = manager
        self.product_name = product_name
        self.product_image = product_image
        self.product_price = product_price
        self.product_sold = product_sold
