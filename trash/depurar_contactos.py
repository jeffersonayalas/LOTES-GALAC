
import pandas as pd


def encontrar_proximo_rif(libro_excel, columna_rif, rif_inicial):
    """
    Encuentra el RIF que sigue después de un RIF inicial en un archivo Excel.

    Args:
        excel_path: La ruta al archivo Excel.
        columna_rif: El nombre de la columna que contiene los RIFs.
        rif_inicial: El RIF a partir del cual se busca el siguiente.

    Returns:
        El RIF que sigue al RIF inicial, o None si no se encuentra.
    """
    try:
        

        # Encuentra el índice del RIF inicial
        indice_inicial = libro_excel[libro_excel[columna_rif] == rif_inicial].index

        if indice_inicial.empty:
            return None # RIF inicial no encontrado #Quiere decir que no se encontro el elemento

        indice_inicial = indice_inicial[0] # toma el primer indice si hay varios.
                                                # Obtiene el siguiente índice
                                                
        indice_siguiente = indice_inicial + 1


        if pd.notna(libro_excel.loc[indice_siguiente, columna_rif]):
            return libro_excel.loc[indice_siguiente, columna_rif]
        elif(indice_siguiente >= len(libro_excel)):
            return None
        else:
            return None

    except KeyError:
        print(f"Error: Columna '{columna_rif}' no encontrada en el archivo Excel.")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None
    

def proximo_producto(libro_excel, numero_fila, columna):
    producto = libro_excel.loc[numero_fila, columna] 
    return producto




# Ejemplo de uso:
#excel_file = "ruta/a/tu/archivo.xlsx"  # Reemplaza con la ruta a tu archivo
#rif_column = "RIF"  # Reemplaza con el nombre de tu columna
#initial_rif = "J123456"

#next_rif = encontrar_proximo_rif(excel_file, rif_column, initial_rif)
""" 
if next_rif is not None:
    print(f"El RIF siguiente a '{initial_rif}' es: {next_rif}")
else:
    print(f"No se encontró un RIF siguiente a '{initial_rif}'.")
"""
 