import random
from typing import List
from experimento_nback.ensayo import Ensayo


class GeneradorDeEnsayos:
    @staticmethod
    def generar(nback, n_ensayos, porcentaje_targets) -> List[Ensayo]:
        generador = _GeneradorDeEnsayos(nback, n_ensayos, porcentaje_targets)
        return generador.generar()


class _GeneradorDeEnsayos:
    def __init__(self, nback: int, n_ensayos: int, porcentaje_targets: float):
        self.nback: int = nback
        self.n_ensayos: int = n_ensayos
        self.porcentaje_targets: float = porcentaje_targets
        self.n_targets: int = int(n_ensayos * porcentaje_targets)
        self.letras_validas: List[str] = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "M", "N", "P", "R", "S", "T", "V", "X",
                               "Y", "Z"]
        self._validar_porcentaje(porcentaje_targets)


    def generar(self) -> List[Ensayo]:
        es_target = self._definir_indices_target()
        secuencia = self._crear_secuencia(es_target)
        ensayos: List[Ensayo] = self._generar_lista_de_ensayos(secuencia, es_target)
        return ensayos

    def _validar_porcentaje(self, porcentaje_targets) -> None:
        if not (0.0 <= porcentaje_targets <= 1.0):
            raise ValueError("El porcentaje de targets debe estar entre 0.0 y 1.0")

    def _definir_indices_target(self) -> List[bool]:
        indices_designados_target = self._designar_indices_target()

        es_target: List[bool] = [False] * self.n_ensayos
        for i in indices_designados_target:
            es_target[i] = True

        return es_target

    def _designar_indices_target(self) -> List[int]:
        indices_designados_target: List[int] = random.sample(
            self._indices_validos_para_targets(),
            k=self.n_targets
        )
        return indices_designados_target

    def _indices_validos_para_targets(self) -> List[int]:
        return list(range(self.nback, self.n_ensayos))

    def _crear_secuencia(self, es_target: List[bool]) -> List[str]:
        secuencia: List[str] = [""] * self.n_ensayos

        for i in range(self.n_ensayos):
            if es_target[i]:
                secuencia[i] = secuencia[i - 2]
            else:
                opciones_validas = [letra for letra in self.letras_validas if letra != secuencia[i - 2]]
                secuencia[i] = random.choice(opciones_validas)

        return secuencia

    def _generar_lista_de_ensayos(self, secuencia: List[str], es_target: List[bool]) -> List[Ensayo]:
        return [Ensayo(letra, target) for letra, target in zip(secuencia, es_target)]
