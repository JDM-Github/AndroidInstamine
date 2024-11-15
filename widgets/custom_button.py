from kivy.uix.label	import Label
from kivy.uix.widget import	Widget

from kivy.metrics import dp
from kivy.utils	import get_color_from_hex as GetColor
from kivy.graphics import RoundedRectangle,	Color, Ellipse

from kivy.uix.image	import Image
from kivy.uix.button import	Button
from kivymd.uix.button import MDButton
from kivy.properties import	ObjectProperty


class LeftLabel(Label):
	pass

class CustomButtonWidget(Button):
	pass

class CustomButton(Widget):

	def	__init__(self, manager, text='', on_press=lambda: None, size_hint=(0.8, None),	pos_hint={"center_x": 0.5},	radius=[dp(20)], **kwargs):
		super().__init__(**kwargs)
		self.manager =	manager
		self.on_press =	on_press
		self.tdown	   = False

		self.size_hint = size_hint
		self.height	   = dp(45)
		self.pos_hint  = pos_hint

		self.label = Label(text=text, bold=True)
		self.add_widget(self.label)

		with self.canvas.before:
			self.color = Color(rgba=GetColor(self.manager.theme.main_color))
			self.rounded_rect =	RoundedRectangle(pos=(self.pos), size=self.size, radius=radius)

		self.bind(pos=self.update_rect,	size=self.update_rect)

	def	on_touch_down(self,	touch):
		if self.collide_point(*touch.pos):
			self.tdown = True
			self.color.rgba	= GetColor(self.manager.theme.main_hover_color)

	def	on_touch_up(self, touch):
		if self.tdown:
			self.tdown = False
			self.color.rgba	= GetColor(self.manager.theme.main_color)
			if self.collide_point(*touch.pos):
				self.on_press()

	def	update_rect(self, *args):
		self.rounded_rect.pos  = self.pos
		self.rounded_rect.size = self.size

		self.label.size	= self.size
		self.label.pos = self.pos


class CustomImageButton(Widget):

	manager = ObjectProperty(None)

	def	__init__(self, manager=None, src='', active=False,	is_active=False, on_press=lambda: None,	section='',	**kwargs):
		super().__init__(**kwargs)
		self.active	   = active
		self.is_active = is_active
		self.manager   = manager
		self.on_press  = on_press
		self.tdown	   = False
		self.section   = section

		self.image = Image(source=src)
		self.add_widget(self.image)


		if self.manager and hasattr(self.manager, 'theme'):
			with self.canvas.before:
				self.set_color()
				circle_size	= min(self.width, self.height)
				self.rounded_rect =	Ellipse(pos=(self.center_x - circle_size / 2, self.center_y	- circle_size /	2),	size=(circle_size, circle_size))
		
		self.bind(pos=self.update_rect,	size=self.update_rect)

	def	set_color(self):
		if self.active and self.is_active:
			self.color = Color(rgba=GetColor(self.manager.theme.main_hover_color))
		else:
			self.color = Color(rgba=GetColor(self.manager.theme.main_color))

	def	on_touch_down(self,	touch):
		if self.collide_point(*touch.pos):
			self.tdown = True

			if not self.active:
				self.color.rgba	= GetColor(self.manager.theme.main_hover_color)

	def	on_touch_up(self, touch):
		if self.tdown:
			self.tdown = False

			if self.collide_point(*touch.pos):
				self.on_press()

			self.is_active = not self.is_active
			if not self.active:
				self.color.rgba	= GetColor(self.manager.theme.main_color)

	def	update_rect(self, *args):
		circle_size	= min(self.width, self.height)
		self.rounded_rect.pos =	(self.center_x - circle_size / 2, self.center_y	- circle_size /	2)
		self.rounded_rect.size = (circle_size, circle_size)
		
		image_size = min(self.width, self.height) -	dp(10)
		self.image.pos = (self.center_x	- image_size / 2, self.center_y	- image_size / 2)
		self.image.size	= (image_size, image_size)