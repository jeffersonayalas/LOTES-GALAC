import xmlrpc.client
from Clientes import Cliente
import json

data_db = {
    'url' : 'https://netcomplus.odoo.com',  # Cambia por la URL de tu servidor
    'db' : 's2ctechsoporte-netcom-main-7643792',
    'username' : 'desarrollo@netcomplusve.com',
    'api_key' : '42f6ff04b63fb7ec1518cdb76f4c037018ca5429',  # Considera usar el API key
    'password' : 'python24'  # Este podría no ser necesario si estás usando el API Key
}

url = data_db.get('url')
db = data_db.get('db')
username = data_db.get('username')
api_key = data_db.get('api_key')
password = data_db.get('password')

#Creamos una lista para almacenar clientes
clientes = []
info = []

# Conexión al servicio común para autenticación
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
message = common.version()
print("Odoo Version:", message)

# Autenticación
uid = common.authenticate(db, username, password, {})
print("User ID:", uid)

# Conexión al servicio de modelos
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Archivo para almacenar los resultados
archive = open("api_data.txt", "w")
clientes_faltantes = open("clientes_faltantes.txt", "w")
clientes_facturas = open("clientes_facturas.txt", "w")
process_data = open("process_payment.txt", "w")
diarios_pagos = open('diarios_pagos.txt', 'w')

fecha_especifica = '2025-01-30'  # Formato 'YYYY-MM-DD'
dominio = [
    ('invoice_date', '=', fecha_especifica),  # Filtro por fecha específica
    ('payment_state', '=', 'paid'),# Filtro por estado pagado
    ('move_type', '=', 'out_invoice')
]

# Obtener los registros que cumplen con el dominio
record_ids = models.execute_kw(db, uid, api_key, 'account.move', 'search', [dominio])
print("Total records found:", len(record_ids))

# Especificar los campos que deseas obtener
fields_to_read = [
    'id', 'name', 'move_type','partner_id', 'invoice_partner_display_name', 
    'rif', 'state', "invoice_date", 'invoice_date_due', 'source_id', 'currency_id',
    'invoice_line_ids', 'journal_id', 'street', 'amount_total_signed', 'amount_total_in_currency_signed', 'payment_state',
    'amount_tax', 'amount_untaxed', 'igtf_invoice_amount', 'amount_residual', 'invoice_payments_widget', 'payment_id' ]  # Agrega o ajusta los campos según sea necesario

# Leer los registros obtenidos
if record_ids:
    count = 0
    for record_id in record_ids:
        result_execute = models.execute_kw(db, uid, api_key, 'account.move', 'read', [[record_id]], {'fields': fields_to_read})

        #Obtener el rif de la factura
        rif_cliente = result_execute[0]['rif']
        if rif_cliente == False:
            continue

        count += 1 #Corresponde con el numero de proceso

        # Escribe los resultados en el archivo
        archive.write("\n" + str(result_execute[0]))
        

        invoice_line_ids = result_execute[0]['invoice_line_ids']
        partner_id = result_execute[0]['partner_id']
        partner_data = models.execute_kw(db, uid, api_key, 'res.partner', 'read', [partner_id[0]], {'fields': ['phone', 'city', 'state_id', 'email']})

        productos = [] #Descomponer la estructura de productors e incluir solo el nombre....
        print("--------------------------------------------------------------------------------------------------------------------")
        if invoice_line_ids:

            lines = models.execute_kw(db, uid, api_key, 'account.move.line', 'read', [invoice_line_ids], {'fields': ['product_id', 'name']}) #Lines es un arreglo que contiene diccionarios
            #print(lines)
            for line in lines:
                prod = line['product_id'][1].replace("\n", " ")
                productos.append(prod)

        count_payment = 0
        diarios_de_caja = [
            'FREE MARKET 01',
            'FREE MARKET 02',
            'LOS CAOBOS 01',
            'LOS CAOBOS 02',
            'LOS CAOBOS 03',
            'LOS CAOBOS 04',
            'LOS CAOBOS 05',
            'LOS CAOBOS 06',
            'LOS GUAYOS 01',
            'LOS GUAYOS 02',
            'LA MORITA 01',
            'LA MORITA 02',
            'LA MORITA 04',
            'LA MORITA 05',
            'LA MORITA 06',
            'LA MORITA 03',
            'CAGUA 01',
            'CAGUA 02',
            'GUACARA 01',
            'GUACARA 02',
            'GUACARA 03',
            'GUACARA 04',
            'GUACARA 05',
            'GUACARA 06',
            'PUERTO CABELLO 01',
            'PASEO LAS INDUSTRIAS 01',
            'PASEO LAS INDUSTRIAS 02',
            'PUERTO CABELLO 02',
            'PUERTO CABELLO 03',
            'PUERTO CABELLO 04',
            'PUERTO CABELLO 05',
            'TORRE MOVILNET 01',
            'TORRE MOVILNET 02',
            'TORRE MOVILNET 03',
            'TORRE MOVILNET 04',
            'SAN JOAQUIN 01',
            'TOCUYITO 01',
            'TOCUYITO 02'
        ]
        pay_id = result_execute[0]["invoice_payments_widget"]

        if pay_id != 'false':
            pagos = json.loads(pay_id)
            pay_content = pagos['content'] ### iterar sobre content ###
            total_pays = []
            montos = []

            for pay in pay_content: #content contiene los pagos del cliente (uno o varios pagos - es un arreglo de diccionarios)
                payment_id = pay['account_payment_id']
                ###### REALIZAR CONSULTA PARA OBTENER ID DE PAGO Y EL CREADOR PARA APLICAR LOS FILTROS ######
                fields_payment = [
                    'create_uid', 
                    'journal_id', 'amount', 'currency_id',
                    'amount', 'date', 'payment_method_name', 'move_id']

                payment_data = models.execute_kw(db, uid, api_key, 'account.payment', 'read', [payment_id], {'fields': fields_payment})
                total_pays.append(payment_data[0]) #Puede ser un diccionario que contenga informacion de pagos + tasa
                
                #consultar tasas para pagos
                currency_code = 'VES'

                # Determinar montos totales (se realiza consulta de la tasa a través de API)
                currency_id = models.execute_kw(db, uid, password, 'res.currency', 'search', [[('name', '=', currency_code)]])

                consulta_fecha = payment_data[0].get('date')

                if currency_id:
                    # 1. Intentar obtener la tasa de cambio para la fecha específica
                    rate = models.execute_kw(
                        db,
                        uid,
                        password,
                        'res.currency.rate',
                        'search_read',
                        [[
                            ('currency_id', '=', currency_id[0]),
                            ('name', '=', consulta_fecha)  # Buscar por la fecha exacta
                        ]],
                        {'fields': ['name', 'company_rate', 'currency_id']}
                    )

                    if rate:
                        # Se encontró la tasa para la fecha específica
                        print(rate)
                        print(f"Fecha: {rate[0]['name']}, Tasa: {rate[0]['company_rate']}")
                    else:
                        # 2. Si no encuentra, buscar la fecha más cercana anterior
                        nearest_rate = models.execute_kw(
                            db,
                            uid,
                            password,
                            'res.currency.rate',
                            'search_read',
                            [[
                                ('currency_id', '=', currency_id[0]),
                                ('name', '<', consulta_fecha)  # Buscar la fecha más cercana anterior
                            ]],
                            {'fields': ['name', 'company_rate', 'currency_id'], 'limit': 1}  # Mueve 'limit' aquí en el diccionario de opciones
                        )

                        if nearest_rate:
                            print(f"No se encontró la tasa para la fecha {consulta_fecha}. Se usará la tasa más cercana anterior.")
                            print(f"Fecha: {nearest_rate[0]['name']}, Tasa: {nearest_rate[0]['company_rate']}")
                        else:
                            print("No se encontró ninguna tasa de cambio disponible para la moneda.")
                else:
                    print("No se encontró ninguna moneda con ese código.")

            #print(" - - - - - - " + str(total_pays) + " - - - - - - ")
        else:
            print("- - - - CLIENTE POSIBLEMENTE TIENE DESCUENTO - - - -")


        # - - - - APLICAR FILTROS PARA GENERAR LOS BORRADORES - - - - #
        #Recorremos los pagos del cliente para ver si todos son en bs o en dolares
        datos = [result_execute[0], productos, partner_data, count, data_db, total_pays]
        ob_cliente = Cliente(datos)
        ob_cliente.generar_borrador(clientes_faltantes)
else:
    print("No records found.")
archive.close()  # Asegúrate de cerrar el archivo después de usarlo