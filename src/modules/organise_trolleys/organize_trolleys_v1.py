from src.models.trolley import Trolley
from src.modules.organise_trolleys.base import BaseOrganiseTrolleysModule


class V1OrganiseTrolleysModule(BaseOrganiseTrolleysModule):
    """
    Module to organise Trolleys: Algorithm version 1
    """

    # pour chaque carton, calculer le "centre" du carton
    # Regrouper les cartons par localisation de leur centre
    # pour chaque groupe de cartons, créer un chariot
    def run(self) -> list[Trolley]:
        distance_treshold: float = 10.0

        box_centers: list[tuple[float, float]] = []
        for box in self.boxes:
            # Récupération de chaque localisation des produits du carton
            product_locations = []
            for product in box.product_quantity_pairs:
                product_location_id = product.product.location_id
                # Find the location with this id
                product_location = next((l for l in self.instance_data.locations if l.location_id == product_location_id), None)

                if product_location is None:
                    raise ValueError(f'Location with id {product_location_id} not found')

                product_locations.append(product_location)

            # Calculer le centre du carton
            x_center = sum(location.x for location in product_locations) / len(product_locations)
            y_center = sum(location.y for location in product_locations) / len(product_locations)
            box_center = (x_center, y_center)
            box_centers.append(box_center)

        trolleys: list[Trolley] = []
        placed_boxes_indexes: list[int] = []
        current_box_origin: tuple[float, float] = box_centers[0]
        for box in self.boxes:
            # Si le chariot actuel est plein, ajouter un nouveau chariot
            if not trolleys or len(trolleys[-1].boxes) == self.instance_data.number_of_boxes_in_one_trolley:
                trolleys.append(Trolley([]))

            # Pour cette boite, prendre la boite la plus proche de l'origine actuelle
            for i, box_center in enumerate(box_centers):
                if i in placed_boxes_indexes:
                    continue

                distance = ((current_box_origin[0] - box_center[0]) ** 2 + (current_box_origin[1] - box_center[1]) ** 2) ** 0.5

                # Si la distance est inférieure à la distance treshold, ajouter la boite au chariot actuel
                if distance < distance_treshold:
                    placed_boxes_indexes.append(i)
                    trolleys[-1].boxes.append(box)

                    # Si le chariot actuel est plein, ajouter un nouveau chariot et changer la box origine actuelle
                    if len(trolleys[-1].boxes) == self.instance_data.number_of_boxes_in_one_trolley:
                        trolleys.append(Trolley([]))
                        current_box_origin = box_centers[i + 1]

        return trolleys
