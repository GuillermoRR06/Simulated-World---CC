from simulation.model.terrain import Terrain
from simulation.model.world_object import WorldObject
from simulation.model.cell import Cell


grass = Terrain("Grass", ".", 100, 2)
wall = WorldObject("Wall", "#", 200)
tree = WorldObject("Tree", "T", 100)

cell = Cell(grass)

assert cell.terrain is grass
assert cell.world_object is None
assert cell.creature is None
assert cell.is_occupied() is False

cell.place_object(wall)

assert cell.world_object is wall
assert cell.is_occupied() is True


# Intentamos poner otro objeto en una celda ocupada
try:
    cell.place_object(tree)

    # Si llegamos aquí, significa que NO se produjo el error esperado
    raise AssertionError("Expected ValueError when placing object in occupied cell")

except ValueError:
    print("Correcto: no se puede poner un segundo objeto en una celda ocupada")

# La pared debe seguir siendo el objeto de la celda
assert cell.world_object is wall


removed = cell.remove_object()

assert removed is wall
assert cell.world_object is None
assert cell.is_occupied() is False

print("Cell tests passed")