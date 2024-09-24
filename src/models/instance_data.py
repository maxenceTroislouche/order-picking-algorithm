from src.models.arc import Arc
from src.models.location import Location
from src.models.order import Order
from src.models.product import Product
from src.models.shortestpath import ShortestPath


class InstanceData:
    """
    Represents all data contained in an instance file
    """
    number_of_locations: int
    number_of_products: int
    number_of_boxes_in_one_trolley: int
    number_of_dimensions_of_box_capacity: int
    max_weight: int
    max_volume: int
    box_can_accept_mixed_orders: bool
    products: list[Product]
    number_of_orders: int
    orders: list[Order]
    number_of_vertices_intersections: int
    departing_depot_id: int
    arrival_depot_id: int
    arcs: list[Arc]
    shortest_paths: list[ShortestPath]
    locations: list[Location]

    def __init__(self, number_of_locations: int, number_of_products: int, number_of_boxes_in_one_trolley: int,
                 number_of_dimensions_of_box_capacity: int, max_weight: int, max_volume: int,
                 box_can_accept_mixed_orders: bool, products: list[Product], number_of_orders: int, orders: list[Order],
                 number_of_vertices_intersections: int, departing_depot_id: int, arrival_depot_id: int, arcs: list[Arc],
                 shortest_paths: list[ShortestPath], locations: list[Location]):
        self.number_of_locations = number_of_locations
        self.number_of_products = number_of_products
        self.number_of_boxes_in_one_trolley = number_of_boxes_in_one_trolley
        self.number_of_dimensions_of_box_capacity = number_of_dimensions_of_box_capacity
        self.max_weight = max_weight
        self.max_volume = max_volume
        self.box_can_accept_mixed_orders = box_can_accept_mixed_orders
        self.products = products
        self.number_of_orders = number_of_orders
        self.orders = orders
        self.number_of_vertices_intersections = number_of_vertices_intersections
        self.departing_depot_id = departing_depot_id
        self.arrival_depot_id = arrival_depot_id
        self.arcs = arcs
        self.shortest_paths = shortest_paths
        self.locations = locations
