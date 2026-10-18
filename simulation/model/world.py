from .terrain import Terrain
from .cell import Cell
from .creature import Creature

class World:
    def __init__(self, width: int, height: int, default_terrain: Terrain):
        if width <= 0 or height <= 0:
            raise ValueError("World dimensions must be positive")

        self.width = width
        self.height = height

        self.grid = []

        for y in range(height):
            row = []

            for x in range(width):
                terrain = default_terrain.new_instance()
                cell = Cell(terrain)
                row.append(cell)

            self.grid.append(row)

    def is_inside(self, x: int, y: int) -> bool:
        return (
            0 <= x < self.width
            and
            0 <= y < self.height
        )

    def get_cell(self, x: int, y: int) -> Cell:
        if not self.is_inside(x, y):
            raise IndexError("Coordinates outside the world")

        return self.grid[y][x]

    def place_creature(self, creature: Creature, x: int, y: int):
        if not self.is_inside(x, y):
            raise IndexError("Coordinates outside the world")

        if creature.x is not None or creature.y is not None:
            raise ValueError("Creature is already placed in the world")

        cell = self.get_cell(x, y)

        cell.place_creature(creature)

        creature.x = x
        creature.y = y

    def remove_creature(self, x: int, y: int) -> Creature | None:
        cell = self.get_cell(x, y)

        creature = cell.remove_creature()

        if creature is not None:
            creature.x = None
            creature.y = None

        return creature

    def move_creature(
        self,
        creature: Creature,
        new_x: int,
        new_y: int
    ):
        if not self.can_move_to(creature, new_x, new_y):
            raise ValueError("Creature cannot move to that cell")

        old_cell = self.get_cell(
            creature.x,
            creature.y
        )

        destination_cell = self.get_cell(
            new_x,
            new_y
        )

        old_cell.remove_creature()
        destination_cell.place_creature(creature)

        creature.x = new_x
        creature.y = new_y

    def can_move_to(
        self,
        creature: Creature,
        new_x: int,
        new_y: int
    ) -> bool:
        if creature.x is None or creature.y is None:
            return False

        if not self.is_inside(new_x, new_y):
            return False

        delta_x = abs(new_x - creature.x)
        delta_y = abs(new_y - creature.y)

        if delta_x > 1 or delta_y > 1:
            return False

        destination_cell = self.get_cell(new_x, new_y)

        if destination_cell.is_occupied():
            return False

        return True