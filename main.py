from core.gestor_de_ventana import GestorDeVentana
from core.experimento import Experimento
from experimento_bowl.experimento_bowl import ExperimentoBowl
# from experimento_nback.experimento_nback import ExperimentoNBack

def main() -> None:
    gestor_ventana: GestorDeVentana = GestorDeVentana()
    experimento: Experimento = ExperimentoBowl(gestor_ventana)
    experimento.ejecutar()

if __name__ == "__main__":
    main()
