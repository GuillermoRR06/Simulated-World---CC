from lexer.tokens import Token, TokenType
from nodes.nodes import Header
from .cursor_line import ParserError, CursorLine

# Clases que se auto-parsean, ahorran codigo mas adelante
class HeaderField():
    pass

class NameField(HeaderField):
    def Parse(self, cursor, key):
        name = cursor.Expect(TokenType.ID, f"un nombre como valor de '{key}'")
        cursor.ExpectEnd()
        return name.val

class IntField(HeaderField):
    def __init__(self, minimum):
        self.minimum = minimum
        
    def Parse(self, cursor, key):
        negative = cursor.Match(TokenType.MINUS) is not None
        num = cursor.Expect(TokenType.NUMBER, f"un numero entero como valor de '{key}'")
        cursor.ExpectEnd()
        value = -num.val if negative else num.val
        if value < self.minimum:
            cursor.Fail(f"'{key}' debe ser un entero mayor o igual que {self.minimum}")
        return value

# Parser de la cabecera
class HeaderParser():
    
    # Campos que no pueden faltar
    FIELDS = {
        "creaute": NameField(), # Siempre primero
        "faction": NameField(),
        "health": IntField(1),
        "vision": IntField(1),
        "lifespan": IntField(1)
    }
    
    # Metodo Principal. Parsea cada linea de la cabecera, acumula errores
    def Parse(self, lines, closing_line):
        errors : list[tuple[int, str]] = []
        values : dict[str, object] = {}
        lines_of : dict[str, int] = {}
        seen : set[str] = set()
        
        # Parsea cada linea
        for tokens in lines:
            try:
                key, value = self.ParseEntry(CursorLine(tokens), seen)
            except ParserError as pe:
                errors.extend(pe.errors)
                continue
            values[key] = value
            lines_of[key] = tokens[0].line
        
        # Analiza si 'creature' aparece primero
        if (lines) and ("creature" in values) and (lines[0][0].val != "creature"):
            errors.append((lines[0][0].line, "La primera linea no vacia de la cabecera debe ser 'creature <name>"))
        
        # Revisa si aparecen el resto de campos
        for key in self.FIELDS:
            if key not in seen:
                errors.append((closing_line, f"Falta la clave '{key}' en la cabecera"))
        
        # Retorna la cabecera parseada o retorna None
        if all(key in values for key in self.FIELDS):
            return Header(**values, line=lines_of["creature"]), errors
        return None, errors
    
    def ParseEntry(self, cursor, seen):
        key = cursor.Expect(TokenType.ID, f"una clave de la cabecera " f"({", ".join(self, FIELDS)})")
        field = self.FIELDS.get(key.val)
        if field is None:
            cursor.Fail(f"Clave de cabecera desconocida: '{key.val}'")
        if key.val in seen:
            cursor.Fail(f"Clave de cabecera repetida: '{key.val}'")
        see.add(key.val)
        return key.val, field.Parse(cursor, key.val)
    
    
        