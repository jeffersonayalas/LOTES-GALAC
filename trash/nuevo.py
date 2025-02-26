from datetime import datetime

fecha_hora_str = get_celda(libro_excel, rows[0][0], 'Cliente/Proveedor', 'Fecha')

try:
    fecha_partes = fecha_hora_str.strip().split(" ", 1) #se utiliza maxsplit=1 para evitar separar mas de dos elementos

    if len(fecha_partes) >= 1: #se verifica que el array tenga al menos un elemento
        fecha_str = fecha_partes[0]
        fecha = datetime.datetime.strptime(fecha_str, '%d-%m-%Y').strftime('%d/%m/%Y')
    else:
        print("Error: Formato de fecha incorrecto. La cadena está vacía.")
        return None # o algún otro valor de error

except ValueError:
    print("Error: Formato de fecha incorrecto.  No se pudo convertir la fecha.")
    return None # o algún otro valor de error

except Exception as e:
    print(f"Error inesperado: {e}")
    return None # o algún otro valor de error

