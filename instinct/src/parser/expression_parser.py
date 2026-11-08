from ..lexer.tokens import TokenType, Token
from ..nodes.nodes import (Expression, Number, String, Id, FunctionCall, BiOper_Arithmetic, BiOper_Comparator, BiOper_Logic, UniOper)
from .cursor_line import CursorLine, Describe

class ExpressionParser:
    
    BINARY_OPERS = {
        "or" : BiOper_Logic,
        "and": BiOper_Logic,
        "==" : BiOper_Comparator,
        "!=": BiOper_Comparator,
        ">=" : BiOper_Comparator,
        "<=" : BiOper_Comparator,
        ">" : BiOper_Comparator,
        "<" : BiOper_Comparator,
        "+" : BiOper_Arithmetic,
        "-" : BiOper_Arithmetic,
        "*" : BiOper_Arithmetic,
        "/" : BiOper_Arithmetic,
        "%" : BiOper_Arithmetic
    }
    
    LEVELS = [
        ("or",), # Level 0
        ("and",), # Level 1
        ("==", "!=", ">=", "<=", ">", "<"), # Level 2
        ("+", "-"), # Level 3
        ("*", "/", "%") # Level 4
    ]
    
    def __init__(self, cursor: CursorLine):
        self.cursor = cursor
    
    # Parsea los argumentos de una funcion/accion
    def parse_arguments(self):
        args : list[Expression] = []
        if self.cursor.match(TokenType.RIGHT_PAREN):
            return args
        args.append(self.parse_binary())
        while self.cursor.match(TokenType.COMMA):
            args.append(self.parse_binary())
        self.cursor.expect(TokenType.RIGHT_PAREN, "')' o ','")
        return args
    
    # Parsea las operaciones binarias
    def parse_binary(self, level=0):
        if level == len(self.LEVELS):
            return self.parse_atom()
        
        left = self.parse_binary(level+1)
        
        while True:
            token = self.cursor.peek()
            if token is None or token.typ in (TokenType.NUMBER, TokenType.STRING) or token.val not in self.LEVELS[level]:
                return left
            self.cursor.advance()
            right = self.parse_binary(level+1)
            left = self.BINARY_OPERS[token.val](token.line, operator=token.val, left=left, right=right)

    # Parsea un atomo (numero, texto, id que puede ser variable o llamada a funcion, operador unario, expresion entre parentesis)
    def parse_atom(self):
        token : Token = self.cursor.peek()
        if token is None:
            self.cursor.fail(f"Se esperaba una expresion pero se encontro {Describe(token)}.")
        # Token Numero
        if token.typ is TokenType.NUMBER:
            self.cursor.advance()
            return Number(token.line, token.val)
        # Token Texto
        elif token.typ is TokenType.STRING:
            self.cursor.advance()
            return String(token.line, token.val)
        # Token ID (puede ser variable o funcion)
        elif token.typ is TokenType.ID:
            self.cursor.advance()
            if self.cursor.match(TokenType.LEFT_PAREN):
                return FunctionCall(token.line, token.val, self.parse_arguments())
            return Id(token.line, token.val)
        # Token Operador Unario (-, not)
        elif token.typ in (TokenType.MINUS, TokenType.NOT):
            self.cursor.advance()
            return UniOper(token.line, token.val, self.parse_atom())
        # Token "("
        elif token.typ is TokenType.LEFT_PAREN:
            self.cursor.advance()
            express = self.parse_level0()
            self.cursor.expect(TokenType.RIGHT_PAREN, "')'")
            return express
        self.cursor.fail(f"Se esperaba una expresion pero se encontro {Describe(token)}.")