import psycopg2

def leer_txt(connection, path_txt):
    """Lee el archivo TXT e inserta los datos en la base de datos."""
    try:
        with open(path_txt, "r", encoding="latin-1") as data_clientes: #utf-8 si latin-1 falla
            hoja_cliente = ""
            for linea in data_clientes:
                datos_cliente = linea.split(";") # strip() para eliminar espacios en blanco
                
                print(len(datos_cliente))
                if len(datos_cliente) == 26: #Verifica que la línea tenga 3 elementos
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
def insertar_cliente(cod_galac, nombre, rif, conn):
    """Inserta un cliente en la tabla 'clientes' de forma segura."""
    try:
        cur = conn.cursor()
        query = "INSERT INTO contactos (cod_galac, nombre_cliente, rif) VALUES (%s, %s, %s);"
        cur.execute(query, (cod_galac, nombre, rif))
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

def insertar_tasa(conn, path_txt):
    """Lee el archivo TXT e inserta los datos en la base de datos."""
    try:
        with open(path_txt, "r", encoding="latin-1") as data_clientes: #utf-8 si latin-1 falla
            hoja_cliente = ""
            for linea in data_clientes:
                datos_cliente = linea.split(";") # strip() para eliminar espacios en blanco
                
                print(len(datos_cliente))
                if len(datos_cliente) == 26: #Verifica que la línea tenga 3 elementos
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
        #return hoja_cliente
        return 0


def consultar_data(conn):

    cur = conn.cursor()
    query = "SELECT * FROM contacts;"
    cur.execute(query)
    rows = cur.fetchall()
    #print(rows)

    for fila in rows:
        print(fila)

def drop(conn):
    #Se eliminan todos los datos de la tabla
    return 0









