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
