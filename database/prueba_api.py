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
    print("SOLICITUD HACIA:", f'{base_url}/clientes/')

    try:
        response = requests.post(f'{base_url}/clientes/', headers=headers, json=cliente_data)

        if response.status_code == 201:  # Código de éxito para creación
            return response.json()  # Devuelve la respuesta en formato JSON
        else:
            print(f'Error: {response.status_code}, {response.text}')
            return None
    except Exception as e:
        print(f'Error durante la solicitud: {e}')
        return None
    

def obtain_client(id_client: str):
    base_url = DB_HOST  # Asegúrate de que DB_HOST esté definido con la URL base de tu API

    headers = {
        'Content-Type': 'application/json'
    }

    print("VERIFICACION DE CLIENTE:", id_client)

    # Realizar la petición GET para obtener el cliente
    print("SOLICITUD HACIA:", f'{base_url}/clientes/{id_client}')

    try:
        response = requests.get(f'{base_url}/clientes/{id_client}', headers=headers)

        if response.status_code == 200:  # Código de éxito para éxito en lectura
            return response.json()  # Devuelve la respuesta en formato JSON
        else:
            print(f'Error: {response.status_code}, {response.text}')
            return None
    except Exception as e:
        print(f'Error durante la solicitud: {e}')
        return None



def make_client():
    client = {
        "odoo_id": "272727",
        "rif": "V00000000",
        "cod_galac": "030303030",
        "nombre_cliente": "SENORA DE LAS FLORES"
    }
    if insert_clients(client):
        print("CLIENTE INSERTADO CORRECTAMENTE")


def consult_client():
    rif = "V-306123528"
    result = obtain_client(rif)
    if result:
        print("CODIGO DE GALAC DEL CLIENTE: ", result.get("cod_galac"))
    

consult_client()
    