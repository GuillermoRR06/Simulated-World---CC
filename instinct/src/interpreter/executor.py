from ..errors.errors import RuntimeError
from .evaluator import EvaltuationContext
from ..nodes.nodes import Statement, Label, Assign, Goto, IfGoto, ActionCall
from ..semantic.catalog import Catalog

# Ejecuta las instrucciones y determina si consumen turno (True) o no (False)
class ExecutorStatements:
    
    def __init__(self, catalog: Catalog):
        self.catalog = catalog
        
        self.statements = {
            Label : self.execute_Label,
            Assign : self.execute_Assign,
            Goto : self.execute_Goto,
            IfGoto : self.execute_IfGoto,
            ActionCall : self.execute_ActionCall
        }
    
    # Ejecuta una instruccion. Si detecta un error en tiempo de ejecucion, acaba el turno (esto puede modificarse en el futuro)
    def execute_statement(self, statement: Statement, context: EvaltuationContext) -> bool:
        handler = self.statements.get(type(statement))
        try:
            return handler(statement, context)
        except RuntimeError as error:
            if error.line is None:
                error.line = statement.line
        return True
    
    # Lo detecto... y ya
    def execute_Label(self, statement, context):
        return False

    # Guarda la variable en el contexto
    def execute_Assign(self, statement, context):
        context.state.variables[statement.name] = statement.value.evaluate(context)
        return False

    # Ejecuta el salto
    def execute_Goto(self, statement, context):
        context.state.GotoJump(statement.target)
        return False
    
    # Evalua la condicion. Si es verdadera ejecuta el salto
    def execute_IfGoto(self, statement, context):
        if statement.condition.evaluate(context) == 1:
            context.state.GotoJump(statement.target)
        return False

    # Ejecuta la accion, teniendo en cuenta si es del tipo que consume turno o no
    def execute_ActionCall(self, statement, context):
        name = statement.name
        args = [arg.evaluate(context) for arg in statement.args]
        
        # Analiza si la accion es del tipo que no consume turno
        if not self.catalog.consumes_turn(name):
            context.env.execute_action(name, args)
            return False
        
        # En caso de que lo anterior no se cumpla, ejecuta la accion y consume el turno
        turns = self.catalog.turns_taken(name, args)
        context.env.execute_action(name, args)
        context.state.sleep_turns = turns - 1
        return True
        