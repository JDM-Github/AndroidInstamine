# from kivy.config import Config
# WIDTH  = int(720 * 0.5)
# HEIGHT = int(1400 * 0.5)
# Config.set('graphics', 'width', WIDTH)
# Config.set('graphics', 'height', HEIGHT)
# Config.set('graphics', 'resizable', False)
# Config.write()

from kivy.app import App
from kivy.uix.label import Label

from sqlalchemy import inspect, create_engine, Column, MetaData, Table
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker

class MainApp(App):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def build(self):
		return Label(text="Hello World")

if __name__ == "__main__":
	MainApp().run()
