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
    datos_fecha = fecha.strip().split('/')
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
   
    if len(art) > 1:
        prod = art[1].lstrip(" ")
    productos = {
        'Residencial FTTH 1 Gbps': 'PLN-FTH-0014',
        'Residencial FTTH 1 Gbps PD24': 'PLN-FTH-0035',
        'Residencial FTTH 10 Gbps': 'PLN-FTH-0100',
        'Residencial FTTH 10 Mbps': 'PLN-FTH-0013',
        'Residencial FTTH 100 Mbps': 'PLN-FTH-0024',
        'Residencial FTTH 100 Mbps PD24': 'PLN-FTH-0030',
        'Residencial FTTH 2.5 Gbps': 'PLN-FTH-0099',
        'Residencial FTTH 20 Mbps': 'PLN-FTH-0017',
        'Residencial FTTH 200 Mbps': 'PLN-FTH-0019',
        'Residencial FTTH 200 Mbps PD24': 'PLN-FTH-0031',
        'Residencial FTTH 250 Mbps': 'PLN-FTH-0101',
        'Residencial FTTH 30 Mbps': 'PLN-FTH-0015',
        'Residencial FTTH 35 Mbps': 'PLN-FTH-0018',
        'Residencial FTTH 400 Mbps': 'PLN-FTH-0001',
        'Residencial FTTH 400 Mbps PD24': 'PLN-FTH-0032',
        'Residencial FTTH 400 Mbps promocional día del amor': 'PLN-FTH-0036',
        'Residencial FTTH 600 Mbps': 'PLN-FTH-0003',
        'Residencial FTTH 600 Mbps PD24': 'PLN-FTH-0033',
        'Residencial FTTH 700 Mbps': 'PLN-FTH-0025',
        'Residencial FTTH 80 Mbps': 'PLN-FTH-0023',
        'Residencial FTTH 800 Mbps': 'PLN-FTH-0010',
        'Residencial FTTH 800 Mbps PD24': 'PLN-FTH-0034',
        'Residencial FTTH 85 Mbps': 'PLN-FTH-0022',
        'Residencial FTTH 850 Mbps': 'PLN-FTH-0011',
        'Residencial FTTH Esencial - 50Mbps': 'PLN-FTH-0009',
        'Residencial Performance Plus': 'PLN-RF-0012',
        'Residencial Performance Plus 50 Mbps': 'PLN-RF-0018',
        'Residencial RF 15 Mbps': 'PLN-RF-0019',
        'Residencial RF 50 Mbps': 'PLN-RF-0020',
        'Residencial Select 35 Mbps': 'PLN-RF-0004',
        'Residencial Ultra 30 Mbps': 'PLN-RF-0003',
        'Antena Parabólica Banda C de 2,4m': 'ATN-0001',
        'Antena Parabólica microperforada de 16ft': 'ATN-0002',
        'Antena marca Mimosa modelo B24': 'ATN-0003',
        'Antena marca Mimosa modelo C5C': 'ANT-MMS-0006',
        'Antena marca Mimosa modelo C5X': 'ANT-MMS-0005',
        'Antena marca RF Elements modelo HG3TPA60V2 Horn asimétrica de 60° (60°H 25°V) 17 dBi': 'ANT-RFE-0008',
        'Antena marca Ubiquiti modelo LAP-GPS LiteAP GPS 90': 'ANT-UBN-0001',
        'Antena marca Ubiquiti modelo LiteBeam AC GEN2 LBE-5AC gen2': 'ANT-UBN-0003',
        'Antena marca Ubiquiti modelo PBE-5AC-GEN2 POWER BEAM': 'ANT-UBN-0002',
        'Antena marca Ubiquiti modelo ROCKET PRISM 5AC-GEN2 (Radio)': 'ANT-UBN-0007',
        'Antena marca Ubiquiti modelo UAP-AC-PRO MM': 'ANT-UBN-0004',
        'Bobina de cable coaxial RG11 de 305 m': 'BOB-001',
        'Bobina de cable coaxial RG6 153 metros': 'BOB-002',
        'Carrete de fibra óptica marca APT modelo ADSS-48H/5KM 48H Span 120': 'CFO-APT-0043',
        'Carrete de fibra óptica marca APT modelo ADSS-96H/5KM 96H Span 120': 'CFO-APT-0030',
        'Carrete de fibra óptica marca APT modelo ASU-24-120M/5KM Mini ADSS (ASU) G.652D 24H Span 120': 'CFO-APT-0028',
        'Carrete de fibra óptica marca APT modelo G.657A2 DP02/2KM Drop con mensajero': 'CFO-APT-0027',
        'Carrete de fibra óptica marca APT modelo G.657A2 DP06/2KM Drop 6H con mensajero': 'CFO-APT-0042',
        'Carrete de fibra óptica marca APT modelo Mini ADSS (ASU) G.652D 12H Span 80': 'CFO-APT-0041',
        'Carrete de fibra óptica marca CSS modelo FO Mini ADSS (ASU) G.652D MINI-ADSS-12B1.3/4KM 12H Span 80': 'CFO-CSS-0046',
        'Carrete de fibra óptica marca Cablix modelo ADSS-09G652024-SJ100/4km ADSS 24H Span 100': 'CFO-CBX-0017',
        'Carrete de fibra óptica marca Cablix modelo G.657A2 DCSSF09G657A2002 Cablix Drop 2H con mensajero 2Km': 'CFO-CBX-0006',
        'Carrete de fibra óptica marca Cablix modelo Mini ADSS (ASU) G.652D 12H Span 100 4km': 'CFO-CBX-0021',
        'Carrete de fibra óptica marca Cablix modelo Mini ADSS (ASU) G.652D 24H Span 100 4km': 'CFO-CBX-0025',
        'Carrete de fibra óptica marca DISTELNET modelo G.657A2 DP02/2KM Drop con mensajero': 'CFO-DST-0044',
        'Carrete de fibra óptica marca DISTELNET modelo GJYXFCH-1B6A1 1H 2KM Drop con mensajero': 'CFO-DIS-0028',
        'Carrete de fibra óptica marca Domus modelo G.657A2 DFB-01M outdoor Drop 1H con mensajero 1km': 'CFO-DOM-0021',
        'Carrete de fibra óptica marca Fiberhome modelo ADSS Mini 8H 4Km Fiberhome': 'CFO-FBH-0019',
        'Carrete de fibra óptica marca Fiberhome modelo ASU 24H SPAN 80 4KM': 'CFO-FBH-0013',
        'Carrete de fibra óptica marca Fiberhome modelo FO Mini ADSS (ASU) G.652D MINI-ADSS-12C/4KM 12H Span 80': 'CFO-FBH-0012',
        'Carrete de fibra óptica marca Fiberhome modelo G.657A2 IC-FIG8A2-2C Drop 2H con mensajero 1Km OUTDOOR': 'CFO-FBH-0009',
        'Carrete de fibra óptica marca Fiberhome modelo G.657A2ICDROPA21C Drop 1H sin mensajero 1Km In/Out': 'CFO-FBH-0007',
        'Carrete de fibra óptica marca Fiberhome modelo LPOC-ADSS-128C-S100/4KM 128H Span 100': 'CFO-FBH-0026',
        'Carrete de fibra óptica marca Fiberhome modelo LPOC-ADSS-96C-S100/4KM 96H Span 100': 'CFO-FBH-0024',
        'Carrete de fibra óptica marca Fiberhome modelo OC-ADSS-48C-S100/4KM 48H Span 100': 'CFO-FBH-0002',
        'Carrete de fibra óptica marca Fiberhome modelo OCADSS72CS100/4KM 72H Span 100': 'CFO-FBH-0003',
        'Carrete de fibra óptica marca Fujikura modelo ADSS 24H SPAN 150 5KM': 'CFO-FJK-0014',
        'Carrete de fibra óptica marca Fujikura modelo ADSS Mini 12H 4Km': 'CFO-FJK-0016',
        'Carrete de fibra óptica marca Optictimes modelo ADSS Mini 8H 5Km': 'CFO-OPT-0020',
        'Carrete de fibra óptica marca Optictimes modelo ADSS-24B1-100S/5KM ADSS 24H Span 100': 'CFO-OPT-0018',
        'Carrete de fibra óptica marca Optictimes modelo ADSS-24B1-200S/5KM 24H Span 200': 'CFO-OPT-0001',
        'Carrete de fibra óptica marca Optictimes modelo ADSS-48B1-120S/5KM 48H Span 120': 'CFO-OPT-0011',
        'Carrete de fibra óptica marca Optictimes modelo ADSS-96B1-100S/5KM 96H Span 100': 'CFO-OPT-0008',
        'Carrete de fibra óptica marca Optictimes modelo ADSS-96B1-100S/5KM 96H Span 120': 'CFO-OPT-0023',
        'Carrete de fibra óptica marca Optictimes modelo ASU-24B1-120M/5KM Mini ADSS (ASU) G.652D 24H Span 120': 'CFO-OPT-0010',
        'Carrete de fibra óptica marca Optictimes modelo Drop G.657A2 1H con mensajero 1Km': 'CFO-OPT-0022',
        'Carrete de fibra óptica marca Optictimes modelo G.657A2 GJYXFCH-2B6/2KM Drop 2H con mensajero': 'CFO-OPT-0005',
        'Carrete de fibra óptica marca Optictimes modelo G.657A2 1KM Drop 2H con mensajero': 'CFO-OPT-0021',
        'Carrete de fibra óptica marca Optictimes modelo GYFXTY-8 Flat 8H 5Km': 'CFO-OPT-0015',
        'Carrete de fibra óptica marca Optictimes modelo Mini ADSS (ASU) G.652D ASU-12B1-80M/5km 12H Span 80': 'CFO-OPT-0004',
        'Carrete de fibra óptica marca TECNE modelo G.657A2 APT-DPO2/2KM Drop con mensajero': 'CFO-TEC-0045',
        'Servicio Instalación de clientes': 'RV-CUA-0008',
        'Dedicado Netcom Tecne': 'SER-0001',
        'Mbps Dedicado': 'PLN-DED-0001',
        'Asistencia técnica estándar': 'SER-0001',
        'Pyme 40 Mbps': 'PLN-RF-0014',
        'Pyme 50 Mbps': 'PLN-RF-0015',
        'Pyme Básico Asimétrico': 'PLN-RF-0006',
        'Pyme FTTH 100 Mbps': 'PLN-FTH-0002',
        'Pyme FTTH 300 Mbps': 'PLN-FTH-0006',
        'Pyme FTTH 350 Mbps': 'PLN-FTH-0008',
        'Pyme FTTH 400 Mbps': 'PLN-FTH-0007',
        'Pyme FTTH 450 Mbps': 'PLN-FTH-0012',
        'Pyme FTTH 500 Mbps': 'PLN-FTH-0016',
        'Pyme FTTH 60 Mbps': 'PLN-FTH-0005',
        'Pyme Performance': 'PLN-RF-0017',
        'Pyme Plus Más': 'PLN-RF-0002',
        'Pyme Plus Ultra': 'PLN-RF-0010',
        'Pyme Ultra Asimétrico': 'PLN-RF-0007',
        'Alquiler de IP Pública': 'AIP-NET-0001',
        'Community Plus 10 Mbps': 'PLN-CAB-0001',
        'Community Plus 100 Mbps': 'PLN-CAB-0002',
        'Community Plus 15 Mbps': 'PLN-CAB-0003',
        'Community Plus 150 Mbps': 'PLN-CAB-0015',
        'Community Plus 20 Mbps': 'PLN-CAB-0004',
        'Community Plus 25 Mbps': 'PLN-CAB-0005',
        'Community Plus 30 Mbps': 'PLN-CAB-0006',
        'Community Plus 35 Mbps': 'PLN-CAB-0007',
        'Community Plus 4 Mbps': 'PLN-CAB-0008',
        'Community Plus 40 Mbps': 'PLN-CAB-0009',
        'Community Plus 45 Mbps': 'PLN-CAB-0010',
        'Community Plus 50 Mbps': 'PLN-CAB-0011',
        'Community Plus 60 Mbps': 'PLN-CAB-0012',
        'Community Plus 70 Mbps': 'PLN-CAB-0013',
        'Community Plus 8 Mbps': 'PLN-CAB-0016',
        'Community Plus 80 Mbps': 'PLN-CAB-0014',
        'Dedicado Netcom Tecne': 'SRV-MDC-0001',
        'Prefijo de IPs públicas': 'SRV-PIP-0001',
        'Servicio BGP': 'SRV-BGP-0001',
        'Servicio de Habilitación de Puertos': 'SRV-HPT-0001',
        'Servicio de apertura de puertos': 'SRV-APT-0001'
    }

    # Verificar si el producto está en las claves del diccionario
    for clave in productos.keys():
        if prod in clave:
            print("PRODUCTOS --------------->>>>", productos.get(clave))
            return productos[clave]  # Devuelve el código de producto correspondiente
    
    return 'P0001'  # Retorna None si no se encuentra el producto
        
    """ 
    found = any(producto in key for key in productos.keys())

    if found:
        print(f'El producto "{producto}" se encuentra parcialmente en alguna de las llaves del diccionario.')
    return productos.get(prod, 'P0001')"
    """


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


        
            
    
    

    


