import xmlrpc.client
from Clientes import Cliente


url = 'https://netcomplus.odoo.com'  # Cambia por la URL de tu servidor
db = 's2ctechsoporte-netcom-main-7643792'
username = 'desarrollo@netcomplusve.com'
api_key = '42f6ff04b63fb7ec1518cdb76f4c037018ca5429'  # Considera usar el API key
password = 'python24'  # Este podría no ser necesario si estás usando el API Key

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

fecha_especifica = '2025-01-30'  # Formato 'YYYY-MM-DD'
dominio = [
    ('invoice_date', '=', fecha_especifica),  # Filtro por fecha específica
    ('payment_state', '=', 'paid'),# Filtro por estado pagado
    ('move_type', '=', 'out_invoice')
]

# Obtener los registros que cumplen con el dominio
record_ids = models.execute_kw(db, uid, password, 'account.move', 'search', [dominio])

print("Total records found:", len(record_ids))

# Especificar los campos que deseas obtener
fields_to_read = [
    'id', 'name', 'move_type','partner_id', 'invoice_partner_display_name', 
    'rif', 'state', "invoice_date", 'invoice_date_due', 'source_id', 'currency_id',
    'invoice_line_ids', 'journal_id', 'street', 'amount_total_signed', 'amount_total_in_currency_signed', 'payment_state',
    'amount_tax', 'amount_untaxed', 'igtf_invoice_amount', 'amount_residual', 'invoice_payments_widget']  # Agrega o ajusta los campos según sea necesario

# Leer los registros obtenidos
if record_ids:
    count = 0
    for record_id in record_ids:
        print("--------------------------------------------------------------------------------------------------------------------")
        result_execute = models.execute_kw(db, uid, password, 'account.move', 'read', [[record_id]], {'fields': fields_to_read})
        #print(record_id)
        #print('Productos de la factura de: ' + str(result_execute[0]['invoice_partner_display_name']))
        # Escribe los resultados en el archivo
        archive.write("\n" + str(result_execute[0]))

        invoice_line_ids = result_execute[0]['invoice_line_ids']

        productos = [] #DEscomponer la estructura de productors e incluir solo el nombre....
        if invoice_line_ids:
            lines = models.execute_kw(db, uid, password, 'account.move.line', 'read', [invoice_line_ids], {'fields': ['product_id', 'name']}) #Lines es un arreglo que contiene diccionarios
            #productos = lines
            #print(productos)
            #print(" - - - " + str(lines) + " - - - ")
            #print("Invoice line IDs:", result_execute[0]['invoice_line_ids'])
            
            for line in lines:
                #print(line['name'])
                productos.append(line['name'])
                #print(line)
        
        print(productos)
        
        #Obtener el rif de la factura
        rif_cliente = result_execute[0]['rif']
        if rif_cliente == None:
            continue

        datos = [result_execute[0], productos]
        ob_cliente = Cliente(datos)
        ob_cliente.generar_borrador()
else:
    print("No records found.")

archive.close()  # Asegúrate de cerrar el archivo después de usarlo