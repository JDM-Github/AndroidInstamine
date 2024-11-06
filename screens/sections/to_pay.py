from .base_section import OrderedProductListSection

class ToPay(OrderedProductListSection):

	def __init__(self, manager, id, **kwargs):
		super().__init__(manager, "orders/getAllOrderById?userId="+id+"&toPay=true", pay=True, **kwargs)
