from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

from kivy.metrics import dp, sp
from .base_section import BaseSection

from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex as GetColor
from widgets import RoundedTextInput, CustomButton, CustomImageButton

class LiveSection(BaseSection):
	def __init__(self, manager, **kwargs):
		super().__init__(**kwargs)
		self.manager = manager
		self.display_screen()

	def display_screen(self):
		self.main_layout     = BoxLayout(orientation="vertical", size_hint=(1.1, 1), pos_hint={"center_x": 0.5, "center_y": 0.5})
		self.screen          = Image(size_hint=(1, 0.4), pos_hint={"center_x": 0.5})

		self.create_comment_section()
		self.main_layout.add_widget(self.screen)
		self.main_layout.add_widget(self.comment_section_layout)
		self.main_layout.add_widget(Widget(size_hint=(1, 0.03)))
		self.add_widget(self.main_layout)
		self.set_instamine()

	def set_instamine(self):
		self.instamine_button = CustomButton(self.manager, text="INSTAMINE", size_hint=(None, None), radius=[dp(10)])
		self.instamine_button.pos_hint = {"center_x": 0.85}
		self.instamine_button.size = (dp(100), dp(40))
		self.instamine_button.pos = (0, self.manager.height*0.6)
		self.add_widget(self.instamine_button)

	def create_comment_section(self):
		self.comment_section_layout = BoxLayout(orientation="vertical", size_hint=(0.85, 0.5), pos_hint={"center_x": 0.5})
		self.comment_section_layout.add_widget(Widget(size_hint=(1, 0.05)))

		self.label_instance = Label(text="768345 watching...", color=self.manager.theme.font_color_88, size_hint=(1, 0.05), halign="left")
		self.comment_section_layout.add_widget(self.label_instance)
		self.bind(size=lambda *args: self.label_instance.setter('text_size')(self.label_instance, (self.width, None)))
		self.comment_section_layout.add_widget(Widget(size_hint=(1, 0.05)))

		self.scrollview = ScrollView(size_hint=(1, 0.8))
		self.comments_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
		self.comments_layout.bind(minimum_height=self.comments_layout.setter('height'))
		self.scrollview.add_widget(self.comments_layout)
		self.comment_section_layout.add_widget(self.scrollview)
		self.comment_section_layout.add_widget(Widget(size_hint=(1, 0.05)))

		self.comment_input = RoundedTextInput(hint_text="Say Something...", size_hint=(0.7, 1))
		# self.comment_input.input.multiline = True

		self.submit_button = CustomImageButton(self.manager, src='assets/send.png', size_hint=(0.1, 1),
			on_press=lambda : self.add_comment("JD", None, True))


		self.add_comment("OTHER", "This is a test", False)
		self.add_comment("OTHER", "This is a test", False)
		self.add_comment("OTHER", "This is a test", False)

		Clock.schedule_interval(lambda _: self.add_comment("OTHER", "This is a test", False), 4)


		self.share_button = CustomImageButton(self.manager, src='assets/share.png', size_hint=(0.1, 1))
		self.heart_button = CustomImageButton(self.manager, src='assets/heart.png', size_hint=(0.1, 1))

		input_layout = BoxLayout(size_hint=(1, 0.1), pos_hint={"center_x": 0.5}, spacing=10)
		input_layout.add_widget(self.comment_input)
		input_layout.add_widget(self.submit_button)
		input_layout.add_widget(self.share_button)
		input_layout.add_widget(self.heart_button)

		self.comment_section_layout.add_widget(input_layout)

	def add_comment(self, says_by, message, is_me):
		comment_text = message if message else self.comment_input.input.text
		if comment_text.strip():
			new_comment = Comment(self.manager, says_by, is_me,
				text=comment_text, size_hint_y=None, height=dp(40))
			self.comments_layout.add_widget(new_comment)
			if is_me:
				self.comment_input.input.text = ''

			self.scrollview.scroll_to(new_comment)


class Comment(Label):

	def __init__(self, manager, says_by, is_me, **kwargs):
		super().__init__(**kwargs)
		self.is_me = is_me
		self.text = f"[b][color=#dddddd]{says_by}[/color][/b]: {self.text}"
		self.markup = True

		self.color = manager.theme.comment_text_color
		self.font_size = sp(12)
		self.halign = 'left'
		self.valign = 'top'
		self.bind(pos=self._update, size=self._update)
		self.bind(texture_size=self.test)
	
	def test(self, *_):
		self.height = self.texture_size[1] + dp(20)
		self._update()
	
	def _update(self, *_):
		self.text_size = (self.width*0.9, None)
		self.canvas.before.clear()
		with self.canvas.before:
			Color(rgba=GetColor("00000088" if self.is_me else "00000055"))
			RoundedRectangle(radius=[dp(20)], size=self.size,
				pos=self.pos)
