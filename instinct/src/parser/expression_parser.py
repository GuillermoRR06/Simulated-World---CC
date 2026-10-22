from lexer.tokens import TokenType
from nodes.nodes import (Expression, Number, String, Id, FunctionCall, BiOper, UniOper)
from .cursor_line import CursorLine, Describe

class ExpressionParser():
    
    BINARY_LEVELS = (
        (TokenType.OR),
        (TokenType.AND),
        (TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL),
        (TokenType.PLUS, TokenType.MINUS),
        (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.REMAINDER)
    )
    
    def __init__(self):
        self.primaries = {
            TokenType.NUMBER : self.ParseNumber,
            TokenType.STRING : self.ParseString,
            TokenType.ID : self.ParseId,
            TokenType.LEFT_PAREN : self.ParseGroup
        }
    
    def Parse(self, cursor):
        return self.ParseBinary(cursor, 0)
    
    def ParseArguments(self, cursor):
        args : list[Expression] = []
        if cursor.Match(TokenType.RIGHT_PAREN):
            return args
        args.append(self.Parse(cursor))
        while cursor.Match(TokenType.COMMA):
            args.append(self.Parse(cursor))
        cursor.Expect(TokenType.RIGHT_PAREN, "')' o ','")
        return args
    
    def ParseBinary(self, cursor, level):
        if level == len(self.BINARY_LEVELS):
            return self.ParseUnary(cursor)
        left = self.ParseBinary(cursor, level+1)
        while (op := cursor.Match(*self.BINARY_LEVELS[level])) is not None:
            right = self.ParseBinary(cursor, level+1)
            left = BiOper(left, op.val, right, line=op.line)
        return left
    
    def ParseUnary(self, cursor):
        op = cursor.Match(TokenType.MINUS, TokenType.NOT)
        if op is None:
            return self.ParsePrimary(cursor)
        operand = self.ParseUnary(cursor)
        if op.typ == TokenType.MINUS and isinstance(operand, Number):
            return Number(-operand.value, line=op.line)
        return UniOper(op.val, operand, line=op.line)
    
    def ParsePrimary(self, cursor):
        tok = cursor.Peek()
        handler = self.primaries.get(tok.typ) if tok is not None else None
        if handler is None:
            cursor.Fail(f"Se esperaba una expresion pero se encontro {Describe(tok)}.")
        return handler(cursor)
    
    def ParseNumber(self, cursor):
        tok = cursor.Advance()
        return Number(tok.val, line=tok.line)
    
    def ParseString(self, cursor):
        tok = cursor.Advance()
        return String(tok.val, line=tok.line)
    
    def ParseId(self, cursor):
        name = cursor.Advance()
        if cursor.Match(TokenType.LEFT_PAREN):
            return FunctionCall(name.val, self.ParseArguments(cursor), line=name.line)
        return Id(name.val, line=name.line)
    
    def ParseGroup(self, cursor):
        name = cursor.Advance()
        inner = self.Parse(cursor)
        cursor.Expect(TokenType.RIGHT_PAREN, "')'")
        return inner