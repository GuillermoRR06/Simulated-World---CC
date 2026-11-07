from ..nodes.nodes import (Program, Label, Assign, IfGoto, Goto, ActionCall,
    BiOper_Arithmetic, BiOper_Comparator, BiOper_Logic, UniOper, Number, String, Id, FunctionCall)
from .catalog import Catalog, default_catalog
from ..errors.errors import SemanticError

#Clase que define el analizador semantico
class SemanticAnalyzer:
    def __init__(self, catalog=None):
        self.catalog = default_catalog() if catalog is None else catalog
        
        self.VISIT_METHODS = {
            Label : self.visit_Label,
            Assign : self.visit_Assign,
            IfGoto : self.visit_IfGoto,
            Goto : self.visit_Goto,
            ActionCall : self.visit_ActionCall,
            BiOper_Arithmetic : self.visit_BiOper,
            BiOper_Comparator : self.visit_BiOper,
            BiOper_Logic : self.visit_BiOper,
            UniOper : self.visit_UniOper,
            Number : self.visit_Number,
            String : self.visit_String,
            Id : self.visit_Id,
            FunctionCall : self.visit_FunctionCall
        }
        
        self.reset()
    
    def reset(self):
        self.errors : list[tuple[int, str]] = [] # Errores
        self.labels : dict[str : int] = {} # { Nombre : Linea }
        self.gotos : list[tuple[str, int]] = [] # [Destino, Linea]
        self.assigned : set[str] = set() # Variables
        self.uses : list[tuple[str, int]] = [] # [Nombre, Linea]
    
    # Metodo Principal: Analiza la semantica del archivo .ins
    def analyze(self, program):
        self.reset()
        
        # Forma el contexto. Revisa todas las etiquetas existentes
        for node in program.body:
            if isinstance(node, Label):
                self.VISIT_METHODS[Label](node)
        
        # Visita el resto de nodos y verifica su correctitud semantica
        for statement in program.body:
            if not isinstance(node, Label):
                self.VISIT_METHODS[type(node)](node)
        
        # Reporta errores si los hay
        if self.errors:
            raise SemanticError(sorted(self.errors, key=lambda e: (e[0] == 0, e[0])))
        
        # Agrega las etiquetas
        program.labels = {name: idx for name, idx in self.labels.items()}

    # Visitar Label: comprueba si es una etiqueta nueva (la agrega) o ya existente (reporta error)
    def visit_Label(self, node):
        if node.name in self.labels:
            first = self.labels[node.name][1]
            self.errors.append((node.line, f"Etiqueta duplicada '{node.name}', ya definida en linea {first}"))
        else:
            self.labels[node.name] = (node.line)

    # Metodo auxiliar para analizar llamados de funciones o acciones
    def check_call(self, node, kind: str, arity: int | None, other_kind: str, other_arity: int | None):
        if arity is None:
            error = ""
            if other_arity is not None: error = f"Es una {other_kind}, no una {kind}."
            self.errors.append((node.line, f"{kind.upper()} desconocida: {node.name} {error}"))
        elif len(node.args) != arity:
            self.errors.append((node.line, f"La {kind} {node.name} espera {arity} argumento(s), pero ha recibido {len(node.args)}"))
        for a in node.args:
            self.VISIT_METHODS[type(a)](a)

    # Visitar asignaciones. Si es una constante/percepcion reporta error
    def visit_Assign(self, node):
        self.VISIT_METHODS[type(node.value)](node.value)
        kind = self.catalog.read_only_kind(node.name)
        if kind:
            self.errors.append((node.line, f"No se puede asignar a '{node.name}', es una {kind}"))
        else:
            self.assigned.add(node.name)

    # Visitar goto. Si la etiqueta objetivo no existe, reporta error
    def visit_Goto(self, node):
        if node.target not in self.labels:
            self.errors.append((node.line, f"'goto' a una etiqueta que no existe: '{node.target}'"))
    
    # Visitar if-goto
    def visit_IfGoto(self, node):
        self.VISIT_METHODS[type(node.condition)](node.condition)
        self.visit_Goto(node)
    
    # Visitar llamada a una accion
    def visit_ActionCall(self, node):
        self.check_call(node, "accion", self.catalog.action_arity(node.name), "funcion", self.catalog.function_arity(node.name))
    
    # Visitar un numero
    def visit_Number(self, node):
        pass
    
    # Visitar un texto
    def visit_String(self, node):
        pass
    
    # Visitar un identificador
    def visit_Id(self, node):
        self.uses.append((node.name, node.line))

    # Visitar llamada a una funcion
    def visit_FunctionCall(self, node):
        self.check_call(node, "funcion", self.catalog.function_arity(node.name), "accion", self.catalog.action_arity(node.name))

    # Visitar operadores binarios
    def visit_BiOper(self, node):
        self.VISIT_METHODS[type(node.left)](node.left)
        self.VISIT_METHODS[type(node.right)](node.right)

    # Visitar operadores unarios
    def visit_UniOper(self, node):
        self.VISIT_METHODS[type(node.operand)](node.operand)