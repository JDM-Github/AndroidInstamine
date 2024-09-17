from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle, Ellipse, RoundedRectangle
from kivy.utils import get_color_from_hex as GetColor
from kivy.uix.screenmanager import Screen

class HomeScreen(Screen):

	def display_design(self):
		self.size = self.manager.size
		with self.canvas.before:
			Color(rgba=GetColor(self.manager.theme.main_color))
			Rectangle(size=self.size)

			Color(rgba=GetColor("#ffffff"))
			RoundedRectangle(
				size=(self.width, Utility.get_value_percentage(self.height, 0.25)),
				radius=[dp(30), dp(30), 0, 0])

		self.display_widget()

	def display_widget(self):
		self.clear_widgets()
		widget = Widget(size=self.manager.size, pos=(0, 0))
		spacepadd = Utility.get_value_percentage(self.height, 0.015)
		layout = BoxLayout(size=self.manager.size, orientation='vertical', padding=spacepadd, spacing=spacepadd)

		main_color     = self.manager.theme.main_color
		main_color_88  = self.manager.theme.main_color_88
