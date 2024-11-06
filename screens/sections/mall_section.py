from .base_section import ProductListSection

class MallSection(ProductListSection):

	def __init__(self, manager, **kwargs):
		super().__init__(manager, "product/products", **kwargs)
