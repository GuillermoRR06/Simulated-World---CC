from abc import ABC, abstractmethod

class RuntimeEnvironment(ABC):
    
    @abstractmethod
    def read_perception(self, name: str) -> int|str:
        pass
    
    @abstractmethod
    def call_function(self, name: str, args: list[int|str]) -> int|str:
        pass
    
    @abstractmethod
    def execute_action(self, name: str, args: list[int|str]) -> int|str:
        pass