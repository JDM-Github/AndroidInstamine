from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.dropdown import DropDown

from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex as GetColor
from datetime import datetime, timedelta
import calendar

class CustomButton(Button):
	def __init__(self, manager, **kwargs):
		super().__init__(**kwargs)
		white_color  = GetColor("#FFFFFF")
		pinkish_color = GetColor(manager.theme.main_color)

		self.background_normal = ''
		self.background_color = pinkish_color
		self.color = white_color
		self.padding = [10, 10, 10, 10]

class CustomSpinnerOption(SpinnerOption):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		white_color   = GetColor("#FFFFFF")
		pinkish_color = GetColor("#7C1E73")

		self.background_normal = ''
		self.background_color = pinkish_color 
		self.color = white_color
		self.font_size = 16

class LimitedHeightDropDown(DropDown):
	def __init__(self, **kwargs):
		super(LimitedHeightDropDown, self).__init__(**kwargs)
		self.max_height = dp(300)

class DatePicker(BoxLayout):
	def __init__(self, manager, callback, pop, **kwargs):
		super().__init__(**kwargs)
		self.manager     = manager
		white_color      = GetColor("#FFFFFF")
		pinkish_color    = GetColor(self.manager.theme.main_color)
		text_color       = GetColor("#333333")
		self.orientation = "vertical"
		self.spacing     = dp(5)
		self.pop         = pop

		self.callback    = callback
		self.selected_day = datetime.now().day
		self.year         = datetime.now().year
		self.month        = datetime.now().month
		self.months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
		self.date_text = ""

		nav_bar = BoxLayout(size_hint_y=None, height=dp(30), spacing=dp(5))
		kwargs_spinner = {
			'option_cls'        : CustomSpinnerOption,
			'background_normal' : '',
			'background_color'  : pinkish_color,
			'color'             : white_color,
			'sync_height'       : True,
			'dropdown_cls'      : LimitedHeightDropDown
		}
		self.month_spinner = Spinner(text=self.months[self.month - 1], values=self.months, **kwargs_spinner)
		self.year_spinner  = Spinner(text=str(self.year), values=[str(i) for i in range(1970, 2100)], **kwargs_spinner)

		self.month_spinner.bind(text=self.on_month_change)
		self.year_spinner .bind(text=self.on_year_change)

		nav_bar.add_widget(self.month_spinner)
		nav_bar.add_widget(self.year_spinner)
		self.add_widget(nav_bar)

		self.days_grid = GridLayout(cols=7, size_hint_y=None, spacing=dp(2))
		self.days_grid.bind(minimum_height=self.days_grid.setter('height'))
		self.populate_days()

		self.scroll = ScrollView(do_scroll_x=False, do_scroll_y=True, size_hint=(1, 1))
		self.scroll.add_widget(self.days_grid)
		self.add_widget(self.scroll)

		self.selected_date_label        = Label(text="Selected Date: None", size_hint_y=None, height=dp(20), color=text_color)
		self.selected_date_CustomButton = CustomButton(self.manager, text="SELECT", size_hint_y=None, height=dp(40),
			on_press=self.return_callback)

		self.add_widget(self.selected_date_label)
		self.add_widget(self.selected_date_CustomButton)

	def return_callback(self, *args):
		self.callback(self.date_text)
		self.pop.dismiss()

	def populate_days(self):
		self.days_grid.clear_widgets()
		first_day_of_month = datetime(self.year, self.month, 1)
		last_day_of_month  = datetime(self.year, self.month + 1, 1) - timedelta(days=1)

		for _ in range(first_day_of_month.weekday()):
			self.days_grid.add_widget(Label())

		for day in range(1, last_day_of_month.day + 1):
			btn = CustomButton(self.manager, text=str(day), size_hint_y=None, height=dp(40))
			btn.bind(on_press=self.on_day_select)
			self.days_grid.add_widget(btn)

	def on_month_change(self, spinner, text):
		self.month = self.months.index(text) + 1
		self.selected_day = 1
		self.date_text = f"{self.month}/{self.selected_day}/{self.year}"
		self.selected_date_label.text = f"Selected Date: {self.date_text}"

		self.populate_days()

	def on_year_change(self, spinner, text):
		self.year = int(text)
		self.selected_day = 1
		self.date_text = f"{self.month}/{self.selected_day}/{self.year}"
		self.selected_date_label.text = f"Selected Date: {self.date_text}"

		self.populate_days()

	def on_day_select(self, instance):
		self.selected_day = instance.text
		self.date_text = f"{self.month}/{self.selected_day}/{self.year}"
		self.selected_date_label.text = f"Selected Date: {self.date_text}"

class DatePickerPopup(Popup):
	def __init__(self, manager, callback, **kwargs):
		super().__init__(**kwargs)
		self.title = "DATE PICKER"
		self.title_color = GetColor(manager.theme.main_color)
		self.title_align = 'center'
		self.background = ''
		self.size_hint = (0.8, 0.5)
		self.date_picker = DatePicker(manager, callback, self)
		self.content = self.date_picker
