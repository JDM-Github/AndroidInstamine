
class ThemeHandler:

	def __init__(self):
		self.light_color      = "#AC5EA3"
		self.main_color       = "#9C3E93"
		self.darker_color     = "#AD85A9"
		self.main_error_color = "#fC3E93"
		self.main_hover_color = "#7C1E73"
		self.main_color_88    = "#9C3E9388"

		self.white_bg         = "#eaeaea"
		self.font_color_88    = "#ffffff88"

		self.comment_text_color = "#aaaaaa"
		self.comment_user_color = "#dddddd"


class OriginalColor(ThemeHandler):

	def __init__(self):
		super().__init__()

