from operate_database import connection_database
from database import get_cliente



def search_client(rif_cliente): #Se obtiene el rif de cliente para realizar la busqueda en la base de datos de Galac
    connect = connection_database()
    suscripciones = get_cliente(connect, rif_cliente)

    for fila in suscripciones:
        print(fila)
        generate_data(fila)

    
    
        
def generate_data(codigo_cliente):
    cod_borrador = codigo_cliente
    return 0
