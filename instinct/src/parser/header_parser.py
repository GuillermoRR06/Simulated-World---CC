from ..lexer.tokens import TokenType
from ..nodes.nodes import Header
from .cursor_line import CursorLine, Describe
from ..errors.errors import ParserError

# Clases que se auto-parsean, ahorran codigo mas adelante
class NameField():
    def parse(self, cursor, key):
        name = cursor.expect(TokenType.ID, f"un nombre como valor de '{key}'")
        if cursor.peek() is not None:
            cursor.fail(f"Sobra {Describe(cursor.peek())} al final de la instruccion")
        return name.val

class IntField():
    def __init__(self, minimum):
        self.minimum = minimum
        
    def parse(self, cursor, key):
        negative = cursor.match(TokenType.MINUS) is not None
        num = cursor.expect(TokenType.NUMBER, f"un numero entero como valor de '{key}'")
        if cursor.peek() is not None:
            cursor.fail(f"Sobra {Describe(cursor.peek())} al final de la instruccion")
        value = -num.val if negative else num.val
        if value < self.minimum:
            cursor.fail(f"'{key}' debe ser un entero mayor o igual que {self.minimum}")
        return value

# Parser de la cabecera
class HeaderParser:
    
    # Campos que no pueden faltar
    FIELDS = {
        "creature": NameField(), # Siempre primero
        "faction": NameField(),
        "health": IntField(1),
        "vision": IntField(1),
        "lifespan": IntField(1)
    }
    
    def __init__(self, cursor: CursorLine):
        self.cursor = cursor
    
    # Metodo Principal. Parsea cada linea de la cabecera, acumula errores
    def parse(self, lines, closing_line):
        errors : list[tuple[int, str]] = []
        values : dict[str, object] = {}
        lines_of : dict[str, int] = {}
        seen : set[str] = set()
        
        # Parsea cada linea
        for tokens in lines:
            self.cursor.load(tokens)
            try:
                key, value = self.parse_field(seen)
            except ParserError as pe:
                errors.extend(pe.errors)
                continue
            values[key] = value
            lines_of[key] = tokens[0].line
        
        # Analiza si 'creature' aparece primero
        if (lines) and ("creature" in values) and (lines[0][0].val != "creature"):
            errors.append((lines[0][0].line, "La primera linea no vacia de la cabecera debe ser 'creature <name>'"))
        
        # Revisa si aparecen el resto de campos
        for key in self.FIELDS:
            if key not in seen:
                errors.append((closing_line, f"Falta la clave '{key}' en la cabecera"))
        
        # Retorna la cabecera parseada o retorna None
        if all(key in values for key in self.FIELDS):
            return Header(**values, line=lines_of["creature"]), errors
        
        return None, errors
    
    def parse_field(self, seen):
        key = self.cursor.expect(TokenType.ID, f"una clave de la cabecera ({", ".join(self.FIELDS)})")
        field = self.FIELDS.get(key.val)
        if field is None:
            self.cursor.fail(f"Clave de cabecera desconocida: '{key.val}'")
        if key.val in seen:
            self.cursor.fail(f"Clave de cabecera repetida: '{key.val}'")
        seen.add(key.val)
        return key.val, field.parse(self.cursor, key.val)
    
    
        