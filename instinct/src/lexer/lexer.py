from .tokens import TokenType, Token, KEYWORDS, TWO_CHAR_SYMBOLS, ONE_CHAR_SYMBOLS

#Excepcion de error lexico
class LexerError(Exception):
    def __init__(self, msj: str, line: int, column: int):
        super().__init__(f"Error Lexico en linea {line} | columna {column} : {msj}")

class Lexer:
    def __init__(self):
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens : list[Token] = []
        
    #Funcion para tokenizar texto
    def Tokenize(self, code) -> list[Token]:
        while self.pos < len(code):
            c = code[self.pos]
            
            # Si se encuentra algun tipo de espacio: lo ignora y avanza
            if c in " \t\r":
                self.pos += 1
                self.col += 1

            # Si encuentra un salto de linea
            elif c == "\n":
                self.ignore_extra_newlines(code)
            
            # Si encuentra un '#' esa linea es un comentario
            elif c == "#":
                self.ignore_comment(code)
            
            # Si encuentra un " eso puede empezar un string
            elif c == '"':
                self.match_string(code)
            
            # Si encuentra un digito deberia empezar un numero
            elif c.isdigit():
                self.match_number(code)
            
            # Si encuentra una letra o un guion bajo, eso es un identificador (o una palabra reservada)
            elif c.isalpha() or c == "_":
                self.match_id_or_key(code)
            
            # Si encuentra un simbolo, revisa primero si pertenece a un operador de dos caracteres, si no, revisa si es un operador de un caracter.
            # Si es una de las cosas anteriores, agrega el token. Si tampoco es, reporta error por caracter desconocido
            else:
                self.match_operator(code)
        
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.col))
        return self.tokens
    
    # Varios saltos de liena seguidos valen por un token NEWLINE. Se agrega un token NEWLINE y se ignoran
    # los demas saltos de linea consecutivos
    def ignore_extra_newlines(self, code):
        self.tokens.append(Token(TokenType.NEWLINE, "\n", self.line, self.col))
        while self.pos < len(code) and code[self.pos] == "\n":
            self.pos += 1
            self.line += 1
        self.col = 1
    
    # Nombre autoexplicativo
    def ignore_comment(self, code):
        while self.pos < len(code) and code[self.pos] != "\n":
            self.pos += 1
            self.col += 1
    
    # Busca la comilla de cierre. Si lo hace agrega el token, si no lanza error
    def match_string(self, code):
        start = self.pos
        self.pos += 1
        while self.pos < len(code) and code[self.pos] not in '"\n':
            self.check_caracter(code[self.pos])
            self.pos += 1
        if self.pos >= len(code) or code[self.pos] == "\n":
            raise LexerError("Texto sin cerrar (falta la comilla de cierre)", self.line, self.col)
        self.tokens.append(Token(TokenType.STRING, code[start+1:self.pos], self.line, self.col))
        self.pos += 1
        self.col += self.pos - start + 1
    
    # Recibe el numero hasta que encuentra algo que no sea digito. Luego agrega el token
    def match_number(self, code):
        start = self.pos
        while self.pos < len(code) and code[self.pos].isdigit():
            self.check_caracter(code[self.pos])
            self.pos += 1
        self.tokens.append(Token(TokenType.NUMBER, int(code[start:self.pos]), self.line, self.col))
        self.col += self.pos - start
    
    # Recibe la palabra hasta que ya no obtiene un digito o una letra o un guion bajo
    # Si es una palabra reservada, agrega su token
    # En otro caso, agrega el token ID
    def match_id_or_key(self, code):
        start = self.pos
        while self.pos < len(code) and (code[self.pos].isalnum() or code[self.pos] == "_"):
            self.check_caracter(code[self.pos])
            self.pos += 1
        text = code[start:self.pos]
        if text in KEYWORDS.keys():
            self.tokens.append(Token(KEYWORDS[text], text, self.line, self.col))
        else:
            self.tokens.append(Token(TokenType.ID, text, self.line, self.col))
        self.col += self.pos - start + 1
    
    # Revisa si es un operador de dos caracteres o de un caracter. Entonces agrega el token respectivo o lanza error
    def match_operator(self, code):
        two = code[self.pos:self.pos+2]
        if two in TWO_CHAR_SYMBOLS.keys():
            self.tokens.append(Token(TWO_CHAR_SYMBOLS[two], two, self.line, self.col))
            self.pos += 2
            self.col += 2
        else:
            one = code[self.pos]
            if one not in ONE_CHAR_SYMBOLS.keys():
                raise LexerError(f"{one!r} es un Caracter Prohibido", self.line, self.col)
            self.tokens.append(Token(ONE_CHAR_SYMBOLS[one], one, self.line, self.col))
            self.pos += 1
            self.col += 1
    
    # Revisa si un caracter es un caracter prohibido
    def check_caracter(self, char):
        if char not in ONE_CHAR_SYMBOLS.keys() and not (char.isalnum() or char == "_" or char in " \t\r"):
            raise LexerError(f"{char!r} es un Caracter Prohibido", self.line, self.col)
        