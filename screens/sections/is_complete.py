from .base_section import OrderedProductListSection

class IsComplete(OrderedProductListSection):

	def __init__(self, manager, id, **kwargs):
		super().__init__(manager, "orders/getAllOrderById?userId="+id+"&isComplete=true", complete=True, **kwargs)
