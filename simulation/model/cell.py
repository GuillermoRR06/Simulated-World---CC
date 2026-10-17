from .terrain import Terrain
from .world_object import WorldObject

class Cell:
    def __init__(self, terrain: Terrain):
        if terrain is None:
            raise ValueError("A cell must have terrain")

        self.terrain = terrain
        self.world_object: WorldObject | None = None
        self.creature = None

    def is_occupied(self) -> bool:
        return self.world_object is not None or self.creature is not None

    def place_object(self, world_object: WorldObject):
        if self.is_occupied():
            raise ValueError("The cell is already occupied")

        self.world_object = world_object

    def remove_object(self):
        world_object = self.world_object  #Para guardar el objeto que acabamos de quitar
        self.world_object = None
        return world_object