from kivy.uix.label import Label
from kivy.metrics import sp
from .base_section import BaseSection

class TopNotification(Label):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.text        = "Notification"
		self.size_hint_x = 0.9
		self.font_size   = sp(16)
		self.halign      = 'left'
		self.valign      = 'top'
		self.bold        = True
		self.bind(pos=self._update, size=self._update)

	def _update(self, *_):
		self.text_size = (self.width*0.9, None)

class NotificationSection(BaseSection):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
