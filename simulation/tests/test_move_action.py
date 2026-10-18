from simulation.actions.move_action import MoveAction
from simulation.model.creature import Creature
from simulation.model.species import Species
from simulation.model.terrain import Terrain
from simulation.model.world import World
from simulation.model.world_object import WorldObject


grass = Terrain(
    "Grass",
    ".",
    100,
    2
)

species = Species(
    "TestCreature",
    "test",
    100,
    5,
    80
)

world = World(
    7,
    1,
    grass
)

creature = Creature(species)

world.place_creature(
    creature,
    0,
    0
)

wall = WorldObject(
    "Wall",
    "#",
    200
)

world.get_cell(
    3,
    0
).place_object(wall)


move_action = MoveAction()


moved_steps = move_action.execute(
    world,
    creature,
    dx=1,
    dy=0,
    speed=5
)


assert moved_steps == 2

assert creature.x == 2
assert creature.y == 0

assert world.get_cell(
    0,
    0
).creature is None

assert world.get_cell(
    1,
    0
).creature is None

assert world.get_cell(
    2,
    0
).creature is creature

assert world.get_cell(
    3,
    0
).world_object is wall


print("MoveAction tests passed")