from .base_section import OrderedProductListSection

class ToShip(OrderedProductListSection):

	def __init__(self, manager, id, **kwargs):
		super().__init__(manager, "orders/getAllOrderById?userId="+id+"&toShip=true", ship=True, **kwargs)
