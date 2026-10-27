from lexer.lexer import Lexer
from parser.parser import Parser
from semantic.semantic import SemanticAnalyzer, default_catalog

class Compiler:
    
    def __init__(self):
        self.catalog = default_catalog()
    
    def Compile(self, source : str):
        tokens = Lexer(source).Tokenize()
        program = Parser(tokens).Parse()
        analysis = SemanticAnalyzer(self.catalog)
        analysis.Analyze(program)
        return program