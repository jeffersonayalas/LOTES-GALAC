from trash.fila import get_celda
import datetime


def numero(borrador):
    return str(borrador)


def codigo_vendedor(diario): 
    vendedor = diario

    if vendedor == "BELLA FLORIDA 01":
        return '00007'
    elif vendedor == "BELLA FLORIDA 02":
        return "00008"
    elif vendedor == "FREE MARKET 01":
        return "00013"
    elif vendedor == "FREE MARKET 02":
        return "00014"
    elif vendedor == "LOS CAOBOS 01":
        return '00011'
    elif vendedor == "LOS CAOBOS 02":
        return "00017"
    elif vendedor == "LOS CAOBOS 03":
        return "00017"
    elif vendedor == "LOS CAOBOS 04":
        return "00017"
    elif vendedor == "LOS CAOBOS 05":
        return "00017"
    elif vendedor == "LOS CAOBOS 06":
        return "00017"
    elif vendedor == "LOS GUAYOS 01":
        return "00016"
    elif vendedor == "LOS GUAYOS 02":
        return "00028"
    elif vendedor == "LA MORITA 01" or vendedor == "LA MORITA 02" or vendedor == "LA MORITA 03":
        return "00012"
    elif vendedor == "LA MORITA 04" or vendedor == "LA MORITA 05" or vendedor == "LA MORITA 06":
        return "00019"
    elif vendedor == "CAGUA 01" or vendedor == "CAGUA 02":
        return "00020"
    elif vendedor in ("GUACARA 01", "GUACARA 02", "GUACARA 06"):
        return "00009"
    elif vendedor in ("GUACARA 04", "GUACARA 05", "GUACARA 06"):
        return "00029"
    elif vendedor in ("PUERTO CABELLO 1", "PUERTO CABELLO 2", "PUERTO CABELLO 3"):
        return "00015"
    elif vendedor in ("PUERTO CABELLO 4", "PUERTO CABELLO 5"):
        return "00018"
    elif vendedor == "PASEO LAS INDUSTRIAS 01":
        return "00024"
    elif vendedor == "CAJA PASEO LAS INDUSTRIAS 02":
        return "00025"
    elif vendedor == "SAN JOAQUIN 01":
        return "00021"
    elif vendedor == "TORRE MOVILNET 01":
        return '00002'
    elif vendedor == "TORRE MOVILNET 02":
        return '00003'
    elif vendedor == "TORRE MOVILNET 03":
        return '00023'
    elif vendedor == "TORRE MOVILNET 04":
        return '00026'
    elif vendedor == "TOCUYITO 01":
        return '00022'
    elif vendedor == "TOCUYITO 02":
        return '00027'
    elif vendedor == "FACTURACION 3":
        return '00006'
    elif "BANCO" in vendedor:
        return "00001"
    else:
        return "00001"
    

def get_observaciones(fecha):
    datos_fecha = fecha.strip().split('-')
    mes = datos_fecha[1]
    meses = {
            "01": "ENERO",
            "02": "FEBRERO",
            "03": "MARZO",
            "04": "ABRIL",
            "05": "MAYO",
            "06": "JUNIO",
            "07": "JULIO",
            "08": "AGOSTO",
            "09": "SEPTIEMBRE",
            "10": "OCTUBRE",
            "11": "NOVIEMBRE",
            "12": "DICIEMBRE",
        }
    
    return meses.get(mes, "Mes inválido")

def get_art(producto): #Funcion que devuelve codigo de articulo de acuerdo al plan del cliente
    art = producto.strip().split("]")
    prod = " "
    #print(art)
    if len(art) > 1:
        prod = art[1].lstrip(" ")
   
    productos = {
            "Residencial FTTH 100 Mbps": "FR100",
            "Residencial FTTH 200 Mbps": "FR200",
            "Residencial FTTH 400 Mbps": "FR400",
            "Residencial FTTH 450 Mbps": "FR400",
            "Residencial FTTH 600 Mbps": "FR600",
            "Residencial FTTH 700 Mbps": "FR700",
            "Residencial FTTH 800 Mbps": "FR800",
            "Residencial FTTH 850 Mbps": "FR850",
            "Residencial FTTH 1 Gbps": "FR1000",
            "Community Plus": "0004", ##### INACTIVO #### 
            "Pyme FTTH 100 Mbps": "FP100", 
            "Pyme FTTH 60 Mbps": "FP50",
            "Pyme FTTH 300 Mbps": "FP300",
            "Pyme FTTH 400 Mbps": "FP400",
            "Pyme FTTH 450 Mbps": "FP450",
            "Pyme FTTH 500 Mbps": "FP500",          
        }
    
    return productos.get(prod, False)


def get_tasa(tasa):
    return tasa

def get_fecha(fecha_hora_str):

        fecha_partes = fecha_hora_str.split(" ", 1) #se utiliza maxsplit=1 para evitar separar mas de dos elementos

        if fecha_partes is not None and len(fecha_partes) >= 1: #se verifica que el array tenga al menos un elemento
            fecha_str = fecha_partes[0]
            fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').strftime('%d/%m/%Y')
            fecha = fecha_partes[0]
            #fecha = "0-0-0"
            return fecha
        
def get_rif(rif):
    if rif != False:
        rif_comp = rif.split("-")
        return rif_comp[0] + rif_comp[1]
    
def get_nombre(nombre):
    nombre_data = nombre.split("-")
    if len(nombre_data) > 1:
        return nombre_data[1].lstrip()
    else:
        return nombre_data[0].lstrip()


        
            
    
    

    


