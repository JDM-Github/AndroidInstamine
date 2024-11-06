from .base_section import OrderedProductListSection

class WhoOrder(OrderedProductListSection):

	def __init__(self, manager, id, **kwargs):
		super().__init__(manager, "orders/getAllOrderFromUsers?sellerId="+id, order=True, **kwargs)

