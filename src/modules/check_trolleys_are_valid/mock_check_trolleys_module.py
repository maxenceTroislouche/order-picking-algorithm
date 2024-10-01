from src.modules.check_trolleys_are_valid.base import BaseCheckTrolleysAreValidModule


class MockCheckTrolleysModule(BaseCheckTrolleysAreValidModule):
    """
    Fake checker that never raises an exception
    """

    def run(self):
        pass
