from typing import TextIO

from src.models.arc import Arc
from src.models.instance_data import InstanceData
from src.models.location import Location
from src.models.order import Order, ProductQuantityPair
from src.models.product import Product
from src.models.shortestpath import ShortestPath
from src.modules.instance_parser.base import BaseInstanceParserModule
from src.utils.string import check_line_is_comment, check_line_is_whitespace, get_int, get_n_ints, get_ints


class InstanceParserModuleException(Exception):
    pass


class InstanceParserModule(BaseInstanceParserModule):
    """
    Implementation of the BaseInstanceParserModule class
    """

    @staticmethod
    def get_next_line(file: TextIO, allow_whitespace_lines: bool = False) -> str:
        line = file.readline()
        while line:
            if check_line_is_comment(line) or (not allow_whitespace_lines and check_line_is_whitespace(line)):
                line = file.readline()
                continue

            return line[:-1] if line[-1] == '\n' else line

        raise InstanceParserModuleException(f'No more lines')

    @staticmethod
    def get_number_of_locations(line: str) -> int:
        return get_int(line, InstanceParserModuleException)

    @staticmethod
    def get_number_of_products(line: str) -> int:
        return get_int(line, InstanceParserModuleException)

    @staticmethod
    def get_number_of_boxes_in_one_trolley(line: str) -> int:
        return get_int(line, InstanceParserModuleException)

    @staticmethod
    def get_number_of_dimensions_of_box_capacity(line: str) -> int:
        number_of_dimensions = get_int(line, InstanceParserModuleException)
        if number_of_dimensions != 2:
            raise InstanceParserModuleException(
                f'Expected 2 dimensions for the box capacity, got {number_of_dimensions}')

        return number_of_dimensions

    @staticmethod
    def get_max_weight_and_max_volume_of_box(line: str) -> list[int]:
        return get_n_ints(line, 2, InstanceParserModuleException)

    @staticmethod
    def get_box_can_accept_mixed_orders(line: str) -> bool:
        val = get_int(line, InstanceParserModuleException)
        if val not in (0, 1):
            raise InstanceParserModuleException(
                f'Expected 0 or 1 for the acceptance of mixed orders in boxes, got {val}')

        return val == 1

    @staticmethod
    def get_product_from_line(line: str) -> Product:
        [product_id, weight, volume, location] = get_n_ints(line, 4, InstanceParserModuleException)
        return Product(product_id, weight, volume, location)

    @staticmethod
    def get_number_of_orders(line: str) -> int:
        return get_int(line, InstanceParserModuleException)

    @staticmethod
    def get_order_from_line(line: str, products: list[Product]) -> Order:
        def get_product_from_product_id(product_id: int) -> Product:
            for p in products:
                if p.product_id == product_id:
                    return p

            raise InstanceParserModuleException(f'Product with id {product_id} not found')

        data = get_ints(line, InstanceParserModuleException)
        order_id, max_number_of_boxes, number_of_product_types = data[:3]
        products_quantity_pairs = []

        if len(data) != 3 + number_of_product_types * 2:
            raise InstanceParserModuleException(
                f'Expected {3 + number_of_product_types * 2} elements for the order, got {len(data)}')

        for i in range(3, len(data), 2):
            product = get_product_from_product_id(data[i])
            products_quantity_pairs.append(ProductQuantityPair(product, data[i + 1]))

        return Order(order_id, max_number_of_boxes, number_of_product_types, products_quantity_pairs)

    @staticmethod
    def get_number_of_vertices_intersections(line: str) -> int:
        return get_int(line, InstanceParserModuleException)

    @staticmethod
    def get_departing_depot(line: str) -> int:
        return get_int(line, InstanceParserModuleException)

    @staticmethod
    def get_arrival_depot(line: str) -> int:
        return get_int(line, InstanceParserModuleException)

    @staticmethod
    def get_arc_from_line(line: str) -> Arc:
        [start_localisation_id, end_localisation_id, distance] = get_n_ints(line, 3, InstanceParserModuleException)
        return Arc(start_localisation_id, end_localisation_id, distance)

    @staticmethod
    def get_shortest_path_from_line(line: str) -> ShortestPath:
        [start_localisation_id, end_localisation_id, distance] = get_n_ints(line, 3, InstanceParserModuleException)
        return ShortestPath(start_localisation_id, end_localisation_id, distance)

    @staticmethod
    def get_location_from_line(line: str) -> Location:
        split_line = line.split(' ')

        for s in split_line:
            if s.strip() == '':
                split_line.remove(s)

        if len(split_line) != 4:
            raise InstanceParserModuleException(f'Expected 4 elements for the location, got {len(split_line)}')

        numbers_string = ' '.join(split_line[:-1])
        [location_id, x, y] = get_n_ints(numbers_string, 3, InstanceParserModuleException)
        name = split_line[-1][1:-1]  # Remove the quotes
        return Location(location_id, x, y, name)

    def run(self) -> InstanceData:
        with open(self.instance_filepath, 'r') as f:
            number_of_locations = self.get_number_of_locations(self.get_next_line(f))
            number_of_products = self.get_number_of_products(self.get_next_line(f))
            number_of_boxes_in_one_trolley = self.get_number_of_boxes_in_one_trolley(self.get_next_line(f))
            number_of_dimensions_of_box_capacity = self.get_number_of_dimensions_of_box_capacity(self.get_next_line(f))
            [max_weight, max_volume] = self.get_max_weight_and_max_volume_of_box(self.get_next_line(f))
            box_can_accept_mixed_orders = self.get_box_can_accept_mixed_orders(self.get_next_line(f))

            products = []
            for _ in range(number_of_products):
                products.append(self.get_product_from_line(self.get_next_line(f)))

            number_of_orders = self.get_number_of_orders(self.get_next_line(f))

            orders = []
            for _ in range(number_of_orders):
                orders.append(self.get_order_from_line(self.get_next_line(f), products))

            number_of_vertices_intersections = self.get_number_of_vertices_intersections(self.get_next_line(f))
            departing_depot_id = self.get_departing_depot(self.get_next_line(f))
            arrival_depot_id = self.get_arrival_depot(self.get_next_line(f))

            line = self.get_next_line(f)
            arcs = []
            while not check_line_is_whitespace(line):
                arcs.append(self.get_arc_from_line(line))
                line = self.get_next_line(f, allow_whitespace_lines=True)

            line = self.get_next_line(f)
            shortest_paths = []
            while not check_line_is_whitespace(line):
                shortest_paths.append(self.get_shortest_path_from_line(line))
                line = self.get_next_line(f, allow_whitespace_lines=True)

            locations = []
            for _ in range(number_of_locations + 2):  # +2 for the depots
                locations.append(self.get_location_from_line(self.get_next_line(f)))

            return InstanceData(number_of_locations, number_of_products, number_of_boxes_in_one_trolley,
                                number_of_dimensions_of_box_capacity, max_weight, max_volume,
                                box_can_accept_mixed_orders, products, number_of_orders, orders,
                                number_of_vertices_intersections, departing_depot_id, arrival_depot_id, arcs,
                                shortest_paths, locations)
