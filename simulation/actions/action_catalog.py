from .action import Action
from .move_action import MoveAction
from .attack_action import AttackAction
from .consume_action import ConsumeAction
from .reproduce_action import ReproduceAction
from .wait_action import WaitAction
from .roar_action import RoarAction
from .say_action import SayAction

from ..model.world import World
from ..model.creature import Creature


class ActionCatalog:

    def __init__(self):

        self._actions = {}

        self.register(
            "move", MoveAction(), (int, int, int)
        )

        self.register(
            "attack", AttackAction(), (int, int, int)
        )

        self.register(
            "consume", ConsumeAction(),
            (int, int, int, int)
        )

        self.register(
            "reproduce", ReproduceAction(),
            (int, int, int)
        )

        self.register(
            "wait", WaitAction(), (int,) # Tupla de un solo elemento
        )

        self.register(
            "roar", RoarAction(), ((int, str),) # Tupla de un elemento que puede recibir un str o un int
        )

        self.register(
            "say", SayAction(), ((int, str),)
        )


    def register(
        self,
        name: str,
        action: Action,
        parameter_types: tuple
    ):

        if name in self._actions:
            raise ValueError(
                f"Action already registered: {name}"
            )

        self._actions[name] = (
            action,
            parameter_types
        )


    def _get_entry(self, name: str):

        if name not in self._actions:
            raise ValueError(
                f"Unknown action: {name}"
            )

        return self._actions[name]


    def execute(
        self,
        name: str,
        world: World,
        creature: Creature,
        args: list[int | str]
    ):

        action, parameter_types = self._get_entry(name)

        if len(args) != len(parameter_types):

            raise ValueError(
                f"{name} expects {len(parameter_types)} arguments, "
                f"received {len(args)}"
            )

        for index, (value, expected) in enumerate(
            zip(args, parameter_types),
            start=1
        ):

            if isinstance(expected, tuple):
            
                allowed = expected
            
            else:
            
                allowed = (expected,)

            if type(value) not in allowed:

                names = " or ".join(
                    t.__name__ for t in allowed
                )

                raise ValueError(
                    f"{name}: argument {index} must be {names}"
                )

        return action.execute(
            world,
            creature,
            *args
        )


    def consumes_turn(self, name: str) -> bool:

        action, _ = self._get_entry(name)

        return action.consumes_turn