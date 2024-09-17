
class Utility:

	@staticmethod
	def get_size(size, percentage):
		return size[0] * percentage, size[1] * percentage

	@staticmethod
	def get_value_percentage(size, percentage):
		return size * percentage
