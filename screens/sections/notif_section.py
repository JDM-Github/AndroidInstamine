from kivy.app import App
from .base_section import BaseSection
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, StringProperty

from widgets import ThemedPopup


class NotificationWidget(BoxLayout):
	unread = BooleanProperty(True)
	title = StringProperty("Notification")
	message = StringProperty("Notification test message")
	date = StringProperty("2022-05-10")

	def open_notification(self):
		popup = ThemedPopup(App.get_running_app().sm, self.title, self.message)
		popup.open()
	
class NotificationSection(BaseSection):
	pass
