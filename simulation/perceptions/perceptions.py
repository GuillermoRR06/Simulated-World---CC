from abc import ABC, abstractmethod
from dataclasses import dataclass
from random import Random

from ..model.world import World
from ..model.creature import Creature


@dataclass
class PerceptionContext:
    world: World
    creature: Creature
    tick: int
    rng: Random


class Perception(ABC):

    @abstractmethod
    def read(self,context: PerceptionContext):
        pass