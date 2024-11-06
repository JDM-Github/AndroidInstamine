from .base_section import OrderedProductListSection

class ToReceive(OrderedProductListSection):

	def __init__(self, manager, id, **kwargs):
		super().__init__(manager, "orders/getAllOrderById?userId="+id+"&toReceive=true", receive=True, **kwargs)
