from ..errors.errors import RuntimeError
from collections.abc import Callable

class Catalog:
    def __init__(self):
        self.actions: dict[str, int] = {}
        self.functions: dict[str, int] = {}
        self.perceptions: set[str] = set()
        self.constants: dict[str, int | str] = {}
        
        # Ejecucion de las acciones
        self.free_actions : set[str] = set() # No consumen turno
        self.durations : dict[str, Callable[[list], int]] = {} # Turnos ocupados (wait)

    # Seccion para registrar nuevas acciones/funciones/percepciones/constantes
    def Register_Action(self, name: str, arity: int, consumes_turn: bool = True, duration: Callable[[list], int] | None = None):
        if name in self.actions or name in self.functions:
            raise ValueError(f"Ya existe una accion o funcion llamada '{name}'")
        self.actions[name] = arity
        
        if not consumes_turn:
            self.free_actions.add(name)
        
        if duration is not None:
            self.durations[name] = duration

    def Register_Function(self, name: str, arity: int):
        if name in self.actions or name in self.functions:
            raise ValueError(f"Ya existe una accion o funcion llamada '{name}'")
        self.functions[name] = arity

    def Register_Perception(self, name: str):
        if name in self.perceptions or name in self.constants:
            raise ValueError(f"Ya existe una percepcion o constante llamada '{name}'")
        self.perceptions.add(name)

    def Register_Constant(self, name: str, value: int | str):
        if name in self.perceptions or name in self.constants:
            raise ValueError(f"Ya existe una percepcion o constante llamada '{name}'")
        self.constants[name] = value

    # Acceder a las acciones/funciones/percepciones/constantes
    def action_arity(self, name: str):
        return self.actions.get(name)

    def function_arity(self, name: str):
        return self.functions.get(name)

    def is_perception(self, name: str):
        return name in self.perceptions

    def is_constant(self, name: str):
        return name in self.constants

    def constant_value(self, name: str):
        return self.constants[name]

    def read_only_kind(self, name: str):
        if name in self.constants:
            return "constante"
        if name in self.perceptions:
            return "percepcion"
        return None
    
    # Consultar sobre las acciones
    def consumes_turn(self, name: str) -> bool:
        # Retorna True si consume un turno
        return name not in self.free_actions
    
    def turns_taken(self, name: str, args: list) -> int:
        # Retorna la cantidad de turnos que consume la accion (1 por defecto)
        duration = self.durations.get(name)
        return 1 if duration is None else duration(args)

# Acciones/Funciones/Percepciones/Constantes definidas en la base del lenguaje
BASE_ACTIONS = {
    "wait": 1, "move": 3, "attack": 3, "consume": 4,
    "reproduce": 3, "roar": 1, "say": 1,
}

BASE_FUNCTIONS = {"see": 2, "name": 2}

BASE_CONSTANTS = {"NONE": -1, "GROUND": 0, "OBJECT": 1, "ALLY": 2, "ENEMY": 3}

BASE_PERCEPTIONS = (
    "health", "age", "lifespan", "vision", "species", "faction",
    "x", "y", "terrain_here", "reserve_here",

    "width", "height", "tick",
    "total_creatures", "total_allies", "total_enemies", "random",

    "allies_near", "enemies_near", "objects_near",
    "enemy_dist", "enemy_dx", "enemy_dy",
    "ally_dist", "ally_dx", "ally_dy",
    "object_dist", "object_dx", "object_dy",
    "roars_near", "last_roar",
)

BASE_FREE_ACTIONS = {"say"}

# Retorna la cantidad de turnos n que ocupa wait(n)
def _wait_duration(args: list) -> int:
    n = args[0]
    if not isinstance(n, int):
        raise RuntimeError("'wait' solo recibe un parametro de tipo numero", None)
    return max(n, 1)

BASE_DURATIONS = {"wait": _wait_duration}

# Crea un catalogo por defecto
def default_catalog() -> Catalog:
    catalog = Catalog()
    for name, arity in BASE_ACTIONS.items():
        catalog.Register_Action(name, arity, consumes_turn=(name not in BASE_FREE_ACTIONS), duration=(BASE_DURATIONS.get(name)))
    for name, arity in BASE_FUNCTIONS.items():
        catalog.Register_Function(name, arity)
    for name, value in BASE_CONSTANTS.items():
        catalog.Register_Constant(name, value)
    for name in BASE_PERCEPTIONS:
        catalog.Register_Perception(name)
    return catalog