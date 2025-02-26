import requests

class ClienteAPI:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'application/json'
        }
        if api_key:
            self.headers['Authorization'] = f'Bearer {api_key}'

    def insert_cliente(self, cliente_data):
        try:
            response = requests.post(f'{self.base_url}/clientes/', json=cliente_data, headers=self.headers)
            response.raise_for_status()  # Lanza un error para códigos de estado 4xx o 5xx
            return response.json()  # Devuelve los datos del cliente creado
        except requests.exceptions.HTTPError as err:
            print(f'Error del cliente: {err.response.status_code} - {err.response.text}')
            return None
        except Exception as e:
            print(f'Error inesperado: {str(e)}')
            return None

# Ejemplo de uso
if __name__ == '__main__':
    api_key = 'tu_api_key_aqui'  # Si tu API requiere autenticación
    base_url = 'https://api.ejemplo.com'  # Reemplaza con tu URL base

    cliente_api = ClienteAPI(base_url, api_key)

    # Datos del nuevo cliente
    nuevo_cliente = {
        'rif': 'J-12345678-9',
        'nombre': 'Juan Pérez',
        'direccion': 'Calle Falsa 123',
        'telefono': '0123-456789',
        'email': 'juan@example.com'
    }

    # Inserción del nuevo cliente
    cliente_creado = cliente_api.insert_cliente(nuevo_cliente)

    if cliente_creado:
        print('Cliente creado:', cliente_creado)
