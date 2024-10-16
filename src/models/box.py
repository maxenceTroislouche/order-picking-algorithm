from src.models.order import Order
from src.models.product import Product
from src.models.product_quantity_pair import ProductQuantityPair


class Box:
    """
    Represents a box
    """
    BOX_ID_COUNTER = 1

    id: int
    order: Order
    product_quantity_pairs: list[ProductQuantityPair]
    used_volume: int
    used_weight: int

    def __init__(self, order: Order, product_quantity_pairs: list[ProductQuantityPair] = None):
        self.id = Box.BOX_ID_COUNTER
        Box.BOX_ID_COUNTER += 1
        self.order = order
        # Si product_quantity_pairs est None, on l'initialise à une liste vide
        self.product_quantity_pairs = product_quantity_pairs if product_quantity_pairs is not None else []

        # Calcul de used_space et used_weight seulement si product_quantity_pairs n'est pas vide
        self.used_volume = sum([pqp.product.volume * pqp.quantity for pqp in self.product_quantity_pairs])
        self.used_weight = sum([pqp.product.weight * pqp.quantity for pqp in self.product_quantity_pairs])

    def add_product_quantity_pair(self, product_quantity_pair: ProductQuantityPair) -> None:
        self.product_quantity_pairs.append(product_quantity_pair)
        self.used_volume += product_quantity_pair.product.volume * product_quantity_pair.quantity
        self.used_weight += product_quantity_pair.product.weight * product_quantity_pair.quantity

    def edit_product_quantity_pair(self, product_quantity_pair: ProductQuantityPair) -> None:
        for old_pqp in self.product_quantity_pairs:
            if old_pqp.product.product_id == product_quantity_pair.product.product_id:
                self.used_volume += old_pqp.product.volume * (product_quantity_pair.quantity - old_pqp.quantity)
                self.used_weight += old_pqp.product.weight * (product_quantity_pair.quantity - old_pqp.quantity)
                old_pqp.quantity = product_quantity_pair.quantity
                return

        raise ValueError(f'Product {product_quantity_pair.product} not found in box {self}')

    def add_product(self, product: Product):
        for product_quantity_pair in self.product_quantity_pairs:
            if product_quantity_pair.product.product_id == product.product_id:
                product_quantity_pair.quantity += 1
                self.used_volume += product.volume
                self.used_weight += product.weight
                return
        self.add_product_quantity_pair(ProductQuantityPair(product, 1))

    def remove_product(self, product):
        for product_quantity_pair in self.product_quantity_pairs:
            if product_quantity_pair.product.product_id == product.product_id:
                product_quantity_pair.quantity -= 1
                self.used_volume -= product.volume
                self.used_weight -= product.weight
                if product_quantity_pair.quantity == 0:
                    self.product_quantity_pairs.remove(product_quantity_pair)
                return
        raise ValueError(f'Product {product} not found in box {self}')
