from ..interpreter.evaluator import EvaltuationContext
from ..interpreter.executor import ExecutorStatements
from .environment import RuntimeEnvironment
from .state import RuntimeState
from ..semantic.catalog import Catalog

from enum import Enum, auto

# Permite establecer como termino el turno de una criatura
class TurnEnd(Enum):
    ACTION = auto() # Se ejecuto una accion que consume turno
    WAITING = auto() # La criatura esta bajo el efecto de wait(n)
    END_FILE = auto() # Se llego al final del registro
    LIMIT = auto() # Se alcanzo el limite de 100 instrucciones sin accion. Equivale a wait(1)

# Ejecuta un turno de una criatura
class RuntimeEngine:
    
    MAX_INSTRUCTIONS = 100
    
    def __init__(self, catalog: Catalog): # Mismo catalogo con el que se compilo el programa
        self.catalog = catalog
        self.executor = ExecutorStatements(catalog)
    
    def execute_turn(self, state: RuntimeState, env: RuntimeEnvironment) -> TurnEnd:
        # Comprueba si la criatura esta bajo el efecto de wait(n)
        if state.sleep_turns > 0:
            state.sleep_turns -= 1
            return TurnEnd.WAITING
        
        context = EvaltuationContext(state, env, self.catalog)
        body = state.program.body
        
        for _ in range(self.MAX_INSTRUCTIONS):
            statement = body[state.counter]
            state.counter += 1
            ends_turn = self.executor.execute_statement(statement, context)
            
            if state.counter > len(body):
                state.GotoJump("start")
                return TurnEnd.ACTION if ends_turn else TurnEnd.END_FILE
            
            if ends_turn:
                return TurnEnd.ACTION
            
        return TurnEnd.LIMIT