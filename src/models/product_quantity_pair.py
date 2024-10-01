from src.models.product import Product


class ProductQuantityPair:
    """
    Represents a pair of product and quantity.
    """
    product: Product
    quantity: int

    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity

    def __eq__(self, other):
        return self.product == other.product and self.quantity == other.quantity