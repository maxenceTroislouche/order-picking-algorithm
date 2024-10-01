from src.models.trolley import Trolley
from src.modules.organise_trolleys.base import BaseOrganiseTrolleysModule


class DummyOrganiseTrolleysModule(BaseOrganiseTrolleysModule):
    """
    Dummy module to organise Trolleys
    """

    def run(self) -> list[Trolley]:
        trolleys = [Trolley([])]
        current_trolley = 0

        for box in self.boxes:
            # If the current trolley is full, add a new one as the current trolley
            if len(trolleys[current_trolley].boxes) == self.instance_data.number_of_boxes_in_one_trolley:
                trolleys.append(Trolley([]))
                current_trolley += 1

            trolleys[current_trolley].boxes.append(box)
