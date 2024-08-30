# from kivy.config import Config
# WIDTH  = int(720*0.5) # Must be INT
# HEIGHT = int(1400*0.5) # Must be INT
# Config.set('graphics', 'width', WIDTH)
# Config.set('graphics', 'height', HEIGHT)
# Config.set('graphics', 'resizable', '0')
# Config.write()

# from src import MainField, MainScreen, JDMApp

# if __name__ == "__main__":
#     JDMApp("JDM-Android Template", (WIDTH, HEIGHT)).run(screen_name="main", screen=MainScreen(), widget=MainField())

from kivy.app import App
from kivy.uix.label import Label

class MyApp(App):

    def build(self):
        return Label(text='Hello world')


if __name__ == '__main__':
    MyApp().run()