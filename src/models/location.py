class Location:
    """
    Represents a location in the warehouse
    """
    location_id: int
    x: int
    y: int
    name: str

    def __init__(self, location_id: int, x: int, y: int, name: str):
        self.location_id = location_id
        self.x = x
        self.y = y
        self.name = name
