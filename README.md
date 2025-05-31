# Predicción de Ventas y Carga de Datos a PostgreSQL y Supabase

Este proyecto implementa un pipeline automatizado de análisis de ventas que incluye generación de datos, entrenamiento de un modelo de predicción usando machine learning para series de tiempo y carga a bases de datos.

---

## Estructura del Proyecto

El pipeline está compuesto por tres scripts Python, cada uno con su respectivo archivo `.bat` para ejecución automatizada:

1. **ETL (`ETL.py`)**
   - Genera datos sintéticos de ventas.
   - Extrae datos de temperatura de Bogotá desde una API open-meteo.
   - Limpia nulos y outliers.
   - Genera un archivo con la data limpiada

2. **Modelo (`modelo.py`)**
   -Carga la data limpiada 
   - Entrena un modelo de series temporales con machine learning (skforecast) RandomForestregressor, aplica gridsearch para optimizacion de hiperparametros.
   - Predice ventas y guarda resultados en `data_predicha.csv`.

4. **Carga (`load_db.py`)**
   - Carga los datos a PostgreSQL local.
   - Exporta y sincroniza la tabla con Supabase.
   - Calcula RMSE por categoría.

Cada script tiene un archivo `.bat` asociado que genera un log (`.txt`) del proceso.

---

##  Instrucciones de Uso

### 1. Requisitos Previos

- Tener instalado **Anaconda** o **Miniconda**.
- Tener instalado **PostgreSQL local** (puerto por defecto 5433).
- Tener cuenta y proyecto en **Supabase** con base de datos PostgreSQL activa.

### 2. Instalación y Entorno

1. Crea un nuevo entorno de Conda:

```bash
conda create -n cun_env python=3.10
conda activate cun_env
```

2. Instala los paquetes necesarios:

```bash
pip install numpy pandas scikit-learn skforecast==0.12.0 jupyter sqlalchemy psycopg2-binary
```
```bash
pip install notebook
```

---

##  Ejecución Paso a Paso

### 1. Ejecutar ETL

```bash
etl.bat
```

- Ejecuta `ETL.py`
- Genera y limpia los datos
- Log generado: `etl_log.txt`
- Genera los archivos data_modelo (data para entrenar modelo de sales predictions) y data_final (data con los demas variables a cargar en postgress) 

### 2. Ejecutar el Modelo

```bash
modelo.bat
```

- Ejecuta `modelo.py`
- Entrena modelo de predicción de ventas
- Exporta archivo `data_predicha.csv`
- Log generado: `modelo_log.txt`

### 🗃️ 3. Cargar Datos en PostgreSQL y Supabase

```bash
load_db.bat
```

- Ejecuta `load_db.py`
- Sube los datos a PostgreSQL
- Crea copia en Supabase
- Calcula el RMSE por categoría
- Log generado: `load_db_log.txt`
- sales_categoria.csv 

---

## 🔧 Configuración

### 🔁 Rutas del Entorno

Asegúrate de modificar en los archivos `.bat` esta línea:

```bat
CALL C:\Users\TU_USUARIO\anaconda3\Scripts\activate.bat cun_env
```

Reemplaza `TU_USUARIO` con tu nombre de usuario real en Windows y verifica que `cun_env` sea el nombre correcto del entorno.

---

## Logs

Cada `.bat` genera un archivo `.log` o `.txt` donde se guarda el detalle del proceso y los errores:

- `etl_log.txt`
- `modelo_log.txt`
- `load_db_log.txt`

---

## 🛠️ Personalización

- Modifica las credenciales de PostgreSQL y Supabase en `load_db.py` si usas otros puertos, hosts o contraseñas.
- Asegúrate de que la base de datos local `prueba_cun` esté creada antes de ejecutar.

---

## 🕒 Automatización Diaria (Programador de Tareas de Windows)

Puedes ejecutar automáticamente el pipeline todos los días a la hora que desees:

### 1. Abrir el Programador de Tareas:
- Buscar "Programador de tareas" en el menú de Windows.

### 2. Crear una tarea básica:
- **Nombre:** `Ejecutar_Pipeline_Ventas`
- **Desencadenador:** Todos los días a las x:xx PM
- **Acción:** Iniciar un programa
- **Programa/script:** 
```bash
cmd.exe
```
- **Agregar argumentos:** 
```bash
/c "C:\Users\usuario\Documents\Prueba Tecnica DS\CUN\etl.bat" && "C:\Users\usuario\Documents\Prueba Tecnica DS\CUN\modelo.bat" && "C:\Users\usuario\Documents\Prueba Tecnica DS\CUN\load_db.bat"
```

> ⚠️ Asegúrate de ajustar las rutas reales según la ubicación de los archivos `.bat`.

---

##  Dependencias

- `pandas`
- `numpy`
- `sklearn`
- `skforecast==0.12.0`
- `sqlalchemy`
- `psycopg2-binary`
- `jupyter` (opcional)

---

##  Validación

- Revisa las tablas generadas en PostgreSQL y Supabase.
- Asegúrate de que el archivo `data_predicha.csv` contenga las predicciones.
- Verifica los logs para posibles errores.

---

## 📬 Contacto

Si tienes preguntas, sugerencias o deseas colaborar, no dudes en crear un issue o contactarme directamente luiscarlosps93@gmail.com.
