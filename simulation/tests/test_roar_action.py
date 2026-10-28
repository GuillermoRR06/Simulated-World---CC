from simulation.actions.roar_action import RoarAction
from simulation.model.creature import Creature
from simulation.model.species import Species
from simulation.model.terrain import Terrain
from simulation.model.world import World


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
    100
)

world = World(
    5,
    5,
    grass
)

creature = Creature(
    species
)

world.place_creature(
    creature,
    2,
    3
)

roar = RoarAction()


# -----------------------------
# Roar consume turno
# -----------------------------

assert roar.consumes_turn is True


# -----------------------------
# Emitir rugido
# -----------------------------

event = roar.execute(
    world,
    creature,
    "Tatakae!"
)

assert event.x == 2
assert event.y == 3
assert event.value == "Tatakae!"


# El rugido debe estar en el tick actual

assert len(
    world.current_roars
) == 1

assert world.current_roars[0] is event


# Todavía no pertenece al tick anterior

assert len(
    world.previous_roars
) == 0


# -----------------------------
# Cambiar de tick
# -----------------------------

world.rotate_roars()

assert len(
    world.current_roars
) == 0

assert len(
    world.previous_roars
) == 1

assert world.previous_roars[0] is event


# -----------------------------
# Roar también acepta números
# -----------------------------

number_event = roar.execute(
    world,
    creature,
    42
)

assert number_event.value == "42"

assert len(
    world.current_roars
) == 1


print("RoarAction tests passed")