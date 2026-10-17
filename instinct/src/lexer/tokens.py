import re
from dataclasses import dataclass
from enum import Enum
from functools import cache
from typing import Any

class TokenType(Enum):
    
    #Literales
    NUMBER = (r'\d+', False)
    STRING = (r'"[^"\n]*"', False)
    ID = (r'[A-Aa-z_]\w*', False)
    
    #Operadores de Comparacion
    EQUAL = (r'==', False)
    NOT_EQUAL = (r'!=', False)
    GREATER_EQUAL = (r'>=', False)
    LESS_EQUAL = (r'<=', False)
    GREATER = (r'>', False)
    LESS = (r'<', False)
    
    #Operadores Aritmeticos
    ASSIGN = (r'=', False)
    PLUS = (r'\+', False)
    MINUS = (r'-', False)
    MULTIPLY = (r'\*', False)
    DIVIDE = (r'/', False)
    REMAINDER = (r'%', False)
    
    #Delimitadores
    LEFT_PAREN = (r'\(', False)
    RIGHT_PAREN = (r'\)', False)
    COMMA = (r',', False)
    COLON = (r':', False)
    
    #Estructuras de Flujo
    IF = ('if', True)
    GO_TO = ('goto', True)

    #Operadores Logicos
    AND = ('and', True)
    OR = ('or', True)
    NOT = ('not', True)
    
    #Ignorables/Especiales
    COMMENT = (r'#[^\n]*', False)
    NEWLINE = (r'\n+', False)
    SPACE = (r'[ \t\r]+', False)
    EOF = ('', False)
    MISMATCH = (r'.', False)
    
    def __init__(self, pattern: str, is_keyword: bool):
        self.pattern = pattern
        self.is_keyword = is_keyword
        self._compiled_regex = re.compile(f"{pattern}")
    
    @classmethod
    @cache
    def Keywords(cls) -> dict[str, 'TokenType']:
        return {t.pattern: t for t in cls if t.is_keyword}
    
    @classmethod
    def Get_TokenSpec(cls) -> list[tuple[str, str]]:
        return [(t.name, t.pattern) for t in cls if not t.is_keyword and t is not cls.EOF]

@dataclass
class Token:
    typ: TokenType
    val: Any
    line: int
    col: int
    
    def __repr__(self):
        return f"Token {self.typ.name}, {self.val!r} at {self.line}:{self.col}"