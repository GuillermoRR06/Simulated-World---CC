from .tokens import TokenType, Token, KEYWORDS, TWO_CHAR_SYMBOLS, ONE_CHAR_SYMBOLS

#Excepcion de error lexico
class LexerError(Exception):
    def __init__(self, msj: str, line: int, column: int):
        super().__init__(f"Error Lexico en linea {line} | columna {column} : " + msj)

class Lexer:
    #Funcion para tokenizar texto
    def Tokenize(self, code) -> list[Token]:
        pos, line, col = 0, 1, 1
        tokens : list[Token] = []
        
        while pos < len(code):
            c : str = code[pos]
            
            # Si se encuentra algun tipo de espacio: lo ignora y avanza
            if c in " \t\r":
                pos += 1
                col += 1

            # Si encuentra un salto de linea: agrega el token y avanza hasta que no encuentre mas saltos de linea
            # Varios saltos de linea consecutivos cuentan por un token
            elif c == "\n":
                tokens.append(Token(TokenType.NEWLINE, "\n", line, col))
                while pos < len(code) and code[pos] == "\n":
                    pos += 1
                    line += 1
                col = 1
            
            # Si encuentra un '#' esa linea es un comentario. Lo debe ignorar, pero debe actualizar pos
            elif c == "#":
                while pos < len(code) and code[pos] != "\n":
                    pos += 1
                    col += 1
            
            # Si encuentra un " eso puede empezar un string. Lo recorre hasta encontrar la comilla de cierre
            # Si la encuentra, agrega el token
            # Si no, reporta error lexio
            elif c == '"':
                start = pos
                pos += 1
                while pos < len(code) and code[pos] not in '"\n':
                    pos += 1
                if pos >= len(code) or code[pos] == "\n":
                    raise LexerError("Texto sin cerrar (falta la comilla de cierre)", line, col)
                tokens.append(Token(TokenType.STRING, code[start+1:pos], line, col))
                pos += 1
                col += pos - start + 1
            
            # Si encuentra un digito deberia empezar un numero. Lo recorre hasta que deje de encontrar un digito. Ahi se fija en
            # Si es un caracter de espacio o salto de linea: agrega el token
            # Deberia dar error en un caso asi?: 123a456, lo tacha de error o lo divide en numero 123 e id a456 ?
            elif c.isdigit():
                start = pos
                while pos < len(code) and code[pos].isdigit():
                    pos += 1
                #'''
                #Pendiente a aclarar duda
                #if c not in " \t\r\n":
                    #raise LexerError("Numero mal escrito", line, col)
                #'''
                tokens.append(Token(TokenType.NUMBER, int(code[start:pos]), line, col))
                col += pos - start
            
            # Si encuentra una letra o un guion bajo, eso es un identificador (o una palabra reservada).
            # Recorre hasta que termina la palabra, y antes de agregar el token, comprubea el tipo
            elif c.isalpha() or c == "_":
                start = pos
                while pos < len(code) and (code[pos].isalnum() or code[pos] == "_"):
                    pos += 1
                text = code[start:pos]
                if text in KEYWORDS.keys():
                    tokens.append(Token(KEYWORDS[text], text, line, col))
                else:
                    tokens.append(Token(TokenType.ID, text, line, col))
                col += pos - start + 1
            
            else:
                two = code[pos:pos+2]
                if two in TWO_CHAR_SYMBOLS.keys():
                    tokens.append(Token(TWO_CHAR_SYMBOLS[two], two, line, col))
                    pos += 2
                    col += 2
                else:
                    one = code[pos]
                    if one not in ONE_CHAR_SYMBOLS.keys():
                        raise LexerError(f"{one} es un Caracter Prohibido", line, col)
                    tokens.append(Token(ONE_CHAR_SYMBOLS[one], one, line, col))
                    pos += 1
                    col += 1
        
        tokens.append(Token(TokenType.EOF, "", line, col))
        return tokens
                    
                
            
            
            
                
                    
            
            