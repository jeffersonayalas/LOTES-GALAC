import uuid
import requests
import xmlrpc.client
from dotenv import load_dotenv  # Importar python-dotenv
import os  # Para acceder a las variables de entorno
import json
import re
from datetime import datetime

DB_HOST="http://127.0.0.1:8000"

def update_drafts():
    """Lee el archivo TXT e inserta los datos en la base de datos."""
    archivo = open('BORRADORES.txt', 'r', encoding='utf-8') 
    try:
        # Suponiendo que archivo_txt es una lista de líneas o que contiene el contenido del archivo
        data_clientes = archivo  # utf-8 si latin-1 falla
        hoja_cliente = []

        for linea in data_clientes:
            try:
                datos_cliente = linea.strip().split(";")  # Eliminar espacios en blanco y dividir la línea
                print(len(datos_cliente))

                if len(datos_cliente) == 82:
                    # Crear diccionario CLIENT
                    DRAFT = {
                        "codigo_borrador": datos_cliente[0],
                        "fecha": str(datetime.strptime(datos_cliente[1], '%d/%m/%Y')),
                        "codigo_galac": datos_cliente[2],
                        "vendedor": datos_cliente[3],
                        "observaciones": datos_cliente[4],
                        "monto_exento_descuento": datos_cliente[5],
                        "base_imp_d_des": datos_cliente[6],
                        "total_renglones": datos_cliente[7],
                        "total_iva": datos_cliente[8],
                        "total_facturas": datos_cliente[9],
                        "por_desc": datos_cliente[10],
                        "status_factura": datos_cliente[14],  # Corregido: índice correcto
                        "tipo_documento": datos_cliente[15],  # Corregido: índice correcto
                        "usar_dir_fiscal": datos_cliente[16],  # Corregido: índice correcto

    
                        # Detalles del artículo
                        "descripcion": datos_cliente[67],
                        "cantidad": datos_cliente[69],
                        "precio_sin_iva": datos_cliente[70],
                        "precio_con_iva": datos_cliente[71],

                        # Porcentaje de base
                        "porcentaje_base": datos_cliente[74],
                    }

                    # Manejar el campo ‘porcentaje_base’ para evitar errores
                    if DRAFT['porcentaje_base'] == '':
                        DRAFT['porcentaje_base'] = 0.0  # O un valor que tenga sentido en tu contexto

                    print("Cliente -----------------> ", DRAFT)

                    # Ahora llamar a la función insert_clients con el CLIENT
                    result = insert_drafts(DRAFT)
                    #result = None

                    if result:
                        print("BORRADOR AGREGADO CORRECTAMENTE: " + str(DRAFT))
                        hoja_cliente.append(DRAFT)  # Mantener un registro de los clientes agregados
                    else:
                        print("ERROR AL AGREGAR BORRADOR.")
                    
                else:
                    print(f"Línea incorrecta, se esperaba 87 elementos: {linea.strip()}")
                
            except Exception as e:
                print(f"Error en la línea: {linea.strip()}. Error: {e}")

        return hoja_cliente  #Podrías devolver la lista de clientes agregados

    except FileNotFoundError as e:
        print(f"Archivo bd_clientes.txt no encontrado. {e}")

    except Exception as e:
        print(f"Error al leer o procesar el archivo: {e}")

def insert_drafts(draft_data):
    # URL del endpoint donde se va a insertar el borrador
    base_url = DB_HOST  # Asegúrate de que DB_HOST esté definido correctamente

    # Realizar la petición POST a la API
    headers = {
        'Content-Type': 'application/json'
    }

    # Construye la URL del endpoint de borradores
    request_url = f'{base_url}/borradores/'
    print("SOLICITUD HACIA:", request_url)

    try:
        # Realizar la petición POST para insertar el borrador
        response = requests.post(request_url, json=draft_data, headers=headers)

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200 or response.status_code == 201:  # 201 para creación exitosa
            print("Borrador insertado con éxito:", response.json())  # Procesar la respuesta según tus necesidades
            return response.json()  # Devuelve la respuesta del servidor
        else:
            print(f"Error al insertar borrador: {response.status_code}, {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error durante la solicitud: {e}")
        return None
    
def validate_draft(atributos):
    # Crea conexión con la API
    base_url = DB_HOST  # Asegúrate de que DB_HOST esté definido con la URL base de tu API

    headers = {
        'Content-Type': 'application/json'
    }

    # Construye la URL con los parámetros especificados
    request_url = f"{base_url}/consultar-borrador/?codigo_galac={atributos[2]}&"
    request_url += f"fecha={datetime.strptime(atributos[1], '%d/%m/%Y')}&"
    request_url += f"observaciones={atributos[4]}&"

    """ 
    request_url += f"total_facturas={atributos[9]}&"
    request_url += f"base_imp_d_desc={atributos[6]}""
    """

    print("SOLICITUD HACIA:", request_url)

    try:
        # Realizar la petición GET para consultar el borrador
        response = requests.get(request_url, headers=headers)

        if response.status_code == 200:  # Código de éxito
            return response.json()  # Devuelve la respuesta del borrador
        else:
            print(f'Error: {response.status_code}, {response.text}')
            return None
            
    except Exception as e:
        print(f'Error durante la solicitud: {e}')
        return None
    

update_drafts()