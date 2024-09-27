from kivy.uix.floatlayout import FloatLayout

class BaseSection(FloatLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.size_hint = (1, 1)
		self.pos_hint = {"center_x": 0.5, "center_y": 0.5}