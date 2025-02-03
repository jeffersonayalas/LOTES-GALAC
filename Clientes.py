from operate_database import connection_database
from database import get_cliente
from Borradores import *


class Cliente:

    def __init__(self, info_odoo): #data es un diccionario que contiene los campos de factura obtenidos de odoo
        self.rif = info_odoo['rif']
        self.connect = connection_database()
        self.suscripciones = get_cliente(self.connect, self.rif) #Se guarda un arreglo con las suscripciones (Codigo de Galac)
        self.info_factura = info_odoo
        self.borradores = [] 

    def get_suscription(self):
        return self.suscripciones
       
    def generar_borrador(self): #Se obtiene el rif de cliente para realizar la busqueda en la base de datos de Galac
        #Recorremos las suscripciones del cliente y generamos un borrador para cada una 
        if self.suscripciones != None:
            for sus in self.suscripciones:
                print("- - -" + str(sus) + "- - -")
                obj = Borrador(self.rif, 50.50, self.info_factura, sus) #Se pasa el rif para obtener el objeto borrador con los campos correspondientes
                self.borradores.append(obj)
                obj.get_borrador()
            return self.borradores
            
    def generate_data(self, codigo_cliente):
        cod_borrador = codigo_cliente
        return 0
