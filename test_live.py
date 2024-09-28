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


if __name__ == '__main__':
    YouTubeApp().run()


# https://www.youtube.com/live/9XLVZ_4OcTc