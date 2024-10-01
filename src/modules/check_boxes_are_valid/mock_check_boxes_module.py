from src.modules.check_boxes_are_valid.base import BaseCheckBoxesAreValidModule


class MockCheckBoxesModule(BaseCheckBoxesAreValidModule):
    """
    Fake checker that never raises an exception
    """

    def run(self):
        pass
