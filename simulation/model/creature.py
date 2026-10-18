from .species import Species


class Creature:
    def __init__(self, species: Species):
        if species is None:
            raise ValueError("A creature must have a species")

        self.species = species

        self.health = species.initial_health
        self.age = 0

        self.x: int | None = None
        self.y: int | None = None

    def take_damage(self, amount: int):
        if amount < 0:
            raise ValueError("Damage cannot be negative")

        self.health = max(0, self.health - amount)

    def heal(self, amount: int):
        if amount < 0:
            raise ValueError("Healing cannot be negative")

        self.health += amount

    def is_alive(self) -> bool:
        return self.health > 0
