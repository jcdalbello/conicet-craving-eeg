from abc import ABC, abstractmethod

class Experimento(ABC):
    @abstractmethod
    def ejecutar(self) -> None:
        pass
