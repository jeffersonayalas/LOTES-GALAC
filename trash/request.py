import requests
from bs4 import BeautifulSoup
import re 
from datetime import datetime
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # <-- ADD THIS LINE

# Ejemplo de uso (REEMPLAZA con tus datos):
nombre_base_datos = "GDATA"
usuario_superusuario = "postgres"
contrasena_superusuario = "123456"  # ¡Nunca hardcodear contraseñas en producción!

req = open("request.txt", "a+")
info = ""

# --- ejecutar diariamente --- #
def get_bcv():
    # Making a GET request

    r = requests.get('https://www.bcv.org.ve/glosario/cambio-oficial', verify=False)
    print(r)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('div', id='dolar', class_='col-sm-12')
    content = soup.find_all('strong')
    cadena_limpia = re.sub(r'</?strong>', '', str(content[4]))
    cadena_limpia = re.sub(r'\s+', '', cadena_limpia)  # Eliminar espacios en blanco
    numero_str = cadena_limpia
    numero_float = float(numero_str.replace(",", "."))
    info = ("\n"+ (str(datetime.now().date()) + ";" + str(numero_float)))
    fecha = datetime.now().date()
    tasa = numero_float
    req.write(info)
    #print("Tasa del dolar: " + str(numero_float + 1) )
    return fecha, tasa

def create_table_bcv(conn):
    nombre_tabla1 = "datos_tasa"
   
    #Crear tablas en la base de datos
    try:
        #conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE
        cur = conn.cursor()
        # Construye la consulta SQL usando placeholders.
        # Tabla 1
        query_del = sql.SQL("DROP TABLE IF EXISTS {nombre_tabla1}").format(nombre_tabla1=sql.Identifier(nombre_tabla1))
        cur.execute(query_del) 
        conn.commit()  # Importante: Confirmar la transacción
        
        query1 = sql.SQL("""
        CREATE TABLE {nombre_tabla1} (
            id SERIAL PRIMARY KEY,
            fecha DATE NOT NULL,
            tasa FLOAT NOT NULL
        )
        """).format(nombre_tabla1=sql.Identifier(nombre_tabla1))
        cur.execute(query1)
        print(f"Tabla '{nombre_tabla1}' creada exitosamente.")

        conn.commit() 
        cur.close()
        
        return True

    except psycopg2.Error as e:
        print(f"Error al crear la tabla: {e}")
        return False
    
def connection_database(host = "localhost", puerto="5432"):
    # Conexión como superusuario
    conn = psycopg2.connect(user=usuario_superusuario, password=contrasena_superusuario, host=host, port=puerto)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE
    return conn

def cerrar_conexiones(conn, database):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = %s AND pid <> pg_backend_pid();
        """, (database,))  #Aquí está el cambio, se usa datname
        conn.commit()
        print(f"Se intentó cerrar conexiones a '{database}'.")
        # Recuperamos el número de sesiones cerradas
        num_cerradas = cur.rowcount
        print(f"Se cerraron {num_cerradas} conexiones a '{database}'.")
    except psycopg2.Error as e:
        print(f"Error al cerrar conexiones: {e}")
    finally:
        cur.close()  # Cierra el cursor para liberar recursos

def crear_base_datos(conn, nombre_bd): #This function drop the database if exist
    try:
        
        cur = conn.cursor()
        # Crea la base de datos
        #cur.execute(f"CREATE DATABASE {nombre_bd}")
        query_del = sql.SQL("DROP DATABASE IF EXISTS {nombre_bd}").format(nombre_bd=sql.Identifier(nombre_bd))
        cur.execute(query_del) 

        conn.commit()  # Importante: Confirmar la transacción
        cur.execute(sql.SQL("CREATE DATABASE {}").format(
        sql.Identifier(nombre_bd))
        
        )
        conn.commit()  # Importante: Confirmar la transacción

        print(f"Base de datos '{nombre_bd}' creada exitosamente.")
        cur.close()
        return True

    except psycopg2.Error as e:
        print(f"Error al crear la base de datos: {e}")
        if conn:
            conn.rollback()  # Revertir la transacción en caso de error
        return False
    

def get_tasa(connection, path_txt, fecha, tasa):
    """Lee el archivo TXT e inserta los datos en la base de datos."""
    try:
        with open(path_txt, "r", encoding="latin-1") as data_bcv: #utf-8 si latin-1 falla
            hoja_bcv = ""
            

            if insertar_tasa(fecha, tasa, connection):
                print("Los datos de Tasa BCV: ", fecha, tasa)

            '''
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
            '''
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

def consultar_data(conn, tabla):
    cur = conn.cursor()
    query = sql.SQL("""SELECT * FROM {tabla}""").format(tabla=sql.Identifier(tabla))
    cur.execute(query)
    rows = cur.fetchall()
    for fila in rows:
        print(fila)
    
    cur.close()

def update_data_txt():
    txt = open("request.txt", "w")
    fecha, tasa = get_bcv()
    txt.write(str(fecha) + ";" + str(tasa))

#get_bcv()
conn = connection_database()
contenido = req.read()
print(req.read())

""" 
if not contenido:
    print("Contenido vacio")
else:
    print(contenido)
"""
""" 

if len(contenido) == 0:
    print("Archivo vacio")
    cerrar_conexiones(conn, "datos_bcv")
    crear_base_datos(conn, "datos_bcv")
    create_table_bcv(conn)
    fecha, tasa = get_bcv()
    get_tasa(conn, "request.txt", fecha, tasa) 

"""


def main():
    fecha, tasa = get_bcv()
    get_tasa(conn, "request.txt", fecha, tasa)

main()


consultar_data(conn, "datos_tasa")
