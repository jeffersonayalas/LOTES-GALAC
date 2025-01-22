def obtener_nombre_cliente(id_factura, ruta_facturas, ruta_clientes):
    """Obtiene el nombre del cliente a partir del ID de la factura.

    Args:
        id_factura: El ID de la factura a buscar.
        ruta_facturas: La ruta al archivo facturas.txt.
        ruta_clientes: La ruta al archivo bd_clientes.txt.

    Returns:
        El nombre del cliente, o None si no se encuentra.
    """
    try:
        with open(ruta_facturas, 'r', encoding='utf-8') as archivo_facturas:
            for linea in archivo_facturas:
                partes = linea.strip().split(';') # Ajusta el delimitador si es necesario (',', ' ', etc.)
                if partes[0] == id_factura: # Asume que el ID de la factura está en la primera columna
                    id_cliente = partes[1] # Asume que el ID del cliente está en la segunda columna. Ajusta si es diferente
                    break  # Sale del bucle una vez encontrado el ID
            else:  # Se ejecuta si el bucle termina sin encontrar el ID
                return None

        with open(ruta_clientes, 'r', encoding='utf-8') as archivo_clientes:
            for linea in archivo_clientes:
                partes = linea.strip().split(';') #Ajusta el delimitador si es necesario
                if partes[0] == id_cliente: # Asume que el ID del cliente está en la primera columna
                    return partes[1] # Asume que el nombre del cliente está en la segunda columna. Ajusta si es diferente
            else:
                return None # No se encontró el cliente

    except FileNotFoundError:
        return None # Maneja el caso de archivos no encontrados


# Ejemplo de uso:
id_factura_a_buscar = "12345"  # Reemplaza con el ID de la factura que deseas buscar
ruta_facturas = "facturas.txt"
ruta_clientes = "bd_clientes.txt"

nombre_cliente = obtener_nombre_cliente(id_factura_a_buscar, ruta_facturas, ruta_clientes)

if nombre_cliente:
    print(f"El nombre del cliente para la factura {id_factura_a_buscar} es: {nombre_cliente}")
else:
    print(f"No se encontró el cliente para la factura {id_factura_a_buscar}")

