from src.models.product import Product
from src.models.product_quantity_pair import ProductQuantityPair


class Order:
    """
    Represents an order.
    """
    order_id: int
    max_number_of_boxes: int
    number_of_product_types: int
    products: list[ProductQuantityPair]
    number_of_products: int

    def __init__(self, order_id: int, max_number_of_boxes: int, number_of_product_types: int,
                 products: list[ProductQuantityPair]):
        self.order_id = order_id
        self.max_number_of_boxes = max_number_of_boxes
        self.number_of_product_types = number_of_product_types
        self.products = products
        self.number_of_products = sum([pqp.quantity for pqp in self.products])
