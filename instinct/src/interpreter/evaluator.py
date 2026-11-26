from ..errors.errors import InstinctRuntimeError
from ..semantic.catalog import Catalog
from ..runtime.state import RuntimeState
from ..runtime.environment import RuntimeEnvironment

# Contexto para evaluar las expresiones (algunos tipos no lo necesitan, pero otros como Id y FunctionCall si)
class EvaltuationContext:
    
    def __init__(self, state: RuntimeState, env: RuntimeEnvironment, catalog: Catalog):
        self.state = state
        self.env = env
        self.catalog = catalog
    
    def read_name(self, name: str) -> int | str:
        if name in self.state.variables:
            return self.state.variables[name]
        
        if self.catalog.is_constant(name):
            return self.catalog.constant_value(name)
        
        if self.catalog.is_perception(name):
            return self.env.read_perception(name)
        
        raise InstinctRuntimeError(f"'{name}' no es una variable, ni una constante, ni una percepcion", self.line)
    
    def call_function(self, name: str, args):
        return self.env.call_function(name, args)