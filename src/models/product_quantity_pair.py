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

    @staticmethod
    def flatten_product_quantity_pairs_list(product_quantity_pairs: list["ProductQuantityPair"]) -> list[Product]:
        new_list = []
        for product_quantity_pair in product_quantity_pairs:
            for _ in range(product_quantity_pair.quantity):
                new_list.append(product_quantity_pair.product)
        return sorted(new_list, key=lambda x: x.product_id)