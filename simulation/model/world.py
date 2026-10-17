from .terrain import Terrain
from .cell import Cell


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