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


class Order:
    """
    Represents an order.
    """
    order_id: int
    max_number_of_boxes: int
    number_of_product_types: int
    products: list[ProductQuantityPair]

    def __init__(self, order_id: int, max_number_of_boxes: int, number_of_product_types: int,
                 products: list[ProductQuantityPair]):
        self.order_id = order_id
        self.max_number_of_boxes = max_number_of_boxes
        self.number_of_product_types = number_of_product_types
        self.products = products
