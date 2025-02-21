from operate_database import update_database
import requests

#Actualizar base de datos
archivo_datos = open('db_contactos.txt', "r", encoding='utf-8')


def leer_txt(archivo_txt):
    """Lee el archivo TXT e inserta los datos en la base de datos."""
    try:
        data_clientes = archivo_txt #utf-8 si latin-1 falla
        hoja_cliente = ""
        for linea in data_clientes:
            datos_cliente = linea.split(";") # strip() para eliminar espacios en blanco
                
            print(len(datos_cliente))
            if len(datos_cliente) == 27 or len(datos_cliente) == 26: #Verifica que la línea tenga 3 elementos
                cod_galac, nombre_cliente, rif = datos_cliente[0], datos_cliente[1], datos_cliente[2]
                try:
                    print("Cliente: ", datos_cliente)
                    enviar_cliente(None, rif, cod_galac, nombre_cliente)
                    sep = "---------------------------------------------\n"
                    hoja_cliente += str(sep + "Nombre: " + str(nombre_cliente) + "\nRif: " + str(rif) + "\n")
                except Exception as e:
                        print(f"Error en la linea: {linea.strip()}. Error: {e}")
            else:
                print(f"Línea incorrecta: {linea.strip()}")
                continue
        return hoja_cliente
                    

    except FileNotFoundError as e:
        print("Archivo bd_clientes.txt no encontrado. {e}")
    except Exception as e:
        print(f"Error al leer o procesar el archivo: {e}")


def enviar_cliente(odoo_id, rif, cod_galac, nombre_cliente):
    # Definición del cliente
    cliente_data = {
        "odoo_id": odoo_id,
        "rif": rif,
        "nombre_cliente": nombre_cliente,
        "cod_galac": cod_galac
    }

    url = "http://localhost:8000/clientes/"  # Reemplaza con la URL de tu API

    response = requests.post(url, json=cliente_data)

    if response.status_code == 201:  # Código de éxito para creación
        print("Cliente agregado con éxito:", response.json())
    else:
        print("Error al agregar cliente:", response.status_code, response.text) 


leer_txt(archivo_datos)