import xmlrpc.client

url = 'https://netcomplus.odoo.com'  # Cambia por la URL de tu servidor
db = 's2ctechsoporte-netcom-main-7643792'
username = 'desarrollo@netcomplusve.com'
api_key = '42f6ff04b63fb7ec1518cdb76f4c037018ca5429'  # Considera usar el API key
password = 'python24'  # Este podría no ser necesario si estás usando el API Key
# Autenticación
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

# Conexión al modelo
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

fields = models.execute_kw(db, uid, password, 'account.move', 'fields_get', [])

for field_name, field_info in fields.items():
    print(f"Campo: {field_name}, Tipo: {field_info['type']}")
