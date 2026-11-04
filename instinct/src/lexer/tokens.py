from dataclasses import dataclass
from enum import Enum, auto
from typing import Any

class TokenType(Enum):
    
    #Literales
    NUMBER = auto()
    STRING = auto()
    ID = auto()
    
    #Operadores de Comparacion
    EQUAL = auto()
    NOT_EQUAL = auto()
    GREATER_EQUAL = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    LESS = auto()
    
    #Operadores Aritmeticos
    ASSIGN = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    REMAINDER = auto()
    
    #Delimitadores
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    COMMA = auto()
    COLON = auto()
    
    #Estructuras de Flujo
    IF = auto()
    GO_TO = auto()

    #Operadores Logicos
    AND = auto()
    OR = auto()
    NOT = auto()
    
    #Ignorables/Especiales
    NEWLINE = auto()
    EOF = auto()

KEYWORDS = {
    "if" : TokenType.IF,
    "goto" : TokenType.GO_TO,
    "and" : TokenType.AND,
    "or" : TokenType.OR,
    "not" : TokenType.NOT
}

TWO_CHAR_SYMBOLS = {
    "==" : TokenType.EQUAL,
    "!=" : TokenType.NOT_EQUAL,
    ">=" : TokenType.GREATER_EQUAL,
    "<=" : TokenType.LESS_EQUAL
}

ONE_CHAR_SYMBOLS = {
    ">" : TokenType.GREATER,
    "<" : TokenType.LESS,
    "=" : TokenType.ASSIGN,
    "+" : TokenType.PLUS,
    "-" : TokenType.MINUS,
    "*" : TokenType.MULTIPLY,
    "/" : TokenType.DIVIDE,
    "%" : TokenType.REMAINDER,
    "(" : TokenType.LEFT_PAREN,
    ")" : TokenType.RIGHT_PAREN,
    "," : TokenType.COMMA,
    ":" : TokenType.COLON
}

@dataclass
class Token:
    typ: TokenType
    val: Any
    line: int
    col: int
    
    def __repr__(self):
        return f"Token {self.typ.name}, linea: {self.line} | columna: {self.col} | valor: {self.val!r}"