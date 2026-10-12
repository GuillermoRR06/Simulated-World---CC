from re import I
from nodes.nodes import (Program, Label, Assign, If_Goto, Goto, Action,
    Bi_Operator, Uni_Operator, Number, String, Id
)

class SemanticError(Exception):
    pass

class SemanticAnalyzer:
    def __init__(self):
        self.declared_vars = set()
        self.declared_labels = set()
    
    def Analyze(self, program: Program):
        self.declared_vars.clear()
        self.declared_labels.clear()
        
        if program.head: self.declared_vars.update({'creature', 'faction', 'health', 'vision', 'lifespan'})
        
        for s in program.body:
            if isinstance(s, Label):
                if s.name in self.declared_labels:
                    raise SemanticError(f"Etiqueta Duplicada: '{s.name}'.")
                self.declared_labels.add(s.name)
        
        for s in program.body:
            self.VisitStatemnet(s)
    
    #Analizar instrucciones
    def VisitStatemnet(self, statment):
        if isinstance(statment, Label): pass
        
        elif isinstance(statment, Assign):
            self.VisitExpression(statment.value)
            self.declared_vars.add(statment.name)
            
        elif isinstance(statment, Goto):
            if statement.target not in self.declared_labels:
                raise SemanticError(f"Error en goto: Etiqueta de Destino '{statment.target}' NO declarada.")
            
        elif isinstance(statment, If_Goto):
            self.VisitExpression(statment.condition)
            if statement.target not in self.declared_labels:
                raise SemanticError(f"Error en if...goto: Etiqueta de Destino '{statment.target}' NO declarada.")
            
        elif isinstance(statment, Action):
            for a in statment.args:
                self.VisitExpression(a)
                
        else:
            raise SemanticError(f"Instruccion NO reconocida: '{type(statment).__name__}'.")
    
    #Analizar expresiones
    def VisitExpression(self, exp):
        if isinstance(exp, (Number, String)): return
        
        elif isinstance(exp, Id):
            if exp.name not in self.declared_vars:
                raise SemanticError(f"Variable NO definida: '{exp.name}'.")
            
        elif isinstance(exp, Bi_Operator):
            self.VisitExpression(exp.left)
            self.VisitExpression(exp.right)
            
        else:
            raise SemanticError(f"Expresion NO reconocida: '{type(exp).__name__}'.")