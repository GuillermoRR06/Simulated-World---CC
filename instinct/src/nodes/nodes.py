from dataclasses import dataclass
from typing import List, Optional

# Tipo Base para Polimorfismo
@dataclass
class AstNode:
    pass

# Cabecera del Programa
@dataclass
class Header(AstNode):
    creature : str
    faction : str
    health : int
    vision : int
    lifespan: int

# Nodo Raiz que describe un Programa
@dataclass
class Program(AstNode):
    head : Header
    body : List[AstNode]

# Nodos que describen las instrucciones
@dataclass
class Label(AstNode):
    name : str

@dataclass
class Assign(AstNode):
    name : str
    value : AstNode

@dataclass
class Goto(AstNode):
    target : str

@dataclass
class If_Goto(AstNode):
    condition : AstNode
    target : str

@dataclass
class Action(AstNode):
    name : str
    args : List[AstNode]

# Nodos que describen las expresiones
@dataclass
class Number(AstNode):
    value : int

@dataclass
class String(AstNode):
    value : int

@dataclass
class Id(AstNode):
    name : str

@dataclass
class Function_Call(AstNode):
    name : str
    args : List[AstNode]

# Nodos que describen los operadores
@dataclass
class Bi_Operator(AstNode):
    left : AstNode
    operator : str
    right : AstNode

@dataclass
class Uni_Operator(AstNode):
    operator : str
    operand : AstNode

#Printear los nodos
def DumpAst(node, indent=0):
    pad = " " * indent 
    if hasattr(node, "__dataclass_fields__"):
        print(f"{pad}{node.__class__.__name__}:")
        for i in node.__dataclass_fields__:
            value = getattr(node, field)
            if isinstance(value, list):
                print(f"{pad} {i}: [")
                for j in value:
                    DumpAst(item, indent+2)
                print(f"{pad} ]")
            elif hasattr(value, "__dataclass_fields__"):
                print(f"{pad} {i}:")
                DumpAst(item, indent+2)
            else:
                print(f"{pad} {i}: {value}")
    else:
        print(f"{pad}{node}")