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
    
    def remove_widgets(self, *args):
        app = App.get_running_app()
        manager = app.sm

        if not manager.main_state['user']['isSeller']:
            self.ids.bottom_grid.remove_widget(self.ids.who_order)
            self.ids.bottom_grid.remove_widget(self.ids.my_product)
        else:
            self.ids.orders.parent.remove_widget(self.ids.orders)
            self.ids.top_profile.parent.remove_widget(self.ids.top_profile)

            self.ids.bottom_grid.remove_widget(self.ids.buy_again)
            self.ids.bottom_grid.remove_widget(self.ids.recently_viewed)
            

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
