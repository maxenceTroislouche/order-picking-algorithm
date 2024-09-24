class Product:
    """
    Represents a product in the store.
    """
    product_id: int
    location_id: int
    weight: int
    volume: int

    def __init__(self, product_id: int, location_id: int, weight: int, volume: int):
        self.product_id = product_id
        self.location_id = location_id
        self.weight = weight
        self.volume = volume
