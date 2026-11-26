from simulation.loaders.terrain_loader import TerrainLoader
from simulation.loaders.object_loader import ObjectLoader
from simulation.loaders.resource_catalog import ResourceCatalog
from simulation.loaders.map_loader import MapLoader
from simulation.loaders.map_factory import MapFactory


catalog = ResourceCatalog()

grass = TerrainLoader().load("terrains/grass.te")
rock = ObjectLoader().load("objects/rock.ob")

catalog.add_terrain(grass)
catalog.add_object(rock)


map_loader = MapLoader(catalog)

map_definition = map_loader.load(
    "maps/plain_with_rocks.map"
)


factory = MapFactory(catalog)

world = factory.create_world(map_definition)


# Test 1: dimensiones

assert world.width == 10
assert world.height == 5


# Test 2: terreno normal

cell = world.get_cell(0, 0)

assert cell.terrain.name == "Grass"
assert cell.world_object is None


# Test 3: celda con objeto

cell = world.get_cell(3, 1)

assert cell.terrain.name == "Grass"
assert cell.world_object.name == "Rock"


# Test 4: independencia de terrenos

terrain1 = world.get_cell(0, 0).terrain
terrain2 = world.get_cell(1, 0).terrain

assert terrain1 is not terrain2

terrain1.resource = 30

assert terrain2.resource == 100
assert grass.resource == 100


# Test 5: independencia de objetos

rock1 = world.get_cell(3, 1).world_object
rock2 = world.get_cell(4, 1).world_object

assert rock1 is not rock2

rock1.resource = 20

assert rock2.resource == 100
assert rock.resource == 100


# Test 6: reconstruir el mundo

new_world = factory.create_world(map_definition)

assert new_world is not world

assert new_world.get_cell(0, 0).terrain.resource == 100

assert new_world.get_cell(3, 1).world_object.resource == 100


print("Map factory tests passed")