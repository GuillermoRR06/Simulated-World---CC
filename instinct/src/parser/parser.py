from lexer.tokens import TokenType
from nodes.nodes import (
    Program, Header, Label, Goto, IfGoto,
    Assign, ActionCall, Number, String, Id,
    FunctionCall, BiOper, UniOper)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current = self.tokens[self.pos] if self.tokens else None