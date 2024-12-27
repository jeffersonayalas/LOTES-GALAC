import pandas as pd 
import os

# --- functions --- #
def leer_excel(ruta_excel, nombre_cliente, columna_nombre="Cliente"):
    try:
        df = pd.read_excel(ruta_excel, header=0)
        #print(df) #lIBRO COMPLETO - incluyendo planes
        #print(df.columns) #Celdas
        df[columna_nombre].str.contains(nombre_cliente).any() #Devuelve True si el cliente fue encontrado
        return df[columna_nombre].str.contains(nombre_cliente).any() #any devuelve True si al menos un valor es True
    except FileNotFoundError:
        print('No encontrado')
        return False
    except Exception as e:
        print(f"Error al leer el archivo Excel: {e}")
        return False

# Lee ambos archivos Excel
try:
    df_plantilla = pd.read_excel("plantilla.xlsx", header=0, sheet_name="PLANTILLA DE FACTURAS GALAC")
    #df_otro = pd.read_excel("otro_archivo.xlsx", header=0, sheet_name="NombreDeLaHoja") # Reemplaza con el nombre de tu hoja y el archivo

    #Archivo txt
    f = open("clientes.exp", "r", encoding="latin-1")
except FileNotFoundError:
    print("Uno o ambos archivos no se encontraron.")
    exit() # Sale del programa si no encuentra los archivos
except Exception as e:
    print(f"Ocurrió un error al leer los archivos: {e}")
    exit()

# Define las columnas a comparar (ajusta según tus necesidades)
columnas_a_comparar = ["0", "1", "2"] # Reemplaza con los nombres de tus columnas

input_cols = [0, 1, 2]
df = pd.read_excel("plantilla.xlsx", header=0, sheet_name="PLANTILLA DE FACTURAS GALAC", )
df_cols = df.columns
#f = open("myfile.txt", "w")


#Leer archivo txt

count = 0
libro = open("clientes_faltantes.txt", "w")
clientes_facturas = open("clientes_facturas.txt", "w")
for linea in f:
    lineas = linea.split(';') #Obtenemos un arreglo con los datos del cliente
    print(lineas)

    if leer_excel('SUSCRIPTION.xlsx', lineas[1]):
        clientes_facturas.write(linea)
        continue
    else: 
        
        #Clientes no encontrados
        libro.write(linea) #Escribe el nombre del cliente
        count += 1
    

#Realizar busqueda entre txt y excel
for col in df_cols:
    #print(col)
    var = str(df[col].head(12))
    #print(df[col].head())
    #print(df[col].head(12)) # DAR FORMATO A LA SALIDA# 
    #f.write(var)

#libro = f.read()
#print(libro)

#Exportar archivos
df.to_csv("export.csv", sep=",", header=True, index=False)
f.close()

# --- condiciones --- #
'''
nombre_cliente = lineas[1]
if nombre_cliente:
    print(f"El nombre del cliente es: {nombre_cliente}")
else:
    print("No se pudo obtener el nombre del cliente.")
'''



