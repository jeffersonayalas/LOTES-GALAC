import psycopg2
from get_elements import codigo_vendedor, get_observaciones, get_art, get_fecha
from fila import get_celda
import datetime
import pandas as pd
from create_database import connection_database


def consultar(id_cliente, libro_excel, monto_tasa, n_borrador, datos_cli): #Se le envia el id cliente de galac
        
    #if len(id_cliente) <= 3:
    #producto_celda = libro_excel["Facturas conciliadas/Líneas de factura/Producto"]
        
    
    rif = id_cliente.split("-")
    #conn = psycopg2.connect("dbname=GDATA user=postgres password=123456")
    conn = connection_database()
    cur = conn.cursor()
    query = "SELECT nombre_cliente, cod_galac, rif FROM contactos WHERE rif = %s;"

    if len(rif) == 2:
        cur.execute(query, (rif[0] + rif[1],))
        rows = cur.fetchall()

        #Consultar siguiente celda
        #next_dat = next_layer(libro_excel, rif)

        if len(rows) > 0:
            
            print(rows)

            # --- CAMPOS --- #
            tasa = monto_tasa
            borrador = "B-{:09d}".format(n_borrador) 
            datos_cliente = rows[0]
            vendedor = codigo_vendedor(libro_excel, id_cliente)
            fecha_format = str(get_celda(libro_excel, id_cliente, 'RIF', 'Fecha')).split(" ")
            fecha = fecha_format[0]
            codigo_cliente = rows[0][1]
            observaciones = get_observaciones(fecha)
            base_imponible = get_celda(libro_excel, id_cliente, 'RIF', 'Facturas conciliadas/Base imponible')*tasa
            por_desc = int(get_celda(libro_excel, id_cliente, 'RIF', 'Facturas conciliadas/Líneas de factura/Descuento (%)'))
            descuento = int((por_desc/100) * base_imponible) 
            monto_exento_descuento = descuento
            base_imp_d_des = base_imponible - descuento
            total_renglones = base_imponible
            bs = get_celda(libro_excel, id_cliente, "RIF", "Total Bs")

            if float(bs) > 0:
                total_iva = base_imp_d_des * 0.16
            else: 
                total_iva = 0
            #print("IVA:"  + str(total_iva))
            
            total_facturas = get_celda(libro_excel, id_cliente, 'RIF', 'Facturas conciliadas/Total') * tasa
            cod_moneda = get_celda(libro_excel, id_cliente, 'RIF', 'Facturas conciliadas/Moneda')
            nivel_precio = 'PR1'
            cod_almacen = 'UNICO'
            status_factura = 'BOR'
            tipo_documento = 'FAC'
            cancelada = 'N'
            usar_dir_fiscal = 'N'
            no_despacho_imprimir = 0
            cambio_bolivares = 1 ######
            monto_abono = 0
            vencimiento = fecha
            condicion_pago = "Contado"
            talonario = 'TN1'
            forma_inicial = 'MON'
            porcentaje_inicial = 0
            numero_cuotas = 1
            monto_cuotas = (base_imponible//1)
            monto_ultima_cuota = total_facturas
            forma_pago = 'CON' #########
            num_dias_ven = 30
            editar_monto_cuota = 'N'
            numero_control = ''
            tipo_transaccion = 'REG'
            num_planilla_exp = ''
            num_factura_afectada = ''
            tipo_venta = 'VEI' #depende del tipo de persona (Contribuyente/No contribuyente) venta interna
            iva_retenido = 0
            fecha_ap_iva_ret = fecha
            num_comp_ret_iva = 0
            fecha_com_ret_iva = fecha
            se_retuvo_iva = 'N'
            fact_pre_siva = 'N'
            reservar_mercancia = 'N'
            fecha_retiro = fecha
            vuelto_cobro_directo = ''
            por_desc_1 = 0
            por_desc_2 = 0
            mont_desc_1 = 0
            mont_desc_2 = 0
            por_ali_1 = 16
            por_ali_2 = 8
            por_ali_3 = 31
            monto_iva_a1 = base_imponible * 0.16
            monto_iva_a2 = 0
            monto_iva_a3 = 0
            agravable_a1 = base_imponible
            agravable_a2 = 0
            agravable_a3 = 0
            fecha_fact_af = fecha
            apl_dec_iva_esp = 'N'
            base_imp_igtf = 0 ##### ----- revisar ----- ####
            igtf_mon_local = 0
            igtf_mon_ext = 0
            alicuota_igtf = 3
            descripcion = str(get_celda(libro_excel, id_cliente, 'RIF', 'Facturas conciliadas/Líneas de factura/Producto'))
            alicuota_iva = 'ALG'
            cantidad = 1
            precio_sin_iva = base_imponible
            precio_con_iva = total_facturas
            porcentaje_base = 100
            codigo_vendedor_1 = ""
            codigo_vendedor_2 = ""
            codigo_vendedor_3 = ""
            campo_extra_1 = ""
            campo_extra_2 = ""
            codigo_articulo = str(get_art(descripcion))
            cod_moneda = "VED"
            cod_moneda_cobro = "BOLIVARES"
            
            return [
            borrador,
            datetime.datetime.strptime(fecha_format[0], '%Y-%m-%d').strftime('%d/%m/%Y'), codigo_cliente, 
            vendedor, observaciones, f"{monto_exento_descuento:.2f}", f"{base_imp_d_des:.2f}", f"{total_renglones:.2f}", f"{total_iva:.2f}", 
            f"{total_facturas:.2f}", f"{por_desc:.2f}", cod_moneda, nivel_precio, cod_almacen, status_factura, tipo_documento, cancelada,
            usar_dir_fiscal, str(no_despacho_imprimir), str(cambio_bolivares), str(monto_abono), datetime.datetime.strptime(fecha_format[0], '%Y-%m-%d').strftime('%d/%m/%Y'), condicion_pago,
            talonario, forma_inicial, str(porcentaje_inicial), str(numero_cuotas), f"{monto_cuotas:.2f}", f"{monto_ultima_cuota:.2f}", forma_pago,
            str(num_dias_ven), editar_monto_cuota, numero_control, tipo_transaccion, num_planilla_exp, num_factura_afectada, tipo_venta,
            f"{iva_retenido:.2f}", datetime.datetime.strptime(fecha_format[0], '%Y-%m-%d').strftime('%d/%m/%Y'), str(num_comp_ret_iva), 
            datetime.datetime.strptime(fecha_format[0], '%Y-%m-%d').strftime('%d/%m/%Y'), se_retuvo_iva, fact_pre_siva, reservar_mercancia,
            datetime.datetime.strptime(fecha_format[0], '%Y-%m-%d').strftime('%d/%m/%Y'),cod_almacen, str(no_despacho_imprimir),
            vuelto_cobro_directo,  str(por_desc_1), str(por_desc_2), str(mont_desc_1), str(mont_desc_2), str(por_ali_1), str(por_ali_2), str(por_ali_3), f"{monto_iva_a1:.2f}", f"{monto_iva_a2:.2f}",
            f"{monto_iva_a3:.2f}", f"{agravable_a1:.2f}", str(agravable_a2), str(agravable_a3), datetime.datetime.strptime(fecha_format[0], '%Y-%m-%d').strftime('%d/%m/%Y'), apl_dec_iva_esp, 
            f"{base_imp_igtf:.2f}", f"{igtf_mon_local:.2f}", f"{igtf_mon_ext:.2f}",
            f"{alicuota_igtf:.2f}", descripcion, alicuota_iva, str(cantidad), f"{precio_sin_iva:.2f}", f"{precio_con_iva:.2f}", 
            str(por_desc), f"{total_renglones:.2f}", str(porcentaje_base), 
            codigo_vendedor_1, codigo_vendedor_2, codigo_vendedor_3, campo_extra_1, campo_extra_2, codigo_articulo, cod_moneda_cobro ]
         
        cur.close()
        conn.close()
        #return True
   
""" 
        #Si este codigo funciona, debe devolver True
    except psycopg2.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    except Exception as e:
        print(f"Error inesperado en la consulta: {e}")
"""

