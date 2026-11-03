from abc import ABC, abstractmethod

class RuntimeEnvironment(ABC):
    
    @abstractmethod
    def Read_Perception(self, name: str) -> int|str:
        pass
    
    @abstractmethod
    def Call_Function(self, name: str, args: list[int|str]) -> int|str:
        pass
    
    @abstractmethod
    def Execute_Action(self, name: str, args: list[int|str]) -> int|str:
        pass