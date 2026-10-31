from .perceptions import PerceptionContext

from .self_perceptions import (
    HealthPerception,
    AgePerception,
    LifespanPerception,
    VisionPerception,
    SpeciesPerception,
    FactionPerception,
    XPerception,
    YPerception,
    TerrainHerePerception,
    ReserveHerePerception,
)

from .world_perceptions import (
    WidthPerception,
    HeightPerception,
    TickPerception,
    TotalCreaturesPerception,
    TotalAlliesPerception,
    TotalEnemiesPerception,
    RandomPerception,
)

from .nearby_perceptions import (
    AlliesNearPerception,
    EnemiesNearPerception,
    ObjectsNearPerception,

    EnemyDistPerception,
    EnemyDxPerception,
    EnemyDyPerception,

    AllyDistPerception,
    AllyDxPerception,
    AllyDyPerception,

    ObjectDistPerception,
    ObjectDxPerception,
    ObjectDyPerception,

    RoarsNearPerception,
    LastRoarPerception,
)

from .vision_functions import (
    see,
    name,
)


class PerceptionCatalog:

    def __init__(self):

        self._perceptions = {

            # Propias
            "health": HealthPerception(),
            "age": AgePerception(),
            "lifespan": LifespanPerception(),
            "vision": VisionPerception(),
            "species": SpeciesPerception(),
            "faction": FactionPerception(),
            "x": XPerception(),
            "y": YPerception(),
            "terrain_here": TerrainHerePerception(),
            "reserve_here": ReserveHerePerception(),

            # Mundo
            "width": WidthPerception(),
            "height": HeightPerception(),
            "tick": TickPerception(),
            "total_creatures": TotalCreaturesPerception(),
            "total_allies": TotalAlliesPerception(),
            "total_enemies": TotalEnemiesPerception(),
            "random": RandomPerception(),

            # Cercanas
            "allies_near": AlliesNearPerception(),
            "enemies_near": EnemiesNearPerception(),
            "objects_near": ObjectsNearPerception(),

            "enemy_dist": EnemyDistPerception(),
            "enemy_dx": EnemyDxPerception(),
            "enemy_dy": EnemyDyPerception(),

            "ally_dist": AllyDistPerception(),
            "ally_dx": AllyDxPerception(),
            "ally_dy": AllyDyPerception(),

            "object_dist": ObjectDistPerception(),
            "object_dx": ObjectDxPerception(),
            "object_dy": ObjectDyPerception(),

            "roars_near": RoarsNearPerception(),
            "last_roar": LastRoarPerception(),
        }

        self._functions = {
            "see": see,
            "name": name,
        }

    def read(self, perception_name: str, context: PerceptionContext):

        if perception_name not in self._perceptions:
            raise KeyError(
                f"Unknown perception: {perception_name}"
            )

        perception = self._perceptions[perception_name]

        return perception.read(context)

    def call(self, function_name: str, context: PerceptionContext, *args):

        if function_name not in self._functions:
            raise KeyError(
                f"Unknown perception function: {function_name}"
            )

        function = self._functions[function_name]

        return function(context, *args)