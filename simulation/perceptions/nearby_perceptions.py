from .perceptions import (Perception, PerceptionContext)


def _distance(x1: int, y1: int, x2: int, y2: int) -> int:

    return max(abs(x2 - x1), abs(y2 - y1))


def _visible_creatures(context: PerceptionContext):
    observer = context.creature

    vision = observer.species.vision

    visible = []

    for other in context.world.get_creatures():

        if other is observer:
            continue

        distance = _distance(observer.x, observer.y, other.x, other.y)

        if distance <= vision:
            visible.append((other, other.x, other.y, distance))

    return visible

class AlliesNearPerception(Perception):

    def read(self, context: PerceptionContext):
        visible = _visible_creatures(context)

        faction = context.creature.species.faction

        return sum(
            1
            for other, _, _, _ in visible
            if other.species.faction == faction
        )

class EnemiesNearPerception(Perception):

    def read(self, context: PerceptionContext):
        visible = _visible_creatures(context)

        faction = (context.creature.species.faction)

        return sum(
            1
            for other, _, _, _ in visible
        if other.species.faction != faction
        )

def _visible_objects(context: PerceptionContext):
    observer = context.creature
    vision = observer.species.vision

    objects = []

    for y, row in enumerate(context.world.grid):
        for x, cell in enumerate(row):

            if cell.world_object is None:
                continue

            distance = _distance(observer.x, observer.y, x, y)

            if distance <= vision:
                objects.append((cell.world_object, x, y, distance))

    return objects

class ObjectsNearPerception(Perception):

    def read(self, context: PerceptionContext):
        return len(_visible_objects(context))

def _direction_component(difference: int) -> int:

    if difference > 0:
        return 1

    if difference < 0:
        return -1

    return 0

def _nearest_creature(context: PerceptionContext, same_faction: bool):
    faction = context.creature.species.faction

    candidates = []

    for other, x, y, distance in _visible_creatures(context):

        is_ally = (other.species.faction == faction)

        if is_ally == same_faction:
            candidates.append((other, x, y, distance))

    if not candidates:
        return None

    return min(candidates, key=lambda item: item[3])

def _creature_target_info(context: PerceptionContext, same_faction: bool):
    observer = context.creature

    nearest = _nearest_creature(context, same_faction)


    if nearest is None:
        return -1, 0, 0

    target, target_x, target_y, distance = nearest

    dx = _direction_component(target_x - observer.x)

    dy = _direction_component(target_y - observer.y)

    return distance, dx, dy


class EnemyDistPerception(Perception):

    def read(self, context: PerceptionContext):

        distance, dx, dy = _creature_target_info(context, False)

        return distance


class EnemyDxPerception(Perception):

    def read(self, context: PerceptionContext):
        distance, dx, dy = _creature_target_info(context, False)

        return dx


class EnemyDyPerception(Perception):

    def read(self, context: PerceptionContext):
        distance, dx, dy = _creature_target_info(context, False)

        return dy


class AllyDistPerception(Perception):

    def read(self, context: PerceptionContext):
        distance, dx, dy = _creature_target_info(context, True)

        return distance


class AllyDxPerception(Perception):

    def read(self, context: PerceptionContext):
        distance, dx, dy = _creature_target_info(context, True)

        return dx


class AllyDyPerception(Perception):

    def read(self, context: PerceptionContext):
        distance, dx, dy = _creature_target_info(context, True)

        return dy


def _nearest_object(context: PerceptionContext):
    visible_objects = _visible_objects(context)

    if not visible_objects:
        return None

    nearest = min(visible_objects, key=lambda item: item[3]) #Compara el cuarto elemento de cada elemento de la tupla y devuelve el minimo, cosas locas de Python

    return nearest

def _object_target_info(context: PerceptionContext):
    observer = context.creature

    nearest = _nearest_object(context)

    if nearest is None:
        return -1, 0, 0

    target, target_x, target_y, distance = nearest

    dx = _direction_component(target_x - observer.x)

    dy = _direction_component(target_y - observer.y)

    return distance, dx, dy

class ObjectDistPerception(Perception):

    def read(self, context: PerceptionContext):
        distance, dx, dy = _object_target_info(context)

        return distance


class ObjectDxPerception(Perception):

    def read(self, context: PerceptionContext):
        distance, dx, dy = _object_target_info(context)

        return dx


class ObjectDyPerception(Perception):

    def read(self, context: PerceptionContext):
        distance, dx, dy = _object_target_info(context)

        return dy

def _visible_roars(context: PerceptionContext):
    observer = context.creature
    vision = observer.species.vision

    visible = []

    for roar in context.world.previous_roars:

        distance = _distance(observer.x, observer.y, roar.x,roar.y)

        if distance <= vision:
            visible.append((roar, distance))

    return visible

class RoarsNearPerception(Perception):

    def read(self, context: PerceptionContext):
        return len(_visible_roars(context))

class LastRoarPerception(Perception):

    def read(self, context: PerceptionContext):
        visible = _visible_roars(context)

        if not visible:
            return ""

        last_roar, distance = visible[-1]

        return last_roar.value