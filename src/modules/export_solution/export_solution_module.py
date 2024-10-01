from typing import NoReturn, List

from src.models.trolley import Trolley
from src.modules.export_solution.base import BaseExportSolutionModule


class ExportSolutionModule(BaseExportSolutionModule):
    file_string: list[str] = []

    def write_file_string_to_file(self) -> NoReturn:
        with self.solution_filepath.open("w") as file:
            file.writelines(s + "\n" for s in self.file_string)

    def add_number_of_trolleys(self, trolleys: List[Trolley]):
        self.file_string.append(f"//Nb tournees")
        self.file_string.append(f"{len(trolleys)}")

    def add_trolley_data(self, trolley: Trolley) -> NoReturn:
        self.file_string.append(f"//idTournee nbColis")
        self.file_string.append(f"{trolley.id} {len(trolley.boxes)}")
        self.file_string.append(f"//IdColis IdCommandeInColis NbProducts IdProd1 QtyProd1 IdProd2 QtyProd2 ...")
        for box in trolley.boxes:
            nb_products = len(box.product_quantity_pairs)
            tmp_string = ""
            tmp_string += f"{box.id} {box.order.order_id} {nb_products} "
            for pq in box.product_quantity_pairs:
                tmp_string += f"{pq.product.product_id} {pq.quantity} "
            self.file_string.append(tmp_string)

    def run(self) -> NoReturn:
        self.add_number_of_trolleys(self.trolleys)

        for trolley in self.trolleys:
            self.add_trolley_data(trolley)

        self.write_file_string_to_file()
