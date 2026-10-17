from simulation.model.world_object import WorldObject

wall = WorldObject("Wall", "#", 200)

assert wall.name == "Wall"
assert wall.char == "#"
assert wall.resource_max == 200
assert wall.resource == 200

print("WorldObject tests passed")