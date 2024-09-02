from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

# Sample verification code for demonstration
VERIFICATION_CODE = "123456"

class VerificationScreen(Screen):
    def __init__(self, **kwargs):
        super(VerificationScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.label = Label(text="Enter Verification Code")
        layout.add_widget(self.label)

        self.code_input = TextInput(multiline=False, password=True, halign='center', font_size=32)
        layout.add_widget(self.code_input)

        self.verify_button = Button(text="Verify Code", on_press=self.verify_code)
        layout.add_widget(self.verify_button)

        self.add_widget(layout)

    def verify_code(self, instance):
        if self.code_input.text == VERIFICATION_CODE:
            self.manager.current = 'success'
        else:
            self.show_error_popup()

    def show_error_popup(self):
        popup = Popup(title='Error',
                      content=Label(text='Incorrect verification code!'),
                      size_hint=(0.8, 0.4))
        popup.open()

class SuccessScreen(Screen):
    def __init__(self, **kwargs):
        super(SuccessScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.label = Label(text="Verification Successful!", font_size=32)
        layout.add_widget(self.label)
        
        self.add_widget(layout)

class VerificationApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(VerificationScreen(name='verification'))
        sm.add_widget(SuccessScreen(name='success'))
        return sm

if __name__ == "__main__":
    VerificationApp().run()
