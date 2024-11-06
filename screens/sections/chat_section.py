from kivy.app import App

from handle_requests import RequestHandler
from popup.popups import ChatPopup
from .base_section import BaseSection
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ObjectProperty, StringProperty

class CommentItem(ButtonBehavior, BoxLayout):
    manager = ObjectProperty(None)
    partner_id = StringProperty("")
    profile_pic = StringProperty("assets/profile.png")
    user_name = StringProperty("John Dave")
    comment = StringProperty("TEST")

    def on_release(self, *_):
        self.open_chat()

    def open_chat(self):
        RequestHandler.request_loader(self.parent.parent.parent.parent, self.manager,
            lambda: RequestHandler.create_req_suc_error("post", "chats/retrieve-chat",
            {
                'userId': self.manager.main_state['user']['id'],
                'partnerId': self.partner_id
            }, self.on_success, self.on_error))

    def on_error(self, error):
        RequestHandler.show_error_popup(self.manager, "Chat opening error", error.get('message'))

    def on_success(self, result):
        popup = ChatPopup(
            self.manager,
            chat_id=self.partner_id,
            chat_partner=self.user_name,
            all_chats=result.get('messages', []))
        popup.open()


class ChatSection(BaseSection):

    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager
        self.load_all_chats()

    def load_all_chats(self):
        user = self.manager.main_state['user']['id']
        RequestHandler.request_loader(self.manager.home, self.manager,
            lambda: RequestHandler.create_req_suc_error("post", "chats/get-chats", {
                'userId': user
            }, self.on_sucess, self.on_error))
    
    def on_sucess(self, response):
        self.all_users = None
        widget = self.ids.comment_list
        widget.clear_widgets()

        if response.get('success') and 'chats' in response:            
            for chat in response.get('chats', []):
                if not chat.get('lastMessage', None):
                    continue

                chat_partner = CommentItem(
                    manager=self.manager,
                    partner_id=chat.get('partnerId'),
                    profile_pic=chat.get('profileImage'),
                    user_name=chat.get('username'),
                    comment=chat.get('lastMessage').get('message')
                )
                widget.add_widget(chat_partner)
        else:
            RequestHandler.show_error_popup(self.manager, "Loading Chats", "No Chats found.")

    def on_error(self, error):
        RequestHandler.show_error_popup(self.manager, "Loading Chats", "Error Loading Chats: " + error.get('message'))

