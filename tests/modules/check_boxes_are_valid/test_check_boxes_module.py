import unittest

from src.models.box import Box
from src.models.instance_data import InstanceData
from src.models.order import Order
from src.models.product import Product
from src.models.product_quantity_pair import ProductQuantityPair
from src.modules.check_boxes_are_valid.check_boxes_module import CheckBoxesModule, CheckBoxesModuleException


class TestCheckBoxesModule(unittest.TestCase):
    product_1 = Product(1, 1, 5, 2)
    product_2 = Product(2, 2, 10, 3)

    product_quantity_pair_1 = ProductQuantityPair(product_1, 1)
    product_quantity_pair_2 = ProductQuantityPair(product_2, 2)

    order_1 = Order(1, 1, 2, [product_quantity_pair_1, product_quantity_pair_2])
    order_2 = Order(2, 1, 2, [product_quantity_pair_1, product_quantity_pair_2])

    box_1 = Box(order_1, [product_quantity_pair_1, product_quantity_pair_2])
    box_2 = Box(order_2, [product_quantity_pair_1, product_quantity_pair_2])

    def test_get_box_weight_and_volume(self):
        box = Box(self.order_1, [self.product_quantity_pair_1, self.product_quantity_pair_2])
        check_box_module = CheckBoxesModule.get_box_weight_and_volume(box)

        self.assertEqual(check_box_module, (25, 8))

    def test_check_boxes_weight_and_volume(self):
        box = Box(self.order_1, [self.product_quantity_pair_1, self.product_quantity_pair_2])
        boxes = [box]

        instance_data = InstanceData(1, 1, 1, 1, 1, 1, False, [], 2, [], 1, 1, 1, [], [], [])
        check_box_module = CheckBoxesModule(instance_data, boxes)

        with self.assertRaises(CheckBoxesModuleException):
            check_box_module.check_boxes_weight_and_volume(boxes)

    def test_sort_boxes_by_order(self):
        boxes = [self.box_1, self.box_2]

        instance_data = InstanceData(1, 1, 1, 1, 100, 100, False, [], 2, [], 1, 1, 1, [], [], [])

        check_box_module = CheckBoxesModule(instance_data, boxes)
        boxes_by_order = check_box_module.sort_boxes_by_order(boxes)

        self.assertEqual(boxes_by_order, {1: [self.box_1], 2: [self.box_2]})

    def test_get_product_quantity_pairs_from_boxes(self):
        boxes = [self.box_1, self.box_2]

        instance_data = InstanceData(1, 1, 1, 1, 100, 100, False, [], 2, [], 1, 1, 1, [], [], [])

        check_box_module = CheckBoxesModule(instance_data, boxes)
        product_quantity_pairs = check_box_module.get_product_quantity_pairs_from_boxes(boxes)

        self.assertEqual(product_quantity_pairs, {1: 2, 2: 4})

    def test_check_order_products_are_in_boxes(self):
        boxes = [self.box_1, self.box_2]

        instance_data = InstanceData(1, 1, 1, 1, 100, 100, False, [], 2, [], 1, 1, 1, [], [], [])

        check_box_module = CheckBoxesModule(instance_data, boxes)

        with self.assertRaises(CheckBoxesModuleException):
            check_box_module.check_order_products_are_in_boxes(self.order_1, boxes)
