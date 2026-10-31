from .perceptions import PerceptionContext
from .nearby_perceptions import _distance


NONE = -1
GROUND = 0
OBJECT = 1
ALLY = 2
ENEMY = 3

def see(context: PerceptionContext, x: int, y: int) -> int:

    observer = context.creature

    distance = _distance(observer.x, observer.y, x, y)

    # 1. Primero se comprueba la visión
    if distance > observer.species.vision:
        return NONE

    # 2. Dentro de vision, pero fuera del mapa:
    # el borde se comporta como un objeto
    if not context.world.is_inside(x, y):
        return OBJECT

    cell = context.world.get_cell(x, y)

    # 3. Si hay criatura, tiene prioridad
    if cell.creature is not None:

        if cell.creature.species.faction == observer.species.faction:
            return ALLY

        return ENEMY

    # 4. Si hay objeto.
    if cell.world_object is not None:
        return OBJECT

    # 5. Si no hay nada sobre el terreno
    return GROUND

def name(context: PerceptionContext, x: int, y: int) -> str:

    observer = context.creature

    distance = _distance(observer.x, observer.y, x, y)

    # Fuera del radio de vision.
    if distance > observer.species.vision:
        return ""

    # Fuera del mapa.
    if not context.world.is_inside(x, y):
        return ""

    cell = context.world.get_cell(x, y)

    if cell.creature is not None:
        return cell.creature.species.name

    if cell.world_object is not None:
        return cell.world_object.name

    return cell.terrain.name