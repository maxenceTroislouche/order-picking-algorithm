import unittest

from src.models.box import Box
from src.models.order import Order
from src.models.trolley import Trolley


class TestTrolley(unittest.TestCase):
    def test_id_counter(self):
        trolley = Trolley([])
        trolley_2 = Trolley([])

        self.assertEqual(trolley.id, 1)
        self.assertEqual(trolley_2.id, 2)
