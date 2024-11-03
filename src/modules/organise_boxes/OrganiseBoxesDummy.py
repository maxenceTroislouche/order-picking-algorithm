from src.models.box import Box
from src.models.instance_data import InstanceData
from src.modules.organise_boxes.base import BaseOrganiseBoxesModule


class OrganiseBoxesDummy(BaseOrganiseBoxesModule):
    """
    Dummy implementation of the OrganiseBoxes module, organizing boxes in the order they are received.
    """
    def __init__(self, instance_data: InstanceData) -> None:
        super().__init__(instance_data)

    def run(self) -> list[Box]:
        boxes = []
        max_volume = self.instance_data.max_volume
        max_weight = self.instance_data.max_weight
        for order in self.instance_data.orders:
            order_boxes : list[Box] = [Box(order, []) for _ in range(order.max_number_of_boxes)]
            i_box = 0
            for order_product_quantity_pair in order.products:
                line_weight = order_product_quantity_pair.quantity * order_product_quantity_pair.product.weight
                line_volume = order_product_quantity_pair.quantity * order_product_quantity_pair.product.volume
                # If the box is full, move to the next box
                if line_weight + order_boxes[i_box].used_weight > max_weight or line_volume + order_boxes[i_box].used_volume > max_volume:
                    i_box += 1
                    if i_box >= len(order_boxes):
                        raise NotImplementedError("The order is too big to fit in the boxes")
                order_boxes[i_box].add_product_quantity_pair(order_product_quantity_pair)
            boxes.extend(order_boxes)
        return boxes
