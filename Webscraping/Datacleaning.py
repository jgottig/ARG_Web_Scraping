import os
import pandas as pd

# Ruta de la carpeta que contiene los archivos CSV (en este caso, la carpeta 'Bajadas' en la misma ubicación que el script)
carpeta = r'C:\Users\jgott\OneDrive\Desktop\Test Streamlit\simple-streamlit-app\Bajadas'    

# Lista para almacenar los DataFrames de cada archivo CSV
dataframes = []

# Recorre los archivos en la carpeta
for archivo in os.listdir(carpeta):
    if archivo.endswith('.csv'):
        ruta_completa = os.path.join(carpeta, archivo)
        # Lee cada archivo CSV y agrega el DataFrame a la lista
        df = pd.read_csv(ruta_completa)
        dataframes.append(df)

# Concatena los DataFrames en uno solo
df_consolidado = pd.concat(dataframes, ignore_index=True)

#Limpieza de titulos
df_consolidado = df_consolidado.rename(columns={df_consolidado.columns[0]: 'Comercio',
                                                df_consolidado.columns[1]: 'Distancia',
                                                df_consolidado.columns[2]: 'Precio de lista',
                                                df_consolidado.columns[3]: 'Promo A',
                                                df_consolidado.columns[4]: 'Promo B',
                                                 df_consolidado.columns[5]: 'Nombre Del Articulo',
                                                 df_consolidado.columns[6]: 'Articulo + Pagina'})

#Elimino duplicados
# Concatena las columnas "Comercio" y "Nombre Del Articulo"
df_consolidado['Concatenado'] = df_consolidado['Comercio'] + ' ' + df_consolidado['Nombre Del Articulo']
df_consolidado = df_consolidado.drop_duplicates(subset='Concatenado', keep='first')

df_consolidado['Precio de lista'] = df_consolidado['Precio de lista'].str.replace('[^\d,]', '', regex=True)
df_consolidado['Precio de lista'] = df_consolidado['Precio de lista'].str.replace(',', '.')
df_consolidado['Precio de lista'] = pd.to_numeric(df_consolidado['Precio de lista'], errors='coerce')

# Agrupa por "Nombre Del Articulo" y encuentra el valor máximo de "Precio de lista" para cada grupo
max_precio_lista_por_articulo = df_consolidado.groupby('Nombre Del Articulo')['Precio de lista'].transform('max')

# Crea la nueva columna "Precio Final" y llena los valores según la lógica especificada
df_consolidado['Precio Final'] = df_consolidado['Precio de lista'].fillna(max_precio_lista_por_articulo)

# Crea la nueva columna "Cadena" basada en la lógica especificada
df_consolidado['Cadena'] = ''

# Asigna valores según la lógica
df_consolidado.loc[df_consolidado['Comercio'].str.contains('La Gallega', case=False, na=False), 'Cadena'] = 'La Gallega'
df_consolidado.loc[df_consolidado['Comercio'].str.contains('F U L', case=False, na=False), 'Cadena'] = 'Full'
df_consolidado.loc[df_consolidado['Comercio'].str.contains('C O T O', case=False, na=False), 'Cadena'] = 'COTO'
df_consolidado.loc[df_consolidado['Comercio'].str.contains('Carrefour', case=False, na=False), 'Cadena'] = 'Carrefour'
df_consolidado.loc[df_consolidado['Comercio'].str.contains('Axion', case=False, na=False), 'Cadena'] = 'Axion'
df_consolidado.loc[df_consolidado['Comercio'].str.contains('S I M P L I C I T Y', case=False, na=False), 'Cadena'] = 'Simplicity'
df_consolidado.loc[df_consolidado['Comercio'].str.contains('Jumbo', case=False, na=False), 'Cadena'] = 'Jumbo'
df_consolidado.loc[df_consolidado['Comercio'].str.contains('Libertad', case=False, na=False), 'Cadena'] = 'Libertad'

#Crear Data Frame de Productos:
df_productos = df_consolidado[['Nombre Del Articulo']].drop_duplicates().reset_index(drop=True)

# Crea el DataFrame Cadenas_Precios_Bajos

df_Cadenas_Precios_Bajos = df_consolidado.loc[df_consolidado.groupby(['Cadena', 'Nombre Del Articulo'])['Precio Final'].idxmin()]

ruta_consolidado_csv = r'C:\Users\jgott\OneDrive\Desktop\Test Streamlit\simple-streamlit-app\NUEVO.csv' 
ruta_productos_csv = r'C:\Users\jgott\OneDrive\Desktop\Test Streamlit\simple-streamlit-app\Productos.csv'
ruta_cadena_precios_bajos_csv = r'C:\Users\jgott\OneDrive\Desktop\Test Streamlit\simple-streamlit-app\Cadena_Precios_Bajos.csv'

# Guarda el DataFrame modificado en un nuevo archivo CSV
df_consolidado.to_csv(ruta_consolidado_csv, index=False)
df_productos.to_csv(ruta_productos_csv, index=False)
df_Cadenas_Precios_Bajos.to_csv(ruta_cadena_precios_bajos_csv, index=False)