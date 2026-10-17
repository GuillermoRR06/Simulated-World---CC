from dataclasses import dataclass
from typing import List

# Tipo Raiz
@dataclass
class AstNode:
    line: int = field(default=0, kw_only=True, compare=False, repr=False)

# Tipo que representa Expresiones
@dataclass
class Expression(AstNode):
    pass

# Tipo que representa Instrucciones
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

# Nodo Raiz que describe un Programa
@dataclass
class Program(AstNode):
    head: Header
    body: list[Statement]
    labels: dict[str, int] = field(default_factory=dict, compare=False, repr=False)

# Nodos que describen las instrucciones
@dataclass
class Label(Statement):
    name : str

@dataclass
class Assign(Statement):
    name : str
    value : Expression

@dataclass
class Goto(Statement):
    target : str

@dataclass
class IfGoto(Statement):
    condition : Expression
    target : str

@dataclass
class ActionCall(Statement):
    name : str
    args : List[Expression]

# Nodos que describen las expresiones
@dataclass
class Number(Expression):
    value : int

@dataclass
class String(Expression):
    value : str

@dataclass
class Id(Expression):
    name : str

@dataclass
class FunctionCall(Expression):
    name : str
    args : List[Expression]

# Nodos que describen los operadores
@dataclass
class BiOper(Expression):
    left : Expression
    operator : str
    right : Expression

@dataclass
class UniOper(Expression):
    operator : str
    operand : Expression

#Printear los nodos
def FormatAst(node, indent: int = 0) -> str:
    pad = "  " * indent
    if not isinstance(node, AstNode):
        return f"{pad}{node!r}"
 
    out = [f"{pad}{type(node).__name__} (linea {node.line})"]
    for f in fields(node):
        if f.name == "line":
            continue
        value = getattr(node, f.name)
        if isinstance(value, list):
            if not value:
                out.append(f"{pad}  {f.name}: []")
            else:
                out.append(f"{pad}  {f.name}:")
                out.extend(FormatAst(item, indent + 2) for item in value)
        elif isinstance(value, AstNode):
            out.append(f"{pad}  {f.name}:")
            out.append(FormatAst(value, indent + 2))
        else:
            out.append(f"{pad}  {f.name}: {value!r}")
    return "\n".join(out)

def DumpAst(node, indent: int = 0) -> None:
    print(FormatAst(node, indent))