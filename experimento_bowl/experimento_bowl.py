from psychopy import visual, core, event

from core.experimento import Experimento
from core.gestor_de_ventana import GestorDeVentana
from core.transmisor_lsl import TransmisorLSL

class ExperimentoBowl(Experimento):
    def __init__(self, gestor_ventana: GestorDeVentana, transmisor_lsl: TransmisorLSL):
        self.DURACION_DE_MUESTRA: int = 3
        self.gestor_ventana: GestorDeVentana = gestor_ventana
        self.transmisor_lsl: TransmisorLSL = transmisor_lsl
        self.mensaje = visual.TextStim(self.gestor_ventana.win, text="")
        self.texto_contador = visual.TextStim(self.gestor_ventana.win, text="", height=100)


    def ejecutar(self) -> None:
        print("Configurando Lab Streaming Layer...")
        print("Inicializando ventana de PsychoPy...")

        self._actualizar_texto_en_pantalla("Presione ESPACIO cuando este listo para empezar.")
        self._esperar_por_barra_espaciadora()
        self._enviar_trigger_por_lsl('inicio_registro_plano')
        self._iniciar_contador(self.DURACION_DE_MUESTRA)
        self._enviar_trigger_por_lsl('fin_registro_plano')
        self._actualizar_texto_en_pantalla("Fin de la muestra plana.\nPresione ESPACIO para empezar la muestra en el bowl de agua")
        self._esperar_por_barra_espaciadora()
        self._enviar_trigger_por_lsl('inicio_registro_bowl_con_hielo')
        self._iniciar_contador(self.DURACION_DE_MUESTRA)
        self._enviar_trigger_por_lsl('fin_registro_bowl_con_hielo')
        self._actualizar_texto_en_pantalla("Fin del experimento.\nPresione ESPACIO para salir.")
        self._esperar_por_barra_espaciadora()
        self._terminar()


    def _actualizar_texto_en_pantalla(self, texto: str) -> None:
        self.mensaje.text = texto
        self.mensaje.draw()
        self.gestor_ventana.actualizar()

    def _enviar_trigger_por_lsl(self, trigger: str) -> None:
        self.transmisor_lsl.enviar_trigger(trigger)

    def _iniciar_contador(self, duracion: int) -> None:
        reloj: core.CountdownTimer = core.CountdownTimer(duracion)
        ultimo_segundo_mostrado: int = duracion + 1

        while reloj.getTime() > 0:
            tiempo_restante: int = int(reloj.getTime()) + 1

            if tiempo_restante != ultimo_segundo_mostrado:
                self.texto_contador.text = str(tiempo_restante)
                ultimo_segundo_mostrado = tiempo_restante

            # Se actualiza la pantalla constantemente para mantener la sincronizacion entre la tasa de refresco del
            # monitor y el clock del CPU, y la prioridad del proceso (polling).
            self.texto_contador.draw()
            self.gestor_ventana.actualizar()

    def _esperar_por_barra_espaciadora(self) -> None:
        event.waitKeys(keyList=['space'])

    def _terminar(self) -> None:
        self.gestor_ventana.cerrar()
        core.quit()
