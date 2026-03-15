from core.gestor_de_ventana import GestorDeVentana
# from experimento_bowl.experimento_bowl import Experimento
from experimento_nback.experimento_nback import ExperimentoNBack

def main() -> None:
    gestor_ventana: GestorDeVentana = GestorDeVentana()
    experimento_bowl = ExperimentoNBack()
    experimento_bowl.ejecutar()

if __name__ == "__main__":
    main()
