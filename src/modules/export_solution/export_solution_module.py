from typing import NoReturn, List

from src.models.trolley import Trolley
from src.modules.export_solution.base import BaseExportSolutionModule


class ExportSolutionModule(BaseExportSolutionModule):
    file_string: str = ""

    def write_file_string_to_file(self) -> NoReturn:
        with self.solution_filepath.open("w") as file:
            file.write(self.file_string)

    def add_number_of_trolleys(self, trolleys: List[Trolley]):
        self.file_string += f"//Nb tournées\n{len(trolleys)}\n"

    def add_trolley_data(self, trolley: Trolley) -> NoReturn:
        self.file_string += "//idTournée nbColis\n"
        self.file_string += f"{trolley.id} {len(trolley.boxes)}\n"
        self.file_string += "//IdColis IdCommandeInColis NbProducts IdProd1 QtyProd1 IdProd2 QtyProd2 ...\n"
        for box in trolley.boxes:
            nb_products = sum(pq.quantity for pq in box.product_quantity_pairs)

            self.file_string += f"{box.id} {box.order.order_id} {nb_products} "
            for pq in box.product_quantity_pairs:
                self.file_string += f"{pq.product.product_id} {pq.quantity} "
            self.file_string += "\n"

    def run(self) -> NoReturn:
        self.add_number_of_trolleys(self.trolleys)

        for trolley in self.trolleys:
            self.add_trolley_data(trolley)

        self.write_file_string_to_file()
