import re
from dataclasses import dataclass
from enum import Enum
from typing import Any

class TokenType(enum):
    
    #Literales
    NUMBER = (r'-?\d+', False)
    STRING = (r'"([^"\n]*)"', False)
    ID = (r'[a-zA-z_]\w*', False)
    
    #Operadores de Comparacion
    EQUAL = (r'==', False)
    NOT_EQUAL = (r'!=', False)
    GREATER = (r'>', False)
    LESS = (r'<', False)
    GREATER_EQUAL = (r'>=', False)
    LESS_EQUAL = (r'<=', False)
    
    #Operadores Aritmeticos
    ASSIGN = (r'=', False)
    PLUS = (r'\+', False)
    MINUS = (r'-', False)
    MULTIPLY = (r'\*', False)
    DIVIDE = (r'/', False)
    REMINDER = (r'%', False)
    
    #Operadores Logicos
    NOT = (r'\bnot\b', True)
    AND = (r'\band\b', True)
    OR = (r'\bor\b', True)
    
    #Delimitadores
    LEFT_PAREN = (r'\(', False)
    RIGHT_PAREN = (r'\)', False)
    COMMA = (r',', False)
    COLON = (r':', False)
    NEWLINE = (r'\n+', False)
    SPACE = (r'[ \t]+', False)
    EOF = (r'$', False)
    MISMATCH = (r'.', False)
    
    #Estructuras de Flujo
    IF = (r'\bif\b', True)
    GO_TO = (r'\bgoto\b', True)
    
    #Comentario
    COMMENT = (r'#[^\n]*', False)
    
    def __init__(self, pattern: str, is_keyword: bool):
        self.pattern = pattern
        self.is_keyword = is_keyword
        self._compiled_regex = re.compile(f"{pattern}")
    
    @classmethod
    def keywords(cls) -> dict[str, 'TokenType']:
        if not hasattr(cls, "kw_map"):
            cls._kw_map = {member.name.lower(): x for x in cls if x.is_keyword}
        return cls._kw_map
    
    @classmethod
    def get_token_spec(cls) -> list[tuple[str, str]]:
        return [(token.name, token.pattern) for token in cls]

@dataclass
class Token:
    typ: TokenType
    val: Any
    line: int
    col: int
    
    def __repr__(self):
        return f"Token {self.typ.name}, {self.val!r} at {self.line}:{self.col}"