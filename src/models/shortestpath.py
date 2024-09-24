class ShortestPath:
    """
    Represent the shortest path between two nodes in a graph.
    """
    start_localisation_id: int
    end_localisation_id: int
    distance: int

    def __init__(self, start_localisation_id: int, end_localisation_id: int, distance: int):
        self.start_localisation_id = start_localisation_id
        self.end_localisation_id = end_localisation_id
        self.distance = distance
