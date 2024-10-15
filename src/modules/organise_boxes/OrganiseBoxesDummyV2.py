from src.models.box import Box
from src.models.instance_data import InstanceData
from src.models.product import Product
from src.models.product_quantity_pair import ProductQuantityPair
from src.modules.organise_boxes.base import BaseOrganiseBoxesModule


class OrganiseBoxesDummyV2(BaseOrganiseBoxesModule):
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
            # Trier les produits par leur location_id pour minimiser les déplacements
            sorted_products = sorted(order.products, key=lambda pq: pq.product.location_id)

            # Aplatir la liste des produits
            flat_product_list = ProductQuantityPair.flatten_product_quantity_pairs_list(sorted_products)

            order_boxes: list[Box] = [Box(order, []) for _ in range(order.max_number_of_boxes)]
            i_box = 0

            # Distribuer les produits dans les cartons
            for product in flat_product_list:
                # Vérifier si le produit peut être ajouté au carton actuel
                if (product.weight + order_boxes[i_box].used_weight > max_weight or
                    product.volume + order_boxes[i_box].used_volume > max_volume):
                    i_box += 1  # Passer au carton suivant

                    if i_box >= len(order_boxes):
                        # Si on dépasse le nombre maximum de cartons, essayer de réinsérer les produits
                        print("Nombre maximum de cartons atteint, redistribution en cours...")
                        self.redistribute_remaining_products(order_boxes, flat_product_list[i_box:])
                        break

                order_boxes[i_box].add_product(product)

            boxes.extend(order_boxes)
        return boxes

    def redistribute_remaining_products(self, boxes: list[Box], remaining_products: list[Product]) -> None:
        """
        Tente de redistribuer les produits restants dans les cartons existants en respectant les
        contraintes de poids et de volume.
        """
        max_weight = self.instance_data.max_weight
        max_volume = self.instance_data.max_volume

        for product in remaining_products:
            placed = False
            # Essayer de placer le produit dans un carton existant
            for box in boxes:
                if (product.weight + box.used_weight <= max_weight and
                    product.volume + box.used_volume <= max_volume):
                    box.add_product(product)
                    placed = True
                    break

            # Si aucun carton ne peut accueillir le produit, on a un problème (normalement évité)
            if not placed:
                raise ValueError("Impossible de répartir les produits dans le nombre de cartons disponibles.")
