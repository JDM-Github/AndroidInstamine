import io
import yt_dlp
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
import socketio

sio = socketio.Client()

def get_stream_url(yt_url):
    ydl_opts = {'format': 'best'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(yt_url, download=False)
            formats = info_dict.get('formats', None)

            for f in formats:
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                    return f['url']
        except Exception as e:
            print(e)
            return None

class StreamingApp(App):
    def build(self):
        self.img_widget = Image()
        return self.img_widget

    def on_start(self):
        sio.connect('http://localhost:3000')
        yt_url = "https://www.youtube.com/live/1Xjn_qRCOtc"
        stream_url = get_stream_url(yt_url)
        sio.emit('start_stream', stream_url)

        @sio.on('frame')
        def on_frame(data):
            Clock.schedule_once(lambda dt: self.update_image(data))

    def update_image(self, frame_data):
        buf = io.BytesIO(frame_data)
        buf.seek(0)
        core_image = CoreImage(buf, ext='jpeg')
        self.img_widget.texture = core_image.texture

if __name__ == '__main__':
    StreamingApp().run()
