import unittest
from io import StringIO
from pathlib import Path

from src.models.product import Product
from src.modules.instance_parser.instance_parser import InstanceParserModule, InstanceParserModuleException


class TestInstanceParser(unittest.TestCase):
    def test_get_next_line(self):
        test_file = StringIO("1\n2\n3\n")
        instance_parser = InstanceParserModule(Path(""))
        self.assertEqual(instance_parser.get_next_line(test_file), "1")
        self.assertEqual(instance_parser.get_next_line(test_file), "2")
        self.assertEqual(instance_parser.get_next_line(test_file), "3")
        self.assertRaises(InstanceParserModuleException, lambda: instance_parser.get_next_line(test_file))

    def test_get_number_of_locations(self):
        instance_parser = InstanceParserModule(Path(""))
        self.assertEqual(instance_parser.get_number_of_locations("123"), 123)
        self.assertRaises(InstanceParserModuleException, lambda: instance_parser.get_number_of_locations("salut"))

    def test_get_number_of_products(self):
        instance_parser = InstanceParserModule(Path(""))
        self.assertEqual(instance_parser.get_number_of_products("456"), 456)
        self.assertRaises(InstanceParserModuleException, lambda: instance_parser.get_number_of_products("salut"))

    def test_get_number_of_boxes_in_one_trolley(self):
        instance_parser = InstanceParserModule(Path(""))
        self.assertEqual(instance_parser.get_number_of_boxes_in_one_trolley("789"), 789)
        self.assertRaises(
            InstanceParserModuleException,
            lambda: instance_parser.get_number_of_boxes_in_one_trolley("salut")
        )

    def test_get_number_of_dimensions_of_box_capacity(self):
        instance_parser = InstanceParserModule(Path(""))
        self.assertEqual(instance_parser.get_number_of_dimensions_of_box_capacity("2"), 2)
        self.assertRaises(
            InstanceParserModuleException,
            lambda: instance_parser.get_number_of_dimensions_of_box_capacity("salut")
        )
        self.assertRaises(
            InstanceParserModuleException,
            lambda: instance_parser.get_number_of_dimensions_of_box_capacity("3")
        )

    def test_get_max_weight_and_max_volume_of_box(self):
        instance_parser = InstanceParserModule(Path(""))
        self.assertEqual(instance_parser.get_max_weight_and_max_volume_of_box("1 2"), [1, 2])
        self.assertRaises(
            InstanceParserModuleException,
            lambda: instance_parser.get_max_weight_and_max_volume_of_box("1 2 3")
        )
        self.assertRaises(
            InstanceParserModuleException,
            lambda: instance_parser.get_max_weight_and_max_volume_of_box("1 salut")
        )

    def test_get_box_can_accept_mixed_orders(self):
        instance_parser = InstanceParserModule(Path(""))
        self.assertTrue(instance_parser.get_box_can_accept_mixed_orders("1"))
        self.assertFalse(instance_parser.get_box_can_accept_mixed_orders("0"))
        self.assertRaises(
            InstanceParserModuleException,
            lambda: instance_parser.get_box_can_accept_mixed_orders("2")
        )
        self.assertRaises(
            InstanceParserModuleException,
            lambda: instance_parser.get_box_can_accept_mixed_orders("salut")
        )

    def test_get_number_of_orders(self):
        instance_parser = InstanceParserModule(Path(""))
        self.assertEqual(instance_parser.get_number_of_orders("123"), 123)
        self.assertRaises(InstanceParserModuleException, lambda: instance_parser.get_number_of_orders("salut"))

    def test_get_order_from_line(self):
        instance_parser = InstanceParserModule(Path(""))
        products = [
            Product(1, 10, 20, 30),
            Product(2, 30, 40, 50),
            Product(3, 50, 60, 70)
        ]

        order = instance_parser.get_order_from_line("1 2 2 1 3 3 2", products)
        self.assertEqual(order.order_id, 1)
        self.assertEqual(order.max_number_of_boxes, 2)
        self.assertEqual(order.number_of_product_types, 2)
        self.assertEqual(len(order.products), 2)
        self.assertEqual(order.products[0].product.product_id, 1)
        self.assertEqual(order.products[0].quantity, 3)
        self.assertEqual(order.products[1].product.product_id, 3)
        self.assertEqual(order.products[1].quantity, 2)

    def test_get_number_of_vertices_intersections(self):
        instance_parser = InstanceParserModule(Path(""))
        self.assertEqual(instance_parser.get_number_of_vertices_intersections("123"), 123)
        self.assertRaises(InstanceParserModuleException, lambda: instance_parser.get_number_of_vertices_intersections("salut"))

    def test_get_departing_depot(self):
        instance_parser = InstanceParserModule(Path(""))
        self.assertEqual(instance_parser.get_departing_depot("123"), 123)
        self.assertRaises(InstanceParserModuleException, lambda: instance_parser.get_departing_depot("salut"))

    def test_get_arrival_depot(self):
        instance_parser = InstanceParserModule(Path(""))
        self.assertEqual(instance_parser.get_arrival_depot("123"), 123)
        self.assertRaises(InstanceParserModuleException, lambda: instance_parser.get_arrival_depot("salut"))

    def test_get_arc_from_line(self):
        instance_parser = InstanceParserModule(Path(""))
        arc = instance_parser.get_arc_from_line("1 2 3")
        self.assertEqual(arc.start_localisation_id, 1)
        self.assertEqual(arc.end_localisation_id, 2)
        self.assertEqual(arc.distance, 3)

    def test_get_shortest_path_from_line(self):
        instance_parser = InstanceParserModule(Path(""))
        shortest_path = instance_parser.get_shortest_path_from_line("1 2 3")
        self.assertEqual(shortest_path.start_localisation_id, 1)
        self.assertEqual(shortest_path.end_localisation_id, 2)
        self.assertEqual(shortest_path.distance, 3)

    def test_get_location_from_line(self):
        instance_parser = InstanceParserModule(Path(""))
        location = instance_parser.get_location_from_line('1 2 3 "Toilets"')
        self.assertEqual(location.location_id, 1)
        self.assertEqual(location.x, 2)
        self.assertEqual(location.y, 3)
        self.assertEqual(location.name, "Toilets")

    def test_instance_parser(self):
        instance_filepath = Path("./instance.txt")
        instance_data = InstanceParserModule(instance_filepath).run()
        self.assertEqual(instance_data.number_of_locations, 400)
        self.assertEqual(instance_data.number_of_products, 313)
        self.assertEqual(instance_data.number_of_boxes_in_one_trolley, 6)
        self.assertEqual(instance_data.number_of_dimensions_of_box_capacity, 2)
        self.assertEqual(instance_data.max_weight, 12000)
        self.assertEqual(instance_data.max_volume, 92160)
        self.assertEqual(instance_data.box_can_accept_mixed_orders, False)
        self.assertEqual(len(instance_data.products), 313)
        self.assertEqual(instance_data.number_of_orders, 6)
        self.assertEqual(len(instance_data.orders), 6)
        self.assertEqual(instance_data.number_of_vertices_intersections, 157)
        self.assertEqual(instance_data.departing_depot_id, 0)
        self.assertEqual(instance_data.arrival_depot_id, 401)
        self.assertEqual(len(instance_data.arcs), 605)
        self.assertEqual(len(instance_data.shortest_paths), 80601)
        self.assertEqual(len(instance_data.locations), 402)
