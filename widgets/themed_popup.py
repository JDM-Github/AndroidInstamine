from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.graphics import RoundedRectangle, Color
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivy.utils import get_color_from_hex as GetColor

class ThemedPopup(Popup):
	def __init__(self, manager, title="Popup", message="", separator_height=dp(2), **kwargs):
		super().__init__(**kwargs)
		white_color   = GetColor("#FFFFFF")
		pinkish_color = GetColor(manager.theme.main_color)
		text_color    = GetColor("#333333")

		self.separator_height = separator_height
		self.separator_color = pinkish_color

		layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
		scroll_view = ScrollView(size_hint=(1, None), height=dp(120))
		self.error_message = Label(
			text_size=(self.width, None),
			text=message, halign='center', valign='middle', color=text_color, size_hint_y=None)
		self.error_message.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
		scroll_view.add_widget(self.error_message)

		close_button = Button(text="Close", size_hint=(1, None), height=dp(40),
						background_normal='', background_color=pinkish_color, color=white_color)
		close_button.bind(on_press=self.dismiss)

		layout.add_widget(scroll_view)
		layout.add_widget(close_button)

		self.title = title
		self.title_color = pinkish_color
		self.title_align = 'center'
		self.content = layout
		
		self.size_hint = (0.8, 0.4)
		self.auto_dismiss = False

		self.background = ''
		self.bind(size=self.update_size)

	def update_size(self, *_):
		self.error_message.text_size = (self.width*0.75, None)

