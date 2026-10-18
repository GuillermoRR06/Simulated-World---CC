from ..model.creature import Creature
from ..model.world import World


class MoveAction:
    def execute(
        self,
        world: World,
        creature: Creature,
        dx: int,
        dy: int,
        speed: int
    ) -> int:

        self._validate_direction(dx, dy)

        moved_steps = 0

        for _ in range(max(0, speed)):
            next_x = creature.x + dx
            next_y = creature.y + dy

            if not world.can_move_to(
                creature,
                next_x,
                next_y
            ):
                break

            world.move_creature(
                creature,
                next_x,
                next_y
            )

            moved_steps += 1

        return moved_steps

    def _validate_direction(
        self,
        dx: int,
        dy: int
    ):
        valid_directions = {-1, 0, 1}

        if (
            dx not in valid_directions
            or dy not in valid_directions
        ):
            raise ValueError(
                "dx and dy must be -1, 0 or 1"
            )