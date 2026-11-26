from simulation.actions.action_catalog import ActionCatalog
from simulation.model.terrain import Terrain
from simulation.model.world import World
from simulation.model.species import Species
from simulation.model.creature import Creature


catalog = ActionCatalog()

world = World(
    5, 1,
    Terrain("Grass", ".", 100, 2)
)

creature = Creature(
    Species("Eldian", "eldia", 100, 4, 200)
)

world.place_creature(creature, 0, 0)


# 1. Movimiento

assert catalog.execute(
    "move", world, creature, [1, 0, 1]
) == 1

assert (creature.x, creature.y) == (1, 0)


# 2. Ataque

catalog.execute(
    "attack", world, creature, [0, 0, 10]
)

cell = world.get_cell(1, 0)

assert cell.terrain.resource == 90


# 3. Funcion auxiliar para comprobar errores

def expect_error(name, args):

    try:
        catalog.execute(
            name, world, creature, args
        )

    except ValueError:
        pass

    else:
        raise AssertionError(
            f"Expected error in {name}"
        )


# 4. Validaciones

expect_error(
    "consume", [0, 0, 25, "incorrecto"]
)

assert cell.terrain.resource == 90
assert creature.health == 100

expect_error("move", [1, 0])
expect_error("move", [2, 0, 1])
expect_error("unknown", [])

assert (creature.x, creature.y) == (1, 0)


# 5. Consumo con cantidades negativas

catalog.execute(
    "consume", world, creature, [0, 0, -5, 5]
)

assert cell.terrain.resource == 95
assert creature.health == 105


# 6. Reproduccion

child = catalog.execute(
    "reproduce", world, creature, [1, 0, 20]
)

assert child.health == 20
assert creature.health == 85

assert world.get_cell(2, 0).creature is child


# 7. Movimiento bloqueado

assert catalog.execute(
    "move", world, creature, [1, 0, 2]
) == 0

assert catalog.consumes_turn("move") is True


# 8. Espera

catalog.execute(
    "wait", world, creature, [3]
)

assert creature.wait_turns_remaining == 2

assert catalog.consumes_turn("wait") is True


# 9. Say

assert catalog.execute(
    "say", world, creature, [42]
) == "42"

assert catalog.consumes_turn("say") is False


# 10. Roar

roar = catalog.execute(
    "roar", world, creature, ["Tatakae!"]
)

assert roar.value == "Tatakae!"

assert catalog.consumes_turn("roar") is True


print("Action catalog tests passed")