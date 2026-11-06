from ..lexer.tokens import Token, TokenType
from ..nodes.nodes import Program, Statement
from .cursor_line import CursorLine
from .header_parser import HeaderParser
from .statement_parser import StatementParser
from ..errors.errors import ParserError

class Parser:
    
    def __init__(self, tokens, headParser=None, statementParser=None):
        self.tokens = tokens
        cursor = CursorLine(tokens)
        self.head = HeaderParser(cursor) if headParser is None else headParser
        self.statements = StatementParser(cursor) if statementParser is None else statementParser
    
    def parse(self):
        errors : list[tuple[int, str]] = []
        lines = self.split_lines()
        start = self.find_start(lines)
        
        if start is None:
            head_lines, body_lines, closing_line = lines, [], 0
            errors.append((0, "Falta la etiqueta obligatoria 'start:'."))
        else:
            head_lines, body_lines = lines[:start], lines[start:]
            closing_line = lines[start][0].line
        
        header, header_errors = self.head.parse(head_lines, closing_line)
        errors.extend(header_errors)
        
        body : list[Statement] = []
        for tokens in body_lines:
            try:
                body.append(self.statements.parse(tokens))
            except ParserError as pe:
                errors.extend(pe.errors)
        
        if errors:
            raise ParserError(sorted(errors, key=lambda e: (e[0] == 0, e[0])))
        
        return Program(header.line, header, body, {})
                
    
    # Divide los tokens en lineas logicas
    def split_lines(self):
        lines : list[list[Token]] = []
        current : list[Token] = []
        
        for t in self.tokens:
            if t.typ in (TokenType.NEWLINE, TokenType.EOF):
                if current:
                    lines.append(current)
                    current = []
            else:
                current.append(t)
        
        if current:
            lines.append(current)
        
        return lines

    # Retorna el indice de la primera linea que empieza con 'start:'
    @staticmethod
    def find_start(lines):
        for i, tokens in enumerate(lines):
            if (len(tokens) >= 2) and (tokens[0].typ == TokenType.ID) and (tokens[0].val == "start") and (tokens[1].typ == TokenType.COLON):
                return i
        return None