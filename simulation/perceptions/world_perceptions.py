from .perceptions import Perception, PerceptionContext

def _other_living_creatures(context: PerceptionContext):
    return [
        other
        for other in context.world.get_creatures()
        if (
            other is not context.creature
            and other.is_alive()
        )
    ]

class WidthPerception(Perception):

    def read(self, context: PerceptionContext):
        return context.world.width


class HeightPerception(Perception):

    def read(self,context: PerceptionContext):
        return context.world.height

class TickPerception(Perception):

    def read(self, context: PerceptionContext):
        return context.tick

class TotalCreaturesPerception(Perception):

    def read(self, context: PerceptionContext):
        creatures = _other_living_creatures(context)

        return len(creatures)

class TotalAlliesPerception(Perception):

    def read(self, context: PerceptionContext):
        creatures = _other_living_creatures(context)

        faction = (context.creature.species.faction)

        return sum(
            1
            for other in creatures
            if other.species.faction == faction
        )

class TotalEnemiesPerception(Perception):

    def read(self, context: PerceptionContext):
        creatures = _other_living_creatures(context)

        faction = (context.creature.species.faction)

        return sum(
            1
            for other in creatures
            if other.species.faction != faction
        )

class RandomPerception(Perception):

    def read(self, context: PerceptionContext):
        return context.rng.randint(0,99)