# CONICET - Craving y Consumo de Papas Fritas (EEG & Biometría)
Repositorio unificado de scripts para experimentos del proyecto de investigación del CONICET "Efecto del consumo de una porción inicial pequeña de papas fritas sobre el deseo de seguir comiendo papas fritas: estudio experimental conductual y de registros de actividad cerebral mediante electroencefalograma".




El proyecto integra tareas conductuales programadas en **PsychoPy** con el envío de marcadores de sincronización a través de **Lab Streaming Layer (LSL)**, permitiendo la captura simultánea y precisa de señales biométricas. En el caso del presente proyecto, las señales se registraron por medio de una placa **BITalino (r)evolution Sensors**.

## Arquitectura del Repositorio

Para mantener la consistencia entre los distintos experimentos del proyecto, utilizamos una estructura de monorepo. **Es mandatorio respetar esta separación lógica:**

* `/core`: Contiene la infraestructura genérica (ej. `gestor_ventana.py`). Ningún código aquí debe contener estímulos específicos de un experimento.
* `/experimentos`: Contiene los paradigmas aislados (ej. Tarea N-back, Prueba del Bowl de Agua). 
* `main.py`: Punto de entrada único. Orquesta la ejecución de los experimentos inyectándoles las dependencias del `core`.

## Requisitos

* Python 3.8
* PsychoPy

# Instalación

```bash
# Clonar el repositorio
git clone https://github.com/jcdalbello/conicet-craving-eeg.git
cd conicet-craving-eeg

# Instalar dependencias
pip install -r requirements.txt
