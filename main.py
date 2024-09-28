# import re
# import json


# # setup the graphics

# from kivy.config import Config
# WIDTH  = int(750  * 0.5) 
# HEIGHT = int(1400 * 0.5) 
# Config.set('graphics', 'width', WIDTH)
# Config.set('graphics', 'height', HEIGHT)
# Config.set('graphics', 'resizable', 0)
# Config.write()

# from kivy.utils import platform
# from kivy.core.window import Window


# if platform == "win":
# 	Window.size  = (WIDTH, HEIGHT)
# 	Window.top   = 30
# 	Window.left  = 1

# from kivy.app import App
# from kivy.uix.screenmanager import ScreenManager
# from screens import LoginScreen, RegisterScreen, HomeScreen
# from theme import OriginalColor



# class Manager(ScreenManager):

# 	def __init__(self, **kwargs):
# 		super().__init__(**kwargs)
# 		self.size = Window.size

# 		self.theme = OriginalColor()
# 		self.main_config = self.load_json_config("config.json")
# 		self.main_state = self.load_json_config("state.json")



# 	def load_json_config(self, filepath):
# 		with open(filepath, 'r') as file:
# 			content = file.read()

# 		content = re.sub(r'//.*', '', content)
# 		content = re.sub(r'/\*[\s\S]*?\*/', '', content)
# 		return json.loads(content)



# 	def save_json_config(self, filepath, data):
# 		with open(filepath, 'w') as file:
# 			json.dump(data, file, indent=4)


# class MyApp(App):

# 	def build(self):

# 		sm       = Manager()

# 		home     = HomeScreen(name="home")
# 		login    = LoginScreen(name='login')
# 		register = RegisterScreen(name='register')
# 		# verify   = VerificationScreen(name='verify')


# 		sm.add_widget(login)
# 		sm.add_widget(register)
# 		# sm.add_widget(verify)
# 		sm.add_widget(home)


# 		login   .display_design()
# 		register.display_design()
# 		# verify  .display_design()
# 		home    .display_design()

# 		if not sm.main_state['already_login']:
# 			sm.current = "login"
# 		else:
# 			sm.current = "home"

# 		return sm

# if __name__ == '__main__':
# 	MyApp().run()
# try:
# 	import cv2
# except:
# 	from cv import cv2

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.video import Video
import yt_dlp

class YouTubeLiveStream(BoxLayout):
    def __init__(self, **kwargs):
        super(YouTubeLiveStream, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Input field for YouTube URL
        self.url_input = TextInput(hint_text='Enter YouTube Live URL', size_hint=(1, 0.1))
        self.add_widget(self.url_input)

        # Button to load stream
        self.stream_button = Button(text='Stream Video', size_hint=(1, 0.1))
        self.stream_button.bind(on_press=self.get_live_stream_url)
        self.add_widget(self.stream_button)

        # Video player
        self.video = Video(size_hint=(1, 0.8))
        self.add_widget(self.video)

    def get_live_stream_url(self, instance):
        url = self.url_input.text
        if url:
            try:
                # Using yt-dlp to get the stream URL
                ydl_opts = {'quiet': True, 'no_warnings': True, 'format': 'best'}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    stream_url = info['url']
                    
                if stream_url:
                    self.video.source = stream_url
                    self.video.state = 'play'
                    self.video.options = {'eos': 'loop'}
                else:
                    print("Failed to retrieve the live stream URL")
            except Exception as e:
                print(f"Error fetching live stream: {e}")

class YouTubeApp(App):
    def build(self):
        return YouTubeLiveStream()

if __name__ == '__main__':
    YouTubeApp().run()