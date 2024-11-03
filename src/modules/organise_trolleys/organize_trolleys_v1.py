from src.models.box import Box
from src.models.product import Product
from src.models.trolley import Trolley
from src.modules.organise_trolleys.base import BaseOrganiseTrolleysModule


class V1OrganiseTrolleysModule(BaseOrganiseTrolleysModule):
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

    # pour chaque carton, calculer le "centre" du carton
    # Regrouper les cartons par localisation de leur centre
    # pour chaque groupe de cartons, créer un chariot
    def run(self) -> list[Trolley]:
        distance_treshold: float = 10.0

        box_centers: list[tuple[float, float]] = []
        for box in self.boxes:
            box_center = self.get_box_center(box)
            box_centers.append(box_center)

        trolleys: list[Trolley] = [Trolley([])]
        placed_boxes_indexes: set[int] = set()
        current_box_origin: tuple[float, float] = box_centers[0]
        for box in self.boxes:
            # Pour cette boite, prendre la boite la plus proche de l'origine actuelle
            for i, box_center in enumerate(box_centers):
                if i in placed_boxes_indexes:
                    continue

                distance = ((current_box_origin[0] - box_center[0]) ** 2 + (current_box_origin[1] - box_center[1]) ** 2) ** 0.5

                # Si la distance est inférieure à la distance treshold, ajouter la boite au chariot actuel
                if distance < distance_treshold:
                    placed_boxes_indexes.add(i)
                    trolleys[-1].boxes.append(box)

                    # Si le chariot actuel est plein, ajouter un nouveau chariot et changer la box origine actuelle
                    if len(trolleys[-1].boxes) == self.instance_data.number_of_boxes_in_one_trolley:
                        trolleys.append(Trolley([]))
                        current_box_origin = box_centers[i + 1]

        return trolleys
