from simulation.loaders.resource_catalog import (
    ResourceCatalog
)

from simulation.model.terrain import Terrain
from simulation.model.world_object import WorldObject


catalog = ResourceCatalog()


grass = Terrain(
    "Grass",
    ".",
    100,
    2
)

water = Terrain(
    "Water",
    "~",
    100,
    1
)

rock = WorldObject(
    "Rock",
    "#",
    100
)


catalog.add_terrain(
    grass
)

catalog.add_terrain(
    water
)

catalog.add_object(
    rock
)


assert (
    catalog.get_terrain_by_char(".")
    is grass
)

assert (
    catalog.get_terrain_by_char("~")
    is water
)

assert (
    catalog.get_object_by_char("#")
    is rock
)

assert (
    catalog.get_terrain_by_char("X")
    is None
)

assert (
    catalog.first_terrain
    is grass
)


duplicate = WorldObject(
    "BadRock",
    ".",
    50
)


try:

    catalog.add_object(
        duplicate
    )

    assert False

except ValueError:

    pass

print(
    "Resource catalog tests passed"
)

