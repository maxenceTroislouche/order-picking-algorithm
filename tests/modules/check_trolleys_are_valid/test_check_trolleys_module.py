import unittest

from src.models.box import Box
from src.models.instance_data import InstanceData
from src.models.order import Order
from src.models.trolley import Trolley
from src.modules.check_trolleys_are_valid.check_trolleys_module import CheckTrolleysModule


class TestCheckTrolleysModule(unittest.TestCase):
    instance_data = InstanceData(1, 1, 1, 1, 100, 100, False, [], 2, [], 1, 1, 1, [], [], [])
    order = Order(1, 1, 2, [])

    def test_check_trolley_contain_all_boxes(self):
        pass

    def test_check_trolley_has_maximum_of_6_boxes(self):
        boxes = []
        box = Box(self.order, [])
        trolleys_1 = [Trolley([box, box, box, box, box, box, box])]
        trolleys_2 = [Trolley([box, box])]

        check_trolleys_module_1 = CheckTrolleysModule(self.instance_data, boxes, trolleys_1)
        check_trolleys_module_2 = CheckTrolleysModule(self.instance_data, boxes, trolleys_2)

        with self.assertRaises(Exception):
            check_trolleys_module_1.check_trolley_has_maximum_of_6_boxes()

        check_trolleys_module_2.check_trolley_has_maximum_of_6_boxes()

    def test_check_box_duplicates_in_trolleys(self):
        pass
