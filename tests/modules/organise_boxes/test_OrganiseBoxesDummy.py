from unittest import TestCase

from src.models.box import Box
from src.models.instance_data import InstanceData
from src.models.order import Order
from src.models.product import Product
from src.models.product_quantity_pair import ProductQuantityPair
from src.modules.organise_boxes.OrganiseBoxesDummy import OrganiseBoxesDummy


class TestOrganiseBoxesDummy(TestCase):
    def test_run(self):
        # create instances data
        instance_data = InstanceData(
            3, 1, 1, 2,
            1, 10, False, [
                Product(1, 1, 1, 1),
                Product(2, 1, 1, 1),
                Product(3, 1, 1, 1),
            ],
            2, [
                Order(1, 2, 1, [
                    ProductQuantityPair(Product(1, 1, 1, 1), 1),
                    ProductQuantityPair(Product(2, 1, 1, 1), 1),
                ]),
                Order(2, 1, 1, [
                    ProductQuantityPair(Product(3, 1, 1, 1), 1),
                ]),
            ],
            1, 2, 3, [], [], []
        )
        # create the module
        organise_boxes_dummy = OrganiseBoxesDummy(instance_data)
        # run the module
        boxes = organise_boxes_dummy.run()
        # check the result
        self.assertEqual(boxes[0].product_quantity_pairs, [ProductQuantityPair(Product(1, 1, 1, 1), 1)])
        self.assertEqual(boxes[1].product_quantity_pairs, [ProductQuantityPair(Product(2, 1, 1, 1), 1)])
        self.assertEqual(boxes[2].product_quantity_pairs, [ProductQuantityPair(Product(3, 1, 1, 1), 1)])
