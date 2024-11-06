from .base_section import ProductListSection


class ProductSection(ProductListSection):

	def __init__(self, manager, **kwargs):
		super().__init__(manager, "product/products", **kwargs)
