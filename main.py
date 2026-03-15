from core.gestor_de_ventana import GestorDeVentana
from experimento_bowl.experimento_bowl import Experimento

def main() -> None:
    gestor_ventana: GestorDeVentana = GestorDeVentana()
    experimento_bowl = Experimento(gestor_ventana)
    experimento_bowl.ejecutar()

if __name__ == "__main__":
    main()
