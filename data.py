import pandas as pd 
import os
import psycopg2

def open_archives(ruta_excel): #Funcion se encargar de abrir el archivo excel y abrir un archivo txt en modo de escritura, debe retornar ambos archivos
    # Lee ambos archivos Excel
    try:
        df_plantilla = pd.read_excel(ruta_excel, header=0)
       
        return df_plantilla
    except FileNotFoundError:
        print("Uno o ambos archivos no se encontraron.")
        exit() # Sale del programa si no encuentra los archivos
    except Exception as e:
        print(f"Ocurrió un error al leer los archivos: {e}")
        exit()
