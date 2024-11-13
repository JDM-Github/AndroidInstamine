from kivy.app import App
from kivy.uix.popup import Popup
# class AddProduct(Popup): pass

from kivy.properties import ListProperty, StringProperty, ColorProperty
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDButton
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label

from handle_requests import RequestHandler
from widgets.themed_popup import ThemedPopup

class MyChat(Label):
    main_color = ColorProperty([0.8, 0.3, 0.8, 1])

class PartnerChat(MyChat): pass

class ChatPopup(Popup):
    chat_id = StringProperty()
    chat_partner = StringProperty()
    all_chats = ListProperty()

    def __init__(self, manager, chat_id, chat_partner, all_chats, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager
        self.chat_id = chat_id
        self.chat_partner = chat_partner
        self.all_chats = all_chats

        self.load_all_chats()
        self.bind(all_chats=self.load_all_chats)
    
    def load_all_chats(self, *_):
        widget = self.ids.chats
        widget.clear_widgets()

        ids = self.manager.main_state['user']['id']
        for chat in self.all_chats:
            if ids == chat.get('sender'):
                widget.add_widget(MyChat(text=chat.get('message')))
            else:
                widget.add_widget(PartnerChat(text=chat.get('message')))
    
    def send_message(self):
        widget = self.ids.text_message

        text = widget.text.strip()
        if text == "":
            return

        widget.text = ""
        self.all_chats.append({
            'sender': self.manager.main_state['user']['id'],
            'message': text
        })

        screen_running = self.manager.get_screen(self.manager.current)
        RequestHandler.request_loader(screen_running, self.manager,
            lambda: RequestHandler.create_req_suc_error("post", "chats/message",
            {
                'userId': self.manager.main_state['user']['id'],
                'partnerId': self.chat_id,
                'message': text
            }, self.on_success, self.on_error))

    def on_error(self, error):
        RequestHandler.show_error_popup(self.manager, "Sending chat error", error.get('message'))

    def on_success(self, result):
        pass

    def set_scroll(self):
        scroll_view = self.ids.y_scroll
        if len(scroll_view.children) < 6:
            return
        scroll_view.scroll_to(scroll_view.children[-1])

    def on_open(self):
        self.set_scroll()

class NotificationPopup(Popup):
    pass

class AddProduct(Popup):
    main_image_path = StringProperty("")
    additional_images = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )
        self.bind(additional_images=self.update_images)

    def choose_main_image(self):
        self.main_image_path = ""
        self.file_manager_open()

    def choose_images(self):
        if not len(self.additional_images) >= 5:
            self.file_manager_open()

    def file_manager_open(self):
        self.file_manager.show('/')

    def exit_manager(self, *args):
        self.file_manager.close()

    def select_path(self, path):
        if not self.main_image_path:
            self.main_image_path = path
        elif len(self.additional_images) < 5:
            self.additional_images.append(path)
        self.file_manager.close()


    def update_images(self, *args):
        images_box = self.ids.images_box
        images_box.clear_widgets()
    
        for image_path in self.additional_images:
            img_layout = FloatLayout(size_hint=(None, None), height="100dp", width="100dp")
            img = Image(source=image_path, size_hint=(None, None), pos_hint={'top': 1, 'right': 1}, size=("100dp", "100dp"), fit_mode="fill")
            img_layout.add_widget(img)

            delete_btn = Button(text="X", size_hint=(None, None), size=("20dp", "20dp"), pos_hint={'top': 1, 'right': 1}, 
                                on_release=lambda btn, img_path=image_path: self.remove_image(img_path))
            img_layout.add_widget(delete_btn)
    
            images_box.add_widget(img_layout)
    
    def remove_image(self, image_path):
        if image_path in self.additional_images:
            self.additional_images.remove(image_path)

    def submit_product(self):
        if not self.main_image_path:
            self.show_error_dialog("Please choose a main image.")
        elif len(self.additional_images) > 5:
            self.show_error_dialog("You cannot add more than 5 additional images.")
        else:
            print("Product created with main image:", self.main_image_path)
            print("Additional images:", self.additional_images)
            self.dismiss()

    def show_error_dialog(self, message):
        dialog = MDDialog(
            text=message,
            buttons=[MDButton(text="OK", on_release=lambda x: dialog.dismiss())],
        )
        dialog.open()

class EditProfile(Popup):

    firstName = StringProperty("")
    lastName = StringProperty("")
    username = StringProperty("")
    phoneNumber = StringProperty("")
    location = StringProperty("")
    bday = StringProperty("")

    main_image_path = StringProperty("")
    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )
    
    def choose_main_image(self):
        self.main_image_path = ""
        self.file_manager_open()
    
    def file_manager_open(self):
        self.file_manager.show('/')

    def exit_manager(self, *args):
        self.file_manager.close()

    def select_path(self, path):
        if not self.main_image_path:
            self.main_image_path = path
        elif len(self.additional_images) < 5:
            self.additional_images.append(path)
        self.file_manager.close()
    
    def save_profile(self):
        RequestHandler.request_loader(self.parent, self.manager,
            lambda: RequestHandler.create_req_suc_error("post", "user/saveProfile",
        {
            'firstName': self.firstName,
            'lastName': self.lastName,
            'username': self.username,
            'phoneNumber': self.phoneNumber,
            'location': self.location,
            'bday': self.bday,
        },
        self.on_success, self.on_error))
    
    def on_error(self, error):
        self.dismiss()
        RequestHandler.show_error_popup(self.manager, "Save Profile Failed", error.get('message'))

    def on_success(self, result):
        self.dismiss()
        popup = ThemedPopup(
            self.manager,
            title='Profile Changed Successfully',
            message=result.get('message'))
        popup.open()

class BuyOrder(Popup):
    pass

class StartStream(Popup):
    link_text = StringProperty("")
    def start_stream(self):
        self.dismiss()
        app = App.get_running_app()
        app.sm.live.start_live(self.link_text)



class Payment(Popup):
    main_image_path = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )

    def choose_main_image(self):
        self.main_image_path = ""
        self.file_manager_open()

    def file_manager_open(self):
        self.file_manager.show('/')

    def exit_manager(self, *args):
        self.file_manager.close()

    def select_path(self, path):
        if not self.main_image_path:
            self.main_image_path = path
        self.file_manager.close()

    def submit_order(self):
        if not self.main_image_path:
            self.show_error_dialog("Please choose a main image.")
        # elif len(self.additional_images) > 5:
        #     self.show_error_dialog("You cannot add more than 5 additional images.")
        # else:
        #     print("Product created with main image:", self.main_image_path)
        #     print("Additional images:", self.additional_images)
        #     self.dismiss()

    def show_error_dialog(self, message):
        dialog = MDDialog(
            text=message,
            buttons=[MDButton(text="OK", on_release=lambda x: dialog.dismiss())],
        )
        dialog.open()
