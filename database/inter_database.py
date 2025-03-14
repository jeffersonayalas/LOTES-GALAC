##############################################################################
               ### ---- NUEVA VERSION DE APLICACION ---- ###
##############################################################################

import uuid
import requests
import xmlrpc.client
from dotenv import load_dotenv  # Importar python-dotenv
import os  # Para acceder a las variables de entorno
import json
import re
from datetime import datetime


DB_HOST="http://127.0.0.1:8000"


def insert_clients(cliente_data):
    base_url = DB_HOST  # Asegúrate de que DB_HOST esté definido con la URL base de tu API

    headers = {
        'Content-Type': 'application/json'
    }

    print("VERIFICACION DE CLIENTE:", cliente_data)

    try:
        if cliente_data != None:
            response = requests.post(f'{base_url}/clientes/', headers=headers, json=cliente_data)

            if response.status_code == 201:  # Código de éxito para creación
                return response.json()  # Devuelve la respuesta en formato JSON
            else:
                print(f'Error: {response.status_code}, {response.text}')
                return None
    except Exception as e:
        print(f'Error durante la solicitud: {e}')
        return None
    

def validar_y_generar_rif(documento):
    """
    Valida el formato del documento (RIF) y siempre retorna una lista.

    Parámetros:
        documento (str o int): El documento a validar o procesar.

    Retorna:
        - Si el formato es correcto, devuelve una lista con el documento.
        - Si el documento es solo numérico, devuelve una lista con las 4 configuraciones posibles.
        - Si el formato no es válido, devuelve una lista vacía.
    """
    # Convertir a string si es un número
    if isinstance(documento, int):
        documento = str(documento)
    
    documento = documento.strip().upper()  # Normalizar el documento
    
    # Expresión regular para validar el formato del RIF
    rif_pattern = re.compile(r'^[VJGP]-\d{6,}$')
    
    # Validar si el documento tiene un formato de RIF válido
    if rif_pattern.match(documento):
        print(f"✅ RIF válido: {documento}")
        return [documento]  # Retornar el documento en una lista
    
    # Si el documento es solo numérico, generar las 4 configuraciones
    if documento.isdigit():
        documentos = [f"{prefix}-{documento}" for prefix in ["V", "J", "G", "P"]]
        return documentos
    
    # Si no cumple con ningún formato válido, retornar una lista vacía
    return []

def get_rif(rif):
    posibles_rif = validar_y_generar_rif(rif)
    
    for rif_attempt in posibles_rif:
        
        #Se realiza busqueda de los posibles rifs en odoo (Si se encuentra se retorna el rif con el que se hizo match)
        client_odoo = buscar_cliente_odoo(rif_attempt)

        if isinstance(client_odoo, dict) and 'id' in client_odoo:
            return rif_attempt
    return None

    

def create_object_client(data):
    rif_client = data.get('rif')
    
    # Buscar cliente en Odoo
    client = buscar_cliente_odoo(rif_client)

    
    if isinstance(client, dict) and 'id' in client:
        print(f"🔍 Cliente encontrado en Odoo con {rif_client}: {client}")
        
        # Construir el nuevo cliente
        new_client = {
            "odoo_id": str(client.get('id')),
            "rif": rif_client,
            "cod_galac": data.get('cod_galac'),  # Asegúrate que este valor es válido
            "nombre_cliente": client.get('name', 'Nombre no disponible')
        }

        # Verificar que todos los campos requeridos contengan datos
        if new_client['rif'] and new_client['cod_galac']:
            cliente_json = json.dumps(data)
            return new_client
        else:
            print("Error: RIF o Código GALAC no están disponibles.")
            return None
    else:
        print(f"Error: Cliente no encontrado para RIF {rif_client}.")
        return None  # o podrías retornar un diccionario vacío {}
    

    
#lEER TXT PARA REALIZAR INSERCION DE CLIENTES 
def update_database(archivo_txt):
    
    try:
        # Suponiendo que archivo_txt es una lista de líneas o que contiene el contenido del archivo
        data_clientes = archivo_txt  # utf-8 si latin-1 falla
        hoja_cliente = []

        for linea in data_clientes:
            try:
                datos_cliente = linea.strip().split(";")  # Eliminar espacios en blanco y dividir la línea

                if len(datos_cliente) == 25 or len(datos_cliente) == 26:  # Verifica que la línea tenga 26 o 27 elementos
                    # Asignar campos a variables
                    cod_galac = datos_cliente[0]
                    nombre = datos_cliente[1]
                    rif = datos_cliente[2]

                    # Crear diccionario CLIENT
                    CLIENT = {
                        'rif': rif,
                        'cod_galac': cod_galac,
                        'nombre_cliente': nombre  # Asegúrate de que la clave sea correcta
                    }

                    print("Cliente -----------------> ", CLIENT)

                    # Ahora llamar a la función insert_clients con el CLIENT
                    CLIENT_DATA = create_object_client(CLIENT)
                    result = insert_clients(CLIENT_DATA)

                    if result:
                        print("CLIENTE AGREGADO CORRECTAMENTE: " + str(CLIENT_DATA))
                        hoja_cliente.append(CLIENT_DATA)  # Mantener un registro de los clientes agregados
                    else:
                        print("ERROR AL AGREGAR CLIENTE.")

                else:
                    print(f"Línea incorrecta, se esperaba 26 o 27 elementos: {linea.strip()}")

            except Exception as e:
                print(f"Error en la línea: {linea.strip()}. Error: {e}")

        return hoja_cliente  #Podrías devolver la lista de clientes agregados

    except FileNotFoundError as e:
        print(f"Archivo bd_clientes.txt no encontrado. {e}")

    except Exception as e:
        print(f"Error al leer o procesar el archivo: {e}")


def obtain_client(id_client: str):
    base_url = DB_HOST  # Asegúrate de que DB_HOST esté definido con la URL base de tu API
    
    headers = {
        'Content-Type': 'application/json'
    }

    print("VERIFICACION DE CLIENTE:", id_client)

    # Construye la URL con el parámetro rif_contains
    request_url = f'{base_url}/buscar-cliente/?rif_contains={id_client}'
    print("SOLICITUD HACIA:", request_url)

    try:
        # Realizar la petición GET para obtener el cliente
        response = requests.get(request_url, headers=headers)

        if response.status_code == 200:  # Código de éxito
            return response.json()  # Devuelve el cliente encontrado
        else:
            print(f'Error: {response.status_code}, {response.text}')
            return None
    except Exception as e:
        print(f'Error durante la solicitud: {e}')
        return None
    

def validate_invoice(rif: str, fecha: str):
    #Crea conexión con la API
    base_url = DB_HOST  # Asegúrate de que DB_HOST esté definido con la URL base de tu API

    headers = {
        'Content-Type': 'application/json'
    }

    # Construye la URL con los parámetros rif y fecha
    request_url = f'{base_url}/buscar-facturas-rif/{rif}?fecha={fecha}'
    print("SOLICITUD HACIA:", request_url)

    try:
        # Realizar la petición GET para obtener la factura
        response = requests.get(request_url, headers=headers)

        if response.status_code == 200:  # Código de éxito
            return response.json()  # Devuelve la factura
        else:
            print(f'Error: {response.status_code}, {response.text}')
            return None
    except Exception as e:
        print(f'Error durante la solicitud: {e}')
        return None
    

def update_drafts():
    archivo = open('clientes_facturas.txt', 'r', encoding='utf-8') 
    try:
        # Suponiendo que archivo_txt es una lista de líneas o que contiene el contenido del archivo
        data_clientes = archivo  # utf-8 si latin-1 falla
        hoja_cliente = []

        for linea in data_clientes:
            try:
                datos_cliente = linea.strip().split("\t")  # Eliminar espacios en blanco y dividir la línea
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

def verify_client_by_cod_galac(cod_galac: str) -> bool:
    base_url = DB_HOST  # Asegúrate de que DB_HOST esté definido con la URL base de tu API
    headers = {
        'Content-Type': 'application/json'
    }

    print("VERIFICACIÓN DE CLIENTE:", cod_galac)

    # Construye la URL con el parámetro cod_galac
    request_url = f'{base_url}/buscar-cliente-cod-galac/?cod_galac={cod_galac}'
    print("SOLICITUD HACIA:", request_url)

    try:
        # Realizar la petición GET para verificar el cliente
        response = requests.get(request_url, headers=headers)

        if response.status_code == 200:  # Código de éxito
            # Si el cliente existe, se espera un mensaje de éxito
            result = response.json()
            return result.get("exists")
        else:
            print(f'Error: {response.status_code}, {response.text}')
            return False
    except Exception as e:
        print(f'Error durante la solicitud: {e}')
        return False

    
############################################################################################################################
                                ### ------------------ ODOO ID --------------------- ###
############################################################################################################################

load_dotenv()

def format_name(name):
    parts = name.split(' - ')

    if len(parts) == 2:
        return parts[1]
    
    else:
        return name


def buscar_cliente_odoo(ci :str):
    url      = os.getenv('ODOO_URL')
    db       = os.getenv('ODOO_DB')
    username = os.getenv('ODOO_USERNAME')
    password = os.getenv('ODOO_PASSW')

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    common.version()

    uid = common.authenticate(db, username, password, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    client_id = models.execute_kw(db, uid, password, 'res.partner.category', 'search', [[['name','=','Clientes']]])[0]

    model_search = 'identification_id' if ((ci[0] == "V" or ci[0] == "E") and len(ci[2:]) < 8) else 'vat'
    ci = ci[2:] if (ci[0] == "V" or ci[0] == "E") else ci
    print(f"CI: {ci}")

    client_info = models.execute_kw(db, uid, password, 'res.partner', 'search', [['&',[model_search,'like', ci],['category_id','=',[client_id]]]])


    print(client_info)
    # print(client_info)
    if len(client_info) > 1:
        return buscar_cliente_odoo2(ci)

    if not client_info: #Si no devuelve nada, quiere decir que el cliente con los ids proporcionados no existen. 
        return False
    # Luego, obtenemos la información del cliente usando el id
    client_info = models.execute_kw(db, uid, password, 'res.partner', 'read', [client_info[0]], {'fields': ['vat', 'name', 'email', 'street', 'phone', 'ref']})

    if not client_info:
        return False
    
    print(client_info)
    
    client_info = client_info[0]
    print(client_info)

    name = format_name(client_info['name'])

    client = {
        'id':      client_info['id'],
        'name':    name,
        'email':   client_info['email'],
        'ci':      client_info['vat'],
        'street':  client_info['street'], 
        'phone':   client_info['phone'],
        'ref':     client_info['ref'] 
        }
    
    return client


def buscar_cliente_odoo2(ci: str):
    url      = os.getenv('ODOO_URL')
    db       = os.getenv('ODOO_DB')
    username = os.getenv('ODOO_USERNAME')
    password = os.getenv('ODOO_PASSW')

    # Conexión al servidor
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    common.version()

    uid = common.authenticate(db, username, password, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    # Obtener el ID de la categoría 'Clientes'
    client_id = models.execute_kw(db, uid, password, 'res.partner.category', 'search', [[['name', '=', 'Clientes']]])[0]

    # Determinar el campo de búsqueda basado en el formato de ci
    model_search = 'identification_id' if ((ci[0] == "V" or ci[0] == "E") and len(ci[2:]) < 8) else 'vat'
    ci = ci[2:] if (ci[0] == "V" or ci[0] == "E") else ci
    print(f"CI: {ci} || Model: {model_search}")

    # Búsqueda de cliente con filtros por identificación y category_id
    client_info = models.execute_kw(db, uid, password, 'res.partner', 'search',
                                    [['&', [model_search, 'like', ci], ['category_id', '=', client_id]]])

    if not client_info:
        return False

    # Leer información del cliente usando el ID obtenido
    client_info = models.execute_kw(db, uid, password, 'res.partner', 'read', [client_info],
                                    {'fields': ['parent_id', 'vat', 'name', 'email', 'street', 'phone', 'ref',
                                                'parent_name']})

    # Verificar si el cliente tiene un parent_id
    if client_info and client_info[0]['parent_id']:
        parent_id = client_info[0]['parent_id'][0]  # Obtener el ID del parent
        # Buscar información del parent_id
        parent_info = models.execute_kw(db, uid, password, 'res.partner', 'read', [parent_id],
                                        {'fields': ['id', 'name', 'vat', 'email', 'street', 'phone', 'ref']})

        parent_info = parent_info[0]
        client={
            'id': parent_info['id'],
            'name': parent_info['name'],
            'email': parent_info['email'],
            'ci': parent_info['vat'],
            'street': parent_info['street'],
            'phone': parent_info['phone'],
            'ref': parent_info['ref']
        }

        return client

    return False  # Si no hay parent_id, devolver False



        
                
          
