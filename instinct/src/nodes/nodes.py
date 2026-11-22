from dataclasses import dataclass
from typing import List
from abc import ABC, abstractmethod
from ..errors.errors import RuntimeError

# Tipo Raiz
@dataclass
class AstNode(ABC):
    line: int

    @abstractmethod
    def format(self, indent=0):
        pass

# Tipo que representa Expresiones
@dataclass
class Expression(AstNode):
    
    @abstractmethod
    def evaluate(self, context):
        pass

# Tipo que representa una Linea
@dataclass
class Statement(AstNode):
   pass

# Cabecera del Programa
@dataclass
class Header(AstNode):
    creature : str
    faction : str
    health : int
    vision : int
    lifespan: int

    def format(self, indent=0):
        return f"-----Cabecera-----\ncreature : {self.creature}\nfaction : {self.faction}\nhealth : {self.health}\nvision : {self.vision}\nlifespan : {self.lifespan}\n------------------"

# Nodo Raiz que describe un Programa
@dataclass
class Program(AstNode):
    head: Header
    body: list[Statement]
    labels: dict[str : int]
    variables : list[str]

    def format(self, indent=0):
        lines = "\n".join(statement.format(0) for statement in self.body)
        return f"{self.head.format()}\n-----Cuerpo-----\n{lines}\n{self.labels}\n----------------"
            

# Nodos que describen las instrucciones
# Sintaxis: <name>:
@dataclass
class Label(Statement):
    name : str

    def format(self, indent=0):
        return f"{" "*indent}Etiqueta: {self.name}"

# Sintaxis: <name> = <expression>
@dataclass
class Assign(Statement):
    name : str
    value : Expression

    def format(self, indent=0):
        return f"{" "*indent}Asignarle a {self.name}:\n{" "*indent}{self.value.format(indent+2)}"

# Sintaxis: goto <name>
@dataclass
class Goto(Statement):
    target : str

    def format(self, indent=0):
        return f"{" "*indent}Goto:\n{" "*indent}Apunta a: {self.target}"

# Sintaxis: if <expression> goto <name>
@dataclass
class IfGoto(Statement):
    condition : Expression
    target : str

    def format(self, indent=0):
        return f"{" "*indent}If-Goto:\n{" "*indent}Condicion:\n{self.condition.format(indent+2)}\n{" "*indent}Apunta a: {self.target}"

# Sintaxis: <name>(<arg_1>, ... <arg_n>)
@dataclass
class ActionCall(Statement):
    name : str
    args : List[Expression]
    
    def format(self, indent=0):
        args = "".join(f"\n{arg.format(indent + 2)}" for arg in self.args)
        return f"{" "*indent}Accion {self.name}:{args}"

# Nodos que describen las expresiones
# Numero
@dataclass
class Number(Expression):
    value : int

    def evaluate(self, context):
        return self.value

    def format(self, indent=0):
        return f"{" "*indent}Numero: {self.value}"

# Texto
@dataclass
class String(Expression):
    value : str

    def evaluate(self, context):
        return self.value

    def format(self, indent=0):
        return f"{" "*indent}Texto: {self.value}"

# Variable
@dataclass
class Id(Expression):
    name : str

    def evaluate(self, context):
        return context.read_name(self.name)

    def format(self, indent=0):
        return f"{" "*indent}Id: {self.name}"

# Llamada a Funcion
@dataclass
class FunctionCall(Expression):
    name : str
    args : List[Expression]

    def evaluate(self, context):
        args = [arg.evaluate(context) for arg in self.args]
        return context.call_function(self.name, args)

    def format(self, indent=0):
        args = "".join(f"\n{arg.format(indent + 2)}" for arg in self.args)
        return f"{" "*indent}Funcion {self.name}:{args}"

# Nodos que describen los operadores
# Operador Binario Aritmetico
@dataclass
class BiOper_Arithmetic(Expression):
    left : Expression
    operator : str
    right : Expression

    def evaluate(self, context):
        if isinstance(self.left.value, str) or isinstance(self.right.value, str):
            raise RuntimeError(f"El operador aritmetico {self.operator} intento operar con texto", self.line)
        # Caso: +
        if self.operator == '+':
            return self.left.value + self.right.value
        # Caso: -
        elif self.operator == '-':
            return self.left.value - self.right.value
        # Caso: *
        elif self.operator == '*':
            return self.left.value * self.right.value
        
        if self.right.evaluate() == 0:
            raise RuntimeError("Se intento dividir por cero", self.line)
        # Caso: /
        elif self.operator == '/':
            return self.left.value // self.right.value
        # Caso: %
        return self.left.value % self.right.value

    def format(self, indent=0):
        return f"{" "*indent}Operador Binario ({self.operator}):\n{" "*indent}{self.left.format(indent+2)}\n{" "*indent}{self.right.format(indent+2)}"

# Operador Binario Comparador
@dataclass
class BiOper_Comparator(Expression):
    left : Expression
    operator : str
    right : Expression

    def evaluate(self, context):
        if type(self.left.value) != type(self.right.value):
            raise RuntimeError(f"El operador de comparacion {self.operator} intento comparar un texto y un numero", self.line)
        
        # Caso: ==
        elif self.operator == '==':
            if self.left.value == self.right.value:
                return 1
            return 0
        
        # Caso: !=
        elif self.operator == '!=':
            if self.left.value != self.right.value:
                return 1
            return 0
        
        if isinstance(self.left.value, str) or isinstance(self.right.value, str):
            raise RuntimeError(f"El operador de comparacion {self.operator} intento comparar un texto", self.line)
        # Caso: >=
        elif self.operator == '>=':
            if self.left.value >= self.right.value:
                return 1
            return 0
        
        # Caso: <=
        elif self.operator == '<=':
            if self.left.value <= self.right.value:
                return 1
            return 0

        # Caso: >
        elif self.operator == '>':
            if self.left.value > self.right.value:
                return 1
            return 0
        
        # Caso: <
        if self.left.value < self.right.value:
            return 1
        return 0

    def format(self, indent=0):
        return f"{" "*indent}Operador Binario ({self.operator}):\n{" "*indent}{self.left.format(indent+2)}\n{" "*indent}{self.right.format(indent+2)}"

# Operador Binario Logico
@dataclass
class BiOper_Logic(Expression):
    left : Expression
    operator : str
    right : Expression

    def evaluate(self, context):
        # Caso: and
        if self.operator == 'and':
            if self.left.value in [0, ""] or self.right.value in [0, ""]:
                return 0
            return 1
        
        # Caso: or
        if self.left.value in [0, ""] and self.right.value in [0, ""]:
            return 0
        return 1

    def format(self, indent=0):
        return f"{" "*indent}Operador Binario ({self.operator}):\n{" "*indent}{self.left.format(indent+2)}\n{" "*indent}{self.right.format(indent+2)}"

# Operador Unario (menos, not)
@dataclass
class UniOper(Expression):
    operator : str
    operand : Expression

    def evaluate(self, context):
        # Caso: -
        if self.operator == '-':
            if isinstance(self.operand.value, str):
                raise RuntimeError(f"El operador {self.operator} intento operar con un texto", self.line)
            return -self.operand.value
        
        # Caso : not
        if self.operand.value in [0, ""]:
            return 1
        return 0
    
    def format(self, indent=0):
        return f"{" "*indent}Operador Unario ({self.operator}):\n{" "*indent}{self.operand.format(indent+2)}"

#Printear los nodos
def DumpAst(node, indent: int = 0) -> None:
    print(node.format())
    
    