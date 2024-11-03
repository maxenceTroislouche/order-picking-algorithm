from src.models.box import Box
from src.models.product import Product
from src.models.trolley import Trolley
from src.modules.organise_trolleys.base import BaseOrganiseTrolleysModule


class OrganiseTrolleysModuleV2(BaseOrganiseTrolleysModule):
    """
    Module to organise Trolleys: Algorithm version 1
    """

    def get_product_location(self, product: Product):
        location_id = product.location_id
        for location in self.instance_data.locations:
            if location.location_id == location_id:
                return location

        raise ValueError(f'Location with id {location_id} not found')

    def get_box_center(self, box: Box) -> tuple[float, float]:
        locations = []

        for product_quantity_pair in box.product_quantity_pairs:
            product = product_quantity_pair.product
            location = self.get_product_location(product)
            locations.append((location.x, location.y))

        x_center = sum(x for x, _ in locations) / len(locations)
        y_center = sum(y for _, y in locations) / len(locations)
        return x_center, y_center

    def get_sublist_of_boxes_sorted_by_distance(self, box_center: tuple[float, float],
                                                max_distance: float, selected_box_ids: set) -> list[Box]:
        # Sort boxes by distance from the current box center
        boxes_sorted_by_distance = sorted(self.boxes, key=lambda b: ((box_center[0] - self.get_box_center(b)[
            0]) ** 2 + (box_center[1] - self.get_box_center(b)[1]) ** 2) ** 0.5)
        # Filter boxes that are too far
        boxes_sorted_by_distance = list(filter(lambda b: ((box_center[0] - self.get_box_center(b)[0]) ** 2 + (
                box_center[1] - self.get_box_center(b)[1]) ** 2) ** 0.5 <= max_distance, boxes_sorted_by_distance))
        # Remove already selected boxes
        boxes_sorted_by_distance = list(filter(lambda b: b.id not in selected_box_ids, boxes_sorted_by_distance))

        return boxes_sorted_by_distance

    def calculate_max_distance(self) -> float:
        """
        Calculate allowed between the chosen box and all the other boxes in the trolley
        For that we use the average distance between the boxes in the trolley
        """
        box_centers = []
        for box in self.boxes:
            box_centers.append(self.get_box_center(box))

        total_distance = 0
        n = 0
        for i in range(len(box_centers)):
            for j in range(i + 1, len(box_centers)):
                n += 1
                total_distance += ((box_centers[i][0] - box_centers[j][0]) ** 2 + (
                            box_centers[i][1] - box_centers[j][1]) ** 2) ** 0.5

        return (total_distance / n) * 4

    def run(self) -> list[Trolley]:
        list_of_trolleys = []

        selected_box_ids = set()

        for box in self.boxes:
            # Already selected box
            if box.id in selected_box_ids:
                continue

            # Create new trolley
            trolley = Trolley([])
            trolley.boxes.append(box)
            selected_box_ids.add(box.id)

            # Get the center of the box
            box_center = self.get_box_center(box)
            max_distance = self.calculate_max_distance()

            # Create a sublist of boxes sorted by distance from the current box center and that respect the max_distance
            boxes_sorted_by_distance = self.get_sublist_of_boxes_sorted_by_distance(box_center, max_distance,
                                                                                    selected_box_ids)

            # Add the boxes to the trolley
            for _box in boxes_sorted_by_distance:
                if len(trolley.boxes) >= 6:
                    break
                trolley.boxes.append(_box)
                selected_box_ids.add(_box.id)

            # Add the trolley to the list of trolleys
            list_of_trolleys.append(trolley)

        return list_of_trolleys
