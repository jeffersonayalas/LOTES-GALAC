import xmlrpc.client
from models.Clientes import Cliente
import json
from database.inter_database import obtain_client
from dotenv import load_dotenv  # Importar python-dotenv
import os 


# Cargar variables de entorno desde el archivo .env
load_dotenv()


# Configuración de la conexión a la base de datos
#DATABASE_URL = "postgresql://postgres:python24@localhost:5432/data_facturas"

data_db = {
        'url'      : os.getenv('ODOO_URL'),
        'db'       : os.getenv('ODOO_DB'),
        'username' : os.getenv('ODOO_USERNAME'),
        'password' : os.getenv('ODOO_PASSW'),
        'api_key'  : os.getenv('API_KEY')
    }

url = data_db.get('url')
db = data_db.get('db')
username = data_db.get('username')
api_key = data_db.get('api_key')
password = data_db.get('password')


#recibe tipo de operacion y realiza una accion de acuerdo a ese tipo
def api_data(*args):
    
    #args solo puede tener dos o 3 argumentos
    
    operation_type = args[0]
    fecha = args[1]
    print("FECHA: --------------------->>>> ", fecha)
    client_type = None

    if len(args) == 3:
        if len(args[2]) == 1:
            client_type = args[2][0]
        else:
            client_type = args[2]

   
    clientes_facturas = open("clientes_facturas.txt", "w", encoding='cp1252')
    clientes_faltantes = open("clientes_faltantes.txt", "w", encoding='cp1252')
    process_data = open("process_payment.txt", "w", encoding='cp1252')
    archive = open("api_data.txt", "w")
    errores = open("errores.txt", "w", encoding='cp1252')
    clientes_juridicos = open("clientes_juridicos.txt", "w", encoding='cp1252')
    clientes_nuevos = open("clientes_nuevos.txt", "w", encoding='cp1252')
    
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

    fecha_especifica = fecha  # Formato 'YYYY-MM-DD'

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
        'id', 'name', 'invoice_origin','move_type','partner_id', 'invoice_partner_display_name', 
        'rif', 'state', "invoice_date", 'invoice_date_due', 'source_id', 'currency_id', 
        'invoice_line_ids', 'journal_id', 'street', 'amount_total_signed', 'amount_total_in_currency_signed', 'payment_state',
        'amount_tax', 'amount_untaxed', 'igtf_invoice_amount', 'amount_residual', 'invoice_payments_widget', 'payment_id' ]  # Agrega o ajusta los campos según sea necesario
    
    # Leer los registros obtenidos
    if record_ids:
        count = 0
        count_desc = 0
        for record_id in record_ids:
            result_execute = models.execute_kw(db, uid, api_key, 'account.move', 'read', [[record_id]], {'fields': fields_to_read})

            #Obtener el rif de la factura
            rif_cliente = result_execute[0]['rif']
            street = result_execute[0]['street']
            
            if rif_cliente == False or street == False:
                errores.write("\n" + str(result_execute[0]))
                continue

            count += 1 #Corresponde con el numero de proceso

            # Escribe los resultados en el archivo
            archive.write("\n" + str(result_execute[0]))
            
            invoice_line_ids = result_execute[0]['invoice_line_ids']
            partner_id = result_execute[0]['partner_id']
            partner_data = models.execute_kw(db, uid, api_key, 'res.partner', 'read', [partner_id[0]], {'fields': ['phone', 'city', 'state_id', 'email']})

            productos = [] #Descomponer la estructura de productos e incluir solo el nombre....
            print("--------------------------------------------------------------------------------------------------------------------")
            if invoice_line_ids:
                lines = models.execute_kw(db, uid, api_key, 'account.move.line', 'read', [invoice_line_ids], {'fields': ['product_id', 'name']}) #Lines es un arreglo que contiene diccionarios
                for line in lines:
                    prod = line['product_id'][1].replace("\n", " ")
                    productos.append(prod)

            pagos = cons_payments(result_execute[0]["invoice_payments_widget"], models, data_db, uid)

            if pagos == None:
                pagos_txt = open("pagos_txt.txt", "w")
                pagos_txt.write(str(result_execute[0]) + "\n")
                continue

            if '[SRV-CUA-0008] Servicio Instalación de clientes ' in productos:
                clientes_nuevos.write(str(result_execute[0]) + '\n')

            
            #Obtener el rif de la factura
            rif_cliente = result_execute[0]['rif']
            street = result_execute[0]['street']
            invoice_origin = result_execute[0].get('invoice_origin')
            
            if rif_cliente == False or street == False or invoice_origin == False:
                errores.write("\n" + str(result_execute[0]))
                continue

            result_execute[0]['invoice_payments_widget'] = pagos
            datos = [result_execute[0], productos, partner_data, count, data_db] #Ajustar el arreglo de productos para que vaya dentro de la informacion de las facturas
            
            if operation_type == 1:
                fact_operation(datos, client_type)
            else:
                create_clients(datos)

            print('Numero de clientes procesados:  ' + str(count))
            process_data = open("process_payment.txt", 'a')
            process_data.write(str(pagos) + "\n")
    else:
        print("No records found.")
    archive.close()  # Asegúrate de cerrar el archivo después de usarlo

    if operation_type == 0:
        clientes_faltantes.close()
        clientes_faltantes_1 = open('clientes_faltantes.txt', 'r')
        clientes_faltantes_1.seek(0)
        return clientes_faltantes_1
    else: 
        clientes_facturas.close()
        clientes_facturas_1 = open('clientes_facturas.txt', 'r')
        clientes_facturas_1.seek(0)
        return clientes_facturas_1
    

def fact_operation(info_client, client_type):
    #Recorremos los pagos del cliente para ver si todos son en bs o en dolares
    ob_cliente = Cliente(info_client)
    ob_cliente.generar_borrador(client_type)

def create_clients(info_client):
    ob_cliente = Cliente(info_client)

    rif_digits = ob_cliente.rif.split("-")[1]

    #Separar busqueda de rif por casos
    rif_completo = rif_digits
    rif_sin_ultimo_digito = rif_digits[:-1] 
    rif_sin_primer_digito = rif_digits[1:]

    rifs = [rif_completo, rif_sin_ultimo_digito, rif_sin_primer_digito]
    
    for rif in rifs:
        result = obtain_client(rif)
        if result != None:
            return 0
        
    if result == None:
        ob_cliente.generate_data()
    


def cons_payments(info_pagos, models, data_db, uid):
    
    pay_id = info_pagos
    
    #Si el pago es diferente de false se retorna el contenido encontrado, de los contrario se retorna 0, por lo tanto datos[5] = 0 (pay_content = None)
    if pay_id != 'false':
        pagos = json.loads(pay_id)
        pay_content = pagos['content']  # Un arreglo de diccionarios
        
        currency_code = 'VES'
        currency_id = models.execute_kw(db, uid, api_key, 'res.currency', 'search', [[('name', '=', currency_code)]])
     
        if currency_id:
            for pay in pay_content:  # Iterar sobre cada pago
                consulta_fecha = pay.get('date')

                # 1. Intentar obtener la tasa de cambio para la fecha específica
                rate = models.execute_kw(db, uid, api_key, 'res.currency.rate', 'search_read',
                                          [[('currency_id', '=', currency_id[0]), ('name', '=', consulta_fecha)]],
                                          {'fields': ['name', 'company_rate', 'currency_id']})
                
                # Si se encontró una tasa
                if rate:
                    pay['rate'] = rate[0]['company_rate']
                else:
                    # 2. Buscar la fecha más cercana anterior
                    nearest_rate = models.execute_kw(
                        db,
                        uid,
                        api_key,
                        'res.currency.rate',
                        'search_read',
                        [[
                            ('currency_id', '=', currency_id[0]),
                            ('name', '<', consulta_fecha)  # Buscar tasa más cercana anterior
                        ]],
                        {'fields': ['name', 'company_rate', 'currency_id'], 'limit': 1}
                    )

                    if nearest_rate:
                        pay['rate'] = nearest_rate[0]['company_rate']
                    else:
                        print(f"No se encontró ninguna tasa de cambio disponible para la moneda en la fecha {consulta_fecha}.")
            return pay_content #Se retorna contenido de pago ()
        else:
            print("No se encontró ninguna moneda con ese código.")
    else:
        return None
   


    
