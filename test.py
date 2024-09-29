from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.utils import get_color_from_hex as GetColor
from datetime import datetime, timedelta
import calendar

class CustomButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        white_color  = GetColor("#FFFFFF")
        pinkish_color = GetColor("9C3E93")
        text_color  = GetColor("#333333")

        self.background_normal = ''
        self.background_color = pinkish_color
        self.color = white_color

class DatePicker(BoxLayout):
    def __init__(self, **kwargs):
        super(DatePicker, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(5)

        

        self.year = datetime.now().year
        self.month = datetime.now().month

        # Month and Year selection
        self.months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        # Create navigation bar
        nav_bar = BoxLayout(size_hint_y=None, height=dp(20))
        self.month_spinner = Spinner(text=self.months[self.month - 1], values=self.months)
        self.month_spinner.bind(text=self.on_month_change)
        self.year_spinner = Spinner(text=str(self.year), values=[str(i) for i in range(1970, 2100)])
        self.year_spinner.bind(text=self.on_year_change)

        nav_bar.add_widget(self.month_spinner)
        nav_bar.add_widget(self.year_spinner)

        self.add_widget(nav_bar)

        # Create the grid for days
        self.days_grid = GridLayout(cols=7, size_hint_y=None)
        self.days_grid.bind(minimum_height=self.days_grid.setter('height'))

        self.populate_days()

        self.scroll = ScrollView(do_scroll_x=False, do_scroll_y=True, size_hint=(1, 1))
        self.scroll.add_widget(self.days_grid)
        self.add_widget(self.scroll)
        

        # Label to show the selected datex
        self.selected_date_label = Label(text="Selected Date: None", size_hint_y=None, height=dp(20))
        self.add_widget(self.selected_date_label)

        self.selected_date_CustomButton = CustomButton(text="SELECT", size_hint_y=None, height=dp(40))
        self.add_widget(self.selected_date_CustomButton)

    def populate_days(self):
        # Clear previous days
        self.days_grid.clear_widgets()

        # Get the first and last day of the month
        first_day_of_month = datetime(self.year, self.month, 1)
        last_day_of_month = datetime(self.year, self.month + 1, 1) - timedelta(days=1)

        # Add empty labels for days before the first day of the month
        for _ in range(first_day_of_month.weekday()):
            self.days_grid.add_widget(Label())

        # Add days of the month
        for day in range(1, last_day_of_month.day + 1):
            btn = CustomButton(text=str(day), size_hint_y=None, height=dp(40))
            btn.bind(on_release=self.on_day_select)
            self.days_grid.add_widget(btn)

    def on_month_change(self, spinner, text):
        self.month = self.months.index(text) + 1
        self.populate_days()

    def on_year_change(self, spinner, text):
        self.year = int(text)
        self.populate_days()

    def on_day_select(self, instance):
        selected_day = instance.text
        self.selected_date_label.text = f"Selected Date: {selected_day}/{self.month}/{self.year}"

class DatePickerPopup(Popup):
    def __init__(self, **kwargs):
        super(DatePickerPopup, self).__init__(**kwargs)
        self.title = "DATE PICKER"
        self.title_color = GetColor("9C3E93")
        self.title_align = 'center'
        self.background = ''
        self.size_hint = (0.8, 0.4)
        self.date_picker = DatePicker()
        self.content = self.date_picker

class MainApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical')

        open_popup_CustomButton = CustomButton(text="Open Date Picker", size_hint_y=None, height=40)
        open_popup_CustomButton.bind(on_release=self.show_date_picker)

        self.selected_date_label = Label(text="Selected Date: None", size_hint_y=None, height=40)
        
        main_layout.add_widget(open_popup_CustomButton)
        main_layout.add_widget(self.selected_date_label)

        return main_layout

    def show_date_picker(self, instance):
        popup = DatePickerPopup()
        popup.bind(on_dismiss=self.update_selected_date)
        popup.open()

    def update_selected_date(self, instance):
        selected_date = instance.date_picker.selected_date_label.text
        self.selected_date_label.text = selected_date

if __name__ == '__main__':
    MainApp().run()
