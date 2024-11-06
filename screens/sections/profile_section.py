from kivy.app import App

from handle_requests import RequestHandler
from popup.popups import EditProfile
from .base_section import BaseSection
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import BooleanProperty, StringProperty

from widgets import ThemedPopup


class ProfileWidget(BoxLayout):
    unread = BooleanProperty(True)
    title = StringProperty("")
    message = StringProperty("")
    date = StringProperty("2022-05-10")

class ProfileSection(BaseSection):

    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager
        Clock.schedule_once(self.remove_widgets)

    def sign_out(self):
        app = App.get_running_app()
        manager = app.sm

        manager.main_state['user'] = {}
        manager.main_state['already_login'] = False
        manager.save_json_config("state.json", manager.main_state)
        manager.current = "login"

    def open_edit_profile(self):
        popup = EditProfile(self.manager)
        popup.open()

    def become_seller(self):
        app = App.get_running_app()
        manager = app.sm

        if manager.main_state['user']['isSeller']:
            popup = ThemedPopup(
                manager,
                title='Account Become a Seller',
                message="You are already a seller")
            popup.open()
        else:
            RequestHandler.request_loader(self.parent, manager,
                lambda: RequestHandler.create_req_suc_error("post", "user/seller",
                    {'email': manager.main_state['user']['email']}, self.on_success, self.on_error))
    
    def remove_widgets(self, *args):
        app = App.get_running_app()
        manager = app.sm

        if not manager.main_state['user']['isSeller']:
            if self.ids.who_order in self.ids.bottom_grid.children:
                self.ids.bottom_grid.remove_widget(self.ids.who_order)
            if self.ids.my_product in self.ids.bottom_grid.children:
                self.ids.bottom_grid.remove_widget(self.ids.my_product)

    def on_error(self, error):
        app = App.get_running_app()
        manager = app.sm
        RequestHandler.show_error_popup(manager, "Becoming a Seller Failed", "Becoming a Seller: " + error.get('message'))

    def on_success(self, result):
        app = App.get_running_app()
        manager = app.sm

        manager.main_state['user']['isSeller'] = True
        manager.save_json_config('state.json', manager.main_state)
        popup = ThemedPopup(
            manager,
            title='Account Become a Seller',
            message=result.get('message'))
        popup.open()

    def go_to_my_products(self):
        app = App.get_running_app()
        manager = app.sm

        if not manager.main_state['user']['isSeller']:
            popup = ThemedPopup(manager, "Not a Seller", "You are not a seller to have products")
            popup.open()
        else:
            self.parent.parent.parent.update_button_active('myproduct')

    def go_to_likes(self):
        self.parent.parent.parent.update_button_active('mylikes')
    def go_to_recently_viewed(self):
        self.parent.parent.parent.update_button_active('recentlyViewed')
    def go_to_pay(self):
        self.parent.parent.parent.update_button_active('toPay')
    def go_to_ship(self):
        self.parent.parent.parent.update_button_active('toShip')
    def go_to_receive(self):
        self.parent.parent.parent.update_button_active('toReceive')
    def go_is_complete(self):
        self.parent.parent.parent.update_button_active('isComplete')
    def go_is_order(self):
        self.parent.parent.parent.update_button_active('whoOrder')
