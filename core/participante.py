from typing import List

from core.genero import Genero

class Participante:
    def __init__(self, nombre: str, sujeto: str, edad: str, genero: Genero):
        self.nombre = nombre
        self.sujeto = sujeto
        self.edad = edad
        self.genero = genero

    @classmethod
    def diccionario_para_gui(cls):
        generos: List[str] = Genero.lista()
        info = {'Nombre': '', 'Sujeto': '', 'Edad': '', 'Genero': generos}
        return info

    @classmethod
    def desde_diccionario(cls, info_gui):
        return cls(
            nombre = info_gui['Nombre'],
            sujeto = info_gui['Sujeto'],
            edad = info_gui['Edad'],
            genero = Genero(info_gui['Genero'])
        )
