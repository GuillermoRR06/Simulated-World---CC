from ..lexer.tokens import TokenType
from ..errors.errors import ParserError

def Describe(token):
    if token is None: return "final de la linea"
    if token.typ == TokenType.STRING: return f'"{token.val}"'
    return f"{token.val}"

# Cursor que permite analizar la sintaxis del codigo linea por linea
class CursorLine():
    def __init__(self, tokens):
        self.load(tokens or [])
    
    def load(self, tokens=[]):
        self.tokens = tokens
        self.pos = 0
    
    def peek(self, extra=0):
        i = self.pos + extra
        return self.tokens[i] if i < len(self.tokens) else None
    
    def advance(self):
        token = self.peek()
        if token is not None:
            self.pos += 1
            return token
        return None
    
    def match(self, *types):
        token = self.peek()
        if token is not None and token.typ in types:
            self.pos += 1
            return token
        return None
    
    def fail(self, msg):
        token = self.peek() or self.tokens[-1]
        raise ParserError([(token.line, msg)])
    
    def expect(self, typ, msg):
        token = self.match(typ)
        if token is None: self.fail(f"Se esperaba {msg} pero se encontro {Describe(self.peek())}")
        return token