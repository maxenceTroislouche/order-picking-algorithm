from src.models.box import Box
from src.models.instance_data import InstanceData
from src.modules.organise_boxes.base import BaseOrganiseBoxesModule
from src.models.product_quantity_pair import ProductQuantityPair


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
                # left_qty : left quantity of the product to put in the boxes
                left_qty = order_product_quantity_pair.quantity
                product_weight = order_product_quantity_pair.product.weight
                product_volume = order_product_quantity_pair.product.volume

                line_weight = left_qty * product_weight
                line_volume = left_qty * product_volume

                while (line_weight + order_boxes[i_box].used_weight > max_weight
                       or line_volume + order_boxes[i_box].used_volume > max_volume):
                    # first, we try to find how many individual products we can fit in the box :
                    # max_added_volume = max_volume - used_volume
                    # n_volume = max_added_volume / product_volume (integer division)
                    # max_added_weight = max_weight - used_weight
                    # n_weight = max_added_weight / product_weight (integer division)
                    # n = min(n_volume, n_weight) (number of products that can be added)
                    n = min((max_volume - order_boxes[i_box].used_volume) // product_volume,
                            (max_weight - order_boxes[i_box].used_weight) // product_weight)
                    # if we can fit at least one product, we add it to the box
                    if n > 0:
                        order_boxes[i_box].add_product_quantity_pair(ProductQuantityPair(order_product_quantity_pair.product, n))
                        left_qty -= n
                    # if we can't fit any product, we move to the next box
                    i_box += 1
                    # if we are out of boxes, we stop
                    if i_box >= len(order_boxes):
                        raise NotImplementedError(f"The order {order.order_id} is too big to fit in the boxes")

                order_boxes[i_box].add_product_quantity_pair(ProductQuantityPair(order_product_quantity_pair.product, left_qty))
            boxes.extend(order_boxes)
        return boxes

