from typing import NoReturn

from src.modules.check_trolleys_are_valid.base import BaseCheckTrolleysAreValidModule


class CheckTrolleyModuleException(Exception):
    pass


class CheckTrolleysModule(BaseCheckTrolleysAreValidModule):
    def check_trolley_contain_all_boxes(self):
        box_set = set(self.boxes)

        trolley_boxes_set = set()
        for trolley in self.trolleys:
            for box in trolley.boxes:
                if box not in box_set:
                    raise CheckTrolleyModuleException(f"Box {box} should'nt be in any trolley")
                trolley_boxes_set.add(box)

        for box in box_set:
            if box not in trolley_boxes_set:
                raise CheckTrolleyModuleException(f"Box {box} should be in a trolley")

    def check_trolley_has_maximum_of_6_boxes(self):
        for trolley in self.trolleys:
            if len(trolley.boxes) > 6:
                raise CheckTrolleyModuleException(f"Trolley {trolley} contains more than 6 boxes")

    def check_box_duplicates_in_trolleys(self):
        box_set = set()
        for trolley in self.trolleys:
            for box in trolley.boxes:
                if box in box_set:
                    raise CheckTrolleyModuleException(f"Box {box} is duplicated in the trolleys")
                box_set.add(box)

    def run(self) -> NoReturn:
        # Check that the trolleys contain all boxes
        self.check_trolley_contain_all_boxes()
        # Check that a trolley has a maximum of 6 boxes
        self.check_trolley_has_maximum_of_6_boxes()
        # Check that there are no box duplicates in the trolleys
        self.check_box_duplicates_in_trolleys()
