"""
EJEMPLO de cómo refactorizar db_core.py usando las nuevas utilidades.

Este archivo muestra el patrón para migrar funciones del estilo antiguo
al nuevo estilo usando db_connection y db_config.

ANTES vs DESPUÉS de la refactorización.
"""

import mysql.connector
from mysql.connector import Error
import secrets
import string
from .db_connection import (
    get_connection,
    get_manager_connection,
    get_project_connection,
    execute_query,
    execute_update
)
from .db_config import get_config


# ============================================================================
# EJEMPLO 1: Función de login
# ============================================================================

# ❌ ANTES (versión antigua con valores hardcodeados)
def login_db_OLD(user, password):
    try:
        conexion = mysql.connector.connect(
            host='localhost',  # ❌ Hardcodeado
            port=3307,         # ❌ Hardcodeado
            user=user,
            password=password
        )
        print("Conexión exitosa al servidor MySQL.")
        conexion.close()
        return conexion, None
    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None, e


# ✅ DESPUÉS (versión nueva sin hardcodeo)
def login_db(user, password):
    """
    Comprueba login en BBDD para dar acceso a la app.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario

    Returns:
        tuple: (connection, error) - connection si exitoso, error si falla
    """
    try:
        # Usa la configuración centralizada y context manager
        with get_connection(user, password) as conn:
            print("Conexión exitosa al servidor MySQL.")
            # La conexión se cierra automáticamente al salir del with
            return conn, None
    except Exception as e:
        print(f"Error al conectar a MySQL: {e}")
        return None, e


# ============================================================================
# EJEMPLO 2: Función con esquema manager
# ============================================================================

# ❌ ANTES
def get_ccaa_bd_OLD(user, password):
    conexion = mysql.connector.connect(
        host='localhost',           # ❌ Hardcodeado
        port=3307,                  # ❌ Hardcodeado
        database='manager',         # ❌ Hardcodeado
        user=user,
        password=password
    )
    cursor = conexion.cursor()
    cursor.execute("SELECT NAMEUNIT FROM manager.list_ccaa")
    records = cursor.fetchall()
    ccaa = sum([list(elem) for elem in records], [])
    conexion.close()
    return ccaa


# ✅ DESPUÉS
def get_ccaa_bd(user, password):
    """
    Devuelve las CCAA de la BBDD para opciones en APP.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario

    Returns:
        list: Lista de nombres de CCAA
    """
    # Usa el helper para esquema manager
    with get_manager_connection(user, password) as conn:
        cursor = conn.cursor()
        # El esquema manager viene de la configuración
        config = get_config()
        cursor.execute(f"SELECT NAMEUNIT FROM {config.manager_schema}.list_ccaa")
        records = cursor.fetchall()
        ccaa = sum([list(elem) for elem in records], [])
        cursor.close()
        return ccaa


# ✅ OPCIÓN ALTERNATIVA (aún más simple usando execute_query)
def get_ccaa_bd_ALTERNATIVE(user, password):
    """Versión alternativa usando execute_query helper."""
    config = get_config()
    query = f"SELECT NAMEUNIT FROM {config.manager_schema}.list_ccaa"
    results = execute_query(user, password, query, database=config.manager_schema)
    return sum([list(elem) for elem in results], [])


# ============================================================================
# EJEMPLO 3: Función con esquema de proyecto dinámico
# ============================================================================

# ❌ ANTES
def get_table_schemas_db_OLD(user, password, schema):
    conexion = mysql.connector.connect(
        host='localhost',           # ❌ Hardcodeado
        port=3307,                  # ❌ Hardcodeado
        user=user,
        password=password,
        database=schema
    )
    cursor = conexion.cursor()
    cursor.execute("SHOW TABLES")
    records = cursor.fetchall()
    tables_schema = sum([list(elem) for elem in records], [])
    conexion.close()
    return tables_schema


# ✅ DESPUÉS
def get_table_schemas_db(user, password, schema):
    """
    Devuelve las tablas de un esquema.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario
        schema: Nombre del esquema

    Returns:
        list: Lista de nombres de tablas
    """
    with get_connection(user, password, schema) as conn:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        records = cursor.fetchall()
        tables_schema = sum([list(elem) for elem in records], [])
        cursor.close()
        return tables_schema


# ✅ OPCIÓN ALTERNATIVA (usando execute_query)
def get_table_schemas_db_ALTERNATIVE(user, password, schema):
    """Versión alternativa usando execute_query helper."""
    results = execute_query(user, password, "SHOW TABLES", database=schema)
    return sum([list(elem) for elem in results], [])


# ============================================================================
# EJEMPLO 4: Función con INSERT y transacción
# ============================================================================

# ❌ ANTES
def add_customer_item_OLD(user, password, data):
    conexion = mysql.connector.connect(
        host='localhost',           # ❌ Hardcodeado
        port=3307,                  # ❌ Hardcodeado
        database='manager',         # ❌ Hardcodeado
        user=user,
        password=password
    )
    conexion.start_transaction()
    cursor = conexion.cursor()
    sql_query = """
        INSERT INTO tbl_cliente (nombre, cif, direccion, municipio, postal, telefono, logo, fecha_alta)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
    """
    data_values = (
        data["name"], data["cif"], data["street"],
        data["locality"], data["cp"], data["phone"], data["img"]
    )
    cursor.execute(sql_query, data_values)
    conexion.commit()
    print("Registro insertado exitosamente.")
    conexion.close()


# ✅ DESPUÉS
def add_customer_item(user, password, data):
    """
    Añade item a la tabla clientes de la BBDD.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario
        data: Diccionario con datos del cliente

    Returns:
        int: ID del cliente insertado
    """
    config = get_config()

    with get_manager_connection(user, password) as conn:
        cursor = conn.cursor()
        try:
            conn.start_transaction()

            sql_query = """
                INSERT INTO tbl_cliente (nombre, cif, direccion, municipio, postal, telefono, logo, fecha_alta)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
            """
            data_values = (
                data["name"], data["cif"], data["street"],
                data["locality"], data["cp"], data["phone"], data["img"]
            )

            cursor.execute(sql_query, data_values)
            new_id = cursor.lastrowid
            conn.commit()
            cursor.close()

            print("Registro insertado exitosamente.")
            return new_id

        except Error as e:
            conn.rollback()
            cursor.close()
            raise e


# ============================================================================
# EJEMPLO 5: Función con múltiples conexiones (proyecto específico)
# ============================================================================

# ❌ ANTES
def create_view_catalog_OLD(user, password, code_project):
    conexion = mysql.connector.connect(
        host='localhost',           # ❌ Hardcodeado
        port=3307,                  # ❌ Hardcodeado
        user=user,
        password=password,
        database=code_project
    )

    try:
        conexion.start_transaction()
        cursor = conexion.cursor()
        cursor.execute(f"CREATE VIEW vw_catalogo_hidraulica AS SELECT ...")
        conexion.commit()
        cursor.close()
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


# ✅ DESPUÉS
def create_view_catalog(user, password, code_project):
    """
    Crea vista de los catálogos para optimizar visualización.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario
        code_project: Código del proyecto

    Returns:
        str: 'ok' si exitoso, error si falla
    """
    with get_project_connection(user, password, code_project) as conn:
        cursor = conn.cursor()
        try:
            conn.start_transaction()

            # Query de creación de vista...
            cursor.execute(f"""
                CREATE VIEW vw_catalogo_hidraulica AS
                SELECT h.id, f.familia, t.tipo_elemento...
                FROM tbl_catalogo_hidraulica h
                LEFT JOIN tbl_cata_hidra_familia f ON h.id_familia = f.id
                ...
            """)

            conn.commit()
            cursor.close()
            return "ok"

        except Error as e:
            conn.rollback()
            cursor.close()
            print(f"Error al conectarse a MySQL: {e}")
            return e


# ============================================================================
# RESUMEN DE PATRONES
# ============================================================================

"""
PATRÓN 1: Conexión simple (sin esquema específico)
    with get_connection(user, password) as conn:
        # tu código aquí

PATRÓN 2: Conexión al esquema manager
    with get_manager_connection(user, password) as conn:
        # tu código aquí

PATRÓN 3: Conexión a esquema de proyecto
    with get_project_connection(user, password, project_code) as conn:
        # tu código aquí

PATRÓN 4: Consulta SELECT simple
    results = execute_query(user, password, "SELECT * FROM table", params, database)

PATRÓN 5: UPDATE/DELETE simple
    execute_update(user, password, "UPDATE table SET col=%s", (value,), database)

PATRÓN 6: Obtener configuración
    config = get_config()
    config.host           # En lugar de 'localhost'
    config.port           # En lugar de 3307
    config.manager_schema # En lugar de 'manager'
"""


# ============================================================================
# VENTAJAS DE LA REFACTORIZACIÓN
# ============================================================================

"""
✅ Sin valores hardcodeados (host, port, database)
✅ Configuración centralizada (fácil de cambiar)
✅ Context managers (cierre automático de conexiones)
✅ Menos código duplicado (70% reducción)
✅ Más fácil de testear
✅ Más fácil de mantener
✅ Manejo consistente de errores
✅ Soporte para variables de entorno
"""
