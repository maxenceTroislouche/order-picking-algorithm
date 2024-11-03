from collections import defaultdict
from typing import NoReturn, List, Dict

from src.models.box import Box
from src.models.order import Order
from src.models.product_quantity_pair import ProductQuantityPair
from src.modules.check_boxes_are_valid.base import BaseCheckBoxesAreValidModule


class CheckBoxesModuleException(Exception):
    pass


class CheckBoxesModule(BaseCheckBoxesAreValidModule):
    @staticmethod
    def get_box_weight_and_volume(box: Box) -> tuple[float, float]:
        box_weight = 0
        box_volume = 0

        for product_quantity in box.product_quantity_pairs:
            box_weight += product_quantity.product.weight * product_quantity.quantity
            box_volume += product_quantity.product.volume * product_quantity.quantity

        return box_weight, box_volume

    def check_boxes_weight_and_volume(self, boxes: List[Box]):
        # Check that the box's weight is not above the maximum weight
        # Check that the box's content's volume is not above the maximum volume
        for box in boxes:
            weight, volume = self.get_box_weight_and_volume(box)

            if weight > self.instance_data.max_weight:
                raise CheckBoxesModuleException(f"Box {box} is too heavy")

            if volume > self.instance_data.max_volume:
                raise CheckBoxesModuleException(f"Box {box} is too big")

    @staticmethod
    def sort_boxes_by_order(boxes: List[Box]) -> dict[int, List[Box]]:
        boxes_by_order = defaultdict(list)

        for box in boxes:
            boxes_by_order[box.order_id].append(box)

        return boxes_by_order

    @staticmethod
    def get_product_quantity_pairs_from_boxes(boxes: List[Box]) -> Dict[int, int]:
        product_quantity_pairs = {}

        for box in boxes:
            for product_quantity_pair in box.product_quantity_pairs:
                if product_quantity_pair.product.product_id not in product_quantity_pairs:
                    product_quantity_pairs[product_quantity_pair.product.product_id] = 0
                product_quantity_pairs[product_quantity_pair.product.product_id] += product_quantity_pair.quantity

        return product_quantity_pairs

    def check_order_products_are_in_boxes(self, order: Order, boxes: List[Box]):
        product_quantity_pairs = self.get_product_quantity_pairs_from_boxes(boxes)

        print(f"product_quantity_pairs : {product_quantity_pairs}")

        if len(product_quantity_pairs) != order.number_of_product_types:
            print(f"")
            print(f"product_quantity_pairs: {sorted(product_quantity_pairs.keys())}")
            print(f"order: {sorted(order.products, key=lambda x: x.product.product_id)}")
            print(f"orders: {self.instance_data.orders}")
            print(f"boxes: {self.boxes}")
            raise CheckBoxesModuleException(f"Order {order.order_id} is not fulfilled: expected: {order.number_of_product_types}, got: {len(product_quantity_pairs)}")

        # Check that the quantity of each product in the order is the same as the quantity of the product in the boxes
        for product_quantity_pair in order.products:
            if product_quantity_pairs[product_quantity_pair.product.product_id] != product_quantity_pair.quantity:
                raise CheckBoxesModuleException(f"Order {order.order_id} is not fulfilled")

    def run(self) -> NoReturn:
        self.check_boxes_weight_and_volume(self.boxes)

        sorted_boxes_dict = self.sort_boxes_by_order(self.boxes)
        orders = self.instance_data.orders

        for order in orders:
            self.check_order_products_are_in_boxes(order, sorted_boxes_dict[order.order_id])
