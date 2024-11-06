from .base_section import ProductListSection

class CheckUserProducts(ProductListSection):

	def __init__(self, manager, email, **kwargs):
		super().__init__(manager, "product/products?email="+email, **kwargs)
