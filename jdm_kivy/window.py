import json
from plyer import orientation
from kivy.core.window import Window
from kivy.app import App, platform
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, TransitionBase, SlideTransition
from .widget import JDMWidget, JDMScreen

class JDMRootManager(ScreenManager):
	"""
	JDMRootManager is a custom ScreenManager class designed to handle multiple screens in a Kivy application,
	with additional functionalities for handling mouse and keyboard input, managing screen transitions, and 
	binding custom behaviors to the application's main loop.

	Attributes:
		is_mouse_down (BooleanProperty): Indicates if a mouse button is currently pressed.
		is_mouse_moving (BooleanProperty): Indicates if the mouse is currently moving.
		mouse_button (StringProperty): Stores the identifier of the currently pressed mouse button.
		mouse_x (NumericProperty): The current x-coordinate of the mouse pointer.
		mouse_y (NumericProperty): The current y-coordinate of the mouse pointer.
		mouse_pos (ReferenceListProperty): Combines mouse_x and mouse_y into a single property for convenience.
		prev_screen (StringProperty): Stores the name of the previous screen for potential use in screen transitions.
		prev_screen_widget (ObjectProperty): Stores the widget of the previous screen.
	"""

	is_mouse_down   = BooleanProperty(False)
	is_mouse_moving = BooleanProperty(False)

	mouse_button = StringProperty('')
	mouse_x      = NumericProperty(0)
	mouse_y      = NumericProperty(0)
	mouse_pos    = ReferenceListProperty(mouse_x, mouse_y)

	prev_screen        = StringProperty(None)
	prev_screen_widget = ObjectProperty(None)
	
	def __init__(self, **kwargs):
		"""
		Initializes the JDMRootManager with custom behavior.

		Args:
			**kwargs: Arbitrary keyword arguments for base class initialization.
		"""
		super().__init__(**kwargs)
		self.root: JDMRootManager = self  # Reference to the root manager instance
		self.current_screen: JDMScreen  # Reference to the currently active screen

		self.size = Window.size  # Set the size of the manager to the current window size
		self.elapseTime = None  # Placeholder for tracking elapsed time

		self.__private_variable()  # Initialize private variables (assumed to be defined elsewhere)
		with open(f"jsons/config.json") as f:
			self.__config = json.load(f)  # Load configuration from a JSON file

		# If root_clock is enabled in the config, set up a clock to call the update method at 500 FPS
		if self.__config.get("root_clock"):
			self._main_Clock = Clock.schedule_interval(self.update, 1/500)

		# Bind the hook_keyboard method to handle keyboard input
		Window.bind(on_keyboard=self.hook_keyboard)

	def keyboard_down(self, window, scancode=None, key=None, keyAscii=None, *args):
		"""
		Handles keyboard key press events by forwarding them to the current screen's keyboard_down method.

		Args:
			window: The Kivy window instance.
			scancode: The scancode of the pressed key.
			key: The key identifier.
			keyAscii: The ASCII value of the key, if applicable.
			*args: Additional arguments.
		"""
		self.current_screen.keyboard_down(window, scancode, key, keyAscii, *args)

	def keyboard_up(self, window, scancode=None, key=None, keyAscii=None, *args):
		"""
		Handles keyboard key release events by forwarding them to the current screen's keyboard_up method.

		Args:
			window: The Kivy window instance.
			scancode: The scancode of the released key.
			key: The key identifier.
			keyAscii: The ASCII value of the key, if applicable.
			*args: Additional arguments.
		"""
		self.current_screen.keyboard_up(window, scancode, key, keyAscii, *args)

	def mouse_down(self, window, x, y, button, modifiers):
		"""
		Handles mouse button press events by forwarding them to the current screen's mouse_down method.

		Args:
			window: The Kivy window instance.
			x: The x-coordinate of the mouse pointer.
			y: The y-coordinate of the mouse pointer.
			button: The identifier of the pressed mouse button.
			modifiers: Additional modifiers (e.g., Shift, Ctrl).
		"""
		self.is_mouse_down = True
		self.current_screen.mouse_down(window, x, y, button, modifiers)

	def mouse_move(self, window, x, y, button):
		"""
		Handles mouse movement events by forwarding them to the current screen's mouse_move method.

		Args:
			window: The Kivy window instance.
			x: The x-coordinate of the mouse pointer.
			y: The y-coordinate of the mouse pointer.
			button: The identifier of the mouse button, if pressed during the move.
		"""
		self.is_mouse_moving = True
		self.current_screen.mouse_move(window, x, y, button)

	def mouse_up(self, window, x, y, button, modifiers):
		"""
		Handles mouse button release events by forwarding them to the current screen's mouse_up method.

		Args:
			window: The Kivy window instance.
			x: The x-coordinate of the mouse pointer.
			y: The y-coordinate of the mouse pointer.
			button: The identifier of the released mouse button.
			modifiers: Additional modifiers (e.g., Shift, Ctrl).
		"""
		self.is_mouse_down = False
		self.is_mouse_moving = False
		self.current_screen.mouse_up(window, x, y, button, modifiers)

	def _mouse_pos(self, window, pos):
		"""
		Updates the current mouse position.

		Args:
			window: The Kivy window instance.
			pos: A tuple containing the (x, y) coordinates of the mouse pointer.
		"""
		self.mouse_x, self.mouse_y = pos

	def hook_keyboard(self, _, key, *__):
		"""
		Captures and handles keyboard events, specifically the Escape key for triggering
		the handleBackButton method on the current screen.

		Args:
			_ : Placeholder for the window object.
			key: The keycode of the pressed key.
			*__: Additional arguments.

		Returns:
			bool: True to continue processing the event, False to stop.
		"""
		code = Window._keyboards.get("system").keycode_to_string(key)
		if code == 'escape':
			return self.current_screen.handleBackButton()
		return True

	def __private_variable(self):
		"""
		Initializes private variables for internal use.
	
		Attributes:
			__adding_screen (bool): Indicates whether a screen is currently being added. Used to prevent adding screens directly via add_widget.
			__lowest_lapse (int): A placeholder variable with a default value of 99. Its purpose is not detailed in the code provided.
		"""
		self.__adding_screen = False
		self.__lowest_lapse = 99
	
	def add_widget(self, widget, *args, **kwargs):
		"""
		Overrides the add_widget method to enforce the use of the add_screen method for adding screens.
	
		Args:
			widget: The widget to add.
			*args: Additional positional arguments.
			**kwargs: Additional keyword arguments.
	
		Returns:
			The result of the superclass's add_widget method if a screen is currently being added.
	
		Raises:
			Exception: If add_widget is called directly without using add_screen.
		"""
		if self.__adding_screen:
			return super().add_widget(widget, *args, **kwargs)
	
		raise Exception("Please use the add_screen method.")
	
	def change_screen(self, name: str, transition: TransitionBase = SlideTransition(direction='left')):
		"""
		Changes the current screen to the specified screen with an optional transition.
	
		Args:
			name (str): The name of the screen to switch to.
			transition (TransitionBase): The transition effect to use when changing screens. Defaults to a left-slide transition.
	
		If the specified screen does not exist, it will be created and added using the add_screen method.
		"""
		if name not in self._get_screen_names(): 
			self.add_screen(name)
		self.prev_screen = self.current
		self.prev_screen_widget = self.current_screen
		self.transition = transition
		self.current = name
	
	def add_screen(self, screen_name: str, screen: JDMScreen = None, widget: JDMWidget = None):
		"""
		Adds a new screen to the ScreenManager.
	
		Args:
			screen_name (str): The name of the new screen.
			screen (JDMScreen): The screen object to add. If not provided, a new JDMScreen is created.
			widget (JDMWidget): The widget to add to the screen. If not provided, a new JDMWidget is created.
	
		The method creates and adds a screen with the specified name, along with the provided or default widget.
		"""
		if not screen: 
			screen = JDMScreen(name=screen_name)
		if not widget: 
			widget = JDMWidget()
	
		if not hasattr(self, screen_name):
			self.__adding_screen = True
			setattr(self, screen_name, screen) 
			screen = getattr(self, screen_name)
	
			if not screen.name: 
				screen.name = screen_name 
	
			setattr(screen, screen_name, widget)
			screen.add_widget(getattr(screen, screen_name))
			self.add_widget(screen) 
			self.__adding_screen = False 
	
	def update(self, dt: float):
		"""
		Updates the current screen and, if configured, displays the frames per second (FPS) in the app's title.
	
		Args:
			dt (float): The time elapsed since the last update call.
	
		Actions:
			- Updates the `elapseTime` with the current delta time.
			- Calls the `update` method of the current screen.
			- If "display_fps" is enabled in the configuration, calculates the current FPS.
			- Updates the app's title with the current FPS.
			- Tracks the lowest recorded FPS in `__lowest_lapse`.
		"""
		self.elapseTime = dt  # Update the elapsed time
	
		self.current_screen.update()  # Call the update method of the current screen
	
		if self.__config.get("display_fps"):
			lapse = f"{(1 / self.elapseTime):.2f}"  # Calculate FPS and format it to 2 decimal places
			if float(lapse) < self.__lowest_lapse: 
				self.__lowest_lapse = float(lapse)  # Update the lowest recorded FPS if current FPS is lower
			if App.get_running_app(): 
				App.get_running_app().title = (App.get_running_app()._main_title + f" -> FPS: {lapse}")  # Update app title with FPS
	
	def on_stop(self):
		"""
		Called when the application stops. Prints the lowest recorded FPS to the console.
	
		Actions:
			- Outputs the value of `__lowest_lapse` to the console, which represents the lowest FPS recorded during the app's runtime.
		"""
		print(self.__lowest_lapse)  # Print the lowest FPS recorded
