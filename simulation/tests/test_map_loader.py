from simulation.loaders.terrain_loader import (
    TerrainLoader
)

from simulation.loaders.object_loader import (
    ObjectLoader
)

from simulation.loaders.resource_catalog import (
    ResourceCatalog
)

from simulation.loaders.map_loader import (
    MapLoader
)


catalog = ResourceCatalog()


terrain_loader = TerrainLoader()

grass = terrain_loader.load(
    "terrains/grass.te"
)

catalog.add_terrain(
    grass
)


object_loader = ObjectLoader()

rock = object_loader.load(
    "objects/rock.ob"
)

catalog.add_object(
    rock
)


map_loader = MapLoader(
    catalog
)


map_definition = map_loader.load(
    "maps/plain_with_rocks.map"
)


assert map_definition.name == (
    "Plain with rocks"
)

assert map_definition.width == 10

assert map_definition.height == 5

assert map_definition.rows[1] == (
    "...##....."
)


print(
    "Map loader tests passed"
)