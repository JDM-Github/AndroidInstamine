import time
from kivy.uix.screenmanager import Screen
from handle_requests import RequestHandler
from widgets import ThemedPopup

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex as GetColor
from kivy.graphics import Color, Rectangle, RoundedRectangle
from widgets import RoundedTextInput, CustomButton, Utility, ThemedPopup, CustomImageButton

from kivy.properties import ObjectProperty

class VerifyScreen(Screen):

    def display_design(self):
        self.data = {}
        self.last_code_sent_time = None
        self.retry_delay = 30
        self.max_delay = 99999

        self.failed_attempts = 0
        self.locked = False

        self.display_widget()

    def display_widget(self):
        self.clear_widgets()
    
        widget    = Widget(size=self.manager.size, pos=(0, 0))
        spacepadd = Utility.get_value_percentage(self.height, 0.015)
        layout    = BoxLayout(size=self.manager.size, orientation='vertical', padding=spacepadd, spacing=spacepadd)

        main_color     = self.manager.theme.main_color
        main_color_88  = self.manager.theme.main_color_88

        common_kwargs = {
            'line_color': main_color,
            'fg_color': main_color,
            'hint_color': main_color_88,
        }

        self.email = RoundedTextInput(icon_source='assets/email.png', hint_text="Email to verify", **common_kwargs)
        layout.add_widget(self.email)
        layout.add_widget(Widget(size_hint_y=None, height=self.manager.height*0.01))
        self.code_answer = RoundedTextInput(icon_source='assets/pass.png', hint_text="Verify your account", **common_kwargs)
        layout.add_widget(self.code_answer)

        layout.add_widget(Widget(size_hint_y=None, height=self.manager.height*0.02))
        resend_code = CustomButton(self.manager, text="Send/Resend Code", on_press=self.send_code)
        layout.add_widget(resend_code)

        layout.add_widget(Widget(size_hint_y=None, height=self.manager.height*0.01))
        register_btn = CustomButton(self.manager, text="Verifiy Account", on_press=self.verify_email)
        layout.add_widget(register_btn)

        layout.add_widget(Widget(size_hint_y=None, height=self.manager.height*0.18))
        back = CustomImageButton(
            self.manager, src='assets/back.png', size_hint=(None, None), size=(dp(60), dp(60)), pos_hint={'center_x': 0.5},
            on_press=self.go_to_register)

        layout.add_widget(back)
        layout.add_widget(Widget(size_hint_y=None, height=self.manager.height*0.02))

        widget.add_widget(layout)
        self.add_widget(widget)
    
    def go_to_register(self):
        self.manager.current = 'register'

    def set_data(self, data):
        self.data = data
        self.email.input.text = self.data.get('email')
        self.email.input.readonly = True

    def check_email_valid(self):
        success_color = GetColor(self.manager.theme.main_color)
        error_color = GetColor(self.manager.theme.main_error_color)

        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not Utility.validate_email(self.email, email_pattern, error_color, success_color, self._on_error):
            return False

        self.data['email'] = self.email.input.text
        return True

    def send_code(self):
        if not self.check_email_valid():
            return
    
        if self.last_code_sent_time and time.time() - self.last_code_sent_time < self.retry_delay:
            time_left = int(self.retry_delay - (time.time() - self.last_code_sent_time))
            self.on_error_send({'message': f"Please wait {time_left} seconds before requesting another code."})
            return

        self.last_code_sent_time = time.time()
        self.retry_delay = min(self.retry_delay * 2, self.max_delay)

        self.data['verificationCode'] = Utility.generate_verification_code()
        RequestHandler.request_loader(self, self.manager,
            lambda: RequestHandler.create_req_suc_error("post", "send-email", self.data, self.on_success_send, self.on_error_send))

    def verify_email(self):
        if not self.check_email_valid():
            return

        answer = self.code_answer.input.text
        if answer != self.data.get('verificationCode'):
            self.on_error({'message': "The verification code is incorrect. Please try again."})
            return

        RequestHandler.request_loader(self, self.manager,
            lambda: RequestHandler.create_req_suc_error("post", "user/verify", self.data, self.on_success, self.on_error))

    def on_success_send(self, result):
        popup = ThemedPopup(
            self.manager,
            title='Account Verification Send Successfully',
            message=result.get('message'))
        popup.open()

    def on_error_send(self, error):
        RequestHandler.show_error_popup(self.manager, "Account Verification Send Failed", "Error Account Verification Code: " + error.get('message'))

    def on_success(self, result):
        popup = ThemedPopup(
            self.manager,
            title='Account Verification Success',
            message=result.get('message'))
        popup.open()
        self.manager.current = 'login'

    def on_error(self, error):
        RequestHandler.show_error_popup(self.manager, "Verification Failed", "Error Verification: " + error.get('message'))

    def _on_error(self, error):
        RequestHandler.show_error_popup(self.manager, "Invalid Email", error.get('message'))
