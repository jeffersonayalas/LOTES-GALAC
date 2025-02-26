import pandas as pd 
from trash.consultas import consultar
from openpyxl import load_workbook
from trash.fila import get_celda, obtener_numero_fila_por_valor
from trash.depurar_contactos import encontrar_proximo_rif, proximo_producto
from database.get_elements import get_art, codigo_vendedor

n_borr = 0

def export_archives(libro_excel, libro_facturas):
    #Exportar archivos
    libro_excel.to_csv("export.csv", sep=";", header=True, index=False)
    libro_facturas.close()
    
def depurar_nombre(libro_excel, monto):
    count = 0
    clientes_facturas = open('clientes_facturas.txt', 'w')
    datos_cliente = []
    datos_formateados = ''
    
    print("Dimension Pandas: ", len(libro_excel))

    for fila in libro_excel['RIF']:
        count += 1
        rif = fila
    
        if pd.isna(rif):
            continue
       
        elif count == len(libro_excel) -1:
            break
        
        elif pd.notna(rif):
            fila_cliente = obtener_numero_fila_por_valor(libro_excel, "RIF", rif)
            proximo_rif = encontrar_proximo_rif(libro_excel, "RIF", rif) #PASARLE EL NUMERO DE FILA (OBTENER NUMERO DE FILA DEL RIF)
            prox_product = proximo_producto(libro_excel, fila_cliente, "Facturas conciliadas/Líneas de factura/Producto")
            diario = codigo_vendedor(libro_excel, rif)

            #Obtener solo fila con plan mensual
            producto = str(get_celda(libro_excel, rif, 'RIF', 'Facturas conciliadas/Líneas de factura/Producto'))

            if diario == "0000X": #EN CASO DE QUE NO ESTE EN NINGUN DIARO NI BANCO
                continue
           

            if get_art(producto) != False:

                print("ID: " + str(count) + "Rif actual: " + str(rif) + "Proximo Rif:" + str(proximo_rif) + "Producto: " + str(producto) + "Proximo producto: " + str(prox_product))
    
                if proximo_rif == None and pd.notna(prox_product):
                    #print(")
                    continue #Se salta este asiento
        
            #Condiciones
                datos = consultar(rif, libro_excel, monto, count, datos_cliente)
                if datos != None:
                    print(datos)
                    datos_cliente.append(datos)
                    clientes_facturas.write('\n' + '\t'.join(str(dato) for dato in datos))
                    datos_formateados += ('\n' + '\t'.join(str(dato) for dato in datos))
                    print("CLIENTE AGREGADO")
        else:
            continue
            #print('Finalizado...')
    return datos_formateados #Para verificar que termino el proceso
        
           
        
        

