from dataclasses import dataclass
from typing import List
from abc import ABC, abstractmethod

# Tipo Raiz
@dataclass
class AstNode:
    line: int

# Tipo que representa Expresiones
@dataclass
class Expression(AstNode, ABC):
    
    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def format(self, indent):
        pass

# Tipo que representa una Linea
@dataclass
class Statement(AstNode, ABC):
    
    @abstractmethod
    def format(self, evaluate):
        pass

# Cabecera del Programa
@dataclass
class Header(AstNode):
    creature : str
    faction : str
    health : int
    vision : int
    lifespan: int

    def format(self):
        return f"-----Cabecera-----\ncreature : {self.creature}\nfaction : {self.faction}\nhealth : {self.health}\nvision : {self.vision}\nlifespan : {self.lifespan}\n------------------"

# Nodo Raiz que describe un Programa
@dataclass
class Program(AstNode):
    head: Header
    body: list[Statement]
    labels: dict[str : int]
    variables : list[str]

    def format(self):
        tokens = ""
        for t in self.body:
            tokens+=f"{t.format(0)}\n"
        return f"{self.head.format()}\n-----Cuerpo-----\n{tokens}\n{self.labels}\n----------------"
            

# Nodos que describen las instrucciones
# Sintaxis: <name>:
@dataclass
class Label(Statement):
    name : str

    def format(self, indent):
        return f"{" "*indent}Label: {self.name}"    

# Sintaxis: <name> = <expression>
@dataclass
class Assign(Statement):
    name : str
    value : Expression

    def format(self, indent):
        return f"{" "*indent}Asignarle a {self.name}:\n{" "*indent}{self.value.format(indent+2)}"

# Sintaxis: goto <name>
@dataclass
class Goto(Statement):
    target : str

    def format(self, indent):
        return f"{" "*indent}Goto:\n{" "*indent}Apunta a: {self.target}"

# Sintaxis: if <expression> goto <name>
@dataclass
class IfGoto(Statement):
    condition : Expression
    target : str

    def format(self, indent):
        return f"{" "*indent}If-Goto:\n{" "*indent}Condicion:\n{" "*indent}{self.condition.format(indent+2)}\n{" "*indent}Apunta a: {self.target}"

# Sintaxis: <name>(<arg_1>, ... <arg_n>)
@dataclass
class ActionCall(Statement):
    name : str
    args : List[Expression]
    
    def format(self, indent):
        args = ""
        for t in self.args:
            args += f"{" "*indent}{t.format(indent+2)}\n"
        return f"{" "*indent}FunctionCall {self.name}:\n{args}"

# Nodos que describen las expresiones
# Numero
@dataclass
class Number(Expression):
    value : int

    def evaluate(self):
        return self.value

    def format(self, indent):
        return f"{" "*indent}Number: {self.value}"

# Texto
@dataclass
class String(Expression):
    value : str

    def evaluate(self):
        return self.value

    def format(self, indent):
        return f"{" "*indent}String: {self.value}"

# Variable
@dataclass
class Id(Expression):
    name : str

    def evaluate(self):
        pass

    def format(self, indent):
        return f"{" "*indent}Id: {self.name}"

# Llamada a Funcion
@dataclass
class FunctionCall(Expression):
    name : str
    args : List[Expression]

    def evaluate(self):
        pass

    def format(self, indent):
        args = ""
        for t in self.args:
            args += f"{" "*indent}{t.format(indent+2)}\n"
        return f"{" "*indent}FunctionCall {self.name}:\n{args}"

# Nodos que describen los operadores
# Operador Binario Aritmetico
@dataclass
class BiOper_Arithmetic(Expression):
    left : Expression
    operator : str
    right : Expression

    def evaluate(self):
        # Caso: +
        if self.operator == '+':
            if isinstance(self.left.value, str) or isinstance(self.right.value, str):
                raise Exception("Error en Tiempo de Ejecucion")
            return self.left.value + self.right.value
        
        # Caso: -
        elif self.operator == '-':
            if isinstance(self.left.value, str) or isinstance(self.right.value, str):
                raise Exception("Error en Tiempo de Ejecucion")
            return self.left.value - self.right.value
        
        # Caso: *
        elif self.operator == '*':
            if isinstance(self.left.value, str) or isinstance(self.right.value, str):
                raise Exception("Error en Tiempo de Ejecucion")
            return self.left.value * self.right.value
        
        # Caso: /
        elif self.operator == '/':
            if isinstance(self.left.value, str) or isinstance(self.right.value, str):
                raise Exception("Error en Tiempo de Ejecucion")
            return self.left.value // self.right.value
        
        # Caso: %
        if isinstance(self.left.value, str) or isinstance(self.right.value, str):
            raise Exception("Error en Tiempo de Ejecucion")
        return self.left.value % self.right.value

    def format(self, indent):
        return f"{" "*indent}Operador Binario ({self.operator}):\n{" "*indent}{self.left.format(indent+2)}\n{" "*indent}{self.right.format(indent+2)}"

# Operador Binario Comparador
@dataclass
class BiOper_Comparator(Expression):
    left : Expression
    operator : str
    right : Expression

    def evaluate(self):
        # Caso: ==
        if self.operator == '==':
            if self.left.value == self.right.value:
                return 1
            return 0
        
        # Caso: !=
        elif self.operator == '!=':
            if self.left.value != self.right.value:
                return 1
            return 0
        
        # Caso: >=
        elif self.operator == '>=':
            if isinstance(self.left.value, str) or isinstance(self.right.value, str):
                raise Exception("Error en Tiempo de Ejecucion")
            if self.left.value >= self.right.value:
                return 1
            return 0
        
        # Caso: <=
        elif self.operator == '<=':
            if isinstance(self.left.value, str) or isinstance(self.right.value, str):
                raise Exception("Error en Tiempo de Ejecucion")
            if self.left.value <= self.right.value:
                return 1
            return 0

        # Caso: >
        elif self.operator == '>':
            if isinstance(self.left.value, str) or isinstance(self.right.value, str):
                raise Exception("Error en Tiempo de Ejecucion")
            if self.left.value > self.right.value:
                return 1
            return 0
        
        # Caso: <
        if isinstance(self.left.value, str) or isinstance(self.right.value, str):
            raise Exception("Error en Tiempo de Ejecucion")
        if self.left.value < self.right.value:
            return 1
        return 0

    def format(self, indent):
        return f"{" "*indent}Operador Binario ({self.operator}):\n{" "*indent}{self.left.format(indent+2)}\n{" "*indent}{self.right.format(indent+2)}"

# Operador Binario Logico
@dataclass
class BiOper_Logic(Expression):
    left : Expression
    operator : str
    right : Expression

    def evaluate(self):
        # Caso: and
        if self.operator == 'and':
            if self.left.value in [0, ""] or self.right.value in [0, ""]:
                return 0
            return 1
        
        # Caso: or
        if self.left.value in [0, ""] and self.right.value in [0, ""]:
            return 0
        return 1

    def format(self, indent):
        return f"{" "*indent}Operador Binario ({self.operator}):\n{" "*indent}{self.left.format(indent+2)}\n{" "*indent}{self.right.format(indent+2)}"

# Operador Unario (menos, not)
@dataclass
class UniOper(Expression):
    operator : str
    operand : Expression

    def evaluate(self):
        # Caso: -
        if self.operator == '-':
            if isinstance(self.operand.value, str): raise Exception("Error en Tiempo de Ejecucion")
            return -self.operand.value
        
        # Caso : not
        if self.operand.value in [0, ""]:
            return 1
        return 0
    
    def format(self, indent):
        return f"{" "*indent}Operador Unario ({self.operator}):\n{" "*indent}{self.operand.format(indent+2)}"

#Printear los nodos
def DumpAst(node, indent: int = 0) -> None:
    print(node.format())
    
    