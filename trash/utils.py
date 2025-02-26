import psycopg2

def insertar_cliente(cod_galac, nombre, rif, conn):
    """Inserta un cliente en la tabla 'contactos' de forma segura, solo si no existe."""
    try:
        cur = conn.cursor()
        # Usamos ON CONFLICT para evitar el error si el cliente ya existe
        query = """
            INSERT INTO contactos (cod_galac, nombre_cliente, rif)
            VALUES (%s, %s, %s)
            ON CONFLICT (rif) DO NOTHING;
        """
        cur.execute(query, (cod_galac, nombre, rif))
        
        if cur.rowcount == 0:
            print("El cliente ya existe, no se insertó.")
        else:
            print("Cliente insertado correctamente.")
            
        conn.commit()
        
    except psycopg2.Error as e:
        print(f"Error al insertar cliente: {e}")
        conn.rollback()
    except Exception as e:
        print(f"Error inesperado al insertar cliente: {e}")
    finally:
        if cur:
            cur.close()

# Ejemplo de uso:
# conn = psycopg2.connect(database="nombre_db", user="usuario", password="clave", host="localhost", port="5432")
# insertar_cliente('123', 'Juan Perez', 'J-12345678-9', conn)
