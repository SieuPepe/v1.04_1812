import mysql.connector
from mysql.connector import Error


# ==================== GESTIÓN DE PROYECTOS ====================

# SELECCIONA DIRECTORIO PROYECTO
def project_directory_db(user, password, schema):
    try:
        # Establecer la conexión con el servidor MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            user=user,
            password=password,
        )
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Ejecutar la consulta para obtener la lista de CCAA
        cursor.execute(f"SELECT carpeta FROM {schema}.tbl_proyectos where codigo = '{schema}'")
        records = cursor.fetchall()
        folder = sum([list(elem) for elem in records], [])
        # Comprobar conexion y devuelve la conexion
        print("Conexión exitosa al servidor MySQL.")
        conexion.close()
        return folder

    except mysql.connector.Error as e:
        # Si no es posible conectar, devuelve el error
        print(f"Error al conectar a MySQL: {e}")
        return None, e


#AÑADE ITEM A LA TABLA PROYECTO DE LA BBDD
def add_project_item(user, password,data):
    try:
        # Establecer la conexión con el servidor MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            database='manager',
            user=user,
            password=password
        )
        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Consulta SQL con parámetros para evitar SQL Injection
        sql_query = """
               INSERT INTO tbl_proyectos (codigo, nombre, id_cliente, id_clie_usuario, adjudicatario, id_adj_usuario, fecha_creacion, descripcion, id_estado, id_provincia, id_ccaa, carpeta)
               VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s, %s)
               """
        # Datos a insertar
        data_values = (
            data["code"],
            data["name"],
            data["id_customer"],
            data["id_user_customer"],
            data["company"],
            data["id_user_company"],
            data["description"],
            data["id_state"],
            data["id_province"],
            data["id_ccaa"],
            data["folder"]
        )
        # Ejecutar la consulta
        cursor.execute(sql_query, data_values)
        # Confirmar la transacción
        conexion.commit()
        print("Registro insertado exitosamente.")
        conexion.close()
        return "ok"
    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#AÑADE ITEM A LA TABLA PROYECTO DE LA BBDD
def add_economic_project_item(user, password,data):
    try:
        # Establecer la conexión con el servidor MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            database='manager',
            user=user,
            password=password
        )
        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Consulta SQL con parámetros para evitar SQL Injection
        sql_query = """
               INSERT INTO tbl_proy_presupuesto (id_proyecto, tipo_presupuesto, gastos_generales, beneficio_industrial, baja, presupuesto_licitacion, iva)
               VALUES (%s, %s, %s, %s, %s, %s, %s)
               """
        # Datos a insertar
        data_values = (
            data["id_project"],
            data["type"],
            data["gg"],
            data["bi"],
            data["reduction"],
            data["tender"],
            data["iva"]
        )
        # Ejecutar la consulta
        cursor.execute(sql_query, data_values)
        # Confirmar la transacción
        conexion.commit()
        print("Registro insertado exitosamente.")
        conexion.close()
        return "ok"
    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#MODIFICAR ITEM A LA TABLA PROYECTO DE LA BBDD
def mod_project_item(user, password,data_project, data_tender,id_project):
    try:
        # Establecer la conexión con el servidor MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            database='manager',
            user=user,
            password=password
        )

        #modificadar datos de tbl_proyectos
        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Consulta SQL con parámetros para evitar SQL Injection
        sql_query = f"""
               UPDATE tbl_proyectos SET nombre = %s, id_cliente = %s, id_clie_usuario = %s, adjudicatario = %s, id_adj_usuario = %s, fecha_actualizacion = NOW(), descripcion = %s, id_estado = %s, carpeta = %s
               WHERE id = {id_project}
               """
        # Datos a insertar
        data_values = (
            data_project["name"],
            data_project["id_customer"],
            data_project["id_user_customer"],
            data_project["company"],
            data_project["id_user_company"],
            data_project["description"],
            data_project["id_state"],
            data_project["folder"]
        )
        # Ejecutar la consulta
        cursor.execute(sql_query, data_values)
        # Confirmar la transacción
        conexion.commit()
        cursor.close()

        #modificacion de datos de tbl_proy_presupuesto
        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Consulta SQL con parámetros para evitar SQL Injection
        sql_query = f"""
               UPDATE tbl_proy_presupuesto SET gastos_generales = %s, beneficio_industrial = %s, baja = %s, presupuesto_licitacion = %s, iva = %s
               WHERE id_proyecto = {id_project}
               """
        # Datos a insertar
        data_values = (
            data_tender["gg"],
            data_tender["bi"],
            data_tender["reduction"],
            data_tender["tender"],
            data_tender["iva"]
        )
        # Ejecutar la consulta
        cursor.execute(sql_query, data_values)
        # Confirmar la transacción
        conexion.commit()
        cursor.close()
        print("Registro insertado exitosamente.")
        conexion.close()
        return "ok"
    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


# ==================== GESTIÓN DE CLIENTES ====================

#AÑADE ITEM A LA TABLA CLIENTES DE LA BBDD
def add_customer_item(user, password,data):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        database='manager',
        user=user,
        password=password
    )
    conexion.start_transaction()
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Consulta SQL con parámetros para evitar SQL Injection
    sql_query = """
           INSERT INTO tbl_cliente (nombre, cif, direccion, municipio, postal, telefono, logo, fecha_alta)
           VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
           """
    # Datos a insertar
    data_values = (
        data["name"],
        data["cif"],
        data["street"],
        data["locality"],
        data["cp"],
        data["phone"],
        data["img"]
    )
    # Ejecutar la consulta
    cursor.execute(sql_query, data_values)
    # Confirmar la transacción
    conexion.commit()
    print("Registro insertado exitosamente.")
    conexion.close()


#DEVUELVE TODOS LOS CAMPOS DE UN ITEM DE LA TABLA CLIENTES DE LA BBDD
def get_customer_data(user, password, customer):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        database='manager',
        user=user,
        password=password
    )
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Consulta SQL con parámetros para evitar SQL Injection
    sql_query = f"""
           SELECT * FROM tbl_cliente WHERE nombre='{customer}'
           """
    # Ejecutar la consulta
    cursor.execute(sql_query)
    records = cursor.fetchall()
    # Formatear resultados
    option_items = sum([list(elem) for elem in records], [])
    # Cerrar conexión
    conexion.close()

    return option_items


#MODIFICA  LOS CAMPOS DE UN ITEM DE LA TABLA CLIENTES DE LA BBDD
def mod_customer_item(user, password, data, id_costumer):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        database='manager',
        user=user,
        password=password
    )
    conexion.start_transaction()
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Consulta SQL con parámetros para evitar SQL Injection
    sql_query = """
           UPDATE tbl_cliente
           SET nombre = %s, cif= %s, direccion= %s, municipio= %s, postal= %s, telefono= %s, logo= %s
           WHERE id = %s
           """
    # Datos a insertar
    data_values = (
        data["name"],
        data["cif"],
        data["street"],
        data["locality"],
        data["cp"],
        data["phone"],
        data["img"],
        id_costumer
    )
    # Ejecutar la consulta
    cursor.execute(sql_query, data_values)
    # Confirmar la transacción
    conexion.commit()
    print("Registro modificado exitosamente.")
    conexion.close()


# ==================== GESTIÓN DE USUARIOS DE CLIENTES ====================

#DEVUELVE TODOS LOS DATOS DE UN USUARIO DE UN CLIENTES DE LA BBDD
def get_user_customer_data(user, password, id_customer,id_user_customer):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        database='manager',
        user=user,
        password=password
    )
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Consulta SQL con parámetros para evitar SQL Injection
    sql_query = f"""
           SELECT * FROM tbl_clie_usuario WHERE id_cliente ='{str(id_customer)}' and id = '{str(id_user_customer)}'
           """
    # Ejecutar la consulta
    cursor.execute(sql_query)
    records = cursor.fetchall()
    # Formatear resultados
    option_items = [list(elem) for elem in records]
    # Cerrar conexión
    conexion.close()

    return option_items


#DEVUELVE EL ID DEl USUARIO DE UN CLIENTES DE LA BBDD
def get_id_user_customer(user, password, select_user,id_customer):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        database='manager',
        user=user,
        password=password
    )

    select_user_customer = select_user.split(", ")
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Consulta SQL con parámetros para evitar SQL Injection
    sql_query = f"""
           SELECT id FROM manager.tbl_clie_usuario WHERE nombre='{select_user_customer[1]}' and apellidos = '{select_user_customer[0]}' and id_cliente = '{id_customer}'
           """
    # Ejecutar la consulta
    cursor.execute(sql_query)
    records = cursor.fetchall()
    # Formatear resultados
    id_user_customer = [list(elem) for elem in records][0][0]
    # Cerrar conexión
    conexion.close()

    return id_user_customer


#AÑADE ITEM A LA TABLA USUARIOS DE CLIENTES DE LA BBDD
def add_user_customer_item(user, password,data,id_customer):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        database='manager',
        user=user,
        password=password
    )
    conexion.start_transaction()
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Consulta SQL con parámetros para evitar SQL Injection
    sql_query = """
           INSERT INTO tbl_clie_usuario (id_cliente, nombre, apellidos, email, telefono, fecha_alta)
           VALUES (%s, %s, %s, %s, %s, NOW())
           """
    # Datos a insertar
    data_values = (
        id_customer,
        data["name"],
        data["surname"],
        data["email"],
        data["phone"]
    )
    # Ejecutar la consulta
    cursor.execute(sql_query, data_values)
    # Confirmar la transacción
    conexion.commit()
    print("Registro insertado exitosamente.")
    conexion.close()


#MODIFICA  LOS CAMPOS DE UN ITEM DE LA TABLA USUARIOS DE CLIENTES DE LA BBDD
def mod_user_customer_item(user, password, data, id_costumer,id_user_customer):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        database='manager',
        user=user,
        password=password
    )
    conexion.start_transaction()
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Consulta SQL con parámetros para evitar SQL Injection
    sql_query = """
           UPDATE tbl_clie_usuario
           SET nombre = %s, apellidos= %s, email= %s, telefono= %s
           WHERE id = %s and id_cliente = %s
           """
    # Datos a insertar
    data_values = (
        data["name"],
        data["surname"],
        data["email"],
        data["phone"],
        id_user_customer,
        id_costumer
    )
    # Ejecutar la consulta
    cursor.execute(sql_query, data_values)
    # Confirmar la transacción
    conexion.commit()
    print("Registro modificado exitosamente.")
    conexion.close()


# ==================== GESTIÓN DE USUARIOS DE EMPRESA ====================

#DEVUELVE TODOS LOS ID DE LOS USUARIOS DE UN CLIENTES DE LA BBDD
def get_id_user_company(user, password, select_user):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        database='manager',
        user=user,
        password=password
    )

    select_user_company = select_user.split(", ")
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Consulta SQL con parámetros para evitar SQL Injection
    sql_query = f"""
           SELECT id FROM manager.tbl_empr_usuario WHERE nombre='{select_user_company[1]}' and apellidos = '{select_user_company[0]}'
           """
    # Ejecutar la consulta
    cursor.execute(sql_query)
    records = cursor.fetchall()
    # Formatear resultados
    id_user_company = [list(elem) for elem in records][0][0]
    # Cerrar conexión
    conexion.close()

    return id_user_company


#AÑADE ITEM A LA TABLA USUARIOS DE LA EMPRESA DE LA BBDD
def add_user_company_item(user, password,data):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        database='manager',
        user=user,
        password=password
    )
    conexion.start_transaction()
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Consulta SQL con parámetros para evitar SQL Injection
    sql_query = """
           INSERT INTO tbl_empr_usuario (nombre, apellidos, email, telefono, fecha_alta)
           VALUES (%s, %s, %s, %s, NOW())
           """
    # Datos a insertar
    data_values = (
        data["name"],
        data["surname"],
        data["email"],
        data["phone"]
    )
    # Ejecutar la consulta
    cursor.execute(sql_query, data_values)
    # Confirmar la transacción
    conexion.commit()
    print("Registro insertado exitosamente.")
    conexion.close()


#MODIFICA  LOS CAMPOS DE UN ITEM DE LA TABLA USUARIOS DE LA EMPRESA DE LA BBDD
def mod_user_company_item(user, password, data, id_user_company):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        database='manager',
        user=user,
        password=password
    )
    conexion.start_transaction()
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Consulta SQL con parámetros para evitar SQL Injection
    sql_query = """
           UPDATE tbl_empr_usuario
           SET nombre = %s, apellidos= %s, email= %s, telefono= %s
           WHERE id = %s
           """
    # Datos a insertar
    data_values = (
        data["name"],
        data["surname"],
        data["email"],
        data["phone"],
        id_user_company
    )
    # Ejecutar la consulta
    cursor.execute(sql_query, data_values)
    # Confirmar la transacción
    conexion.commit()
    print("Registro modificado exitosamente.")
    conexion.close()


#DEVUELVE TODOS LOS DATOS DE LOS USUARIOS DE LA EMPRESA DE LA BBDD
def get_user_company_data(user, password, id_user_company):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        database='manager',
        user=user,
        password=password
    )
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Consulta SQL con parámetros para evitar SQL Injection
    sql_query = f"""
           SELECT * FROM tbl_empr_usuario WHERE id = '{str(id_user_company)}'
           """
    # Ejecutar la consulta
    cursor.execute(sql_query)
    records = cursor.fetchall()
    # Formatear resultados
    option_items = [list(elem) for elem in records]
    # Cerrar conexión
    conexion.close()

    return option_items


# ==================== GESTIÓN DE CATÁLOGOS ====================

#AÑADE ITEM A LA TABLA CATÁLOGO HIDRÁULICO
def add_catalog_hidro_item(user, password,schema,data):
    try:
        # Establecer la conexión con el servidor MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            user=user,
            password=password
        )

        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Consulta SQL con parámetros para evitar SQL Injection
        sql_query = f"""
               INSERT INTO {schema}.tbl_catalogo_hidraulica (id_familia,id_tipo_hidraulica, id_marca, id_caracteristica, modelo, referencia, id_dni,id_dnf, id_pn, id_angulo, longitud, long_extremos, altura_eje, altura_total, peso, bloque_ref, descripcion, cod_partida)
               VALUES (%s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s)
               """
        # Datos a insertar
        data_values = (
            data[0],
            data[1],
            data[2],
            data[3],
            data[4],
            data[5],
            data[6],
            data[7],
            data[8],
            data[9],
            data[10],
            data[11],
            data[12],
            data[13],
            data[14],
            data[15],
            data[16],
            data[17]
        )
        # Ejecutar la consulta
        cursor.execute(sql_query, data_values)
        # Confirmar la transacción
        conexion.commit()
        print("Registro insertado exitosamente.")
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#MODIFICA  LOS CAMPOS DE UN ITEM DE LA TABLA CATÁLOGO HIDRAULICO DE LA BBDD
def mod_catalog_hidro_item(user, password,schema, data, id_item):
    try:
        # Establecer la conexión con el servidor MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            user=user,
            password=password
        )

        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Consulta SQL con parámetros para evitar SQL Injection
        sql_query = f"""
               UPDATE {schema}.tbl_catalogo_hidraulica
               SET id_familia = %s, id_tipo_hidraulica = %s, id_marca= %s, id_caracteristica= %s, modelo= %s, referencia= %s, id_dni = %s, id_dnf = %s, id_pn= %s, id_angulo = %s, longitud= %s, long_extremos= %s, altura_eje= %s, altura_total= %s, peso= %s, bloque_ref= %s, descripcion= %s , cod_partida = %s
               WHERE id = %s
               """
        # Datos a insertar
        data_values = (
            data[0],
            data[1],
            data[2],
            data[3],
            data[4],
            data[5],
            data[6],
            data[7],
            data[8],
            data[9],
            data[10],
            data[11],
            data[12],
            data[13],
            data[14],
            data[15],
            data[16],
            data[17],
            id_item
        )
        # Ejecutar la consulta
        cursor.execute(sql_query, data_values)
        # Confirmar la transacción
        conexion.commit()
        print("Registro modificado exitosamente.")
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#AÑADE ITEM A LA TABLA CATÁLOGO REGISTRO
def add_catalog_regis_item(user, password,schema,data):
    try:
        # Establecer la conexión con el servidor MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            user=user,
            password=password
        )

        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Consulta SQL con parámetros para evitar SQL Injection
        sql_query = f"""
               INSERT INTO {schema}.tbl_catalogo_registros (id_tipo_registro, id_proveedor, modelo, referencia, dimensionA, dimensionB, dimensionC,  descripcion, cod_partida)
               VALUES (%s, %s, %s, %s, %s, %s,  %s, %s, %s)
               """
        # Datos a insertar
        data_values = (
            data[0],
            data[1],
            data[2],
            data[3],
            data[4],
            data[5],
            data[6],
            data[7],
            data[8]
        )
        # Ejecutar la consulta
        cursor.execute(sql_query, data_values)
        # Confirmar la transacción
        conexion.commit()
        print("Registro insertado exitosamente.")
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#MODIFICA  LOS CAMPOS DE UN ITEM DE LA TABLA CATÁLOGO REGISTRO DE LA BBDD
def mod_catalog_regis_item(user, password,schema, data, id_item):
    try:
        # Establecer la conexión con el servidor MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            user=user,
            password=password
        )

        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Consulta SQL con parámetros para evitar SQL Injection
        sql_query = f"""
               UPDATE {schema}.tbl_catalogo_registros
               SET id_tipo_registro = %s, id_proveedor= %s, modelo= %s, referencia= %s, dimensionA = %s, dimensionB= %s, dimensionC= %s,  descripcion= %s, cod_partida= %s
               WHERE id = %s
               """
        # Datos a insertar
        data_values = (
            data[0],
            data[1],
            data[2],
            data[3],
            data[4],
            data[5],
            data[6],
            data[7],
            data[8],
            id_item
        )
        # Ejecutar la consulta
        cursor.execute(sql_query, data_values)
        # Confirmar la transacción
        conexion.commit()
        print("Registro modificado exitosamente.")
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


# ==================== GESTIÓN DE REGISTROS/INVENTARIO ====================

#AÑADE LOS ITEMS A TODAS LAS TABLAS HIJAS DE UN REGISTRO
def add_register_item(user, password,schema,data_inventory,data_pdf,data_photo,data_element_hidro,data_element_register,data_element_budget_hidro,data_element_budget_regis):
    try:
        # Establecer la conexión con el servidor MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            user=user,
            password=password
        )

        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()

        if len(data_inventory)!=0:
                # Consulta SQL con parámetros para evitar SQL Injection - tbl inventario
                sql_query = f"""
                       INSERT INTO {schema}.tbl_inventario (codigo, id_proyecto, id_municipio, id_estado, observaciones, id_certificacion)
                       VALUES (%s, %s, %s, %s, %s, %s)
                       """
                # Datos a insertar
                data_values = (
                    data_inventory[0],
                    data_inventory[1],
                    data_inventory[2],
                    3,
                    data_inventory[3],
                    3
                )
                # Ejecutar la consulta
                cursor.execute(sql_query, data_values)

        if len(data_element_hidro)!=0:
            for item in data_element_hidro:
                # Consulta SQL con parámetros para evitar SQL Injection- tbl inv_elementos (hidraulicos)
                sql_query = f"""
                       INSERT INTO {schema}.tbl_inv_elementos (id_tipo, id_proyecto, id_inventario, n_linea, id_pieza_conexion, id_tipo_elemento, id_catalogo_elemento,n_orden, existente, id_orientacion, id_material)
                       VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s,%s)
                       """
                # Datos a insertar
                data_values = (
                    item[0],
                    item[1],
                    item[2],
                    item[3],
                    item[4],
                    item[5],
                    item[6],
                    item[7],
                    item[8],
                    item[9],
                    item[10]
                )
                # Ejecutar la consulta
                cursor.execute(sql_query, data_values)

        if len(data_element_register) != 0:
            for item in data_element_register:
                # Consulta SQL con parámetros para evitar SQL Injection- tbl inv_elementos (registros)
                sql_query = f"""
                               INSERT INTO {schema}.tbl_inv_elementos (id_tipo, id_proyecto, id_inventario, n_elementos, id_tipo_elemento, id_catalogo_elemento)
                               VALUES (%s, %s, %s, %s, %s, %s)
                               """
                # Datos a insertar
                data_values = (
                    item[0],
                    item[1],
                    item[2],
                    item[3],
                    item[4],
                    item[5]
                )
                # Ejecutar la consulta
                cursor.execute(sql_query, data_values)

        if len(data_photo) != 0:
            for item in data_photo:
                # Consulta SQL con parámetros para evitar SQL Injection- tbl inv_fotos
                sql_query = f"""
                                       INSERT INTO {schema}.tbl_inv_fotografias (id_proyecto, id_inventario, id_tipo_foto, base64, ruta)
                                       VALUES (%s, %s, %s, %s, %s)
                                       """
                # Datos a insertar
                data_values = (
                    item[0],
                    item[1],
                    item[2],
                    item[3],
                    item[4]
                )
                # Ejecutar la consulta
                cursor.execute(sql_query, data_values)

        if len(data_pdf) != 0:
            for item in data_pdf:
                # Consulta SQL con parámetros para evitar SQL Injection- tbl inv_documentos
                sql_query = f"""
                                       INSERT INTO {schema}.tbl_inv_documentos (id_proyecto, id_inventario, base64, ruta)
                                       VALUES (%s, %s, %s, %s)
                                       """
                # Datos a insertar
                data_values = (
                    item[0],
                    item[1],
                    item[2],
                    item[3]
                )
                # Ejecutar la consulta
                cursor.execute(sql_query, data_values)

        if len(data_element_budget_hidro) != 0:
            for item in data_element_budget_hidro:
                # Consulta SQL con parámetros para evitar SQL Injection- tbl inv_elementos (registros)
                sql_query = f"""
                               INSERT INTO {schema}.tbl_presupuesto (id_partida, cantidad, id_proyecto, id_arqueta, grupo)
                               VALUES (%s, %s, %s, %s, %s)
                               """
                # Datos a insertar
                data_values = (
                    item[0],
                    item[1],
                    item[2],
                    item[3],
                    item[4]
                )
                # Ejecutar la consulta
                cursor.execute(sql_query, data_values)

        if len(data_element_budget_regis) != 0:
            for item in data_element_budget_regis:
                # Consulta SQL con parámetros para evitar SQL Injection- tbl inv_elementos (registros)
                sql_query = f"""
                               INSERT INTO {schema}.tbl_presupuesto (id_partida, cantidad, id_proyecto, id_arqueta, grupo)
                               VALUES (%s, %s, %s, %s, %s)
                               """
                # Datos a insertar
                data_values = (
                    item[0],
                    item[1],
                    item[2],
                    item[3],
                    item[4]
                )
                # Ejecutar la consulta
                cursor.execute(sql_query, data_values)

        # Confirmar la transacción
        conexion.commit()
        print("Registro insertado exitosamente.")
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#MODIDICA UN ITEM DE REGISTRO Y SUS DATOS HIJOS DE LA BBDD
def mod_register_item(user, password,schema,data_inventory,data_pdf,data_photo,data_element_hidro,data_element_register):
    try:
        # Establecer la conexión con el servidor MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            user=user,
            password=password
        )

        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()

        if len(data_inventory)!=0:
                # Consulta SQL con parámetros para evitar SQL Injection - tbl inventario
                sql_query = f"""
                       INSERT INTO {schema}.tbl_inventario (codigo, id_proyecto, id_municipio, id_estado, observaciones, id_certificacion)
                       VALUES (%s, %s, %s, %s, %s, %s)
                       """
                # Datos a insertar
                data_values = (
                    data_inventory[0],
                    data_inventory[1],
                    data_inventory[2],
                    3,
                    data_inventory[3],
                    3
                )
                # Ejecutar la consulta
                cursor.execute(sql_query, data_values)

        if len(data_element_hidro)!=0:
            for item in data_element_hidro:
                # Consulta SQL con parámetros para evitar SQL Injection- tbl inv_elementos (hidraulicos)
                sql_query = f"""
                       INSERT INTO {schema}.tbl_inv_elementos (id_tipo, id_proyecto, id_inventario, n_linea, id_pieza_conexion, id_tipo_elemento, id_catalogo_elemento)
                       VALUES (%s, %s, %s, %s, %s, %s, %s)
                       """
                # Datos a insertar
                data_values = (
                    item[0],
                    item[1],
                    item[2],
                    item[3],
                    item[4],
                    item[5],
                    item[6]
                )
                # Ejecutar la consulta
                cursor.execute(sql_query, data_values)

        if len(data_element_register) != 0:
            for item in data_element_register:
                # Consulta SQL con parámetros para evitar SQL Injection- tbl inv_elementos (registros)
                sql_query = f"""
                               INSERT INTO {schema}.tbl_inv_elementos (id_tipo, id_proyecto, id_inventario, n_elementos, id_tipo_elemento, id_catalogo_elemento)
                               VALUES (%s, %s, %s, %s, %s, %s)
                               """
                # Datos a insertar
                data_values = (
                    item[0],
                    item[1],
                    item[2],
                    item[3],
                    item[4],
                    item[5]
                )
                # Ejecutar la consulta
                cursor.execute(sql_query, data_values)

        if len(data_photo) != 0:
            for item in data_photo:
                # Consulta SQL con parámetros para evitar SQL Injection- tbl inv_fotos
                sql_query = f"""
                                INSERT INTO {schema}.tbl_inv_fotografias (id_proyecto, id_inventario, id_tipo_foto, base64, ruta)
                                VALUES (%s, %s, %s, %s, %s)
                            """
                # Datos a insertar
                data_values = (
                    item[0],
                    item[1],
                    item[2],
                    item[3],
                    item[4]
                )
                # Ejecutar la consulta
                cursor.execute(sql_query, data_values)

        if len(data_pdf) != 0:
            for item in data_pdf:
                # Consulta SQL con parámetros para evitar SQL Injection- tbl inv_documentos
                sql_query = f"""
                            INSERT INTO {schema}.tbl_inv_documentos (id_proyecto, id_inventario, base64, ruta)
                            VALUES (%s, %s, %s, %s)
                            """
                # Datos a insertar
                data_values = (
                    item[0],
                    item[1],
                    item[2],
                    item[3]
                )
                # Ejecutar la consulta
                cursor.execute(sql_query, data_values)
        # Confirmar la transacción
        conexion.commit()
        print("Registro insertado exitosamente.")
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#AÑADE ELEMENTOS DE REGISTRO DEL ITEM SELECCIONADO
def add_register_elements(user, password,schema,data_element_hidro,data_element_register, data_element_budget_hidro, data_element_budget_regis):
    try:
        # Establecer la conexión con el servidor MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            user=user,
            password=password
        )

        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()

        if len(data_element_hidro)!=0:
            for item in data_element_hidro:
                # Consulta SQL con parámetros para evitar SQL Injection- tbl inv_elementos (hidraulicos)
                sql_query = f"""
                       INSERT INTO {schema}.tbl_inv_elementos (id_tipo, id_proyecto, id_inventario, n_linea, id_pieza_conexion, id_tipo_elemento, id_catalogo_elemento,n_orden, existente, id_orientacion, id_material)
                       VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s,%s)
                       """
                # Datos a insertar
                data_values = (
                    item[0],
                    item[1],
                    item[2],
                    item[3],
                    item[4],
                    item[5],
                    item[6],
                    item[7],
                    item[8],
                    item[9],
                    item[10]
                )
                # Ejecutar la consulta
                cursor.execute(sql_query, data_values)

        if len(data_element_register) != 0:
            for item in data_element_register:
                # Consulta SQL con parámetros para evitar SQL Injection- tbl inv_elementos (registros)
                sql_query = f"""
                               INSERT INTO {schema}.tbl_inv_elementos (id_tipo, id_proyecto, id_inventario, n_elementos, id_tipo_elemento, id_catalogo_elemento)
                               VALUES (%s, %s, %s, %s, %s, %s)
                               """
                # Datos a insertar
                data_values = (
                    item[0],
                    item[1],
                    item[2],
                    item[3],
                    item[4],
                    item[5]
                )
                # Ejecutar la consulta
                cursor.execute(sql_query, data_values)

        if len(data_element_budget_hidro) != 0:
            for item in data_element_budget_hidro:
                # Consulta SQL con parámetros para evitar SQL Injection- tbl inv_elementos (registros)
                sql_query = f"""
                                      INSERT INTO {schema}.tbl_presupuesto (id_partida, cantidad, id_proyecto, id_arqueta, grupo)
                                      VALUES (%s, %s, %s, %s, %s)
                                      """
                # Datos a insertar
                data_values = (
                    item[0],
                    item[1],
                    item[2],
                    item[3],
                    item[4]
                )
                # Ejecutar la consulta
                cursor.execute(sql_query, data_values)

        if len(data_element_budget_regis) != 0:
            for item in data_element_budget_regis:
                # Consulta SQL con parámetros para evitar SQL Injection- tbl inv_elementos (registros)
                sql_query = f"""
                                      INSERT INTO {schema}.tbl_presupuesto (id_partida, cantidad, id_proyecto, id_arqueta, grupo)
                                      VALUES (%s, %s, %s, %s, %s)
                                      """
                # Datos a insertar
                data_values = (
                    item[0],
                    item[1],
                    item[2],
                    item[3],
                    item[4]
                )
                # Ejecutar la consulta
                cursor.execute(sql_query, data_values)


        # Confirmar la transacción
        conexion.commit()
        print("Registro insertado exitosamente.")
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#BORRAR ELEMENTOS DEL REGISTRO
def delete_register_item(user, password, schema, id_item):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )

    conexion.start_transaction()
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Consulta SQL con parámetros para evitar SQL Injection
    sql_query = f"""
           DELETE FROM {schema}.tbl_inv_elementos WHERE id_inventario = {id_item}
           """

    # Ejecutar la consulta
    cursor.execute(sql_query)
    # Confirmar la transacción
    conexion.commit()
    print("Registro modificado exitosamente.")
    conexion.close()


#BORRAR ELEMENTOS DEL PRESUPUESTO DEL REGISTRO SELECCIONADO
def delete_register_budget_items(user, password, schema, id_item):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )

    conexion.start_transaction()
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Consulta SQL con parámetros para evitar SQL Injection
    sql_query = f"""
           DELETE FROM {schema}.tbl_presupuesto WHERE id_arqueta = {id_item}
           """

    # Ejecutar la consulta
    cursor.execute(sql_query)
    # Confirmar la transacción
    conexion.commit()
    print("Registro modificado exitosamente.")
    conexion.close()


#MODIFICAR REGISTRO DE LA TABLA INVENTARIO
def mod_register_data(user,password,schema,data,id_item):
    try:
        # Establecer la conexión con el servidor MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            user=user,
            password=password
        )

        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Consulta SQL con parámetros para evitar SQL Injection
        sql_query = f"""
                 UPDATE {schema}.tbl_inventario
                 SET codigo = %s, id_municipio= %s, id_estado= %s, observaciones= %s, id_certificacion= %s
                 WHERE id = %s
                 """
        # Datos a insertar
        data_values = (
            data[0],
            data[1],
            data[2],
            data[3],
            data[4],
            id_item
        )
        # Ejecutar la consulta
        cursor.execute(sql_query, data_values)
        # Confirmar la transacción
        conexion.commit()
        print("Registro insertado exitosamente.")
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#DAR POR FINALIZADO UN  REGISTRO DE LA TABLA INVENTARIO
def close_register_data(user,password,schema,data,id_item):
    try:
        # Establecer la conexión con el servidor MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            user=user,
            password=password
        )

        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Consulta SQL con parámetros para evitar SQL Injection
        sql_query = f"""
                 UPDATE {schema}.tbl_inventario
                 SET codigo = %s, id_municipio= %s, id_estado= %s, observaciones= %s, id_certificacion= %s, fecha_final= NOW()
                 WHERE id = %s
                 """
        # Datos a insertar
        data_values = (
            data[0],
            data[1],
            data[2],
            data[3],
            data[4],
            id_item
        )
        # Ejecutar la consulta
        cursor.execute(sql_query, data_values)
        # Consulta SQL con parámetros para evitar SQL Injection
        sql_query1 = f"""
                 UPDATE {schema}.tbl_pres_certificacion
                 SET certificada = 1, fecha_certificacion= NOW()
                 WHERE id_arqueta = {id_item} and certificada = 0
                 """
        # Ejecutar la consulta
        cursor.execute(sql_query1)
        # Confirmar la transacción
        conexion.commit()
        print("Registro insertado exitosamente.")
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


# ==================== GESTIÓN DE FOTOGRAFÍAS ====================

#AÑADE FOTOS DE REGISTRO
def add_photo_register(user, password,schema,data_photo):
    try:
        # Establecer la conexión con el servidor MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            user=user,
            password=password
        )

        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        if len(data_photo) != 0:
            for item in data_photo:
                # Consulta SQL con parámetros para evitar SQL Injection- tbl inv_fotos
                sql_query = f"""
                            INSERT INTO {schema}.tbl_inv_fotografias (id_proyecto, id_inventario, id_tipo_foto, base64, ruta)
                            VALUES (%s, %s, %s, %s, %s)
                            """
                # Datos a insertar
                data_values = (
                    item[0],
                    item[1],
                    item[2],
                    item[3],
                    item[4]
                )
                # Ejecutar la consulta
                cursor.execute(sql_query, data_values)
        # Confirmar la transacción
        conexion.commit()
        print("Registro insertado exitosamente.")
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#AÑADE FOTO DE EMPLAZAMIENTO DE REGISTRO
def add_photo_site_register(user, password,schema,data_photo):
    try:
        # Establecer la conexión con el servidor MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            user=user,
            password=password
        )

        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()

        if len(data_photo) != 0:
            # Consulta SQL con parámetros para evitar SQL Injection- tbl inv_fotos
            sql_query = f"""
                        INSERT INTO {schema}.tbl_inv_fotografias (id_proyecto, id_inventario, id_tipo_foto, base64, ruta)
                        VALUES (%s, %s, %s, %s, %s)
                        """
            # Datos a insertar
            data_values = (
                data_photo[0],
                data_photo[1],
                data_photo[2],
                data_photo[3],
                data_photo[4]
            )
            # Ejecutar la consulta
            cursor.execute(sql_query, data_values)

        # Confirmar la transacción
        conexion.commit()
        print("Registro insertado exitosamente.")
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#MODIFICACION DE FOTO DE EMPLAZAMIENTO DE REGISTRO
def mod_photo_site_register(user, password,schema,photo,id_type, id_register):
    try:
        # Establecer la conexión con el servidor MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            user=user,
            password=password
        )

        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Consulta SQL con parámetros para evitar SQL Injection- tbl inv_fotos
        sql_query = f"""
                    UPDATE {schema}.tbl_inv_fotografias
                    SET id_tipo_foto= %s
                    WHERE id_inventario = %s and base64= %s
                    """
        # Datos a insertar
        data_values = (
            id_type,
            id_register,
            photo
        )
        # Ejecutar la consulta
        cursor.execute(sql_query, data_values)

        # Confirmar la transacción
        conexion.commit()
        print("Registro insertado exitosamente.")
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


# ==================== GESTIÓN DE PRESUPUESTOS ====================

#MODIFICA LAS CANTIDADES DE LA VENTANA PRESUPUESTO
def mod_amount_budget_item(user, password,schema, amount, id_item):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )

    conexion.start_transaction()
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Consulta SQL con parámetros para evitar SQL Injection
    sql_query = f"""
           UPDATE {schema}.tbl_presupuesto
           SET cantidad = %s
           WHERE id = %s
           """
    # Datos a insertar
    data_values = (
        amount,
        id_item
    )
    # Ejecutar la consulta
    cursor.execute(sql_query, data_values)
    # Confirmar la transacción
    conexion.commit()
    print("Registro modificado exitosamente.")
    conexion.close()


#AÑADE LOS ITEMS AL PRESUPUESTO
def add_budget_item(user, password,schema, data):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )

    conexion.start_transaction()
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Consulta SQL con parámetros para evitar SQL Injection
    sql_query = f"""
           INSERT INTO {schema}.tbl_presupuesto (id_partida, cantidad, id_proyecto, id_arqueta, grupo)
           VALUES (%s, %s, %s, %s, %s)
           """
    # Datos a insertar
    data_values = (
        data[0],
        data[1],
        data[2],
        data[3],
        data[4]
    )
    # Ejecutar la consulta
    cursor.execute(sql_query, data_values)
    # Confirmar la transacción
    conexion.commit()
    print("Registro modificado exitosamente.")
    conexion.close()


#IMPORTA LOS ITEMS DEL PRESUPUESTO A LA TABLA DE CERTIFICACIONES
def import_budget_items(user, password,schema, data):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )

    conexion.start_transaction()
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    for item in data:
        sql_query = f"""
               INSERT INTO {schema}.tbl_pres_certificacion (id_partida, cantidad_certificada, id_proyecto, id_arqueta,certificada,grupo)
               VALUES (%s, %s, %s, %s, %s, %s)
               """
        # Datos a insertar
        data_value = (
            item[1],
            item[2],
            item[3],
            item[4],
            0,
            item[5]
        )
        # Ejecutar la consulta
        cursor.execute(sql_query, data_value)

    # Confirmar la transacción
    conexion.commit()
    print("Registro modificado exitosamente.")
    conexion.close()


#BORRA ITEM DE LA TABLA PRESUPUESTO
def delete_budget_item(user, password,schema, id_item):
    try:
        # Establecer la conexión con el servidor MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            user=user,
            password=password
        )

        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Consulta SQL con parámetros para evitar SQL Injection
        sql_query = f"""
               DELETE FROM {schema}.tbl_presupuesto WHERE id = {id_item}

               """
        # Ejecutar la consulta
        cursor.execute(sql_query)
        # Confirmar la transacción
        conexion.commit()
        print("Registro modificado exitosamente.")
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#MODIFICA LAS CANTIDADES DE LA TABLA DE CERTIFICACIONES
def mod_amount_cost_item(user, password,schema, amount, id_item):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )

    conexion.start_transaction()
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Consulta SQL con parámetros para evitar SQL Injection
    sql_query = f"""
           UPDATE {schema}.tbl_pres_certificacion
           SET cantidad_certificada = %s
           WHERE id = %s
           """
    # Datos a insertar
    data_values = (
        amount,
        id_item
    )
    # Ejecutar la consulta
    cursor.execute(sql_query, data_values)
    # Confirmar la transacción
    conexion.commit()
    print("Registro modificado exitosamente.")
    conexion.close()


#BORRA ITEM DE LA TABLA DE CERTIFICACION
def delete_cost_item(user, password, schema, id_item):
    try:
        # Establecer la conexión con el servidor MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            user=user,
            password=password
        )

        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Consulta SQL con parámetros para evitar SQL Injection
        sql_query = f"""
               DELETE FROM {schema}.tbl_pres_certificacion WHERE id = {id_item}

               """
        # Ejecutar la consulta
        cursor.execute(sql_query)
        # Confirmar la transacción
        conexion.commit()
        print("Registro modificado exitosamente.")
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#CERTIFICA UN ITEM EN LA TABLA DE CERTIFICACIONES
def cert_cost_item(user, password, schema, id_item):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )

    conexion.start_transaction()
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Consulta SQL con parámetros para evitar SQL Injection
    sql_query = f"""
            UPDATE {schema}.tbl_pres_certificacion
            SET certificada = 1 , fecha_certificacion=NOW()
            WHERE id = {id_item}
           """
    # Ejecutar la consulta
    cursor.execute(sql_query)
    # Confirmar la transacción
    conexion.commit()
    print("Registro modificado exitosamente.")
    conexion.close()


#AÑADE UN ITEM A LA TABLA DE CERTIFICACION
def add_cost_item(user, password,schema, data):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )

    conexion.start_transaction()
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Consulta SQL con parámetros para evitar SQL Injection
    sql_query1 = f"""
           INSERT INTO {schema}.tbl_pres_certificacion (id_partida, cantidad_certificada, id_proyecto, id_arqueta,certificada,grupo)
           VALUES (%s, %s, %s, %s, %s,%s)
           """
    # Datos a insertar
    data_values1 = (
        data[0],
        data[1],
        data[2],
        data[3],
        0,
        data[4]
    )
    # Ejecutar la consulta
    cursor.execute(sql_query1, data_values1)
    # Confirmar la transacción
    conexion.commit()
    print("Registro modificado exitosamente.")
    conexion.close()


#MODIFICA UN ITEM DE LA TABAL DE PRESUPUESTO
def mod_item_budget(user, password,schema, data, id_item):
    try:
        # Establecer la conexión con el servidor MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            user=user,
            password=password
        )

        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Consulta SQL con parámetros para evitar SQL Injection
        sql_query = f"""
               UPDATE {schema}.tbl_pres_precios
               SET codigo = %s, id_naturaleza= %s, id_unidades= %s, resumen= %s, descripcion = %s, coste= %s
               WHERE id = %s
               """
        # Datos a insertar
        data_values = (
            data[0],
            data[1],
            data[2],
            data[3],
            data[4],
            data[5],
            id_item
        )
        # Ejecutar la consulta
        cursor.execute(sql_query, data_values)
        # Confirmar la transacción
        conexion.commit()
        print("Registro modificado exitosamente.")
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#AÑADE ITEM DE REGISTRO A LA TABLA CAPITULO
def add_item_chapter(user, password,schema,data):
    try:
        # Establecer la conexión con el servidor MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            user=user,
            password=password
        )

        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Consulta SQL con parámetros para evitar SQL Injection - tbl capitulo
        sql_query = f"""
               INSERT INTO {schema}.tbl_pres_capitulos (codigo_capitulo, id_naturaleza, capitulo)
               VALUES (%s, %s, %s)
               """
        # Datos a insertar
        data_values = (
            data[0],
            data[1],
            data[2]
        )
        # Ejecutar la consulta
        cursor.execute(sql_query, data_values)
        # Confirmar la transacción
        conexion.commit()
        print("Registro insertado exitosamente.")
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#AÑADE ITEM DE REGISTRO A LA TABLA PRECIOS
def add_item_budget(user, password,schema,data):
    try:
        # Establecer la conexión con el servidor MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            user=user,
            password=password
        )

        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Consulta SQL con parámetros para evitar SQL Injection - tbl inventario
        sql_query = f"""
               INSERT INTO {schema}.tbl_pres_precios (codigo, id_naturaleza, id_unidades, resumen, descripcion, coste, id_capitulo)
               VALUES (%s, %s, %s,%s, %s, %s, %s)
               """
        # Datos a insertar
        data_values = (
            data[0],
            data[1],
            data[2],
            data[3],
            data[4],
            data[5],
            data[6]
        )
        # Ejecutar la consulta
        cursor.execute(sql_query, data_values)
        # Confirmar la transacción
        conexion.commit()
        print("Registro insertado exitosamente.")
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#AÑADE GRUPO A LA TABLA GRUPOS DE PRESUPUESTO
def add_group_budget(user, password,schema,data):
    try:
        # Establecer la conexión con el servidor MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            user=user,
            password=password
        )

        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Consulta SQL con parámetros para evitar SQL Injection - tbl inventario
        sql_query = f"""
               INSERT INTO {schema}.tbl_pres_grupo_partidas (codigo, id_naturaleza, id_unidades, resumen, descripcion, id_capitulo)
               VALUES (%s, %s, %s,%s, %s, %s)
               """
        # Datos a insertar
        data_values = (
            data[0],
            data[1],
            data[2],
            data[3],
            data[4],
            data[5]
        )
        # Ejecutar la consulta
        cursor.execute(sql_query, data_values)
        # Confirmar la transacción
        conexion.commit()
        print("Registro insertado exitosamente.")
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#AÑADE ITEM A LA TABLA DE ELEMENTOS DE GRUPOS DE PRESUPUESTOS
def add_item_group_budget(user, password,schema,data):

    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )

    conexion.start_transaction()
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Consulta SQL con parámetros para evitar SQL Injection - tbl inventario
    sql_query = f"""
           INSERT INTO {schema}.tbl_pres_grupo_elementos (id_grupo, id_partida, cantidad)
           VALUES (%s, %s, %s)
           """
    # Datos a insertar
    data_values = (
        data[0],
        data[1],
        data[2]
    )
    # Ejecutar la consulta
    cursor.execute(sql_query, data_values)
    # Confirmar la transacción
    conexion.commit()
    print("Registro insertado exitosamente.")
    conexion.close()


#MODIFICA LA CANTIDAD DE UN ITEM EN LA TABLA DE ELEMENTOS DE GRUPOS DE PRESUPUESTOS
def mod_amount_group_item(user, password,schema, amount, id_item):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )

    conexion.start_transaction()
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Consulta SQL con parámetros para evitar SQL Injection
    sql_query = f"""
           UPDATE {schema}.tbl_pres_grupo_elementos
           SET cantidad = %s
           WHERE id = %s
           """
    # Datos a insertar
    data_values = (
        amount,
        id_item
    )
    # Ejecutar la consulta
    cursor.execute(sql_query, data_values)
    # Confirmar la transacción
    conexion.commit()
    print("Registro modificado exitosamente.")
    conexion.close()


#ELIMINA UN GRUPO DE LA TABLA DE GRUPOS DE PRESUPUESTOS
def delete_group_item(user, password, schema, id_item):
    try:
        # Establecer la conexión con el servidor MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            user=user,
            password=password
        )

        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Consulta SQL con parámetros para evitar SQL Injection
        sql_query = f"""
               DELETE FROM {schema}.tbl_pres_grupo_elementos WHERE id = {id_item}
               """
        # Ejecutar la consulta
        cursor.execute(sql_query)
        # Confirmar la transacción
        conexion.commit()
        print("Registro modificado exitosamente.")
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e
