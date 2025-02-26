import pandas as pd # type: ignore

def buscar_en_excel_pandas(archivo1, archivo2, columna_buscar, valor_buscar):
    """
    Busca un valor en dos hojas de Excel usando Pandas y devuelve las filas que lo contienen.

    Args:
        archivo1: Ruta al primer archivo Excel.
        archivo2: Ruta al segundo archivo Excel.
        columna_buscar: Nombre de la columna donde buscar (ej. "ColumnaA").
        valor_buscar: El valor a buscar.

    Returns:
        Una tupla con dos DataFrames: el primero contiene las filas del archivo1 que coinciden,
        el segundo contiene las filas del archivo2 que coinciden. Devuelve (None, None) si hay un error.
    """
    try:
        df1 = pd.read_excel(archivo1)
        df2 = pd.read_excel(archivo2)

        resultados1 = df1[df1[columna_buscar].str.lower().str.contains(valor_buscar.lower())]
        resultados2 = df2[df2[columna_buscar].str.lower().str.contains(valor_buscar.lower())]

        return resultados1, resultados2

    except FileNotFoundError:
        print("Uno o ambos archivos no se encontraron.")
        return None, None
    except KeyError:
        print(f"La columna '{columna_buscar}' no se encontró en uno o ambos archivos.")
        return None, None
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return None, None


# Ejemplo de uso:
archivo1 = "excel1.xlsx"  # Reemplaza con la ruta a tu primer archivo Excel
archivo2 = "excel2.xlsx"  # Reemplaza con la ruta a tu segundo archivo Excel
columna_buscar = "ColumnaA"  # Reemplaza con el nombre de la columna
valor_buscar = "ejemplo"  # Reemplaza con el valor a buscar

resultados_archivo1, resultados_archivo2 = buscar_en_excel_pandas(archivo1, archivo2, columna_buscar, valor_buscar)

if resultados_archivo1 is not None:
    print("Resultados en archivo 1:")
    print(resultados_archivo1)
else:
    print("No se encontraron resultados en el archivo 1 o hubo un error.")

if resultados_archivo2 is not None:
    print("\nResultados en archivo 2:")
    print(resultados_archivo2)
else:
    print("No se encontraron resultados en el archivo 2 o hubo un error.")

