from src.models.box import Box
from src.models.product import Product
from src.models.product_quantity_pair import ProductQuantityPair
from src.modules.organise_boxes.base import BaseOrganiseBoxesModule


class OrganiseBoxesV1(BaseOrganiseBoxesModule):
    @staticmethod
    def flatten_product_quantity_pairs_list(product_quantity_pairs: list[ProductQuantityPair]) -> list[Product]:
        """
        Flatten a list of ProductQuantityPair into a list of Product repeated according to the quantity
        """
        new_list = []
        for product_quantity_pair in product_quantity_pairs:
            for _ in range(product_quantity_pair.quantity):
                new_list.append(product_quantity_pair.product)

        return new_list

    @staticmethod
    def sort_products_by_localisation(products: list[Product]) -> list[Product]:
        """
        Sort a list of products by localisation
        We suppose that the id of the localisation are in the order of the disposition of the products
        """
        return sorted(products, key=lambda product: product.location_id)

    def sort_list_by_distance(self, list_to_sort: list, product: Product, max_distance: int) -> list:
        """
        Sort a list of products by distance from a product
        """

        def get_distance_between_localisation_id(localisation_id1: int, localisation_id2: int) -> int:
            if localisation_id1 == localisation_id2:
                return 0

            for shortest_path in self.instance_data.shortest_paths:
                if (shortest_path.start_localisation_id == localisation_id1 and
                        shortest_path.end_localisation_id == localisation_id2):
                    return shortest_path.distance

            raise ValueError(f"Shortest path between localisation {localisation_id1} and {localisation_id2} not found")

        l = sorted(list_to_sort, key=lambda p: get_distance_between_localisation_id(product.location_id,
                                                                                    p["product"].location_id))
        return filter(lambda p: get_distance_between_localisation_id(product.location_id,
                                                                     p["product"].location_id) <= max_distance, l)

    def run(self) -> list[Box]:
        list_of_boxes = []

        max_distance_default = 1000

        # for each order, create a list of boxes
        for order in self.instance_data.orders:
            max_distance = max_distance_default

            # sort the list of products from localisation
            flatten_product_quantity_pairs_list = self.flatten_product_quantity_pairs_list(order.products)
            list_of_products = self.sort_products_by_localisation(flatten_product_quantity_pairs_list)

            valid = False
            while not valid:
                order_boxes = []

                # create a set of selected products indexes
                selected_products = set()

                print("Order", order.order_id)
                print("len(list_of_products)", len(list_of_products))

                for i, _ in enumerate(list_of_products):
                    # pick the first product that is not in a box
                    if i in selected_products:
                        continue

                    selected_product_idx = i

                    # create a box
                    box = Box(order, [])
                    box.add_product(list_of_products[selected_product_idx])

                    selected_products.add(selected_product_idx)

                    # create a sublist ordered by the distance from the selected product
                    sublist = [{"idx": j, "product": list_of_products[j]} for j in range(len(list_of_products)) if
                               j not in selected_products]
                    sublist = self.sort_list_by_distance(sublist, list_of_products[selected_product_idx], max_distance)

                    # add the products to the boxes
                    for item in sublist:
                        check_weight = box.used_weight + item["product"].weight <= self.instance_data.max_weight
                        check_volume = box.used_volume + item["product"].volume <= self.instance_data.max_volume

                        if check_weight and check_volume:
                            box.add_product(item["product"])
                            selected_products.add(item["idx"])

                    order_boxes.append(box)

                # check if we respect the max number of boxes rule
                if len(order_boxes) <= order.max_number_of_boxes:
                    valid = True
                    list_of_boxes.extend(order_boxes)
                else:
                    max_distance *= 2

        print("Number of boxes:", len(list_of_boxes))
        return list_of_boxes
