import threading
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image, AsyncImage
from kivy.uix.scrollview import ScrollView
from kivy.effects.scroll import ScrollEffect
from kivy.uix.textinput import TextInput

from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex as GetColor
from kivy.graphics import Rectangle, RoundedRectangle, Color, Line

from kivy.properties import ObjectProperty, StringProperty, NumericProperty

import io
from kivy.core.image import Image as CoreImage
from popup.popups import BuyOrder, ChatPopup
from widgets import CircleImage, RoundedTextInput, CustomButton, LoadingPopup, BackButton, Utility, ThemedPopup, CustomImageButton
from handle_requests import RequestHandler
from widgets.custom_button import CustomButtonWidget, LeftLabel
from widgets.product import ProductItem


class PlaceOrderLiveBottom(BoxLayout):
    pass

class LiveScreenBody(BoxLayout):
    screen = ObjectProperty(Image())

class CommentSection(BoxLayout):

    def __init__(self, manager, send_message, **kwargs):
        super().__init__(
            orientation="vertical", size_hint=(0.85, None), height=Window.height*0.5, pos_hint={"center_x": 0.5},
            **kwargs)
        self.send_message = send_message
        self.manager = manager
        self.create_comment_section()

    def create_comment_section(self, *_):
        self.add_widget(Widget(size_hint=(1, 0.05)))

        self.label_instance = Label(text="768345 watching...", color=self.manager.theme.font_color_88, size_hint=(1, 0.05), halign="left")
        self.add_widget(self.label_instance)
        self.bind(size=lambda *args: self.label_instance.setter('text_size')(self.label_instance, (self.width, None)))
        self.add_widget(Widget(size_hint=(1, 0.05)))

        self.scrollview = ScrollView(size_hint=(1, 0.8), effect_cls=ScrollEffect)
        self.comments_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
        self.comments_layout.bind(minimum_height=self.comments_layout.setter('height'))
        self.scrollview.add_widget(self.comments_layout)
        self.add_widget(self.scrollview)
        self.add_widget(Widget(size_hint=(1, 0.05)))

        self.comment_input = RoundedTextInput(hint_text="Say Something...", size_hint=(0.8, 1))
        self.submit_button = CustomImageButton(self.manager, src='assets/send.png', size_hint=(0.1, 1),
            on_press=lambda : self.send_message(self.comment_input.input))

        # self.add_comment("OTHER", "This is a test", False)
        # self.add_comment("OTHER", "This is a test", False)
        # self.add_comment("OTHER", "This is a test", False)

        self.share_button = CustomImageButton(self.manager, src='assets/share.png', size_hint=(0.1, 1))

        input_layout = BoxLayout(size_hint=(1, 0.1), pos_hint={"center_x": 0.5}, spacing=10)
        input_layout.add_widget(self.comment_input)
        input_layout.add_widget(self.submit_button)
        input_layout.add_widget(self.share_button)

        self.add_widget(input_layout)
    
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

class LiveScreen(Screen):

    def start_live(self, live_url):
        try:
            stream_url = self.manager.get_stream_url(live_url)
            self.manager.sio.emit('start_stream', {"yt_url": stream_url, "streamId": self.manager.main_state['user']['id']})
            # self.save_stream(stream_url)


            self.manager.sio.emit("join_stream", {"streamId": self.manager.main_state['user']['id']})
            @self.manager.sio.on('frame')
            def on_frame(data):
                Clock.schedule_once(lambda dt: self.update_screen(data))

            @self.manager.sio.on("receive_comment")
            def on_receive_comment(data):
                username = data["username"]
                comment = data["comment"]
                is_me = data['id'] == self.manager.main_state['user']['id']
                Clock.schedule_once(lambda dt: self.comment_section.add_comment(username, comment, is_me))

            self.manager.main_state['user']['isStreaming'] = True
            self.manager.main_state['user']['streamUrl'] = stream_url
            self.manager.current = "live"
        except:
            self.manager.main_state['user']['isStreaming'] = False
            self.manager.main_state['user']['streamUrl'] = ""
            RequestHandler.show_error_popup(self.manager, "Starting stream error", "Invalid URL stream")
            self.manager.current = "home"
    
    def end_stream(self):
        self.manager.sio.emit('end_stream', {"streamId": self.manager.main_state['user']['id']})

    def send_comment(self, comment_text):
        comment_data = {
            "id": self.manager.main_state['user']['id'],
            "username": self.manager.main_state['user']['firstName'] + " " + self.manager.main_state['user']['lastName'],
            "comment": comment_text.text
        }
        self.manager.sio.emit("new_comment", {"streamId": self.manager.main_state['user']['id'], "commentData": comment_data})
    
    def save_stream(self, live_url):
        screen_running = self.manager.get_screen(self.manager.current)
        RequestHandler.request_loader(screen_running, self.manager,
            lambda: RequestHandler.create_req_suc_error("post", "user/startStreaming",
            {
                'userId': self.manager.main_state['user']['id'],
                'url': live_url,
            }, None, self.on_error))

    def on_error(self, error):
        self.manager.main_state['user']['isStreaming'] = False
        self.manager.main_state['user']['streamUrl'] = ""
        RequestHandler.show_error_popup(self.manager, "Starting stream error", error.get('message'))
        self.manager.current = "home"

    def set_live(self, live_target):
        self.manager.sio.emit("join_stream", {"streamId": live_target})
        @self.manager.sio.on('frame')
        def on_frame(data):
            Clock.schedule_once(lambda dt: self.update_screen(data))

    def update_screen(self, frame_data):
        try:
            buf = io.BytesIO(frame_data)
            buf.seek(0)
            core_image = CoreImage(buf, ext='jpeg')
            self.layout.ids.screen.texture = core_image.texture
        except:
            pass

    def display_design(self):
        self.size = self.manager.size
        with self.canvas.before:
            self.bg_color = Color(rgba=GetColor(self.manager.theme.main_color_88))
            Rectangle(size=self.size)

            height = Utility.get_value_percentage(self.height, 0.08)
            self.top_color = Color(rgba=GetColor(self.manager.theme.main_color))
            # RoundedRectangle   (
            #     size=(self.width, height),
            #     radius=[dp(30), dp(30), 0, 0]
            # )
            Rectangle(
                size=(self.width, height),
                pos=(0, self.height-height),
            )
        self.display_widget()

    def display_widget(self):
        self.clear_widgets()
        widget = Widget(size=self.manager.size, pos=(0, 0))

        layout_scroll = ScrollView(
            size=(self.manager.width, self.manager.height*0.92), do_scroll_y=True, do_scroll_x=False, effect_cls=ScrollEffect)
        self.layout = LiveScreenBody(
            orientation='vertical', size_hint=(1, None), spacing=Utility.get_value_percentage(self.height, 0.01),
            size=layout_scroll.size)
        
        self.comment_section = CommentSection(self.manager, self.send_comment)
        self.layout.add_widget(self.comment_section)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.top_bar_layout = BoxLayout(
            orientation='horizontal', size_hint=(1, None),
            x=self.manager.width*0.025,
            y=Window.height - Utility.get_value_percentage(self.height, 0.05) - Utility.get_value_percentage(self.height, 0.015),
            width=self.manager.width*0.95,
            height=Utility.get_value_percentage(self.height, 0.05), spacing=dp(10))

        self.back_button = CustomImageButton(self.manager, src='assets/back.png', size_hint=(0.1, 1),
            on_press=lambda *_: self.return_home())
        checkout_label = LeftLabel(text="Live Screen", size_hint=(0.9, 1))

        self.top_bar_layout.add_widget(self.back_button)
        self.top_bar_layout.add_widget(checkout_label)

        layout_scroll.add_widget(self.layout)
        widget.add_widget(layout_scroll)
        widget.add_widget(PlaceOrderLiveBottom())

        widget.add_widget(self.top_bar_layout)
        self.add_widget(widget)
    
    def return_home(self):
        self.manager.current = "home"
        self.manager.home.update_button_active("home")
    

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
