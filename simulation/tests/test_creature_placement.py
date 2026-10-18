from simulation.model.terrain import Terrain
from simulation.model.world_object import WorldObject
from simulation.model.species import Species
from simulation.model.creature import Creature
from simulation.model.world import World


grass = Terrain("Grass", ".", 100, 2)

eldian = Species(
    "Eldian",
    "eldia",
    100,
    5,
    80
)

creature = Creature(eldian)

world = World(5, 4, grass)

world.place_creature(creature, 2, 1)

cell = world.get_cell(2, 1)

assert cell.creature is creature

assert creature.x == 2
assert creature.y == 1

assert cell.is_occupied() is True

try:
    world.place_creature(creature, 3, 2)

    raise AssertionError(
        "Expected ValueError when placing creature twice"
    )

except ValueError:
    pass

assert creature.x == 2
assert creature.y == 1

assert world.get_cell(2, 1).creature is creature
assert world.get_cell(3, 2).creature is None


wall = WorldObject("Wall", "#", 200)

wall_cell = world.get_cell(4, 3)
wall_cell.place_object(wall)

creature2 = Creature(eldian)

try:
    world.place_creature(creature2, 4, 3)

    raise AssertionError(
        "Expected ValueError when placing creature on an object"
    )

except ValueError:
    pass

assert creature2.x is None
assert creature2.y is None
assert world.get_cell(4, 3).world_object is wall
assert world.get_cell(4, 3).creature is None

removed = world.remove_creature(2, 1)

assert removed is creature

assert world.get_cell(2, 1).creature is None

assert creature.x is None
assert creature.y is None

assert world.get_cell(2, 1).is_occupied() is False

print("Primera prueba de placement")