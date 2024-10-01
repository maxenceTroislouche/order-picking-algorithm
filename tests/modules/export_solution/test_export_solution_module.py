import unittest
from pathlib import Path

from src.models.box import Box
from src.models.instance_data import InstanceData
from src.models.order import Order
from src.models.product import Product
from src.models.product_quantity_pair import ProductQuantityPair
from src.models.trolley import Trolley
from src.modules.export_solution.export_solution_module import ExportSolutionModule


class TestExportSolutionModule(unittest.TestCase):
    solution_filepath = Path('solution.txt')
    instance_data = InstanceData(1, 1, 1, 2, 1, 1, 1, [], 1, [], 1, 1, 1, [], [], [])
    order = Order(1, 1, 1, [])
    boxes = []
    trolleys = []

    def test_add_number_of_trolleys(self):
        box = Box(self.order, [])
        trolleys = [Trolley([box, box, box]), Trolley([box])]

        export_solution_module = ExportSolutionModule(self.solution_filepath, self.instance_data, self.boxes,
                                                      self.trolleys)

        export_solution_module.add_number_of_trolleys(trolleys)
        self.assertEqual(export_solution_module.file_string, "//Nb tournées\n2\n")

    def test_add_trolley_data(self):
        product_1 = Product(1, 1, 1, 1)
        product_2 = Product(2, 2, 2, 2)

        box_1 = Box(self.order, [ProductQuantityPair(product_1, 2), ProductQuantityPair(product_2, 4)])
        box_2 = Box(self.order, [ProductQuantityPair(product_1, 2), ProductQuantityPair(product_2, 4)])

        trolleys = [Trolley([box_1, box_2]), Trolley([box_1]), Trolley([box_2])]

        export_solution_module = ExportSolutionModule(self.solution_filepath, self.instance_data, self.boxes,
                                                      self.trolleys)

        for trolley in trolleys:
            export_solution_module.add_trolley_data(trolley)

        self.assertEqual(export_solution_module.file_string,
                         "//idTournée nbColis\n1 2\n//IdColis IdCommandeInColis NbProducts IdProd1 QtyProd1 "
                         "IdProd2 QtyProd2 ...\n1 1 6 1 2 2 4 \n2 1 6 1 2 2 4 \n//idTournée nbColis\n2 1\n//IdColis "
                         "IdCommandeInColis NbProducts IdProd1 QtyProd1 IdProd2 QtyProd2 ...\n1 1 6 1 2 2 4 \n"
                         "//idTournée nbColis\n3 1\n//IdColis IdCommandeInColis NbProducts IdProd1 QtyProd1 IdProd2 "
                         "QtyProd2 ...\n2 1 6 1 2 2 4 \n")
