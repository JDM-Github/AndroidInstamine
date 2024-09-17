from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse

class CircleImage(Widget):

	def __init__(self, source='',  **kwargs):
		super().__init__(**kwargs)
		self.image = Image(source=source)
		with self.canvas.before:
			self.image_circle = Ellipse(texture=self.image.texture, size=self.size, pos=self.pos)

		self.bind(pos=self.update_rect, size=self.update_rect)

	def update_rect(self, *args):
		self.image_circle.pos  = self.pos
		self.image_circle.size = self.size
