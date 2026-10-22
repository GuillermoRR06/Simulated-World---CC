from lexer.tokens import Token, TokenType
from nodes.nodes import Program, Statement
from .cursor_line import ParserError, CursorLine
from .header_parser import HeaderParser
from .statement_parser import StatementParser

class Parser:
    
    def __init__(self, tokens, headParser, statementParser):
        self.tokens = tokens
        self.head = HeaderParser() if headParser is None else headParser
        self.statements = StatementParser() if statementParser is None else statementParser
    
    def Parse(self):
        errors : list[tuple[int, str]] = []
        lines = self.SplitLines()
        start = self.FindStart(lines)
        
        if start is None:
            head_lines, body_lines, closing_line = lines, [], 0
            errors.append((0, "Falta la etiqueta obligatoria 'start:'."))
        else:
            head_lines, body_lines = lines[:start], lines[start:]
            closing_line = lines[start][0].line
        
        header, header_errors = self.head.Parse(head_lines, closing_line)
        errors.extend(header_errors)
        
        body : list[Statement] = []
        for tokens in body_lines:
            try:
                body.append(self.statements.Parse(CursorLine(tokens)))
            except ParserError as pe:
                errors.extend(pe.errors)
        
        if errors:
            raise ParseError(sorted(errors, key=lambda e: (e[0] == 0, e[0])))
        
        return Program(header, body, line=header.line)
                
    
    # Divide los tokens en lineas logicas
    def SplitLines(self):
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
    def FindStart(lines):
        for i, tokens in enumerate(lines):
            if (len(tokens) >= 2) and (tokens[0].typ == TokenType.ID) and (tokens[0].val == "start") and (tokens[1].typ == TokenType.COLON):
                return i
        return None