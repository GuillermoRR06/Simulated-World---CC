from lexer.tokens import TokenType
from nodes.nodes import (Statement, Label, Assign, Goto, IfGoto, ActionCall)
from .expression_parser import ExpressionParser
from .cursor_line import CursorLine, Describe

class StatementParser():
    
    def __init__(self, expressions):
        self.expressions = ExpressionParser() if expressions is None else expressions
        
        self.statements = {
            TokenType.IF : self.ParseIfGoto,
            TokenType.GO_TO : self.ParseGoto,
            TokenType.ID : self.ParseNamed
        }
        
        self.named = {
            TokenType.COLON : self.ParseLabel,
            TokenType.ASSIGN : self.ParseAssign,
            TokenType.LEFT_PAREN : self.ParseActionCall
        }
    
    def Parse(self, cursor):
        first = cursor.Peek()
        handler = self.statements.get(first.typ)
        if handler is None:
            cursor.Fail(f"La linea no encaja en ninguna forma valida" f"(empieza con {Describe(first)})")
        statm = handler(cursor)
        cursor.ExpectEnd()
        return statm
    
    def ParseNamed(self, cursor):
        second = cursor.Peek(1)
        handler = self.named.get(second.typ) if second is not None else None
        if handler is None:
            cursor.Fail(f"Despues de '{cursor.Peek().val}' se esperaba ':', '=' o '(' " f"pero se encontro '{Describe(second)}'.")
        return handler(cursor)
    
    def ParseLabel(self, cursor):
        name = cursor.Advance()
        cursor.Advance()
        return Label(name.val, line=name.line)
    
    def ParseAssign(self, cursor):
        name = cursor.Advance()
        cursor.Advance()
        return Assign(name.val, self.expressions.Parse(cursor), line=name.line)
    
    def ParseActionCall(self, cursor):
        name = cursor.Advance()
        cursor.Advance()
        return ActionCall(name.val, self.expressions.ParseArguments(cursor), line=name.line)
    
    def ParseGoto(self, cursor):
        keyword = cursor.Advance()
        label = cursor.Expect(TokenType.ID, "el nombre de una etiqueta")
        return Goto(label.val, line=keyword.line)
    
    def ParseIfGoto(self, cursor):
        keyword = cursor.Advance()
        condition = self.expressions.Parse(cursor)
        cursor.Expect(TokenType.GO_TO, "'goto' despues de la condicion")
        label = cursor.Expect(TokenType.ID, "el nombre de una etiqueta")
        return IfGoto(condition, label.val, line=keyword.line)
    
    