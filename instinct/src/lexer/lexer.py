import re
from token import NEWLINE
from tokens import TokenType, Token

class LexerError(Exception):
    pass

class Lexer:
    def __init__(self, code: str):
        self.code = code
        regex_parts = [f"(?P<{token.name}>{token.pattern})" for token in TokenType]
        self.master_regex = re.compile("|".join(regex_parts))
    
    def Tokenize(self) -> list[Token]:
        tokens : list[Token] = []
        line, start = 1, 0
        
        for i in self.master_regex.finditer(self.code):
            typ = i.lastgroup
            val = i.group()
            col = i.start() - start + 1
        
            if typ == "SPACE": continue
            if typ == "COMMENT": continue
            
            if typ == "NEWLINE":
                tokens.append(Token(typ=TokenType.NEWLINE, val='\n', line=line, col=col))
                line += val.count('\n')
                start = i.end()
                continue
            
            if typ == "MISMATCH": raise LexerError(f"Caracter Prohibido {val!r} en linea {line}|columna {col}")
            
            token_typ = TokenType[str(typ)]
            parsed_val: str | int = val
            
            if token_typ == TokenType.NUMBER: parsed_val = int(val)
            elif token_typ == TokenType.STRING: parsed_val = val[1:-1]
            elif token_typ == TokenType.ID: parsed_val = TokenType.keywords().get(value, TokenType.ID)
            
            tokens.append(Token(typ=token_typ, val=parsed_val, line=line, col=col))
        
        return tokens
            
            
        