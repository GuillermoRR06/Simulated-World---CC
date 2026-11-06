# Excepcion de Error Lexico
class LexerError(Exception):
    def __init__(self, msj: str, line: int, column: int):
        super().__init__(f"Error Lexico en linea {line} | columna {column} : {msj}")

# Excepcion de Error Sintactico
class ParserError(Exception):
    def __init__(self, errors):
        self.errors = list(errors)
        super().__init__("\n".join(f"Error Sintactico en linea {line}: {msg}" if line else msg for line, msg in self.errors))

# Excepcion de Error Semantico
class SemanticError(Exception):
    def __init__(self, errors):
        self.errors = list(errors)
        super().__init__("\n".join(f"Error Semantico en linea {line}: {msg}" if line else msg for line, msg in self.errors))