from src.models.order import Order
from src.models.product_quantity_pair import ProductQuantityPair


class Box:
    """
    Represents a box
    """
    order: Order
    product_quantity_pairs: list[ProductQuantityPair]

    def __init__(self, order: Order, product_quantity_pairs: list[ProductQuantityPair]):
        self.order = order
        self.product_quantity_pairs = product_quantity_pairs
