from operate_database import connection_database
from database import get_cliente
from get_elements import codigo_vendedor, get_rif, get_nombre
from Borradores import *
import datetime


class Cliente:
    def __init__(self, info_odoo): #data es un diccionario que contiene los campos de factura obtenidos de odoo
        self.connect = connection_database()
        self.nombre = get_nombre(info_odoo[0]['invoice_partner_display_name'])
        self.rif = get_rif(info_odoo[0]['rif'])
        self.nit = "" #No se utiliza en netcom por lo tanto va vacio
        self.cuenta_contable_cxc = ""
        self.c_contable_ingresos = ""
        self.status = "Activo"
        self.telefono = self.get_phone(info_odoo)
        self.fax = "" #NO se usa el fax
        self.direccion = info_odoo[0]["street"]
        self.estado = info_odoo[2][0]['state_id'][1]
        self.ciudad = self.get_city()
        self.zona_postal = "" #No se usa la zona postal
        self.zona_cobranza = self.ciudad
        self.sector_de_negocio = "No Asignado"
        self.codigo_vendedor =  codigo_vendedor(info_odoo[0]['journal_id'][1])
        self.extranjero = 'No'
        self.email = info_odoo[2][0]['email']
        self.persona_contacto = self.nombre
        self.razon_inactividad = ""
        self.activar_aviso = "N"
        self.texto_aviso = ""
        self.cuenta_contable_anticipo = ""
        self.nivel_precio = 0
        self.origen_cliente = 0
        self.fecha_creacion = datetime.datetime.strptime(info_odoo[0]['invoice_date'], '%Y-%m-%d').strftime('%d/%m/%Y')
        
        self.products_client = info_odoo[1] #Se guarda un arreglo con las suscripciones (Codigo de Galac)
        self.info_factura = info_odoo
        self.borradores = [] 
        self.suscription = self.get_suscription()
        self.n_proceso = info_odoo[3]


        """
            codigo_cliente
            nombre
            RIF
            NIT
            Cuenta Contable CxC
            Cuenta Contable Ingresos
            Status
            Telefono
            Fax
            Direccion
            Ciudad
            Zona Postal 
            Zona de cobranzas
            Secto de negocio
            Codigo Vendedor
            Es extranjero
            Correo Electronico
            Persona Contacto
            Razon Inactividad
            Activar aviso al escoger
            Cuenta contable anticipo
            Nivel de precio
            Origen del cliente
            Fecha de creacion del cliente

            ###Si el cliente es Asociado En Cta. De Participación colocar también los siguientes campos: ###
            
            Dia cumpleanos
            Mes cumpleanos
            Correspondencia por enviar
            Fecha cliente desde: igual a fecha de creacion del cliente
        """

    def generate_data(self):
        
        atributos = [
            self.nombre, 
            self.rif, 
            self.nit, 
            self.cuenta_contable_cxc, 
            self.c_contable_ingresos, 
            self.status, 
            self.telefono, 
            self.fax, 
            self.direccion, 
            self.estado, 
            self.ciudad, 
            self.zona_postal, 
            self.zona_cobranza, 
            self.sector_de_negocio, 
            self.codigo_vendedor, 
            self.extranjero, 
            self.email, 
            self.persona_contacto, 
            self.razon_inactividad, 
            self.activar_aviso, 
            self.texto_aviso, 
            self.cuenta_contable_anticipo,
            self.nivel_precio,
            self.origen_cliente, 
            self.fecha_creacion,
        ]
        
        #return atributos
        arch = open("clientes_faltantes.txt", "a")
        for dato in atributos:
            arch.write(str(dato) + "\t")
        arch.write("\n")
        

    def get_suscription(self):
        data = get_cliente(self.connect, self.rif) #Obtiene el codigo de galac dado el rif del cliente
        if data != None:
            return data[0]
        else:  
            return False #Si no se obtiene resultado quiere decir que el cliente no existe, por lo tanto se debe crear (Se hace llamada a funcion que obtiene el ultimo codigo registrado en galac)
          

    def generar_borrador(self, document): #Se obtiene el rif de cliente para realizar la busqueda en la base de datos de Galac
        if self.suscription != False:
            counter_prod = 0
            for prod in self.products_client:
                obj = Borrador(self.rif, 50.50, self.info_factura, self.suscription, counter_prod, ) #Se pasa el rif para obtener el objeto borrador con los campos correspondientes
                self.borradores.append(obj)
                obj.get_cod_borrador()
                obj.get_borrador()
                counter_prod += 1
        else:
            self.generate_data()
        

    def get_phone(self, info_odoo):
        telefono = info_odoo[2][0]["phone"]
        if telefono != False:
            return telefono.replace("+", "")
        else:
            return False
        
    def get_city(self):
        if 'Carabobo' in self.estado:
            return 'VALENCIA'
        elif 'Aragua' in self.estado:
            return 'MARACAY'
        else:
            return False
        

    

        
    


