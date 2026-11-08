from ..lexer.tokens import TokenType
from ..nodes.nodes import (Statement, Label, Assign, Goto, IfGoto, ActionCall)
from .expression_parser import ExpressionParser
from .cursor_line import CursorLine, Describe

# Clase para parsear las lineas de codigo del cuerpo
class StatementParser:    
    def __init__(self, cursor: CursorLine, expressions=None):
        self.STATEMENTS = {
            TokenType.IF : self.parse_if_goto,
            TokenType.GOTO : self.parse_goto,
            TokenType.ID : self.parse_named
        }
    
        self.NAMED = {
            TokenType.COLON : self.parse_label,
            TokenType.ASSIGN : self.parse_assign,
            TokenType.LEFT_PAREN : self.parse_action_call
        }
        self.cursor = cursor
        self.expressions = ExpressionParser(cursor) if expressions is None else expressions
    
    # Verifica que la linea cumpla las formas establecidas. Tambien verifica si sobra alguna expresion al final
    def parse(self, tokens):
        self.cursor.load(tokens)
        first = self.cursor.peek()
        handler = self.STATEMENTS.get(first.typ)
        if handler is None:
            self.cursor.fail(f"La linea no encaja en ninguna forma valida (empieza con {Describe(first)})")
        statm = handler()
        if self.cursor.peek() is not None:
            self.cursor.fail(f"Sobra {Describe(self.cursor.peek())} al final de la instruccion")
        return statm
    
    # Parsea el token siguiente a un ID, para verificar que encaje con: una llamada a accion, una asignacion, o una definicion de etiqueta
    def parse_named(self):
        second = self.cursor.peek(1)
        handler = self.NAMED.get(second.typ) if second is not None else None
        if handler is None:
            self.cursor.fail(f"Despues de '{self.cursor.peek().val}' se esperaba ':', '=' o '(', pero se encontro '{Describe(second)}'.")
        return handler()
    
    # Parsea una linea donde se define una etiqueta
    def parse_label(self):
        name = self.cursor.advance()
        self.cursor.advance()
        return Label(name.line, name.val)
    
    # Parsea una instruccion de asignacion
    def parse_assign(self):
        name = self.cursor.advance()
        self.cursor.advance()
        return Assign(name.line, name.val, self.expressions.parse_binary())
    
    # Parsea una instruccion de llamada a una accion
    def parse_action_call(self):
        name = self.cursor.advance()
        self.cursor.advance()
        return ActionCall(name.line, name.val, self.expressions.parse_arguments())
    
    # Parsea una instruccion de goto
    def parse_goto(self):
        keyword = self.cursor.advance()
        label = self.cursor.expect(TokenType.ID, "el nombre de una etiqueta")
        return Goto(keyword.line, label.val)
    
    # Parsea una instruccion de if-goto
    def parse_if_goto(self):
        keyword = self.cursor.advance()
        condition = self.expressions.parse_binary()
        self.cursor.expect(TokenType.GOTO, "'goto' despues de la condicion")
        label = self.cursor.expect(TokenType.ID, "el nombre de una etiqueta")
        return IfGoto(keyword.line, condition, label.val)
    
    