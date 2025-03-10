# Identificación Automática de Patologías en la Voz

Este repositorio contiene el código y los archivos relacionados con el trabajo de grado titulado **"Identificación automática de patologías en la voz a partir de técnicas de aprendizaje automático"**, desarrollado por **Carlos Felipe Palacio Lozano y Juan Esteban Acosta López** en la **Pontificia Universidad Javeriana Cali**.

## Descripción

El objetivo de este proyecto es desarrollar modelos de **aprendizaje automático y aprendizaje profundo** para la detección de patologías en la voz a partir de señales de audio. Se ha comparado el desempeño de técnicas clásicas de clasificación como **Random Forest** con enfoques basados en **Redes Neuronales Convolucionales (CNN)**.

El sistema final incluye una **interfaz web** que permite a los usuarios cargar archivos de audio y obtener una clasificación en tiempo real sobre la presencia de una patología vocal.

## Estructura del Repositorio

```
Thesis/
│── Data/                 # Conjunto de datos utilizado para entrenar los modelos
│── Models/               # Modelos entrenados en formato .h5 y .pkl
│── Web/                  # Aplicación web para la predicción
│    └── modeloOptimizadoCNN.h5   # Modelo optimizado necesario para la CNN
|    └── requirements.txt         # Dependencias del proyecto
│── Notebooks/            # Notebooks de entrenamiento y evaluación de modelos
│── Jupyter/              # Scripts y experimentos en Jupyter Notebook
│── .gitignore            # Archivos ignorados en Git
│── LICENSE               # Licencia del proyecto
│── README.md             # Este archivo
│── Thesis.pdf            # Documento de la tesis
│── Thesis.pptx           # Presentación de la tesis
```

## Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone https://github.com/Wembie/Thesis.git
cd Thesis
```

### 2. Crear un entorno virtual e instalar dependencias
```bash
python -m venv venv
source venv/bin/activate  # Activar entorno virtual
pip install -r requirements.txt
```

### 3. Descargar el modelo CNN optimizado
Debido a restricciones de tamaño en GitHub, el modelo optimizado de la CNN no está incluido en el repositorio. **Es obligatorio descargarlo y colocarlo en la carpeta `Web/` para que la aplicación funcione correctamente.**

🔗 [Descargar modelo CNN optimizado](https://www.mediafire.com/file/usy3siwodmwos1a/modeloOptimizadoCNN.h5/file)

Una vez descargado, asegúrate de moverlo a la siguiente ruta dentro del repositorio:
```
Thesis/
│── Web/
│    └── modeloOptimizadoCNN.h5
```

### 4. Ejecutar la aplicación web
Para iniciar el servidor, asegúrate de estar en la carpeta `Web/` y ejecuta:
```bash
uvicorn main:app --reload
```
Luego, accede a la interfaz en:
```
http://127.0.0.1:8000
```

## Créditos
**Autores:**
- **Carlos Felipe Palacio Lozano**
- **Juan Esteban Acosta López**

**Director:** Dr. Julián Gil González

**Fecha:** 15 de agosto de 2024

---
Este proyecto es parte del trabajo de grado de Ingeniería de Sistemas y Computación en la **Pontificia Universidad Javeriana Cali**.
