from psychopy import visual, core, event, gui, data
import csv
import serial

from typing import List

from experimento_nback.dominio.participante import Participante
from experimento_nback.dominio.generador_de_ensayos import GeneradorDeEnsayos
from ventana import Ventana
from experimento_nback.dominio.ensayo import Ensayo

class Experimento:
    def __init__(self):
        # TODO: se podria definir el nback (2, 3, 4, etc..) junto con los datos del participante
        self.NBACK: int = 2
        self.N_BLOQUES: int = 4
        # self.N_ENSAYOS: int = 25
        self.N_ENSAYOS: int = 8
        # self.PORCENTAJE_TARGETS: float = 0.30
        self.PORCENTAJE_TARGETS: float = 0.25
        # TODO: consultar por cambio de duracion de tiempo del estimulo a una cantidad random dentro de un rango determinado
        # TODO: consultar como se distribuye el tiempo de un ensayo, por cuanto tiempo debe ser visible la letra, si es que el participante deberia poder responder en cualquier momento en el que se muestre la letra de un ensayo. Actualmente hay un tiempo muerto hasta que el programa acepta input mientras muestra la letra del ensayo.
        self.DURACION_DEL_ESTIMULO: float = 0.5  # en segundos
        self.TIEMPO_MAX_DE_RESPUESTA: float = 1.5  # en segundos
        self.INTERVALO_ENTRE_ENSAYOS: float = 1.0
        self.ventana: Ventana = Ventana()
        self.participante: Participante = self._obtener_datos_participante()
        self.archivo_salida: str = f"datos_nback_{self.participante.sujeto}.csv"

    def ejecutar(self) -> None:
        self._mostrar_instrucciones()
        self._crear_registro_de_la_prueba()
        self._presentacion_de_bloques()
        self._terminar_experimento()

    def _obtener_datos_participante(self) -> Participante:
        # info = {'Nombre': '', 'Sujeto': '', 'Edad': '', 'Genero': ['Femenino', 'Masculino', 'Otro']}
        info = Participante.diccionario_para_gui()
        dlg = gui.DlgFromDict(dictionary=info, title='Datos del Participante')
        if not dlg.OK:
            core.quit()

        participante = Participante.desde_diccionario(info)
        return participante

    def _mostrar_instrucciones(self) -> None:
        self.ventana.mostrar_instrucciones()
        event.waitKeys(keyList=['space'])

    def _crear_registro_de_la_prueba(self) -> None:
        with open(self.archivo_salida, "w", newline="") as archivo:
            writer = csv.writer(archivo)
            writer.writerow(["Nombre", "Sujeto", "Edad", "Genero", "Bloque", "Ensayo", "Letra", "EsTarget", "Respuesta",
                             "TiempoRespuesta", "Precisión"])

    def _presentacion_de_bloques(self) -> None:
        for bloque in range(1, self.N_BLOQUES + 1):
            ensayos: List[Ensayo] = self._generar_ensayos()
            correctos: int = 0
            tiempos: List[float] = []

            for i_ensayo, ensayo in enumerate(ensayos, start=1):
                self._mostrar_letra_del_ensayo(ensayo.letra)

                # Enviar señal por puerto serial
                # port.write(letra.encode())

                # TODO: posiblemente abstraer `keys` en una clase que incluya la tecla presionada y su tiempo de respuesta
                reloj = core.Clock()
                keys = event.waitKeys(maxWait=self.TIEMPO_MAX_DE_RESPUESTA, keyList=['space', 'escape'], timeStamped=reloj)

                self._pausa_entre_ensayos()

                if keys:
                    if keys[0][0] == "escape":
                        self._terminar_experimento()
                        break

                    respuesta = "Presionó"
                    tiempo_respuesta = keys[0][1] * 1000  # Convertir a ms
                    es_correcto = (ensayo.es_target and respuesta == "Presionó") or (
                                not ensayo.es_target and respuesta != "Presionó")
                else:
                    respuesta = "No respondió"
                    tiempo_respuesta = "NR"
                    es_correcto = not ensayo.es_target

                if es_correcto:
                    correctos += 1
                    if isinstance(tiempo_respuesta, (int, float)):
                        tiempos.append(tiempo_respuesta)

                self._guardar_resultados_en_csv(bloque, i_ensayo, ensayo, respuesta, tiempo_respuesta, es_correcto)

            self._feedback(tiempos, bloque, correctos)

            event.waitKeys()

    # TODO: preguntar por la duracion de cada ensayo en pantalla, porque puede haber un tiempo muerto en el que no se tome input del usuario por el wait con DURACION_DEL_ESTIMULO
    def _mostrar_letra_del_ensayo(self, letra: str) -> None:
        self.ventana.cambiar_stim_text(letra)
        self.ventana.mostrar_stim_text()
        core.wait(self.DURACION_DEL_ESTIMULO)

    def _pausa_entre_ensayos(self) -> None:
        self.ventana.limpiar_pantalla()
        core.wait(self.INTERVALO_ENTRE_ENSAYOS)

    def _generar_ensayos(self) -> List[Ensayo]:
        return GeneradorDeEnsayos.generar(self.NBACK, self.N_ENSAYOS, self.PORCENTAJE_TARGETS)

    def _feedback(self, tiempos: List[float], bloque: int, correctos: int) -> None:
        if tiempos:
            tiempo_promedio = sum(tiempos) / len(tiempos)
        else:
            tiempo_promedio = "NR"

        feedback_text = f"Fin del Bloque {bloque}\nPrecisión: {correctos / self.N_ENSAYOS:.2%}\nTiempo promedio: {tiempo_promedio} ms\nPresiona cualquier tecla para continuar"
        self.ventana.cambiar_feedback_text(feedback_text)
        self.ventana.mostrar_feedback_text()

    def _guardar_resultados_en_csv(self, bloque: int, i_ensayo: int, ensayo: Ensayo, respuesta: str, tiempo_respuesta: float, es_correcto: bool) -> None:
        with open(self.archivo_salida, "a", newline="") as archivo:
            writer = csv.writer(archivo)
            writer.writerow(
                [self.participante.nombre, self.participante.sujeto, self.participante.edad,
                 self.participante.genero.value,
                 bloque, i_ensayo, ensayo.letra, ensayo.es_target, respuesta, tiempo_respuesta,
                 "Correcto" if es_correcto else "Incorrecto"])

    def _terminar_experimento(self) -> None:
        self.ventana.cerrar()
        core.quit()
