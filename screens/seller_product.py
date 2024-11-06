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

from popup.popups import ChatPopup
from screens.product_screen import CustomImage, MyGrid, PriceName, ProductReview, Specification
from widgets import RoundedTextInput, Utility, CustomImageButton
from handle_requests import RequestHandler
from widgets.custom_button import CustomButtonWidget
from widgets.product import CustomBoxLayout

class RevenueSold(CustomBoxLayout):
    revenue_text = StringProperty("")
    number_sold = StringProperty("")

class SellerProductScreen(Screen):

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
        bottom_layout.add_widget(RevenueSold(revenue_text='15000', number_sold='1500'))

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

        self.buy_now = CustomButtonWidget(text="Edit", size_hint=(None, None), size = (dp(100), dp(30)), pos_hint = {"center_x": 0.82})
        self.top_bar_layout = BoxLayout(orientation='horizontal', size_hint=(1, None),
            x=self.manager.width*0.025,
            y=Window.height - Utility.get_value_percentage(self.height, 0.05) - Utility.get_value_percentage(self.height, 0.015),
            width=self.manager.width*0.95,
            height=Utility.get_value_percentage(self.height, 0.05), spacing=dp(10))

        self.back_button    = CustomImageButton(self.manager, src='assets/back.png', size_hint=(0.1, 1), on_press=self.return_to_home)
        self.search_bar     = RoundedTextInput(icon_source='assets/pass.png', hint_text="Search...", size_hint=(0.7, 1))
        self.cart_icon      = CustomImageButton(self.manager, src='assets/cart.png', size_hint=(0.1, 1))
        self.message_button = CustomImageButton(self.manager, src='assets/chats.png', size_hint=(0.1, 1))

        self.top_bar_layout.add_widget(self.back_button)
        self.top_bar_layout.add_widget(self.search_bar)
        self.top_bar_layout.add_widget(self.cart_icon)
        self.top_bar_layout.add_widget(self.message_button)

        layout_scroll.add_widget(self.layout)
        widget.add_widget(layout_scroll)
        # widget.add_widget(MyGrid(self.manager, self.open_chat))

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

    def open_chat(self):
        RequestHandler.request_loader(self, self.manager,
            lambda: RequestHandler.create_req_suc_error("post", "chats/retrieve-chat",
            {
                'userId': self.manager.main_state['user']['id'],
                'partnerId': self.product.get('Users').get('id')
            }, self.on_success, self.on_error))

    def on_error(self, error):
        RequestHandler.show_error_popup(self.manager, "Chat opening error", error.get('message'))

    def on_success(self, result):
        popup = ChatPopup(
            self.manager,
            chat_id=self.product.get('Users').get('id'),
            chat_partner=self.product.get('Users').get('username'),
            all_chats=result.get('messages', []))
        popup.open()



