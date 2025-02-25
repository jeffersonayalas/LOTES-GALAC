import psycopg2
from psycopg2 import sql

def leer_txt(connection, archivo_txt):
    """Lee el archivo TXT e inserta los datos en la base de datos."""
    try:
        data_clientes = archivo_txt #utf-8 si latin-1 falla
        hoja_cliente = ""
        for linea in data_clientes:
            datos_cliente = linea.split(";") # strip() para eliminar espacios en blanco
                
            print(len(datos_cliente))
            if len(datos_cliente) == 27 or len(datos_cliente) == 26: #Verifica que la línea tenga 3 elementos
                cod_galac, nombre, rif = datos_cliente[0], datos_cliente[1], datos_cliente[2]
                try:
                    print("Cliente: ", datos_cliente)
                    insertar_cliente(cod_galac, nombre, rif, connection)
                    sep = "---------------------------------------------\n"
                    hoja_cliente += str(sep + "Nombre: " + str(nombre) + "\nRif: " + str(rif) + "\n")
                except Exception as e:
                        print(f"Error en la linea: {linea.strip()}. Error: {e}")
            else:
                print(f"Línea incorrecta: {linea.strip()}")
                continue
        return hoja_cliente
                    

    except FileNotFoundError as e:
        print("Archivo bd_clientes.txt no encontrado. {e}")
    except Exception as e:
        print(f"Error al leer o procesar el archivo: {e}")

# --- Codigo para leer txt de productos clientes --- #
def leer_productos(connection):
    """Lee el archivo TXT e inserta los datos en la base de datos."""
    try:
        with open("productos.txt", "r", encoding="latin-1") as data_productos: #utf-8 si latin-1 falla
            id = 0
            for linea in data_productos:
                id += 1
                datos_cliente = linea.split(";") # strip() para eliminar espacios en blanco
                print(len(datos_cliente))
                if len(datos_cliente) > 0: #Verifica que la línea tenga 3 elementos
                    name, code_object = datos_cliente[0], datos_cliente[1]
                    try:
                        insertar_plan(id, name, code_object, connection)
                    except Exception as e:
                        print(f"Error en la linea: {linea.strip()}. Error: {e}")
                else:
                    print(f"Línea incorrecta: {linea.strip()}")

    except FileNotFoundError:
        print("Archivo bd_clientes.txt no encontrado.")
    except Exception as e:
        print(f"Error al leer o procesar el archivo: {e}")

# --- Codigo para insertar clientes --- #
def insertar_cliente(cod_galac, nombre_cliente, rif, conn):
    """Inserta un cliente en la tabla 'clientes' de forma segura."""
    try:


        if len(rif) > 1:
            rif =  rif[0] + '-' + rif[1:]  # Insertar el guion en la segunda posición

        # Verificar si el cliente ya existe
        query_check = "SELECT COUNT(*) FROM clientes WHERE rif = %s;"
        cur.execute(query_check, (rif,))
        exists = cur.fetchone()[0]

        if exists > 0:
            print("El cliente ya existe en la base de datos.")
            return
        
        cur = conn.cursor()
        query1 = "SELECT column_name FROM information_schema.columns WHERE table_name = 'clientes';"
        print(cur.execute(query1))
        
        conn.commit()

        query = "INSERT INTO clientes (rif, cod_galac, nombre_cliente) VALUES (%s, %s, %s);"
        cur.execute(query, (rif, cod_galac, nombre_cliente))
        conn.commit()
        print("Cliente insertado correctamente.")

    except psycopg2.Error as e:
        print(f"Error al insertar cliente: {e}")
        conn.rollback()
    except Exception as e:
        print(f"Error inesperado al insertar cliente: {e}")
    finally:
        if cur:
            cur.close()

# --- Codigo para insertar el producto --- #
def insertar_plan(id,name, code_object, conn):
    """Inserta un cliente en la tabla 'clientes' de forma segura."""
    try:
        cur = conn.cursor()
        query = "INSERT INTO productos (id, nombre, codigo) VALUES (%s, %s, %s);"
        cur.execute(query, (id, name, code_object))
        conn.commit()
        print("Cliente insertado correctamente.")
    except psycopg2.Error as e:
        print(f"Error al insertar cliente: {e}")
        conn.rollback()
    except Exception as e:
        print(f"Error inesperado al insertar cliente: {e}")
    finally:
        if cur:
            cur.close()

def get_tasa(connection, path_txt):
    """Lee el archivo TXT e inserta los datos en la base de datos."""
    try:
        with open(path_txt, "r", encoding="latin-1") as data_bcv: #utf-8 si latin-1 falla
            hoja_bcv = ""
            id = 0

            for linea in data_bcv:
                id += 1
                datos_tasa = linea.split(";") # strip() para eliminar espacios en blanco
                
                if len(datos_tasa) == 2: #Verifica que la línea tenga 2 elementos
                    fecha, tasa = datos_tasa[0], datos_tasa[1]
                    try:
                        print("Datos de Tasa BCV: ", datos_tasa)
                        insertar_tasa(fecha, tasa, connection)
                        hoja_bcv += str(fecha) + ";" + str(tasa) + "\n"
                    except Exception as e:
                        print(f"Error en la linea: {linea.strip()}. Error: {e}")
                else:
                    print(f"Línea incorrecta: {linea.strip()}")
                    continue
        return hoja_bcv
    
    except FileNotFoundError as e:
        print("Archivo .txt no encontrado. {e}")
    except Exception as e:
        print(f"Error al leer o procesar el archivo: {e}")

def insertar_tasa(fecha, tasa, conn):
    """Inserta un cliente en la tabla 'clientes' de forma segura."""
    try:
        cur = conn.cursor()
        print("DATOS: " + str(fecha) + " " + str(tasa))
        query = "INSERT INTO datos_tasa (fecha, tasa) VALUES (%s, %s);"
        cur.execute(query, (fecha, tasa))
        conn.commit()
        print("Datos insertados correctamente.")
    except psycopg2.Error as e:
        print(f"Error al insertar cliente: {e}")
        conn.rollback()
    except Exception as e:
        print(f"Error inesperado al insertar cliente: {e}")
    finally:
        if cur:
            cur.close()
    return 0


def consultar_data(conn, tabla):
    cur = conn.cursor()
    query = sql.SQL("""SELECT * FROM {tabla}""").format(tabla=sql.Identifier(tabla))
    cur.execute(query)
    rows = cur.fetchall()
    for fila in rows:
        print(fila)
    
    cur.close()

def drop(conn):
    #Se eliminan todos los datos de la tabla
    return 0

def get_cliente(conn, rif, tabla="clientes"): #Retorna los codigo de galac que corresponden a las suscripciones del cliente
    
    if rif != False:
        #rif_comp = rif.split("-")
        #print(rif_comp)
        cur = conn.cursor()
        query = sql.SQL("SELECT cod_galac FROM {tabla} WHERE rif = %s;").format(tabla=sql.Identifier(tabla))
        #dat = rif_comp[0] + rif_comp[1]
        cur.execute(query, (rif,))
        rows = cur.fetchone()

        if rows != None:
            if len(rows) > 0:
                return rows
    else: 
        return None
    
    #Conectar con api para obtener cliente 
    

def get_code_client(conn, code):
    try:
        cur = conn.cursor()
        # Consulta para verificar si el código ya existe
        query = "SELECT COUNT(*) FROM clientes WHERE cod_galac = %s;"
        cur.execute(query, (code,))
        resultado = cur.fetchone()[0]

        cur.close()
        
        return resultado > 0  # Retorna True si existe, False si no
    except Exception as e:
        print(f"Error al consultar la base de datos: {e}")
        return True  # Si hay un error, asumimos que el código ya existe para evitar colisiones.


    









