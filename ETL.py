# -*- coding: utf-8 -*-
"""ETL.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zC7KqgEjQn3azj7-NumrGi0ywK6NhipT
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import requests


#----------------------------------------------
#               Generacion de datos
#--------------------------------------------
# Semilla para reproducibilidad
np.random.seed(42)

n = 1000  # Número de registros

# Crear catálogo de productos con precios
catalogo = {
    pid: round(np.random.uniform(5000, 20000), 2)
    for pid in range(1, 21)
}

product_ids = list(catalogo.keys())

# Asignar categorías no uniformemente a los product_id
categorias = ['Electronica', 'Ropa', 'Libros', 'Hogar', 'Jugueteria', 'Deportes', 'Belleza']
distribucion = {
    'Electronica': [1, 2, 3, 4, 5],
    'Ropa': [6, 7],
    'Libros': [8, 9],
    'Hogar': [10, 11, 12],
    'Jugueteria': [13],
    'Deportes': [14, 15, 16],
    'Belleza': [17, 18, 19, 20]
}

# Crear un diccionario product_id con su respectiva categoría
id_to_category = {pid: cat for cat, pids in distribucion.items() for pid in pids}

# Generar fechas aleatorias dentro del último año
start_date = datetime.now() - timedelta(days=180)
dates = [start_date + timedelta(days=random.randint(0, 180)) for _ in range(n)]

# Selección aleatoria de productos
selected_product_ids = np.random.choice(product_ids, size=n)
prices = [catalogo[pid] for pid in selected_product_ids]
categories = [id_to_category[pid] for pid in selected_product_ids]


# Construcción del DataFrame
data = pd.DataFrame({
    'id': range(1, n+1),
    'date': dates,
    'product_id': selected_product_ids,
    'price': prices,
    'category': categories
})

conteo_por_fecha = data['date'].value_counts().sort_index()

# Paso 2: Generar ventas totales por fecha (~50,000 ± 15,000)
ventas_totales_fecha = pd.Series(
    np.random.uniform(35000, 65000, size=len(conteo_por_fecha)),
    index=conteo_por_fecha.index
)

num_outliers = 10  # número de fechas con outliers
fechas_outliers = np.random.choice(ventas_totales_fecha.index, size=num_outliers, replace=False)

for fecha in fechas_outliers:
    multiplicador = np.random.choice([0.2, 0.3, 2, 3, 4])  # muy bajo o muy alto
    ventas_totales_fecha[fecha] *= multiplicador

# Paso 3: Calcular ventas individuales distribuidas uniformemente
ventas_por_fila = []
for fecha in data['date']:
    total_ventas = ventas_totales_fecha[fecha]
    cantidad_filas = conteo_por_fecha[fecha]
    venta_individual = total_ventas / cantidad_filas
    ventas_por_fila.append(venta_individual)

data['sales'] = ventas_por_fila

# Coordenadas de Bogotá
latitude = 4.7110
longitude = -74.0721

# Fechas según los datos de ventas
fechas_unicas = pd.to_datetime(data['date']).dt.date.unique()
min_fecha = min(fechas_unicas)
max_fecha = max(fechas_unicas)

start_api = min_fecha.strftime('%Y-%m-%d')
end_api = max_fecha.strftime('%Y-%m-%d')

# Construcción de la URL de la API
url = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={latitude}&longitude={longitude}"
    f"&start_date={start_api}&end_date={end_api}"
    f"&daily=temperature_2m_max,temperature_2m_min"
    f"&timezone=America/Bogota"
)

# Petición a la API
response = requests.get(url)
response.raise_for_status()
weather_data = response.json()

# Extraer listas
temps_max = weather_data['daily']['temperature_2m_max']
temps_min = weather_data['daily']['temperature_2m_min']
dates_weather = weather_data['daily']['time']

# Crear lista con datos, colocando NaN si hay valores faltantes
weather_entries = []
for date, max_t, min_t in zip(dates_weather, temps_max, temps_min):
    if max_t is not None and min_t is not None:
        media = (max_t + min_t) / 2
    else:
        media = np.nan
    weather_entries.append((date, media))

# Crear DataFrame
data_clima = pd.DataFrame(weather_entries, columns=['date', 'temp_media'])
data_clima['date'] = pd.to_datetime(data_clima['date'])

#Combinar datas
data['date'] = pd.to_datetime(data['date']).dt.date
data_clima['date'] = pd.to_datetime(data_clima['date']).dt.date
data_final = data.merge(data_clima, on='date', how='left')

#-------------------------------------------------------------
#-                       Limpieza
#-------------------------------------------------------------

data_final['date'] = pd.to_datetime(data_final['date'])

# Crear columna auxiliar con solo el día del mes
data_final['day_of_month'] = data_final['date'].dt.day

# Calcular el promedio de temperatura por día del mes (usando solo los no nulos)
avg_temp_by_day = data_final.dropna(subset=['temp_media']).groupby('day_of_month')['temp_media'].mean()

# Función para aplicar ese promedio solo a los nulos
def fill_temp(row):
    if pd.isna(row['temp_media']):
        return avg_temp_by_day.get(row['day_of_month'], None)
    else:
        return row['temp_media']

# Aplicar la función fila por fila
data_final['temp_media'] = data_final.apply(fill_temp, axis=1)

# Opcional: eliminar la columna auxiliar
data_final.drop(columns=['day_of_month'], inplace=True)
data_modelo= data_final.copy()
data_modelo = data.groupby('date')['sales'].sum().reset_index()
data_modelo.columns = ['ds', 'y']

# Eliminar outliers en sales usando el método IQR
Q1 = data_modelo['y'].quantile(0.25)
Q3 = data_modelo['y'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
data_modelo = data_modelo[(data_modelo['y'] >= lower_bound) & (data_modelo['y'] <= upper_bound)].reset_index(drop=True)

#--------------------------------------------------------------
#                    guardar datos
#--------------------------------------------------------------
data_modelo.to_csv('data_modelo.csv', index=False)
data_final.to_csv('data_final.csv', index=False)

