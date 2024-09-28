# import cv2
# import yt_dlp
# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.label import Label
# from kivy.uix.textinput import TextInput
# from kivy.uix.button import Button
# from kivy.uix.image import Image
# from kivy.clock import Clock
# from kivy.graphics.texture import Texture

# class LiveStreamApp(App):
#     def build(self):
#         self.main_layout = BoxLayout(orientation='vertical')

#         # Text input for YouTube URL
#         self.url_input = TextInput(hint_text='Enter YouTube URL', size_hint=(1, 0.1))
#         self.main_layout.add_widget(self.url_input)

#         # Submit button
#         submit_button = Button(text='Submit', size_hint=(1, 0.1))
#         submit_button.bind(on_press=self.start_stream)
#         self.main_layout.add_widget(submit_button)

#         # Label for messages
#         self.message_label = Label(size_hint=(1, 0.1))
#         self.main_layout.add_widget(self.message_label)

#         # Image widget to display video
#         self.video_display = Image(size_hint=(1, 0.7))
#         self.main_layout.add_widget(self.video_display)

#         # Variable to hold video capture object
#         self.capture = None

#         return self.main_layout

#     def get_stream_url(self, yt_url):
#         ydl_opts = {'format': 'best'}
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             try:
#                 info_dict = ydl.extract_info(yt_url, download=False)
#                 formats = info_dict.get('formats', None)
#                 for f in formats:
#                     if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
#                         return f['url']
#             except Exception as e:
#                 self.message_label.text = f"Error: {str(e)}"
#                 return None

#     def start_stream(self, instance):
#         yt_url = self.url_input.text.strip()
#         if not yt_url:
#             self.message_label.text = "Please enter a valid YouTube URL."
#             return

#         stream_url = self.get_stream_url(yt_url)
#         if stream_url:
#             self.message_label.text = "Streaming..."
#             self.capture = cv2.VideoCapture(stream_url)
#             if not self.capture.isOpened():
#                 self.message_label.text = "Failed to open video stream."
#                 return
#             Clock.schedule_interval(self.update_frame, 1.0 / 30.0)  # 30 FPS
#         else:
#             self.message_label.text = "Failed to retrieve stream URL."

#     def update_frame(self, dt):
#         if self.capture is not None and self.capture.isOpened():
#             ret, frame = self.capture.read()
#             if ret:
#                 # Convert the frame to Kivy texture
#                 buf = cv2.flip(frame, 0).tobytes()
#                 texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
#                 texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
#                 self.video_display.texture = texture
#             else:
#                 self.message_label.text = "Failed to retrieve frame."
#         else:
#             self.message_label.text = "Capture is not opened."

#     def on_stop(self):
#         if self.capture is not None:
#             self.capture.release()

# if __name__ == "__main__":
#     LiveStreamApp().run()
