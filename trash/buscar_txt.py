#funcion para realizar busqueda dentro del archivo txt

def buscar_txt(rut_facturas, rut_clientes):

    txt_facturas = open(rut_facturas, 'r', encoding="latin-1")
    
    #Realizamos la busqueda en los archivos con un ciclo for (anidados probablemente)
    #Se debe obtener el id de la primera factura en la lista y buscarlo en bd_clientes para obtener el nombre de los clientes

    #Primero se recorre el txt_facturas para obtener el ID de la primera factura (vamos por orden de fecha)
    for linea in txt_facturas:
        lineas = linea.split(';')

        print(lineas[2]) #Aqui se realiza una llamada a otra funcion para realizar la busqueda en bd clientes y obtener el nombre
        buscar_nombre_cliente(rut_clientes, lineas[2])



def buscar_nombre_cliente(rut_clientes, id_cliente): #busca el ID pasado del cliente en la base de datos de cliente
    bd_clientes = open(rut_clientes, 'r', encoding="latin-1")
    count = 0

    for linea in bd_clientes:
        lineas = linea.split(';')
        count += 1
        if lineas[0] == id_cliente:
            print('Cliente encontrado exitosamente:', lineas[0])
        else:
            print('Cliente no fue encontrado... Suerte la proxima')

        print(count)


buscar_txt('borradores.txt', 'bd_clientes.txt')


