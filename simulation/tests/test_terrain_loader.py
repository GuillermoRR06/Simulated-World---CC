from simulation.loaders.terrain_loader import TerrainLoader


loader = TerrainLoader()

terrain = loader.load(
    "terrains/grass.te"
)


assert terrain.name == "Grass"
assert terrain.char == "."
assert terrain.resource_max == 100
assert terrain.regen == 2
assert terrain.resource == 100


print(
    "Terrain loader tests passed"
)