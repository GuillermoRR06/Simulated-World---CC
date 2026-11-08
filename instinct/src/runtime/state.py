from ..nodes.nodes import Program

class RuntimeState:
    
    def __init__(self, program: Program):
        self.program = program
        self.variables : dict[str, int|str] = {}
        self.counter = program.labels["start"]
    
    def GotoJump(self, label: str):
        self.counter = self.program.labels[label]