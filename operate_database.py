import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # <-- ADD THIS LINE
from database import insertar_cliente, leer_txt, consultar_data


# Ejemplo de uso (REEMPLAZA con tus datos):
nombre_base_datos = "GDATA"
usuario_superusuario = "postgres"
contrasena_superusuario = "123456"  # ¡Nunca hardcodear contraseñas en producción!

def connection_database(host = "localhost", puerto="5432"):
    # Conexión como superusuario
    conn = psycopg2.connect(user=usuario_superusuario, password=contrasena_superusuario, host=host, port=puerto)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE
    return conn
   


def crear_base_datos(conn, nombre_bd): #This function drop the database if exist
    """Crea una base de datos PostgreSQL.

    Args:
        nombre_bd: Nombre de la base de datos a crear.
        usuario_superusuario: Nombre de usuario del superusuario de PostgreSQL.
        contrasena_superusuario: Contraseña del superusuario.
        host: Host de la base de datos (default: localhost).
        puerto: Puerto de la base de datos (default: 5432).

    Returns:
        True si la base de datos se creó correctamente, False en caso contrario.
    """
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



def create_tables(conn, usuario_superusuario, contrasena_superusuario, host='localhost', puerto='5432'):
    nombre_tabla1 = "contactos"
    nombre_tabla2 = "vendedores"
    nombre_tabla3 = "productos"
    #Crear tablas en la base de datos
    try:
         # Conexión como superusuario
        conn = psycopg2.connect(user=usuario_superusuario, password=contrasena_superusuario, host=host, port=puerto)
        #conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE
        cur = conn.cursor()
        # Construye la consulta SQL usando placeholders.
        # Tabla 1
        query_del = sql.SQL("DROP TABLE IF EXISTS {nombre_tabla1}").format(nombre_tabla1=sql.Identifier(nombre_tabla1))
        cur.execute(query_del) 
        conn.commit() # Importante: Confirmar la transacción
        
        query1 = sql.SQL("""
            CREATE TABLE {nombre_tabla1} (
                cod_galac TEXT NOT NULL,
                nombre_cliente TEXT NOT NULL,
                rif TEXT NOT NULL)
        """).format(nombre_tabla1=sql.Identifier(nombre_tabla1))
        cur.execute(query1)
        print(f"Tabla '{nombre_tabla1}' creada exitosamente.")

        conn.commit() 
        cur.close()
        
        return True

    except psycopg2.Error as e:
        print(f"Error al crear la tabla: {e}")
        return False
    

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

 
def update_database(path_txt):
    connection = connection_database()
    result = leer_txt(connection, path_txt)
    #consultar_data(connection)
    connection.close()
    return [True, result]

def main_database():
    connection = connection_database()
    cerrar_conexiones(connection, "GDATA")
    if crear_base_datos(connection, nombre_base_datos):
        print("Base de Datos creada")
        if create_tables(connection, usuario_superusuario, contrasena_superusuario):
            print("Tabla creada exitosamente. ")
        else: 
            print("No se pudo crear la tabla. ")
        #Si se crea la base de datos
    else:
        print("Proceso fallido.")
        connection.rollback()

    connection.close()
    return True







