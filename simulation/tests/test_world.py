from simulation.model.terrain import Terrain
from simulation.model.world import World


grass = Terrain("Grass", ".", 100, 2)

world = World(3, 2, grass)


assert world.width == 3
assert world.height == 2


assert world.is_inside(0, 0) is True
assert world.is_inside(2, 1) is True

assert world.is_inside(-1, 0) is False
assert world.is_inside(0, -1) is False
assert world.is_inside(3, 0) is False
assert world.is_inside(0, 2) is False


cell = world.get_cell(1, 0)

assert cell.terrain.name == "Grass"
assert cell.terrain.resource == 100


cell1 = world.get_cell(0, 0)
cell2 = world.get_cell(1, 0)

cell1.terrain.resource = 25

assert cell1.terrain.resource == 25
assert cell2.terrain.resource == 100

assert cell1.terrain is not cell2.terrain


try:
    world.get_cell(-1, 0)

    raise AssertionError(
        "Expected IndexError for coordinates outside the world"
    )

except IndexError:
    pass


print("World tests passed")