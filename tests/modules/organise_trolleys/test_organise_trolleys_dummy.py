import unittest

from src.modules.organise_trolleys.dummy import DummyOrganiseTrolleysModule


class MyTestCase(unittest.TestCase):
    def test_something(self):
        instance_data = IMAGINE THE INSTANCE DATA HERE
        boxes = IMAGINE THE BOXES HERE
        dummy_organise_trolleys_module = DummyOrganiseTrolleysModule()
        trolleys = dummy_organise_trolleys_module.run()
        for box in boxes:
            self.assertIn(box, trolleys[0].boxes)

if __name__ == '__main__':
    unittest.main()
