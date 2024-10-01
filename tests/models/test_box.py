import unittest

from src.models.box import Box
from src.models.order import Order


class TestBox(unittest.TestCase):
    def test_id_counter(self):
        order = Order(1, 1, 1, [])

        box = Box(order, [])
        box_2 = Box(order, [])

        self.assertEqual(box.id, 1)
        self.assertEqual(box_2.id, 2)
