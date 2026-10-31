from simulation.model.species import Species
from simulation.model.creature import Creature


eldian = Species(
    "Eldian",
    "eldia",
    100,
    5,
    80
)

creature = Creature(eldian)


assert creature.species is eldian
assert creature.health == 100
assert creature.age == 0

assert creature.x is None
assert creature.y is None

assert creature.is_alive() is True


creature.take_damage(30)

assert creature.health == 70
assert creature.is_alive() is True


creature.heal(20)

assert creature.health == 90


creature.heal(50)

assert creature.health == 140


creature.take_damage(500)

assert creature.health == 0
assert creature.is_alive() is False


print("Creature tests passed")
