from typing import Tuple

from psychopy import visual, core, event


class GestorDeVentana:
    def __init__(
            self,
            size: Tuple[int, int] = (1280, 720),
            fullscr: bool = False,
            color: str = "black",
            units: str = "pix"
        ):
        self._win: visual.Window = visual.Window(
            size = size,
            fullscr = fullscr,
            color = color,
            units = units
        )

    @property
    def win(self) -> visual.Window:
        return self._win

    def actualizar(self) -> None:
        # Aborto global de emergencia
        if 'escape' in event.getKeys():
            print("Experimento abortado por el usuario.")
            self.cerrar()
            core.quit()

        self.win.flip()

    def cerrar(self) -> None:
        self.win.close()
