from psychopy import visual, core, event, gui, data

class Ventana:
    def __init__(self):
        self.win: visual.Window = visual.Window(fullscr=True, color="black", units="pix")
        self._stim_text: visual.TextStim = visual.TextStim(self.win, text="", color="white", height=100)
        self._feedback_text: visual.TextStim = visual.TextStim(self.win, text="", color="white", height=50, pos=(0, 0))
        self._instruction_text: visual.TextStim = visual.TextStim(self.win, text="En esta prueba vas a ver unas letras en la pantalla. Las letras van a ir apareciendo, una a una en la pantalla y\n"
                                                "tu tarea consiste en apretar LA BARRA ESPACIADORA cada vez que una letra sea la misma que la presentada dos ensayos antes.\n"
                                                "O sea que vos vas a tener que recordar la letra que apareció dos ensayos antes.\n\n"
                                                "Vamos a verlo con unos ejemplos:\n\n"
                                                "Mirá atentamente las siguientes letras:\n"
                                                "    T           D          J         D         K    \n"
                                                "                                MAL   BIEN     MAL     \n\n"
                                                "(Para continuar presiona la barra espaciadora)",
                                                 color="white", height=25, wrapWidth=700, pos=(0, 0))

    def mostrar_instrucciones(self) -> None:
        self._instruction_text.draw()
        self.win.flip()

    def cambiar_stim_text(self, letra: str) -> None:
        self._stim_text.text = letra

    def mostrar_stim_text(self) -> None:
        self._stim_text.draw()
        self.win.flip()

    def cambiar_feedback_text(self, text: str) -> None:
        self._feedback_text.text = text

    def mostrar_feedback_text(self) -> None:
        self._feedback_text.draw()
        self.win.flip()

    def limpiar_pantalla(self) -> None:
        self.win.flip()

    def cerrar(self) -> None:
        self.win.close()
