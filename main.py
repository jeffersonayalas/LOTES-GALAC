from demo import depurar_nombre
from data import open_archives
from get_elements import codigo_vendedor
from exportar_clientes import txt_to_csv

from api_odoo_prueba import api_data

def execute_data(ruta_excel, monto):
    #libro_excel = open_archives(ruta_excel)
    #api_data()
    #leer archivo de texto con los borradores
    datos = open('clientes_facturas.txt', 'r')
    print(type(datos))
    return datos
   

    
    
 
   








