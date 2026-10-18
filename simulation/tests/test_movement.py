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

world = World(5, 4, grass)

creature = Creature(eldian)

world.place_creature(creature, 1, 1)

world.move_creature(creature, 2, 1)

assert creature.x == 2
assert creature.y == 1

assert world.get_cell(1, 1).creature is None
assert world.get_cell(2, 1).creature is creature

wall = WorldObject(
    "Wall",
    "#",
    200
)

wall_cell = world.get_cell(3, 1)
wall_cell.place_object(wall)

try:
    world.move_creature(creature, 3, 1)

    raise AssertionError(
        "Expected ValueError when moving into an occupied cell"
    )

except ValueError:
    pass

assert creature.x == 2
assert creature.y == 1

assert world.get_cell(2, 1).creature is creature

try:
    world.move_creature(creature, -1, 1)

    raise AssertionError(
        "Expected IndexError when moving outside the world"
    )

except IndexError:
    pass

assert creature.x == 2
assert creature.y == 1

print("Movement tests passed")