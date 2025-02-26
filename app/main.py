from trash.demo import depurar_nombre
from trash.data import open_archives
from database.get_elements import codigo_vendedor
from trash.exportar_clientes import txt_to_csv

from app.api_odoo_prueba import api_data

def execute_data(ruta_excel, monto):
    #api_data()
    #leer archivo de texto con los borradores
    datos = open('clientes_facturas.txt', 'r')
    print(type(datos))
    return datos
   

    
    
 
   








