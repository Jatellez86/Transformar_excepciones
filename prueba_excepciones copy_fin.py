import pandas as pd
import re
import pyproj

# Ejemplo de datos
# ruta del archivo de excepciones
datos_excep = pd.read_csv("C:\\Users\\javier.tellez\\Downloads\\Informe_Diario_Excepciones.csv")

# dataframe con los datos necesarios para el calculo
parametros = datos_excep[['Fecha',
'Operador',
'Vehiculo',
'Instante',
'DescripcionExcepcion',
'Linea',
'Coche',
'Ruta',
'Offset',
'ServBus',
'ServCond',
'Conductor',
'Parametros'
]]


# Función para extraer los valores de "x" e "y" de una cadena de caracteres
def extract_xy(string):
    pattern = 'x=\"(\d+)\"\s+y=\"(\d+)\"'
    match = re.findall(pattern, string)
    return match

# Crear una nueva columna "Extraccion" y aplicar la función a la columna "Parametros"
parametros['Extraccion'] = parametros['Parametros'].apply(lambda x: extract_xy(x))

# Crear nuevas columnas para cada valor de "x" e "y" encontrado
for i in range(parametros['Extraccion'].apply(len).max()):
    parametros[f'Extraccion {i+1} x'] = parametros['Extraccion'].apply(lambda x: x[i][0] if len(x) > i else '')
    parametros[f'Extraccion {i+1} y'] = parametros['Extraccion'].apply(lambda x: x[i][1] if len(x) > i else '')


# Definir el sistema de referencia de coordenadas UTM para Bogotá (zona 18)
utm_bogota = pyproj.Proj(proj='utm', zone=18, ellps='WGS84', datum='WGS84', units='m')

# Función para convertir coordenadas UTM a latitud y longitud
def convert_utm_to_lat_long(x, y):
    # Convertir de UTM a latitud y longitud
    lat, long = utm_bogota(x, y, inverse=True)
    return lat, long

# Aplicar la función a las columnas correspondientes
for i in range(parametros['Extraccion'].apply(len).max()):
    x_col = f'Extraccion {i+1} x'
    y_col = f'Extraccion {i+1} y'
    lat_col = f'Extraccion {i+1} lat'
    long_col = f'Extraccion {i+1} long'
    parametros[[lat_col, long_col]] = parametros.apply(lambda row: convert_utm_to_lat_long(row[x_col], row[y_col]) if row[x_col] and row[y_col] else (None, None), axis=1, result_type='expand')

print(parametros)

# escribir el dataframe en un archivo csv
parametros.to_csv('C:\\Users\\javier.tellez\\Downloads\\Prueba_Excepciones_3.csv', index=False)
