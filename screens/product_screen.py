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

from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty

from popup.popups import BuyOrder, ChatPopup
from widgets import CircleImage, RoundedTextInput, CustomButton, LoadingPopup, BackButton, Utility, ThemedPopup, CustomImageButton
from handle_requests import RequestHandler
from widgets.custom_button import CustomButtonWidget
from widgets.product import CustomBoxLayout

class CustomImage(AsyncImage):
    border_color = StringProperty("#aaaaaa")

class StarRating(BoxLayout):

    rating = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = dp(2)
        self.size_hint_y = None
        self.height = dp(15)

        self.full_star  = 'assets/fullstar.png'     
        self.half_star  = 'assets/halfstar.png'     
        self.empty_star = 'assets/emptystar.png'    

        self.bind(rating=lambda *_: self.create_star_rating(self.rating))

    def create_star_rating(self, rating):
        for i in range(1, 6):
            if rating >= i: 
                star = Image(source=self.full_star, size_hint=(None, None), size=(dp(15), dp(15)))
            elif i - rating <= 0.5: 
                star = Image(source=self.half_star, size_hint=(None, None), size=(dp(15), dp(15)))
            else: 
                star = Image(source=self.empty_star, size_hint=(None, None), size=(dp(15), dp(15)))
            self.add_widget(star)

class MyGrid(BoxLayout):
    def __init__(self, manager, open_chat, add_cart_product, buy_now_product, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.width = Window.width
        self.height = dp(40)

        self.chat_image = CustomImageButton(manager, src="assets/chats.png", size_hint_x=0.3, on_press=open_chat)
        with self.chat_image.canvas.before:
            Color(rgb=GetColor("#AD85A9")) 
            self.chat_rect = Rectangle(size=self.chat_image.size, pos=self.chat_image.pos)
            self.chat_image.bind(size=self._update_rect, pos=self._update_rect)
        self.add_widget(self.chat_image)

        self.cart_image = CustomImageButton(manager, src="assets/cart.png", size_hint_x=0.3, on_press=add_cart_product)
        with self.cart_image.canvas.before:
            Color(rgb=GetColor("#AD85A9")) 
            self.cart_rect = Rectangle(size=self.cart_image.size, pos=self.cart_image.pos)
            self.cart_image.bind(size=self._update_rect, pos=self._update_rect)
        self.add_widget(self.cart_image)

        self.buy_now_label = CustomButtonWidget(text="BUY NOW", color=(1, 1, 1, 1), bold=True, on_press=buy_now_product)
        self.add_widget(self.buy_now_label)

    def _update_rect(self, *_):
        self.chat_rect.size = self.chat_image.size
        self.chat_rect.pos  = self.chat_image.pos 

        self.cart_rect.size = self.cart_image.size
        self.cart_rect.pos  = self.cart_image.pos 


class PriceName(CustomBoxLayout):
    price_text = StringProperty("")
    title_text = StringProperty("")

class ShopWidget(CustomBoxLayout):
    seller_profile = StringProperty("")
    seller_text = StringProperty("")
    is_active = StringProperty("")
    location_text = StringProperty("")

class SellerInformationResponse(CustomBoxLayout):
    numberProduct = StringProperty("")
    userRating = StringProperty("")
    chatResponse = StringProperty("")
    function = ObjectProperty(None)

    def checkProducts(self):
        self.function()

class Specification(CustomBoxLayout):
    specification = StringProperty("")

class ReviewImage(Image): pass
class ReviewProduct(CustomBoxLayout):

    email = StringProperty("")
    rating = NumericProperty(0)
    review_text = StringProperty("")
    best_feature = StringProperty("")
    product_quality = StringProperty("")

    def __init__(self, email, rating, best_feature, product_quality, review_text, images=[], **kwargs):
        super().__init__(**kwargs)
        self.email = email
        self.rating = rating
        self.review_text = review_text
        self.best_feature = best_feature
        self.product_quality = product_quality

        self.images_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(80))
        for image_source in images[:3]:
            image_widget = ReviewImage(source=image_source)
            self.images_layout.add_widget(image_widget)
        self.images_layout.add_widget(Widget())

        if images:
            self.add_widget(self.images_layout)

class ProductReview(BoxLayout):

    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager
        self.bind(minimum_height=self.setter('height'))
        self.orientation = "vertical"
        self.size_hint_y = None
        self.spacing = dp(5)

        top_layout = CustomBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(30), padding=[dp(20), dp(10)])
        self.ratings_label = Label(
            text="4.9 [color=#9C3E93]Product Ratings[/color] (2.3k)",
            font_size=sp(14),
            color="#111111",
            size_hint=(0.8, 1),
            halign='left',
            markup=True
        )
        self.ratings_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))

        view_all_button = Button(
            text="View All >",
            size_hint=(0.2, 1),
            background_normal="",
            background_down="",
            color="#555555"
        )
        top_layout.add_widget(self.ratings_label)
        top_layout.add_widget(view_all_button)

        self.reviews_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5),)
        self.reviews_layout.bind(minimum_height=self.reviews_layout.setter('height'))

        self.reviews_layout.add_widget(ReviewProduct(
            email="john@example.com",
            rating=4.7,
            review_text="Great product! Highly recommend.",
            best_feature="Performance",
            product_quality="Excellent",
            images=["assets/test_product.jpg", "assets/test_product.jpg"]
        ))

        self.add_widget(top_layout)
        self.add_widget(self.reviews_layout)


class ProductScreen(Screen):

    layout = ObjectProperty(None)

    def update_product(self, product):
        self.product = product
        self.layout.clear_widgets()

        image = AsyncImage(
            color="#aaaaaa",
            source=product.get('product_image'),
            size_hint=(0.9, None),
            pos_hint={'center_x': 0.5},
            height=Window.height*0.40,  
            fit_mode="fill"
        )

        self.other_images.clear_widgets()
        for img in product.get('product_images'):
            self.other_images.add_widget(CustomImage(source=img))

        bottom_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(500), spacing=dp(10))
        bottom_layout.bind(minimum_height=bottom_layout.setter('height'))

        bottom_layout.add_widget(PriceName(price_text=product.get('price'), title_text=product.get('name')))
        bottom_layout.add_widget(ShopWidget(
            seller_profile=product.get('Users').get('profileImage'),
            seller_text=product.get('Users').get('username'),
            is_active="Active" if product.get('Users').get('online') else "OFFLINE",
            location_text=product.get('Users').get('location') + "TEST"
        ))
        bottom_layout.add_widget(SellerInformationResponse(
            numberProduct=product.get('Users').get('numberProduct'),
            userRating="4.5",
            chatResponse="25%",
            function=self.sellerProductSection
        ))
        bottom_layout.add_widget(Specification(specification=product.get('specification')))
        bottom_layout.add_widget(ProductReview(self.manager))
        bottom_layout.add_widget(Widget(size_hint_y=None, height=dp(80)))

        self.layout.add_widget(Widget(size_hint_y=None, height=dp(10)))
        self.layout.add_widget(image)
        self.layout.add_widget(self.product_pic)
        self.layout.add_widget(self.buy_now)
        self.layout.add_widget(bottom_layout)

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

        layout_scroll = ScrollView(size=(self.manager.width, self.manager.height*0.92), do_scroll_y=True, do_scroll_x=False, effect_cls=ScrollEffect)
        self.layout = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=Utility.get_value_percentage(self.height, 0.01), size=layout_scroll.size)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.product_pic = ScrollView(
            size_hint=(0.9, None),
            pos_hint={'center_x': 0.5},
            height=dp(50), 
            do_scroll_x=True, 
            do_scroll_y=False,
            effect_cls=ScrollEffect
        )
        self.other_images = BoxLayout(size_hint=(0.95, None), height=dp(40), pos_hint={'center_x': 0.5}, spacing=dp(5))
        self.other_images.bind(minimum_width=self.other_images.setter('width'))
        self.product_pic.add_widget(self.other_images)

        self.buy_now = CustomButtonWidget(text="Buy Now", size_hint=(None, None), size = (dp(100), dp(30)), pos_hint = {"center_x": 0.82})
        self.buy_now.bind(on_release=self.buy_now_product)

        self.top_bar_layout = BoxLayout(orientation='horizontal', size_hint=(1, None),
            x=self.manager.width*0.025,
            y=Window.height - Utility.get_value_percentage(self.height, 0.05) - Utility.get_value_percentage(self.height, 0.015),
            width=self.manager.width*0.95,
            height=Utility.get_value_percentage(self.height, 0.05), spacing=dp(10))

        self.back_button    = CustomImageButton(self.manager, src='assets/back.png', size_hint=(0.1, 1), on_press=self.return_to_home)
        self.cart_icon      = CustomImageButton(self.manager, src='assets/cart.png', size_hint=(0.1, 1))
        self.message_button = CustomImageButton(self.manager, src='assets/chats.png', size_hint=(0.1, 1))

        self.top_bar_layout.add_widget(self.back_button)
        self.top_bar_layout.add_widget(Widget(size_hint=(0.7, 1)))
        self.top_bar_layout.add_widget(self.cart_icon)
        self.top_bar_layout.add_widget(self.message_button)

        layout_scroll.add_widget(self.layout)
        widget.add_widget(layout_scroll)
        widget.add_widget(MyGrid(self.manager, self.open_chat, self.add_cart_product, self.buy_now_product))

        widget.add_widget(self.top_bar_layout)
        self.add_widget(widget)

    def return_to_home(self, *_):
        self.manager.current = "home"

    def sellerProductSection(self):
        self.manager.current = "home"
        self.manager.home.update_button_active('sellerProducts', {
            'user': self.product.get('Users').get('username'),
            'email': self.product.get('Users').get('email'),
        })
        self.manager.home.back_button.on_press = lambda: self.manager.change_screen("product")
    
    def buy_now_product(self, *_):
        if self.manager.main_state['user']['location'] == "" and \
            self.manager.main_state['user']['phoneNumber'] == "":
            RequestHandler.show_error_popup(self.manager, "Order Error", "Please setup your account information.")
        else:
            self.manager.checkout.update_checkout(self.product)
            self.manager.current = "checkout"

    def on_error_buy_now_product(self, error):
        RequestHandler.show_error_popup(self.manager, "Order product error", str(error))
        self.manager.home.all_middle_section = {}

    def on_success_buy_now_product(self, result):
        popup = BuyOrder()
        popup.open()
        # RequestHandler.show_error_popup(self.manager, "Successfully order a product", "You successfully order the product")
        # self.manager.home.all_middle_section = {}
    

    def add_cart_product(self, *_):
        RequestHandler.request_loader(self, self.manager,
            lambda: RequestHandler.create_req_suc_error("post", "cart/createCart",
            {
                'productId': self.product.get('id'),
                'userId': self.manager.main_state['user']['id']
            }, self.on_success_add_cart_product, self.on_error_add_cart_product))

    def on_error_add_cart_product(self, error):
        RequestHandler.show_error_popup(self.manager, "Order product error", str(error['message']))
        self.manager.home.all_middle_section = {}

    def on_success_add_cart_product(self, result):
        RequestHandler.show_error_popup(self.manager, "Successfully cart a product", "You successfully cart the product")
        self.manager.home.all_middle_section = {}

    def open_chat(self):
        RequestHandler.request_loader(self, self.manager,
            lambda: RequestHandler.create_req_suc_error("post", "chats/retrieve-chat",
            {
                'userId': self.manager.main_state['user']['id'],
                'partnerId': self.product.get('Users').get('id')
            }, self.on_success_open_chat, self.on_error_open_chat))

    def on_error_open_chat(self, error):
        RequestHandler.show_error_popup(self.manager, "Chat opening error", error.get('message'))

    def on_success_open_chat(self, result):
        popup = ChatPopup(
            self.manager,
            chat_id=self.product.get('Users').get('id'),
            chat_partner=self.product.get('Users').get('username'),
            all_chats=result.get('messages', []))
        popup.open()



