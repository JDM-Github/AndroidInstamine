import threading
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image, AsyncImage
from kivy.uix.scrollview import ScrollView
from kivy.effects.scroll import ScrollEffect
from kivy.uix.textinput import TextInput

from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex as GetColor
from kivy.graphics import Rectangle, RoundedRectangle, Color, Line

from kivy.properties import ObjectProperty, StringProperty, NumericProperty

from popup.popups import BuyOrder, ChatPopup
from widgets import CircleImage, RoundedTextInput, CustomButton, LoadingPopup, BackButton, Utility, ThemedPopup, CustomImageButton
from handle_requests import RequestHandler
from widgets.custom_button import CustomButtonWidget, LeftLabel
from widgets.product import ProductItem

# class BindWidget(Widget):

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.radius = [dp(10), dp(10), 0, 0]
#         self.bind(size=self._update, pos=self._update)

#     def _update(self, *_):
#         self.canvas.before.clear()
#         with self.canvas.before:
#             Color(rgba=GetColor("#ffffff"))
#             RoundedRectangle(
#                 pos=(self.pos),
#                 size=(self.width, self.height),
#                 radius=self.radius)

# class CustomImage(AsyncImage):
#     border_color = StringProperty("#aaaaaa")

# class StarRating(BoxLayout):

#     rating = NumericProperty(0)

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.orientation = 'horizontal'
#         self.spacing = dp(2)
#         self.size_hint_y = None
#         self.height = dp(15)

#         self.full_star  = 'assets/fullstar.png'     
#         self.half_star  = 'assets/halfstar.png'     
#         self.empty_star = 'assets/emptystar.png'    

#         self.bind(rating=lambda *_: self.create_star_rating(self.rating))

#     def create_star_rating(self, rating):
#         for i in range(1, 6):
#             if rating >= i: 
#                 star = Image(source=self.full_star, size_hint=(None, None), size=(dp(15), dp(15)))
#             elif i - rating <= 0.5: 
#                 star = Image(source=self.half_star, size_hint=(None, None), size=(dp(15), dp(15)))
#             else: 
#                 star = Image(source=self.empty_star, size_hint=(None, None), size=(dp(15), dp(15)))
#             self.add_widget(star)


class PlaceOrderBottom(BoxLayout):
    checkout_all = ObjectProperty()

    # def __init__(self, manager, open_chat, buy_now_product, **kwargs):
    #     super().__init__(**kwargs)
    #     self.orientation = "horizontal"
    #     self.width = Window.width
    #     self.height = dp(40)

    #     self.chat_image = CustomImageButton(manager, src="assets/chats.png", size_hint_x=0.3, on_press=open_chat)
    #     with self.chat_image.canvas.before:
    #         Color(rgb=GetColor("#AD85A9")) 
    #         self.chat_rect = Rectangle(size=self.chat_image.size, pos=self.chat_image.pos)
    #         self.chat_image.bind(size=self._update_rect, pos=self._update_rect)
    #     self.add_widget(self.chat_image)

    #     self.cart_image = CustomImageButton(manager, src="assets/cart.png", size_hint_x=0.3)
    #     with self.cart_image.canvas.before:
    #         Color(rgb=GetColor("#AD85A9")) 
    #         self.cart_rect = Rectangle(size=self.cart_image.size, pos=self.cart_image.pos)
    #         self.cart_image.bind(size=self._update_rect, pos=self._update_rect)
    #     self.add_widget(self.cart_image)

    #     self.buy_now_label = CustomButtonWidget(text="PLACE ORDER", color=(1, 1, 1, 1), bold=True, on_press=buy_now_product)
    #     self.add_widget(self.buy_now_label)

    # def _update_rect(self, *_):
    #     self.chat_rect.size = self.chat_image.size
    #     self.chat_rect.pos  = self.chat_image.pos 

    #     self.cart_rect.size = self.cart_image.size
    #     self.cart_rect.pos  = self.cart_image.pos 


# class BottomLayout(BoxLayout, BindWidget): pass
# class PriceName(BottomLayout):
#     price_text = StringProperty("")
#     title_text = StringProperty("")

# class ShopWidget(BottomLayout):
#     seller_profile = StringProperty("")
#     seller_text = StringProperty("")
#     is_active = StringProperty("")
#     location_text = StringProperty("")

# class SellerInformationResponse(BottomLayout):
#     numberProduct = StringProperty("")
#     userRating = StringProperty("")
#     chatResponse = StringProperty("")
#     function = ObjectProperty(None)

#     def checkProducts(self):
#         self.function()

# class Specification(BottomLayout):
#     specification = StringProperty("")

# class ReviewImage(Image): pass
# class ReviewProduct(BottomLayout):

#     email = StringProperty("")
#     rating = NumericProperty(0)
#     review_text = StringProperty("")
#     best_feature = StringProperty("")
#     product_quality = StringProperty("")

#     def __init__(self, email, rating, best_feature, product_quality, review_text, images=[], **kwargs):
#         super().__init__(**kwargs)
#         self.email = email
#         self.rating = rating
#         self.review_text = review_text
#         self.best_feature = best_feature
#         self.product_quality = product_quality

#         self.images_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(80))
#         for image_source in images[:3]:
#             image_widget = ReviewImage(source=image_source)
#             self.images_layout.add_widget(image_widget)
#         self.images_layout.add_widget(Widget())

#         if images:
#             self.add_widget(self.images_layout)

# class ProductReview(BoxLayout):

#     def __init__(self, manager, **kwargs):
#         super().__init__(**kwargs)
#         self.manager = manager
#         self.bind(minimum_height=self.setter('height'))
#         self.orientation = "vertical"
#         self.size_hint_y = None
#         self.spacing = dp(5)

#         top_layout = BottomLayout(orientation='horizontal', size_hint_y=None, height=dp(30), padding=[dp(20), dp(10)])
#         self.ratings_label = Label(
#             text="4.9 [color=#9C3E93]Product Ratings[/color] (2.3k)",
#             font_size=sp(14),
#             color="#111111",
#             size_hint=(0.8, 1),
#             halign='left',
#             markup=True
#         )
#         self.ratings_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))

#         view_all_button = Button(
#             text="View All >",
#             size_hint=(0.2, 1),
#             background_normal="",
#             background_down="",
#             color="#555555"
#         )
#         top_layout.add_widget(self.ratings_label)
#         top_layout.add_widget(view_all_button)

#         self.reviews_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5),)
#         self.reviews_layout.bind(minimum_height=self.reviews_layout.setter('height'))

#         self.reviews_layout.add_widget(ReviewProduct(
#             email="john@example.com",
#             rating=4.7,
#             review_text="Great product! Highly recommend.",
#             best_feature="Performance",
#             product_quality="Excellent",
#             images=["assets/test_product.jpg", "assets/test_product.jpg"]
#         ))

#         self.add_widget(top_layout)
#         self.add_widget(self.reviews_layout)

class CheckoutBody(BoxLayout):
    product_grid = ObjectProperty(GridLayout())
    seller_name = StringProperty("Seller Store")
    product_id = StringProperty("")
    seller_id = StringProperty("")
    full_name = StringProperty("John Dave Pega")
    location = StringProperty("John Dave Pega")
    phone_num = StringProperty("(63+) 9303238796")
    product_img = StringProperty("")
    product_name = StringProperty("")
    product_price = StringProperty("0")

    product_item = ObjectProperty(ProductItem())
    total_price = NumericProperty(0)
    number_items = NumericProperty(1)

class CheckoutScreen(Screen):

    def update_total(self, *args):
        self.layout.total_price = args[0].product_price * args[1]
    
    def update_totals(self, *args):
        total = 0
        for product_widget in self.layout.ids.product_grid.children:
            if isinstance(product_widget, ProductItem):
                total += product_widget.product_price * product_widget.product_qty
        self.layout.total_price = total

    def update_checkout(self, product=None, products=[]):
        widget = self.layout.ids.product_grid
        widget.clear_widgets()

        self.layout.full_name = self.manager.main_state['user']['firstName'] + " " + self.manager.main_state['user']['lastName']
        self.layout.location = self.manager.main_state['user']['location']
        self.layout.phone_num = self.manager.main_state['user']['phoneNumber']

        if product:
            self.product = product
            print(self.product)
            self.layout.product_id = self.product['id']
            self.layout.seller_id = self.product['userId']
            self.layout.seller_name = self.product['Users']['firstName'] + " " + self.product['Users']['lastName']
            self.layout.product_img = self.product['product_image']
            self.layout.product_name = self.product['name']
            self.layout.product_price = self.product['price']

            self.layout.number_items = 1
            self.layout.ids.product_item.bind(product_qty=self.update_total)
            widget.add_widget(self.layout.ids.product_item)
            self.update_total(self.layout.ids.product_item, 1)

            self.back_button.on_press = lambda *_: self.manager.change_screen("product")
        else:
            self.layout.number_items = len(products)
            for prod in products:
                product_widget = ProductItem(
                    product_id = prod.product_id,
                    seller_id = prod.seller_id,
                    seller_name = prod.seller_name,
                    product_image = prod.product_image,
                    product_name = prod.product_name,
                    product_price = prod.product_price,
                    product_qty = prod.product_qty,
                )
                product_widget.bind(product_qty=self.update_totals)
                widget.add_widget(product_widget)
            self.update_totals()

            self.back_button.on_press = lambda *_: self.manager.change_screen("home")

    def checkout_all(self):
        products = []
        widget = self.layout.ids.product_grid
        for widget in widget.children:
            if isinstance(widget, ProductItem):
                products.append({
                    "productId": widget.product_id,
                    "numberOfProduct": widget.product_qty,
                    "sellerId": widget.seller_id,
                })

        RequestHandler.request_loader(self, self.manager,
            lambda: RequestHandler.create_req_suc_error("post", "orders/bulkOrder",
            {
                'products': products,
                'userId': self.manager.main_state['user']['id'],
            }, self.on_success_buy_now_product, self.on_error_buy_now_product))
    
    def on_error_buy_now_product(self, error):
        RequestHandler.show_error_popup(self.manager, "Order product error", str(error))
        self.layout.ids.product_grid.clear_widgets()
        self.manager.home.update_button_active("cart")
        self.manager.home.all_middle_section = {}

    def on_success_buy_now_product(self, result):
        RequestHandler.show_error_popup(self.manager, "Successful Order", "You successfully order the product(s).")
        self.manager.home.update_button_active("cart")
        self.manager.home.all_middle_section = {}

    def display_design(self):
        self.size = self.manager.size
        with self.canvas.before:
            Color(rgba=GetColor("#f1f1f1"))
            Rectangle(size=self.size)

            height = Utility.get_value_percentage(self.height, 0.08)
            Color(rgba=GetColor(self.manager.theme.main_color))
            Rectangle(
                size=(self.width, height),
                pos=(0, self.height-height),
            )
        self.display_widget()

    def display_widget(self):
        self.clear_widgets()
        widget = Widget(size=self.manager.size, pos=(0, 0))

        layout_scroll = ScrollView(
            size=(self.manager.width, self.manager.height*0.92), do_scroll_y=True, do_scroll_x=False, effect_cls=ScrollEffect)
        self.layout = CheckoutBody(
            orientation='vertical', size_hint=(1, None), spacing=Utility.get_value_percentage(self.height, 0.01),
            size=layout_scroll.size)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        # self.product_pic = ScrollView(
        #     size_hint=(0.9, None),
        #     pos_hint={'center_x': 0.5},
        #     height=dp(50), 
        #     do_scroll_x=True, 
        #     do_scroll_y=False,
        #     effect_cls=ScrollEffect
        # )
        # self.other_images = BoxLayout(size_hint=(0.95, None), height=dp(40), pos_hint={'center_x': 0.5}, spacing=dp(5))
        # self.other_images.bind(minimum_width=self.other_images.setter('width'))
        # self.product_pic.add_widget(self.other_images)

        # self.buy_now = CustomButtonWidget(text="Buy Now", size_hint=(None, None), size = (dp(100), dp(30)), pos_hint = {"center_x": 0.82})
        # self.buy_now.bind(on_release=self.buy_now_product)

        self.top_bar_layout = BoxLayout(
            orientation='horizontal', size_hint=(1, None),
            x=self.manager.width*0.025,
            y=Window.height - Utility.get_value_percentage(self.height, 0.05) - Utility.get_value_percentage(self.height, 0.015),
            width=self.manager.width*0.95,
            height=Utility.get_value_percentage(self.height, 0.05), spacing=dp(10))

        self.back_button = CustomImageButton(self.manager, src='assets/back.png', size_hint=(0.1, 1),
            on_press=lambda *_: self.manager.change_screen("product"))
        checkout_label = LeftLabel(text="Checkout", size_hint=(0.9, 1))

        self.top_bar_layout.add_widget(self.back_button)
        self.top_bar_layout.add_widget(checkout_label)

        layout_scroll.add_widget(self.layout)
        widget.add_widget(layout_scroll)
        widget.add_widget(PlaceOrderBottom(checkout_all=self.checkout_all))

        widget.add_widget(self.top_bar_layout)
        self.add_widget(widget)
    
    
