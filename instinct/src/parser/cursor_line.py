from lexer.tokens import Token, TokenType

# Error de Parser
class ParserError(Exception):
    def __init__(self, errors):
        self.errors = list(errors)
        super().__init__("\n".join(f"Linea {line}: {msg}" if line else msg for line, msg in self.errors))

def Describe(token):
    if token is None: return "Final de la linea"
    if token.typ == TokenType.STRING: return f'"{token.val}"'
    return f"{token.val}"

# Cursor que permite analizar la sintaxis del codigo linea por linea
class CursorLine():
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def Peek(self, offset=0):
        i = self.pos + offset
        return self.tokens[i] if i < len(self.tokens) else None
    
    def Advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok
    
    def Match(self, *types):
        tok = self.Peek()
        if tok is not None and tok.typ in types:
            self.pos += 1
            return tok
        return None
    
    def Fail(self, msg):
        tok = self.Peek() or self.tokens[-1]
        raise ParserError([(tok.line, msg)])
    
    def Expect(self, typ, msg):
        tok = self.Match(typ)
        if tok is None: self.Fail(f"Se esperaba {msg} pero se encontro {Describe(self.Peek())}")
        return tok
    
    def ExpectEnd(self):
        if self.Peek() is not None: self.Fail(f"Sobra {Describe(self.Peek())} al final de la instruccion")