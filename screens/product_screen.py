import threading
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.effects.scroll import ScrollEffect
from kivy.uix.textinput import TextInput

from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex as GetColor
from kivy.graphics import Rectangle, RoundedRectangle, Color, Line
from kivy.uix.screenmanager import SlideTransition, FadeTransition, WipeTransition, SwapTransition

from widgets import CircleImage, RoundedTextInput, CustomButton, LoadingPopup, BackButton, Utility, ThemedPopup, CustomImageButton
from handle_requests import RequestHandler

class BindWidget(Widget):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.radius = [dp(10), dp(10), 0, 0]
		self.bind(size=self._update, pos=self._update)

	def _update(self, *_):
		self.canvas.before.clear()
		with self.canvas.before:
			Color(rgba=GetColor("#ffffff"))
			RoundedRectangle(
				pos=(self.pos),
				size=(self.width, self.height),
				radius=self.radius)

class CustomImage(Image):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.bind(size=self._update, pos=self._update)

	def _update(self, *_):
		self.canvas.after.clear()
		with self.canvas.after:
			Color(rgb=GetColor("#aaaaaa"))
			Line(rectangle=(self.x, self.y, self.width, self.height), width=1)

class StarRating(BoxLayout):

	def __init__(self, rating, **kwargs):
		super().__init__(**kwargs)
		self.orientation = 'horizontal'
		self.spacing = dp(2)
		self.size_hint_y = None
		self.height = dp(15)

		self.full_star = 'assets/fullstar.png'   
		self.half_star = 'assets/halfstar.png'   
		self.empty_star = 'assets/emptystar.png' 

		self.create_star_rating(rating)

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
	def __init__(self, manager, **kwargs):
		super().__init__(**kwargs)
		self.orientation = "horizontal"
		self.width = Window.width
		self.height = dp(40)

		self.chat_image = CustomImageButton(manager, src="assets/chats.png", size_hint_x=0.3)
		with self.chat_image.canvas.before:
			Color(rgb=GetColor("#AD85A9")) 
			self.chat_rect = Rectangle(size=self.chat_image.size, pos=self.chat_image.pos)
			self.chat_image.bind(size=self._update_rect, pos=self._update_rect)
		self.add_widget(self.chat_image)

		self.cart_image = CustomImageButton(manager, src="assets/cart.png", size_hint_x=0.3)
		with self.cart_image.canvas.before:
			Color(rgb=GetColor("#AD85A9")) 
			self.cart_rect = Rectangle(size=self.cart_image.size, pos=self.cart_image.pos)
			self.cart_image.bind(size=self._update_rect, pos=self._update_rect)
		self.add_widget(self.cart_image)

		self.buy_now_label = Label(text="BUY NOW", color=(1, 1, 1, 1), bold=True) 
		with self.buy_now_label.canvas.before:
			Color(rgb=GetColor("#9C3E93")) 
			self.buy_now_rect = Rectangle(size=self.buy_now_label.size, pos=self.buy_now_label.pos)
			self.buy_now_label.bind(size=self._update_rect, pos=self._update_rect)
		self.add_widget(self.buy_now_label)

	def _update_rect(self, *_):
		self.chat_rect.size = self.chat_image.size
		self.chat_rect.pos  = self.chat_image.pos 

		self.cart_rect.size = self.cart_image.size
		self.cart_rect.pos  = self.cart_image.pos 

		self.buy_now_rect.size = self.buy_now_label.size
		self.buy_now_rect.pos  = self.buy_now_label.pos 

class Toolbar(BoxLayout):

	def __init__(self, manager, **kwargs):
		super().__init__(**kwargs)
		self.orientation = 'horizontal'
		self.size_hint_y = None
		self.height = dp(30)
		self.y = Window.height - dp(40)
		self.padding = [dp(10), 0, dp(10), 0]
		
		# Back Button (on the left)
		back_button = CustomImageButton(manager, src="assets/cart.png", size_hint=(None, None), size=(dp(30), dp(30)))
		self.add_widget(back_button)
		self.add_widget(BoxLayout())

		share_button = CustomImageButton(manager, src="assets/cart.png", size_hint=(None, None), size=(dp(30), dp(30)))
		cart_button = CustomImageButton(manager, src="assets/cart.png", size_hint=(None, None), size=(dp(30), dp(30)))
		menu_button = CustomImageButton(manager, src="assets/cart.png", size_hint=(None, None), size=(dp(30), dp(30)))

		self.add_widget(share_button)
		self.add_widget(cart_button)
		self.add_widget(menu_button)
		# self.add_widget(buttons_layout)

class BottomLayout(BoxLayout, BindWidget):
	pass

class PriceName(BottomLayout):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.orientation = "vertical"
		self.height    = dp(60)
		self.size_hint_y = None
		self.padding = [dp(20), dp(10)]
		self.radius = [dp(0)]

		price = Label(text="P[size=18sp]500[/size]", color="#9C3E93", bold=True, font_size=sp(16),
			halign='left', markup=True)
		price.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))

		product_name = Label(text="Test Title", color="#333333", font_size=sp(18), halign='left', bold=True)
		product_name.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))

		self.add_widget(price)
		self.add_widget(product_name)

class ShopWidget(BottomLayout):

	def __init__(self, manager, **kwargs):
		super().__init__(**kwargs)
		self.manager = manager
		self.orientation = "vertical"
		self.height = dp(100)
		self.size_hint_y = None
		self.padding = [dp(20), dp(5), dp(20), dp(5)]
		self.radius = [dp(0)]
		self.spacing = dp(10)

		top_layout = BoxLayout(orientation='horizontal', size_hint_y=None)
		seller_profile = Image(
			source="path_to_seller_profile_image", 
			size_hint=(None, None),
			size=(dp(50), dp(50)),
			pos_hint={'center_y': 0.5}
		)

		seller_info_layout = BoxLayout(orientation='vertical', padding=[dp(10), 0, dp(10), 0], spacing=dp(5))
		seller_name = Label(
			text="Seller Name or Organization",
			font_size=sp(16),
			color="#111111",
			size_hint_y=None,
			height=dp(20),
			halign='left'
		)
		seller_name.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))

		seller_status = Label(
			text="Active 4 minutes ago",
			font_size=sp(12),
			color="#555555",
			size_hint_y=None,
			height=dp(20),
			halign='left'
		)
		seller_status.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))

		seller_location = Label(
			text="Location: City, Country",
			font_size=sp(12),
			color="#777777",
			size_hint_y=None,
			height=dp(20),
			halign='left'
		)
		seller_location.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))

		seller_info_layout.add_widget(seller_name)
		seller_info_layout.add_widget(seller_status)
		seller_info_layout.add_widget(seller_location)

		view_shop_button = CustomButton(
			self.manager,
			text="View Shop",
			size_hint=(None, None),
			height=dp(40),
			width=dp(100),
			pos_hint={'center_y': 0.5},
		)

		top_layout.add_widget(seller_profile)
		top_layout.add_widget(seller_info_layout)
		top_layout.add_widget(view_shop_button)

		self.add_widget(top_layout)

class SellerInformationResponse(BottomLayout):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.orientation = "horizontal"
		self.height = dp(20)
		self.size_hint_y = None
		self.padding = [dp(20), dp(5), dp(20), dp(5)]
		self.radius = [dp(0)]
		self.spacing = dp(10)

		product_count = Label(
			text="541 [color=#9C3E93]Products[/color]",
			font_size=sp(14),
			color="#111111",
			size_hint=(None, 1),
			width=dp(100),
			halign='left',
			markup=True
		)
		product_count.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))

		rating = Label(
			text="4.8 [color=#9C3E93]Ratings[/color]",
			font_size=sp(14),
			color="#111111",
			size_hint=(None, 1),
			width=dp(100),
			halign='left',
			markup=True
		)
		rating.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))

		chat_response = Label(
			text="43% [color=#9C3E93]Chat Response[/color]",
			font_size=sp(14),
			color="#111111",
			size_hint=(None, 1),
			width=dp(150),
			halign='left',
			markup=True
		)
		chat_response.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))

		self.add_widget(product_count)
		self.add_widget(rating)
		self.add_widget(chat_response)


class Specification(BottomLayout):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.bind(minimum_height=self.setter('height'))
		self.orientation = "vertical"
		self.size_hint_y = None
		self.padding = [dp(20), dp(5), dp(20), dp(20)]
		self.radius = [dp(0)]
		self.spacing = dp(10)

		spec_label = Label(
			text="Specification",
			font_size=sp(16),
			size_hint_y=None,
			height=dp(20),
			color="#111111",
			halign='left',
		)
		spec_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))

		description = Label(
			text="This is a long description about the product specifications. "
				 "It contains detailed information regarding the product's features",
			font_size=sp(14),
			color="#555555",
			size_hint_y=None,
			text_size=(None, None),
			halign='left',
			valign='top',
		)
		description.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
		description.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))

		scroll_view = ScrollView(
			effect_cls=ScrollEffect,
			size_hint=(1, None),
			size=(Window.width, dp(100)),
			do_scroll_x=False,
			do_scroll_y=True
		)
		scroll_view.add_widget(description)


		self.add_widget(spec_label)
		self.add_widget(scroll_view)

class ProductReview(BoxLayout):

	def __init__(self, manager, **kwargs):
		super().__init__(**kwargs)
		self.manager = manager
		self.bind(minimum_height=self.setter('height'))
		self.orientation = "vertical"
		self.size_hint_y = None
		self.spacing = dp(5)

		top_layout = BottomLayout(orientation='horizontal', size_hint_y=None, height=dp(30), padding=[dp(20), dp(10)])
		self.ratings_label = Label(
			text="4.9 [color=#9C3E93]Product Ratings[/color] (2.3k)",
			font_size=sp(16),
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

		self.add_review(
			email="john@example.com",
			rating=5,
			variation="Pink",
			review_text="Great product! Highly recommend.",
			best_feature="Performance",
			product_quality="Excellent",
			images=["assets/test_product.jpg", "assets/test_product.jpg"]
		)

		self.add_review(
			email="john@example.com",
			rating=4.7,
			variation="Pink",
			review_text="Great product! Highly recommend.",
			best_feature="Performance",
			product_quality="Excellent",
			images=["assets/test_product.jpg", "assets/test_product.jpg"]
		)

		self.add_widget(top_layout)
		self.add_widget(self.reviews_layout)

	def add_review(self, email, rating, variation, review_text, best_feature, product_quality, images):
		review_layout = BottomLayout(orientation='vertical', size_hint_y=None, spacing=dp(5), padding=[dp(20), dp(10)])
		review_layout.bind(minimum_height=review_layout.setter('height'))

		user_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(20), spacing=dp(5))

		profile_image = Image(color="#555555", size_hint=(0.1, 1))
		profile_label = Label(
			text=f"{email}",
			font_size=sp(14),
			color="#555555",
			halign='left',
		)
		profile_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
		helpful_button = CustomButton(
			self.manager,
			text="Helpful",
			size_hint=(None, 1),
			width=dp(80),
			radius=[dp(10)]
		)

		kwargs = {
			'font_size': sp(14),
			'color': "#555555",
			'size_hint_y': None,
			'height': dp(15),
			'halign': 'left',
		}
		user_layout.add_widget(profile_image)
		user_layout.add_widget(profile_label)
		user_layout.add_widget(helpful_button)
		rating_label = Label(text=f"{rating} ★", **kwargs)
		rating_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))

		variation_label = Label(text=f"Variation: {variation}", **kwargs)
		variation_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))

		feature_label = Label(text=f"Best Feature: {best_feature}", **kwargs)
		feature_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))

		quality_label = Label(text=f"Product Quality: {product_quality}", **kwargs)
		quality_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))

		review_label = Label(
			text=review_text,
			font_size=sp(14),
			color="#555555",
			halign='left',
			size_hint_y=None,
			height=dp(20),
			text_size=(None, None),
		)
		review_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
		review_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))

		images_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(80))
		for image_source in images[:3]:
			image_widget = Image(
				source=image_source,
				size_hint=(1, None),
				height=dp(70),
			)
			images_layout.add_widget(image_widget)

		review_layout.add_widget(user_layout)
		review_layout.add_widget(StarRating(rating))
		review_layout.add_widget(variation_label)
		review_layout.add_widget(feature_label)
		review_layout.add_widget(quality_label)
		review_layout.add_widget(review_label)

		if images:
			review_layout.add_widget(images_layout)

		self.reviews_layout.add_widget(review_layout)

class ProductScreen(Screen):

	def update_product(self, product_id):
		self.layout.clear_widgets()

		image = Image(
			color="#aaaaaa",
			source="",
			size_hint=(0.9, None),
			pos_hint={'center_x': 0.5},
			height=Window.height*0.40,
			fit_mode="fill"
		)
		self.other_images.clear_widgets()
		self.other_images.add_widget(CustomImage(color="#aaaaaa", source="", size_hint_x=None, width=dp(40)))
		self.other_images.add_widget(CustomImage(color="#aaaaaa", source="", size_hint_x=None, width=dp(40)))
		self.other_images.add_widget(CustomImage(color="#aaaaaa", source="", size_hint_x=None, width=dp(40)))
		self.other_images.add_widget(CustomImage(color="#aaaaaa", source="", size_hint_x=None, width=dp(40)))
		self.other_images.add_widget(CustomImage(color="#aaaaaa", source="", size_hint_x=None, width=dp(40)))

		bottom_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(500), spacing=dp(10))
		bottom_layout.bind(minimum_height=bottom_layout.setter('height'))

		bottom_layout.add_widget(PriceName())
		bottom_layout.add_widget(ShopWidget(self.manager))
		bottom_layout.add_widget(SellerInformationResponse())
		bottom_layout.add_widget(Specification())
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

		self.buy_now = CustomButton(self.manager, text="Buy Now", size_hint=(None, None), radius=[dp(10)])
		self.buy_now.pos_hint = {"center_x": 0.82}
		self.buy_now.size = (dp(100), dp(30))
		self.buy_now.pos = (0, self.manager.height*0.6)

		
		self.top_bar_layout = BottomLayout(orientation='horizontal', size_hint=(1, None),
			x=self.manager.width*0.025,
			y=Window.height - Utility.get_value_percentage(self.height, 0.05) - Utility.get_value_percentage(self.height, 0.015),
			width=self.manager.width*0.95,
			height=Utility.get_value_percentage(self.height, 0.05), spacing=dp(10))

		self.back_button    = CustomImageButton(self.manager, src='assets/back.png', size_hint=(0.1, 1), on_press=self.return_to_home)
		self.search_bar     = RoundedTextInput(icon_source='assets/pass.png', hint_text="Search...", size_hint=(0.7, 1))
		self.cart_icon      = Image(source='assets/cart.png', size_hint=(0.1, 1))
		self.message_button = Image(source='assets/chats.png', size_hint=(0.1, 1))

		self.top_bar_layout.add_widget(self.back_button)
		self.top_bar_layout.add_widget(self.search_bar)
		self.top_bar_layout.add_widget(self.cart_icon)
		self.top_bar_layout.add_widget(self.message_button)

		layout_scroll.add_widget(self.layout)
		widget.add_widget(layout_scroll)
		widget.add_widget(MyGrid(self.manager))

		widget.add_widget(self.top_bar_layout)
		self.add_widget(widget)

	def layout_on_ref_press(self, *args):
		pass

	def return_to_home(self, *_):
		self.manager.current = "home"

