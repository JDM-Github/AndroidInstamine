from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.graphics import Rectangle, RoundedRectangle, Color, Line, Ellipse

from widgets import Utility

class LiveScreen(Screen):

	def display_design(self):
		with self.canvas.before:
			Color(rgba=GetColor(self.manager.theme.main_color))
			Rectangle(size=self.size)
		self.display_widget()

	def display_widget(self):
		pass

