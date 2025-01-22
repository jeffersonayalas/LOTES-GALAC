from demo import depurar_nombre
from data import open_archives
from get_elements import codigo_vendedor
from exportar_clientes import txt_to_csv

def execute_data(ruta_excel, monto):
    libro_excel = open_archives(ruta_excel)
    depurar_nombre(libro_excel, monto)
   

#execute_data("pagos_facturas.xlsx", 51.88)






