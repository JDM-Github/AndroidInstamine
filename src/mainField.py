from jdm_kivy import *
from kivy.uix.label import Label

class MainScreen(JDMScreen): ...
class MainField(JDMWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas:
            Color(rgb=GetColor("#888888"))
            Rectangle(size=self.root.size)

        self.add_widget(Label(
            size=self.root.size, text='JDM-Android Template',
            bold=True, italic=True, font_size=dp(24)))

        self.add_widget(JDMCardBox(
            shadow_pos='b',
            size=(Window.width/2, Window.width/2), 
            pos=(Window.width/4, Window.height/1.8), shadow_width=10)
        )
