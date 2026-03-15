from enum import Enum
from typing import List


class Genero(Enum):
    FEMENINO = 'Femenino'
    MASCULINO = 'Masculino'
    OTRO = 'Otro'

    @staticmethod
    def lista() -> List[str]:
        return [genero.value for genero in Genero]