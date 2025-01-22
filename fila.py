import pandas as pd

def obtener_numero_fila_por_valor(libro_excel, columna, valor):
    """Obtiene el número de fila (iniciando en 1) de una celda con un valor específico en una columna dada."""
    try:
        fila = libro_excel[libro_excel[columna] == valor].index[0] + 1  # +1 para que la numeración empiece en 1
        return fila
    except (FileNotFoundError, KeyError, IndexError):
        return None  # Manejo de errores


# ---- LEER EXCEL ---- #
def obtener_elemento_por_fila_columna(libro_excel, columna, numero_fila):
    """
    Obtiene un elemento de una columna específica dado el número de fila (empezando en 1).
    """
    try:
        elemento = libro_excel.iloc[numero_fila - 1][columna] # -1 porque pandas comienza en 0, y número de fila en 1
        return elemento
    except (FileNotFoundError, KeyError, IndexError):
        return None  # Manejo de errores


def get_celda(libro_excel, id_busqueda, columna_rif, columna_dato):
    fila_buscar = obtener_numero_fila_por_valor(libro_excel, columna_rif, id_busqueda)
    dato = obtener_elemento_por_fila_columna(libro_excel, columna_dato, fila_buscar)
    return dato







