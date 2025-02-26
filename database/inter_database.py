##############################################################################
               ### ---- NUEVA VERSION DE APLICACION ---- ###
##############################################################################

import uuid
import requests
import xmlrpc.client
from dotenv import load_dotenv  # Importar python-dotenv
import os  # Para acceder a las variables de entorno
import json


DB_HOST="http://127.0.0.1:8000"


def insert_clients(cliente_data):
    base_url = DB_HOST  # Asegúrate de que DB_HOST esté definido con la URL base de tu API

    headers = {
        'Content-Type': 'application/json'
    }

    print("VERIFICACION DE CLIENTE:", cliente_data)

    # Realizar la petición POST para insertar un cliente
    print("SOLICITUD HACIA:", f'{base_url}/clientes')

    try:
        response = requests.post(f'{base_url}/clientes', headers=headers, json=cliente_data)

        if response.status_code == 201:  # Código de éxito para creación
            return response.json()  # Devuelve la respuesta en formato JSON
        else:
            print(f'Error: {response.status_code}, {response.text}')
            return None
    except Exception as e:
        print(f'Error durante la solicitud: {e}')
        return None
    

def create_object_client(data):
    rif_client = data.get('rif')
    
    # Buscar cliente en Odoo
    client = buscar_cliente_odoo(rif_client)

    if isinstance(client, dict) and 'id' in client:
        print(f"🔍 Cliente encontrado en Odoo con {rif_client}: {client}")
        
        # Construir el nuevo cliente
        new_client = {
            "uuid": str(uuid.uuid4()),
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
    """Lee el archivo TXT e inserta los datos en la base de datos."""
    
    try:
        # Suponiendo que archivo_txt es una lista de líneas o que contiene el contenido del archivo
        data_clientes = archivo_txt  # utf-8 si latin-1 falla
        hoja_cliente = []

        for linea in data_clientes:
            try:
                datos_cliente = linea.strip().split(";")  # Eliminar espacios en blanco y dividir la línea

                if len(datos_cliente) == 27 or len(datos_cliente) == 26:  # Verifica que la línea tenga 26 o 27 elementos
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

        return hoja_cliente  # Podrías devolver la lista de clientes agregados

    except FileNotFoundError as e:
        print(f"Archivo bd_clientes.txt no encontrado. {e}")

    except Exception as e:
        print(f"Error al leer o procesar el archivo: {e}")

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



        
                
          
