import json


class RoomsGenerator:
    """
    Convert the list of rooms in usable formats
    """

    def __init__(self):
        with open('data/rooms.json', 'r') as fh:
            self.rooms = json.load(fh)
    
    @property
    def rooms_as_list(self):
        rooms = []
        for building, rooms_per_building in self.rooms.items():
            for room in rooms_per_building:
                rooms.append(
                    (building, room)
                )
        return rooms
    
    @property
    def total(self):
        return len(self.rooms_as_list)
