import psycopg2
from database.get_elements import codigo_vendedor, get_observaciones, get_art, get_fecha
from trash.fila import get_celda
import datetime
import pandas as pd
from database.database import get_cliente
from database.inter_database import validate_draft
import json
from datetime import datetime



class Borrador:

    #Campos requeridos: rif, tasa_dolar, diario, pagos (pagos con fecha), base imponible de la factura, descuento, campo_bs, iva, 
    def __init__(self, info, cod_cliente, counter_prod, client_type):
        self.client_type = client_type
        self.impuesto = info[0]['amount_tax']
        self.base_imponible = info[0]['invoice_payments_widget'][-1] #En divisas
        self.api_data = info[4]
        self.info = info[0]
        self.products = info[1]
        self.n_proceso = info[3]
        self.cod_borrador = "B-{:09d}".format(self.n_proceso) 
        self.rif = info[0]['rif'].replace('-', '')
        self.cod_galac = cod_cliente
        self.borrador = self.cod_galac
        self.vendedor = '00001'
        print(self.info['invoice_date'])
        self.fecha_format = self.convert_date_format(str(self.info['invoice_date']))
        self.observaciones = get_observaciones(self.fecha_format)
        self.por_desc = 0
        self.descuento = (self.por_desc/100) * self.base_imponible
        self.monto_exento_descuento = self.descuento
        self.base_imp_d_des = self.base_imponible - self.descuento
        self.total_renglones = self.base_imponible
        self.bs = 0 
        self.total_iva = self.calc_iva()
        self.total_facturas = self.base_imponible + self.total_iva
        self.cod_moneda = 0
        self.nivel_precio = 'PR1'
        self.cod_almacen = 'UNICO'
        self.status_factura = 'BOR'
        self.tipo_documento = 'FAC'
        self.cancelada = 'N'
        self.usar_dir_fiscal = 'N'
        self.no_despacho_imprimir = 0
        self.cambio_bolivares = 1 ######
        self.monto_abono = 0            
        self.vencimiento = self.fecha_format
        self.condicion_pago = "Contado"
        self.talonario = 'TN1'
        self.forma_inicial = 'MON'
        self.porcentaje_inicial = 0
        self.numero_cuotas = 1
        self.monto_cuotas = (self.base_imponible // 1)
        self.monto_ultima_cuota = self.base_imponible
        self.forma_pago = 'CON'
        self.num_dias_ven = 30
        self.editar_monto_cuota = 'N'
        self.numero_control = ''
        self.tipo_transaccion = 'REG'
        self.num_planilla_exp = ''
        self.num_factura_afectada = ''
        self.tipo_venta = 'VEI'  # depende del tipo de persona (Contribuyente/No contribuyente) venta interna
        self.iva_retenido = 0
        self.fecha_ap_iva_ret = self.fecha_format
        self.num_comp_ret_iva = 0
        self.fecha_com_ret_iva = self.fecha_format
        self.se_retuvo_iva = 'N'
        self.fact_pre_siva = 'N'
        self.reservar_mercancia = 'N'
        self.fecha_retiro = self.fecha_format
        self.vuelto_cobro_directo = ''
        self.por_desc_1 = 0
        self.por_desc_2 = 0
        self.mont_desc_1 = 0
        self.mont_desc_2 = 0
        self.por_ali_1 = 16
        self.por_ali_2 = 8
        self.por_ali_3 = 31
        self.monto_iva_a1 = self.base_imponible * 0.16
        self.monto_iva_a2 = 0
        self.monto_iva_a3 = 0
        self.agravable_a1 = self.base_imponible
        self.agravable_a2 = 0
        self.agravable_a3 = 0
        self.fecha_fact_af = self.fecha_format
        self.apl_dec_iva_esp = 'N'
        self.base_imp_igtf = 0  # ----- revisar ----- ####
        self.igtf_mon_local = 0
        self.igtf_mon_ext = 0
        self.alicuota_igtf = 3
        self.descripcion = self.set_descripcion(self.products, counter_prod) #Campo descripcion en galac contiene es los productos de la factura
        self.alicuota_iva = 'ALG'
        self.cantidad = 1
        self.precio_sin_iva = self.base_imponible
        self.precio_con_iva = self.total_facturas
        self.porcentaje_base = 100
        self.codigo_vendedor_1 = ""
        self.codigo_vendedor_2 = ""
        self.codigo_vendedor_3 = ""
        self.campo_extra_1 = ""
        self.campo_extra_2 = ""
        #self.codigo_articulo = str(get_art(self.descripcion))
        self.codigo_articulo = str(get_art(self.descripcion))
        self.cod_moneda = "VED"
        self.cod_moneda_cobro = "BOLIVARES"   
        self.widget_pagos = self.info["invoice_payments_widget"]

    
    def generate_data(self, codigo_cliente):
        cod_borrador = codigo_cliente
        return 0
    
    # Convertir el formato de fecha
    def convert_date_format(self, date_str):
        # Crear una fecha a partir de la cadena actual
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')  # Formato original
        # Devolver la fecha en el nuevo formato
        return date_obj.strftime('%d/%m/%Y')  # Formato deseado
    
    def get_vendedor(self):
        #print(self.info['invoice_payments_widget'])
        if self.info['invoice_payments_widget'][0] != None:
            #diario_inicial = self.info['invoice_payments_widget']['content'][0]['journal_name']
            #print(diario_inicial)
            return 0

    def get_cod_borrador(self):
        if len(self.products) > 1:
            #se mantiene el codigo borrador para todos los producto
            return 0
        
    def get_borrador(self):
        
        """ 
        try:
            # Asegúrate de que 'invoice_date' esté en el formato 'YYYY-MM-DD'
            self.fecha_format = datetime.strptime(self.info['invoice_date'], '%Y-%m-%d').strftime('%d/%m/%Y')
            print("Fecha formateada:", self.fecha_format)
        except ValueError as e:
            print(f"Error al convertir la fecha: {e}")
            return None
        except KeyError as e:
            print(f"Error: Falta la clave {e} en los datos de info.")
            return None"
        """


        # Crear lista de atributos
        atributos = [
            self.cod_borrador,
            self.fecha_format,
            self.cod_galac,
            self.vendedor,
            self.observaciones,
            f"{self.monto_exento_descuento:.2f}",
            f"{self.base_imp_d_des:.2f}",
            f"{self.total_renglones:.2f}",
            f"{self.total_iva:.2f}",
            f"{self.total_facturas:.2f}",
            f"{self.por_desc:.2f}",
            self.cod_moneda,
            self.nivel_precio,
            self.cod_almacen,
            self.status_factura,
            self.tipo_documento,
            self.cancelada,
            self.usar_dir_fiscal,
            str(self.no_despacho_imprimir),
            str(self.cambio_bolivares),
            str(self.monto_abono),
            self.fecha_format,
            self.condicion_pago,
            self.talonario,
            self.forma_inicial,
            str(self.porcentaje_inicial),
            str(self.numero_cuotas),
            f"{self.monto_cuotas:.2f}",
            f"{self.monto_ultima_cuota:.2f}",
            self.forma_pago,
            str(self.num_dias_ven),
            self.editar_monto_cuota,
            self.numero_control,
            self.tipo_transaccion,
            self.num_planilla_exp,
            self.num_factura_afectada,
            self.tipo_venta,
            f"{self.iva_retenido:.2f}",
            self.fecha_format,
            str(self.num_comp_ret_iva),
            self.fecha_format,
            self.se_retuvo_iva,
            self.fact_pre_siva,
            self.reservar_mercancia,
            self.fecha_format,
            self.cod_almacen,
            str(self.no_despacho_imprimir),
            self.vuelto_cobro_directo,
            str(self.por_desc_1),
            str(self.por_desc_2),
            str(self.mont_desc_1),
            str(self.mont_desc_2),
            str(self.por_ali_1),
            str(self.por_ali_2),
            str(self.por_ali_3),
            f"{self.monto_iva_a1:.2f}",
            f"{self.monto_iva_a2:.2f}",
            f"{self.monto_iva_a3:.2f}",
            f"{self.agravable_a1:.2f}",
            str(self.agravable_a2),
            str(self.agravable_a3),
            self.fecha_format,
            self.apl_dec_iva_esp,
            f"{self.base_imp_igtf:.2f}",
            f"{self.igtf_mon_local:.2f}",
            f"{self.igtf_mon_ext:.2f}",
            f"{self.alicuota_igtf:.2f}",
            self.descripcion,
            self.alicuota_iva,
            str(self.cantidad),
            f"{self.precio_sin_iva:.2f}",
            f"{self.precio_con_iva:.2f}",
            str(self.por_desc),
            f"{self.total_renglones:.2f}",
            str(self.porcentaje_base),
            self.codigo_vendedor_1,
            self.codigo_vendedor_2,
            self.codigo_vendedor_3,
            self.campo_extra_1,
            self.campo_extra_2,
            self.codigo_articulo,
            self.cod_moneda_cobro
        ]

        print("TYPE CODE GALAC: ", type(self.cod_galac), "VALOR: ", self.cod_galac)
        if self.cod_galac == "":
            return None
        
        result_val = validate_draft(atributos).get('exists')
        print("ESTADO DE BORRADOR: ", result_val)
        #Validar si el borrador no existe, si existe se cierra el proceso
        if not result_val:
            arch = open("clientes_facturas.txt", "a")
            #si el cliente es en bolivares
            if self.client_type == 'Clientes en Bolivares' and self.impuesto != 0.0:
                for dato in atributos:
                    arch.write(str(dato) + "\t")
                arch.write("\n")
                return atributos
            elif self.client_type == 'Clientes en Divisas' and self.impuesto == 0.0:
                for dato in atributos:
                    arch.write(str(dato) + "\t")
                arch.write("\n")
                return atributos
            else:
                if len(self.client_type) == 2:
                    for dato in atributos:
                        arch.write(str(dato) + "\t")
                    arch.write("\n")
                    return atributos


    def pagos(self):
        return None
    
    def set_producto(self):
        return None
    
    def calc_iva(self):
        #Crear funcion para calcular iva
        if float(self.bs) > 0:
            return self.base_imp_d_des * 0.16
            
        else: ### EN DESARROLLO ###
            return self.base_imp_d_des * 0.16
        
    def set_descripcion(self, lines_names, counter):
        description = ""
        description += lines_names[counter]
        return description

    def descuento():
        return None
