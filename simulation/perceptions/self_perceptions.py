from .perceptions import Perception, PerceptionContext


class HealthPerception(Perception):

    def read(self, context: PerceptionContext):
        return context.creature.health


class AgePerception(Perception):

    def read(self, context: PerceptionContext):
        return context.creature.age


class LifespanPerception(Perception):

    def read(self, context: PerceptionContext):
        return context.creature.species.lifespan


class VisionPerception(Perception):

    def read(self, context: PerceptionContext):
        return context.creature.species.vision


class SpeciesPerception(Perception):

    def read(self, context: PerceptionContext):
        return context.creature.species.name


class FactionPerception(Perception):

    def read(self, context: PerceptionContext):
        return context.creature.species.faction


class XPerception(Perception):

    def read(self, context: PerceptionContext):
        return context.creature.x


class YPerception(Perception):

    def read(self, context: PerceptionContext):
        return context.creature.y

class TerrainHerePerception(Perception):

    def read(self, context: PerceptionContext):
        creature = context.creature

        cell = context.world.get_cell(creature.x, creature.y)

        return cell.terrain.name

class ReserveHerePerception(Perception):

    def read(self, context: PerceptionContext):
        creature = context.creature

        cell = context.world.get_cell(creature.x, creature.y)

        return cell.terrain.resource