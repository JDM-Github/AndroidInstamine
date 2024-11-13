from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

from kivy.metrics import dp, sp

from handle_requests import RequestHandler
from popup.popups import StartStream
from .base_section import BaseSection

from kivy.clock import Clock
from kivy.effects.scroll import ScrollEffect
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex as GetColor
from widgets import RoundedTextInput, CustomButton, CustomImageButton

import io
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage

class LiveSection(BaseSection):
    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager
        self.display_screen()

    def display_screen(self):
        self.main_layout     = BoxLayout(orientation="vertical", size_hint=(1.1, 1), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.screen          = Image(size_hint=(1, 0.4), pos_hint={"center_x": 0.5})
        self.screen.fit_mode = "fill"

        self.create_comment_section()
        self.main_layout.add_widget(self.screen)
        self.main_layout.add_widget(self.comment_section_layout)
        self.main_layout.add_widget(Widget(size_hint=(1, 0.03)))
        self.add_widget(self.main_layout)
        self.set_instamine()
        self.on_start()

    def on_start(self):
        # yt_url = "https://www.youtube.com/live/1Xjn_qRCOtc"
        # stream_url = self.manager.get_stream_url(yt_url)
        # self.manager.sio.emit('start_stream', stream_url)
        try:
            self.manager.sio.emit("join_stream", {"streamId": "1"})

            @self.manager.sio.on('frame')
            def on_frame(data):
                Clock.schedule_once(lambda dt: self.update_screen(data))

            @self.manager.sio.on("receive_comment")
            def on_receive_comment(data):
                username = data["username"]
                comment = data["comment"]
                is_me = data['id'] == self.manager.main_state['user']['id']
                Clock.schedule_once(lambda dt: self.add_comment(username, comment, is_me))
        except:
            RequestHandler.show_error_popup(self.manager, "Stream Error", "Cannot connect to server.")

    def send_comment(self, comment_text):
        try:
            comment_data = {
                "id": self.manager.main_state['user']['id'],
                "username": self.manager.main_state['user']['firstName'] + " " + self.manager.main_state['user']['lastName'],
                "comment": comment_text.text
            }
            self.manager.sio.emit("new_comment", {"streamId": "1", "commentData": comment_data})
        except:
            RequestHandler.show_error_popup(self.manager, "Stream Error", "Cannot connect to server.")

    def update_screen(self, frame_data):
        try:
            buf = io.BytesIO(frame_data)
            buf.seek(0)
            core_image = CoreImage(buf, ext='jpeg')
            self.screen.texture = core_image.texture
        except:
            pass

    def set_instamine(self):
        self.instamine_button = CustomButton(self.manager, text="INSTAMINE", size_hint=(None, None), radius=[dp(10)])
        self.instamine_button.pos_hint = {"center_x": 0.85}
        self.instamine_button.size = (dp(100), dp(40))
        self.instamine_button.pos = (0, self.manager.height*0.6)
        self.add_widget(self.instamine_button)

    def create_comment_section(self):
        self.comment_section_layout = BoxLayout(orientation="vertical", size_hint=(0.85, 0.5), pos_hint={"center_x": 0.5})
        self.comment_section_layout.add_widget(Widget(size_hint=(1, 0.05)))

        self.label_instance = Label(text="768345 watching...", color=self.manager.theme.font_color_88, size_hint=(1, 0.05), halign="left")
        self.comment_section_layout.add_widget(self.label_instance)
        self.bind(size=lambda *args: self.label_instance.setter('text_size')(self.label_instance, (self.width, None)))
        self.comment_section_layout.add_widget(Widget(size_hint=(1, 0.05)))

        self.scrollview = ScrollView(size_hint=(1, 0.8), effect_cls=ScrollEffect)
        self.comments_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
        self.comments_layout.bind(minimum_height=self.comments_layout.setter('height'))
        self.scrollview.add_widget(self.comments_layout)
        self.comment_section_layout.add_widget(self.scrollview)
        self.comment_section_layout.add_widget(Widget(size_hint=(1, 0.05)))

        self.comment_input = RoundedTextInput(hint_text="Say Something...", size_hint=(0.8, 1))
        self.submit_button = CustomImageButton(self.manager, src='assets/send.png', size_hint=(0.1, 1),
            on_press=lambda : self.send_comment(self.comment_input.input))

        self.share_button = CustomImageButton(self.manager, src='assets/share.png', size_hint=(0.1, 1))

        input_layout = BoxLayout(size_hint=(1, 0.12), pos_hint={"center_x": 0.5}, spacing=10)
        input_layout.add_widget(self.comment_input)
        input_layout.add_widget(self.submit_button)
        input_layout.add_widget(self.share_button)

        self.comment_section_layout.add_widget(input_layout)
    
    def start_stream(self, *_):
        popup = StartStream()
        popup.open()

    def add_comment(self, says_by, message, is_me):
        comment_text = message if message else self.comment_input.input.text
        if comment_text.strip():
            new_comment = Comment(self.manager, says_by, is_me,
                text=comment_text, size_hint_y=None, height=dp(40))
            self.comments_layout.add_widget(new_comment)
            if is_me:
                self.comment_input.input.text = ''

            if len(self.comments_layout.children) > 6:
                self.scrollview.scroll_to(new_comment)


class Comment(Label):

    def __init__(self, manager, says_by, is_me, **kwargs):
        super().__init__(**kwargs)
        self.is_me = is_me
        self.text = f"[b][color=#dddddd]{says_by}[/color][/b]: {self.text}"
        self.markup = True

        self.color = manager.theme.comment_text_color
        self.font_size = sp(12)
        self.halign = 'left'
        self.valign = 'top'
        self.bind(pos=self._update, size=self._update)
        self.bind(texture_size=self.update_height)
    
    def update_height(self, *_):
        self.height = self.texture_size[1] + dp(20)
        self._update()
    
    def _update(self, *_):
        self.text_size = (self.width*0.9, None)
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=GetColor("00000088" if self.is_me else "00000055"))
            RoundedRectangle(radius=[dp(20)], size=self.size,
                pos=self.pos)
