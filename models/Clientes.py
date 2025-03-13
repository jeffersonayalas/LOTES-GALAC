
from database.get_elements import codigo_vendedor, get_nombre
from database.inter_database import obtain_client, buscar_cliente_odoo, verify_client_by_cod_galac
from models.Borradores import *
import datetime
import random
import string


class Cliente:
    def __init__(self, info_odoo): #data es un diccionario que contiene los campos de factura obtenidos de odoo
        self.info = info_odoo
        self.codigo = self.code_client()
        self.nombre = get_nombre(info_odoo[0].get('invoice_partner_display_name'))
        self.rif = info_odoo[0].get('rif')
        self.rif_exp = self.rif.replace("-", "")
        self.nit = "" #No se utiliza en netcom por lo tanto va vacio
        self.cuenta_contable_cxc = ""
        self.c_contable_ingresos = ""
        self.status = "Activo"
        self.telefono = self.get_phone(info_odoo)
        self.fax = "" #NO se usa el fax
        self.direccion = info_odoo[0].get("street")
        state_id = info_odoo[2][0].get('state_id', None)

        if isinstance(state_id, (list, dict)) and len(state_id) > 1:
            self.estado = state_id[1]
        else:
            print(f"state_id no es indexable o no tiene suficientes elementos: {state_id}")
            self.estado = 'Carabobo (VE)'  #o maneja el caso según sea necesario
        
        self.ciudad = self.get_city()
        self.zona_postal = "" #No se usa la zona postal
        self.zona_cobranza = self.ciudad
        self.sector_de_negocio = "No Asignado"
        self.codigo_vendedor =  codigo_vendedor(info_odoo[0].get('journal_id')[1])
        self.extranjero = 'No'
        self.email = info_odoo[2][0].get('email')
        self.persona_contacto = self.nombre
        self.razon_inactividad = ""
        self.activar_aviso = "N"
        self.texto_aviso = ""
        self.cuenta_contable_anticipo = ""
        self.nivel_precio = 0
        self.origen_cliente = 0
        self.fecha_creacion = datetime.datetime.strptime(info_odoo[0].get('invoice_date'), '%Y-%m-%d').strftime('%d/%m/%Y')
        self.products_client = info_odoo[1] 
        
        self.borradores = [] 
        self.suscription = self.get_suscription()
        self.n_proceso = info_odoo[3]
        self.record_id = self.rif
        self.pagos = self.info[0].get('invoice_payments_widget')
        self.info[0].get('invoice_payments_widget').append(self.process_payment()) #Arreglo que contiene los pagos
        self.info_factura = info_odoo
    

    def generate_data(self):
        
        atributos = [
            self.codigo,
            self.nombre, 
            self.rif_exp, 
            self.nit, 
            self.cuenta_contable_cxc, 
            self.c_contable_ingresos, 
            self.status, 
            self.telefono, 
            self.fax, 
            self.direccion, 
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
        
        rif_contenido = f"{self.rif}"  # Formatear RIF para comparación
        archivo_faltantes = "clientes_faltantes.txt"

        print("PRODUCTOS DE CLIENTE -------------------------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>.", self.products_client)

        if '[SRV-CUA-0008] Servicio Instalación de clientes ' in self.products_client:
            with open('clientes_nuevos.txt', 'a') as clientes_nuevos:
                for dato in atributos:
                    clientes_nuevos.write(str(dato) + ";")
                clientes_nuevos.write("\n")
        else:
            # Leer el archivo existente para verificar duplicados
            try:
                with open(archivo_faltantes, "r") as arch:
                    lineas = arch.readlines()

                    # Verificar si el RIF ya existe
                    for linea in lineas:
                        if rif_contenido.replace("-", "") in linea:  # Si el RIF ya está en la línea, no lo agregues
                            print(f"El cliente con RIF {self.rif} ya está en el archivo, no se agregará.")
                            return  # Devolver si ya existe

            except FileNotFoundError:
                # Si el archivo no existe, está bien, simplemente se creará
                pass

            print("SUSCRIPCION -------- >>>>>> ", self.suscription)
            
            if self.suscription == False:
                # Si el RIF no está presente, escribir los atributos en el archivo
                with open(archivo_faltantes, "a") as arch:
                    for dato in atributos:
                        arch.write(str(dato) + ";")
                    arch.write("\n")
        
    
    def generar_borrador(self, client_type): #Se obtiene el rif de cliente para realizar la busqueda en la base de datos de Galac
        #Se deben desglosar los montos al momento de enviarlos al borrador 
        
        if self.suscription != False:
            counter_prod = 0
            #Pendiente
            for prod in self.products_client:
                obj = Borrador(self.info_factura, self.suscription, counter_prod, client_type) #Se pasa el rif para obtener el objeto borrador con los campos correspondientes
                self.borradores.append(obj)
                obj.get_cod_borrador() #REVISAR
                obj.get_borrador() 
                counter_prod += 1
        else:
            #Se realiza llamada a funcion para crear el cliente 
            self.generate_data()
        
    
    def process_payment(self):
        #Aca se incluye la base imponible de los pagos en el arreglo de los mismos (guardar como total_pagos)
        #Obtener base imponible en divisas y bs
        base_imponible_desc = 0
        moneda = ''

        if self.pagos != [None]: 
            for pay in self.pagos:
                monto_pago = pay.get('amount')
                rate = pay('rate')
                base_imponible_desc += monto_pago * rate
                moneda = "Bs"

            if self.info[0]['amount_tax'] > 0:
                #base imponible = total - 16%
                base_imponible_desc =  base_imponible_desc - (base_imponible_desc*0.16) 
        

        #print("\nPAGOS DEL CLIENTE: " + str(pay_one) + "BASE IMPONIBLE PARA FACTURA: " +str(base_imponible_desc) + " " + str(moneda))
        return round(base_imponible_desc, 2)
            
        
    def get_suscription(self):
        print("SELF.RIF", self.rif)

        rif_digits = self.rif.split("-")[1]

        #Separar busqueda de rif por casos
        rif_completo = rif_digits
        rif_sin_ultimo_digito = rif_digits[:-1] 
        rif_sin_primer_digito = rif_digits[1:]

        rifs = [rif_completo, rif_sin_ultimo_digito, rif_sin_primer_digito]

        for rif in rifs:
            result = obtain_client(rif)
            if result != None:
                print(result)
                print("CODIGO GALAC: ", result.get('cod_galac'))
                return result.get('cod_galac')
        return False


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
        
    def code_client(self):
        # Generar un nuevo código
        primera_letra = random.choice(string.ascii_uppercase)
        dos_digitos = f"{random.randint(0, 99):02d}"
        tres_letras_1 = ''.join(random.choices(string.ascii_uppercase, k=3))
        un_digito = str(random.randint(0, 9))
        tres_letras_2 = ''.join(random.choices(string.ascii_uppercase, k=3))

        codigo_cliente = f"{primera_letra}{dos_digitos}{tres_letras_1}{un_digito}{tres_letras_2}"

        # Aca se realiza la consulta a la base de datos
        if verify_client_by_cod_galac(codigo_cliente) == True:
            # Si el código ya existe, llamamos a la función nuevamente
            return self.code_client()
        else:
            return codigo_cliente  # Retornar el nuevo código


        

    

        
    


