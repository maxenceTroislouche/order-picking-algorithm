import unittest

from src.models.box import Box
from src.models.order import Order
from src.models.product import Product
from src.models.product_quantity_pair import ProductQuantityPair


class TestBox(unittest.TestCase):
    def test_id_counter(self):
        order = Order(1, 1, 1, [])

        box = Box(order, [])
        box_2 = Box(order, [])

        self.assertEqual(box.id, 1)
        self.assertEqual(box_2.id, 2)

    def test_add_product_quantity_pair(self):
        order = Order(1, 1, 1, [])
        product_quantity_pair = ProductQuantityPair(Product(1, 1, 1, 1), 1)

        box = Box(order, [])
        box.add_product_quantity_pair(product_quantity_pair)

        self.assertEqual(box.product_quantity_pairs, [product_quantity_pair])
        self.assertEqual(box.used_volume, 1)
        self.assertEqual(box.used_weight, 1)

    def test_edit_product_quantity_pair(self):
        order = Order(1, 1, 1, [])
        product_quantity_pair = ProductQuantityPair(Product(1, 1, 1), 1)
        product_quantity_pair_2 = ProductQuantityPair(Product(1, 1, 1), 2)

        box = Box(order, [product_quantity_pair])
        box.edit_product_quantity_pair(product_quantity_pair_2)

        self.assertEqual(box.product_quantity_pairs, [product_quantity_pair_2])
        self.assertEqual(box.used_volume, 2)
        self.assertEqual(box.used_weight, 2)
