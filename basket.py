
class Basket():

	def __init__(self, name):
		self.name = name
		self.products = []

	def get_producs(self):
		return self.products

	def add_product(self, product):
		self.products.append(product)

	def print_products(self):
		txt = ""
		for product in self.products:
			txt += product.code + ', '

		return txt[:-1]
		
	
