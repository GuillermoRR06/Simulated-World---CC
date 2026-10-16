from lexer.tokens import TokenType

from nodes.nodes import (
    Program, Header, Label, Goto, If_Goto,
    Assign, Action, Number, String, Id,
    Function_Call, Bi_Operator, Uni_Operator
)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current = self.tokens[self.pos] if self.tokens else None