from nodes.nodes import (Program, Label, Assign, IfGoto, Goto, ActionCall,
    BiOper, UniOper, Number, String, Id, FunctionCall)
from .catalog import Catalog, default_catalog

#Excepcion de Error Semantico
class SemanticError(Exception):
    def __init__(self, errors):
        self.errors = list(errors)
        super().__init__("\n".join(f"linea {line}: {msg}" if line else msg for line, msg in self.errors))

#Clase que define el analizador semantico
class SemanticAnalyzer:
    def __init__(self):
        self.catalog = default_catalog()
        self.Reset()
    
    def Reset(self):
        self.errors : list[tuple[int, str]] = []
        self.warnings: list[tuple[int, str]] = []
        self.labels : dict[str, [tuple[int, int]]] = {} # { Nombre : [Indice, Linea] }
        self.gotos : list[tuple[str, int]] = [] # [Destino, Linea]
        self.assigned : set[str] = set()
        self.uses : list[tuple[str, int]] = [] # [Nombre, Linea]
        self.index = 0
    
    # Metodo Principal: Analiza la semantica del archivo .ins
    def Analyze(self, program):
        self.Reset()
        
        for index, statement in enumerate(program.body):
            self.index = index
            self.Visit(statement)
        
        self.Resolve()
        
        if self.errors:
            raise SemanticError(sorted(self.errors, key=lambda e: (e[0] == 0, e[0])))
        
        program.labels = {name: idx for name, (idx, _) in self.labels.items()}
    
    # Metodo para llamar a las funciones de visista de cada nodo respectivamente
    def Visit(self, node):
        name = type(node).__name__
        method = getattr(self, f"Visit_{name}", None)
        return method(node)
    
    # Metodo para analizar llamados de funciones o acciones
    def CheckCall(self, node, kind: str, arity: int | None, other_kind: str, other_arity: int | None):
        if arity is None:
            error = ""
            if other_arity is not None: error = f"es una {other_kind}, no una {kind}."
            self.errors.append((node.line, f"{kind.upper()} desconocida: {node.name} {error}"))
        elif len(node.args) != arity:
            self.errors.append((node.line, f"La {kind} {node.name} espera {arity} argumento(s), pero ha recibido {len(node.args)}"))
        for a in node.args:
            self.Visit(a)

    # Metodos para visitar los distintos tipos de nodos AST
    def Visit_Label(self, node):
        if node.name in self.labels:
            first = self.labels[node.name][1]
            self.errors.append((node.line, f"Etiqueta duplicada '{node.name}': ya definida en linea {first}"))
        else:
            self.labels[node.name] = (self.index, node.line)
    
    def Visit_Assign(self, node):
        self.Visit(node.value)
        kind = self.catalog.read_only_kind(node.name)
        if kind:
            self.errors.append((node.line, f"No se puede asignar a '{node.name}': es una {kind}"))
        else:
            self.assigned.add(node.name)
    
    def Visit_Goto(self, node):
        self.gotos.append((node.target, node.line))
    
    def Visit_IfGoto(self, node):
        self.Visit(node.condition)
        self.Visit_Goto(node)
    
    def Visit_ActionCall(self, node):
        self.CheckCall(node, "accion", self.catalog.action_arity(node.name), "function", self.catalog.function_arity(node.name))
    
    def Visit_Number(self, node):
        pass
    
    def Visit_String(self, node):
        pass
    
    def Visit_Id(self, node):
        self.uses.append((node.name, node.line))

    def Visit_FunctionCall(self, node):
        self.CheckCall(node, "function", self.catalog.function_arity(node.name), "accion", self.catalog.action_arity(node.name))

    def Visit_BiOper(self, node):
        self.Visit(node.left)
        self.Visit(node.right)

    def Visit_UniOper(self, node):
        self.Visit(node.operand)
    
    # Metodo para comprobar la correctitud semantica que depende de analizar todo el documento
    def Resolve(self):
        # Comprobar goto
        for target, line in self.gotos:
            if target not in self.labels:
                self.errors.append((line, f"'goto' a una etiqueta que no existe: '{target}'"))
        # Comprobar label 'start'
        if "start" not in self.labels:
            self.errors.append((0, f"Falta la etiqueta 'start'"))