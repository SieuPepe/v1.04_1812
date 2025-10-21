import mysql.connector
from mysql.connector import Error
import secrets
import string
import os


#COMPRUEBA LOGIN EN BBDD PARA DAR ACCESO A LA APP
def login_db(user, password):
    try:
        # Establecer la conexión con el servidor MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            user=user,
            password=password
        )
        #Comprobar conexion y devuelve la conexion
        print("Conexión exitosa al servidor MySQL.")
        conexion.close()
        return conexion, None

    except mysql.connector.Error as e:
        #Si no es posible conectar, devuelve el error
        print(f"Error al conectar a MySQL: {e}")
        return None, e



#COMPRUEBA SI ERES MANAGER PARA DEJARTE ENTRAR EN EL MODULO DE MANAGER
def manager_db(user, password):

    try:
        # Establecer la conexión con el servidor MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            database='manager',
            user=user,
            password=password
        )

        # Comprobar conexion y devuelve la conexion
        print("Conexión exitosa al servidor MySQL.")
        conexion.close()
        return conexion, None

    except mysql.connector.Error as e:
        # Si no es posible conectar, devuelve el error
        print(f"Error al conectar a MySQL: {e}")
        return None, e


#COMPRUEBA SI ERES MANAGER PARA DEJARTE ENTRAR EN EL MODULO DE USUARIOS
def user_db(user, password):
    try:
        # Establecer la conexión con el servidor MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            user=user,
            password=password
        )
        # Comprobar conexion y devuelve la conexion
        print("Conexión exitosa al servidor MySQL.")
        conexion.close()
        return conexion, None

    except mysql.connector.Error as e:
        # Si no es posible conectar, devuelve el error
        print(f"Error al conectar a MySQL: {e}")
        return None, e

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


#DEVUELVE LOS ESQUEMAS DE LA BBDD A LOS QUE TIENE EL USUARIO ACCESO
def get_schemas_db(user,password):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Ejecutar la consulta para obtener la lista de bases de datos
    cursor.execute("SHOW DATABASES")
    # Obtener el resultado
    records = cursor.fetchall()
    schemas = sum([list(elem) for elem in records], [])
    # Cerrar conexión
    conexion.close()

    return schemas


#DEVUELVE LAS CCAA DE LA BBDD PARA OPCIONES EN APP
def get_ccaa_bd(user,password):
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
    # Ejecutar la consulta para obtener la lista de CCAA
    cursor.execute("SELECT NAMEUNIT FROM manager.list_ccaa")
    # Obtener el resultado
    records = cursor.fetchall()
    ccaa = sum([list(elem) for elem in records], [])
    # Cerrar conexión
    conexion.close()

    return ccaa


#DEVUELVE CODIGO DE LA PROVINCIA
def get_id_ccaa_bd(user,password,select_ccaa):
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
    # Ejecutar la consulta para obtener codigo CCAA
    cursor.execute(f"SELECT id FROM manager.list_ccaa WHERE NAMEUNIT='{select_ccaa}'")
    # Obtener el resultado
    records = cursor.fetchall()
    code_ccaa=sum([list(elem) for elem in records], [])
    # Cerrar conexión
    conexion.close()

    return code_ccaa[0]


#DEVUELVE CODIGO DE LA PROVINCIA
def get_id_province_bd(user,password,select_province):
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
    # Ejecutar la consulta para obtener codigo CCAA
    cursor.execute(f"SELECT id FROM manager.list_provincias WHERE NAMEUNIT='{select_province}'")
    # Obtener el resultado
    records = cursor.fetchall()
    code_ccaa=sum([list(elem) for elem in records], [])
    # Cerrar conexión
    conexion.close()

    return code_ccaa[0]


#DEVUELVE CODIGO DE LA CCAA DE LA BBDD PARA OPCIONES DE PROVINCIA EN APP
def get_code_ccaa_bd(user,password,select_ccaa):
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
    # Ejecutar la consulta para obtener codigo CCAA
    cursor.execute(f"SELECT CODNUT2 FROM manager.list_ccaa WHERE NAMEUNIT='{select_ccaa}'")
    # Obtener el resultado
    records = cursor.fetchall()
    code_ccaa=sum([list(elem) for elem in records], [])
    # Cerrar conexión
    conexion.close()

    return code_ccaa[0]


#DEVUELVE LAS PROVINCIAS FILTRADAS POR CCAA DE LA BBDD PARA OPCIONES EN APP
def get_province_bd(user, password, code_ccaa):
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
    # Ejecutar la consulta para obtener la lista de provincias
    cursor.execute(f"SELECT NAMEUNIT FROM manager.list_provincias WHERE CODNUT2='{code_ccaa}'")
    # Obtener el resultado
    records = cursor.fetchall()
    province = sum([list(elem) for elem in records], [])
    # Cerrar conexión
    conexion.close()

    return province


#DEVUELVE EL ID DE UN ELEMENTO DE UNA TABLA DE LA BBDD
def get_id_item_bd(user, password, table, schema, field, item):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Ejecutar la consulta para obtener el campo requerido
    sql_query = "SELECT id FROM " + schema + "." + table + " WHERE "+field+ " = '"+item+"'"
    cursor.execute(sql_query)
    # Obtener el resultado
    records = cursor.fetchall()
    option_items = sum([list(elem) for elem in records], [])
    id_item = option_items[0]
    # Cerrar conexión
    conexion.close()

    return id_item


#DEVUELVE EL ID DE UN ELEMENTO DE UNA TABLA DE LA BBDD CON DOS CAMPOS DE FILTRADO
def get_id_item_sub_bd(user, password, table, schema, field1, item1, field2, item2):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Ejecutar la consulta para obtener el campo requerido
    sql_query = "SELECT id FROM " + schema + "." + table + " WHERE "+field1+ " = '"+item1+"' and "+field2+ " = '"+item2+"'"
    cursor.execute(sql_query)
    # Obtener el resultado
    records = cursor.fetchall()
    option_items = sum([list(elem) for elem in records], [])
    id_item = option_items[0]
    # Cerrar conexión
    conexion.close()

    return id_item


#DEVUELVE EL VALOR DEL CAMPO DE UN ITEM INDICANDO EL ID Y EL CAMPO QUE SE QUIERE MOSTRAR DE UNA TABLA DE LA BBDD
def get_item_id_bd(user, password, table, schema, field, id):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Ejecutar la consulta para obtener el campo requerido
    sql_query = "SELECT "+field+" FROM " + schema + "." + table + " WHERE id = "+str(id)
    cursor.execute(sql_query)
    # Obtener el resultado
    records = cursor.fetchall()
    option_items = sum([list(elem) for elem in records], [])
    if len(option_items)==0:
        # Cerrar conexión
        conexion.close()

        return "no item"
    else:
        item_id = option_items[0]
        # Cerrar conexión
        conexion.close()

        return item_id


#DEVUELVE TODOS LOS ELEMENTOS DE UN CAMPO DE UNA TABLA DE LA BBDD
def get_option_item_bd(user, password, table, schema, field):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Ejecutar la consulta para obtener el cmapo requerido
    sql_query = "SELECT " + field + " FROM " + schema + "." + table
    cursor.execute(sql_query)
    # Obtener el resultado
    records = cursor.fetchall()
    option_items = sum([list(elem) for elem in records], [])
    option_items.sort()
    # Cerrar conexión
    conexion.close()

    return option_items


#DEVUELVE TODOS LOS ELEMENTOS DE UN CAMPO FILTRANDO POR UN CAMPO_ID DE UNA TABLA DE LA BBDD
def get_option_item_sub_bd(user, password, table, schema, field,id,id_field):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Ejecutar la consulta para obtener el cmapo requerido
    sql_query = "SELECT " + field + " FROM " + schema + "." + table +  " WHERE "+ id_field +" = '" + str(id)+"'"
    cursor.execute(sql_query)
    # Obtener el resultado
    records = cursor.fetchall()
    option_items = sum([list(elem) for elem in records], [])
    option_items.sort()
    # Cerrar conexión
    conexion.close()

    return option_items


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


#DEVUELVE LOS USUARIO QUE HAY EN LA BBDD
def get_user_db(user,password):

    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Consulta SQL con parámetros para evitar SQL Injection
    sql_query = f"""
           SELECT user, host FROM mysql.user
           """
    # Ejecutar la consulta
    cursor.execute(sql_query)
    records = cursor.fetchall()
    # Formatear resultados
    option_items = [list(elem) for elem in records]
    users=[]
    for i in range(len(option_items)):
        if option_items[i][1]=="%" and not ('root' in option_items[i][0] or 'mysql' in option_items[i][0]):
            users.append(option_items[i][0])
    # Cerrar conexión
    conexion.close()

    return users


#CREA USUARIO DE BBDD DANDO NOMBRE Y APELLIDOS DE USUARIO
def create_user_bd(user,password,name_user,password_user):

    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    sql_query = f"CREATE USER '{name_user}'@'%' IDENTIFIED BY '{password_user}';"

    # Ejecutar la consulta
    cursor.execute(sql_query)
    conexion.commit()


#CREAR CONTRASEÑA PARA USUARIO BD
def create_pass(lenght=8):
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for i in range(lenght))
    return password


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


#CREA EL ESQUEMA DEL PROYECTO
def create_schemas_db(user,password,db_name):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )
    try:
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Ejecutar la consulta para crear esquema
        cursor.execute(f"CREATE SCHEMA {db_name}")
        cursor.close()
        # Cerrar conexión
        conexion.close()
        return "ok"
    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#COPIAR TABLAS VACIAS DEL PROYECTO TIPO A ESQUEMA PROYECTO
def create_tables_schema_db(user,password, new , example):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )

    try:
        conexion.start_transaction()
        for i in range(len(new)):
            new_table=new[i]
            example_table=example[i]
            # Crear un cursor para ejecutar la consulta
            cursor = conexion.cursor()
            # Ejecutar la consulta para crear esquema
            cursor.execute(f"CREATE TABLE {new_table} LIKE {example_table}")
            cursor.close()
            # Cerrar conexión
        conexion.commit()
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#DEVUELVE LAS TABLAS DE UN ESQUEMA DE LA BBDD A LOS QUE TIENE EL USUARIO ACCESO
def get_table_schemas_db(user,password,schema):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password,
        database=schema
    )

    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Ejecutar la consulta para obtener la lista de bases de datos
    cursor.execute("SHOW TABLES")
    # Obtener el resultado
    records = cursor.fetchall()
    tables_schema = sum([list(elem) for elem in records], [])
    # Cerrar conexión
    conexion.close()

    return tables_schema


#COPIAR CONTENIDO DE TABLAS DEL PROYECTO TIPO A ESQUEMA PROYECTO
def copy_tables_schema_db(user,password, code_project, table):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )

    try:
        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Ejecutar la consulta para copiar datos
        cursor.execute(f"INSERT INTO {code_project}.{table} SELECT * FROM proyecto_tipo.{table}")
        conexion.commit()
        cursor.close()
        # Cerrar conexión
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#CREAR TABLA DE MUNICIPIOS PARA PROYECTO
def create_locality_schema_db(user,password, code_project, cod_province):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )

    try:
        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Ejecutar la consulta para copiar datos
        cursor.execute(f"INSERT INTO {code_project}.tbl_municipios SELECT * FROM manager.list_municipios WHERE CODNUT3 = '{cod_province}'")
        conexion.commit()
        cursor.close()
        # Cerrar conexión
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#CREA VISTA TBL DE PROYECTOS PARA QUE PUEDAS ACCEDER AL ID DESDE EL ESQUEMA SIN SER ADMINISTRADOR
def create_view_projects(user,password, code_project):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password,
        database=code_project
    )

    try:
        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Ejecutar la consulta para crear vista de proyecto
        cursor.execute(f"CREATE VIEW tbl_proyectos AS SELECT * FROM manager.tbl_proyectos")
        conexion.commit()
        cursor.close()
        # Cerrar conexión
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#CREA VISTA DE LOS CATÁLOGOS PARA OPTIMIZAR VISUALIZACIÓN LAS TABLAS DE LA APLICACIÓN
def create_view_catalog(user,password, code_project):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password,
        database=code_project
    )

    try:
        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Ejecutar la consulta para crear vista del catálogo de hidráulica
        cursor.execute(f""" CREATE VIEW vw_catalogo_hidraulica AS
                            SELECT 
                                h.id, 
                                f.familia,
                                t.tipo_elemento,
                                m.marca,
                                c.caracteristica,
                                h.modelo,
                                h.referencia,
                                dni.dni,
                                dnf.dnf,
                                pn.pn,
                                a.angulo,
                                h.longitud,
                                h.long_extremos, 
                                h.altura_eje, 
                                h.altura_total, 
                                h.peso, 
                                h.bloque_ref, 
                                h.descripcion,
                                h.cod_partida
                            FROM tbl_catalogo_hidraulica h
                            LEFT JOIN tbl_cata_hidra_familia f ON h.id_familia = f.id
                            LEFT JOIN tbl_cata_hidra_tipo t ON h.id_tipo_hidraulica = t.id
                            LEFT JOIN tbl_cata_hidra_marcas m ON h.id_marca = m.id
                            LEFT JOIN tbl_cata_hidra_caracteristica c ON h.id_caracteristica = c.id
                            LEFT JOIN tbl_cata_hidra_dni dni ON h.id_dni = dni.id
                            LEFT JOIN tbl_cata_hidra_dnf dnf ON h.id_dnf = dnf.id
                            LEFT JOIN tbl_cata_hidra_pn pn ON h.id_pn = pn.id
                            LEFT JOIN tbl_cata_hidra_angulo a ON h.id_angulo = a.id;
                        """)
        conexion.commit()
        cursor.close()
        cursor = conexion.cursor()
        # Ejecutar la consulta para crear vista del catálogo de registros
        cursor.execute(f""" CREATE VIEW vw_catalogo_registros AS
                            SELECT 
                                h.id, 
                                f.tipo,
                                t.proveedor,
                                h.modelo,
                                h.referencia, 
                                h.dimensionA, 
                                h.dimensionB, 
                                h.dimensionC, 
                                h.descripcion,
                                h.cod_partida
                            FROM tbl_catalogo_registros h
                            LEFT JOIN tbl_cata_regis_tipo f ON h.id_tipo_registro = f.id
                            LEFT JOIN tbl_cata_regis_proveedor t ON h.id_proveedor = t.id
                              """)
        conexion.commit()
        cursor.close()
        # Cerrar conexión
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#CREA VISTA DEL PRESUPUESTO Y CERTIFICACION DEL PROYECTO
def create_view_economic(user,password, code_project):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password,
        database=code_project
    )

    try:
        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Ejecutar la consulta para crear vista del catálogo de hidráulica
        cursor.execute(f""" CREATE VIEW vw_presupuesto AS
                            SELECT
                                a.id,
                                c.codigo as cod_proyecto,
                                b.codigo as arqueta,
                                COALESCE(gp.codigo, d.codigo) as cod_partida,
                                g.tipo AS naturaleza,
                                h.unidad AS unidad,
                                COALESCE(gp.resumen,d.resumen) as resumen,
                                COALESCE(gp.descripcion,d.descripcion) as descripcion,
                                COALESCE(gp.coste,d.coste) as precio_unitario,
                                COALESCE((gpe.cantidad * a.cantidad),a.cantidad) AS cantidad,
                                (COALESCE((gpe.cantidad * a.cantidad),a.cantidad) * COALESCE(gp.coste, d.coste)) AS coste_total,
                                f.codigo_capitulo as cod_capitulo,
                                f.capitulo
                            FROM 
                                tbl_presupuesto a
                            LEFT JOIN 
                                tbl_proyectos c ON a.id_proyecto = c.id
                            LEFT JOIN 
                                tbl_inventario b ON a.id_arqueta = b.id
                            LEFT JOIN 
                                tbl_pres_grupo_partidas e ON a.id_partida = e.id AND a.grupo = 1
                            LEFT JOIN 
                                tbl_pres_grupo_elementos gpe ON e.id = gpe.id_grupo
                            LEFT JOIN 
                                tbl_pres_precios gp ON gpe.id_partida = gp.id
                            LEFT JOIN 
                                tbl_pres_precios d ON a.id_partida = d.id AND a.grupo = 0
                            LEFT JOIN 
                                tbl_pres_capitulos f ON COALESCE(gp.id_capitulo, d.id_capitulo) = f.id
                            LEFT JOIN 
                                tbl_pres_unidades h ON COALESCE(gp.id_unidades, d.id_unidades) = h.id
                            LEFT JOIN 
                                tbl_pres_naturaleza g ON COALESCE(gp.id_naturaleza, d.id_naturaleza) = g.id
                        """)
        conexion.commit()
        cursor.close()
        cursor = conexion.cursor()
        # Ejecutar la consulta para crear vista del catálogo de registros
        cursor.execute(f""" CREATE VIEW vw_certificaciones AS
                            SELECT
                                a.id,
                                c.codigo as cod_proyecto,
                                b.codigo as arqueta,
                                COALESCE(gp.codigo, d.codigo) as cod_partida,
                                g.tipo AS naturaleza,
                                h.unidad AS unidad,
                                COALESCE(gp.resumen,d.resumen) as resumen,
                                COALESCE(gp.descripcion,d.descripcion) as descripcion,
                                COALESCE(gp.coste,d.coste) as precio_unitario,
                                COALESCE((gpe.cantidad * a.cantidad_certificada),a.cantidad_certificada) AS cantidad_certificada,
                                (COALESCE((gpe.cantidad * a.cantidad_certificada),a.cantidad_certificada) * COALESCE(gp.coste, d.coste)) AS coste_total,
                                f.codigo_capitulo as cod_capitulo,
                                f.capitulo,
                                a.fecha_certificacion,
                                a.certificada
                            FROM 
                                tbl_pres_certificacion a
                            LEFT JOIN 
                                tbl_proyectos c ON a.id_proyecto = c.id
                            LEFT JOIN 
                                tbl_inventario b ON a.id_arqueta = b.id
                            LEFT JOIN 
                                tbl_pres_grupo_partidas e ON a.id_partida = e.id AND a.grupo = 1
                            LEFT JOIN 
                                tbl_pres_grupo_elementos gpe ON e.id = gpe.id_grupo
                            LEFT JOIN 
                                tbl_pres_precios gp ON gpe.id_partida = gp.id
                            LEFT JOIN 
                                tbl_pres_precios d ON a.id_partida = d.id AND a.grupo = 0
                            LEFT JOIN 
                                tbl_pres_capitulos f ON COALESCE(gp.id_capitulo, d.id_capitulo) = f.id
                            LEFT JOIN 
                                tbl_pres_unidades h ON COALESCE(gp.id_unidades, d.id_unidades) = h.id
                            LEFT JOIN 
                                tbl_pres_naturaleza g ON COALESCE(gp.id_naturaleza, d.id_naturaleza) = g.id
                        """)
        conexion.commit()
        cursor.close()
        # Cerrar conexión
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#CREA VISTA DE LOS REGISTROS DEL INVENTARIO  PARA DYNAMO
def create_view_inventory(user,password, code_project):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password,
        database=code_project
    )

    try:
        #bloquea la modificacion del elemento en la bbdd
        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Ejecutar la consulta para crear vista del catálogo de hidráulica
        cursor.execute(f""" CREATE VIEW vw_inv_elementos AS
                            SELECT 
                                h.id, 
                                a.codigo,
                                h.n_linea,
                                h.id_pieza_conexion,
                                b.tipo_elemento,
                                c.modelo,
                                h.n_orden,
                                h.existente,
                                d.orientacion,
                                c.bloque_ref,
                                c.angulo,
                                c.dni,
                                e.material
                            FROM tbl_inv_elementos h
                            LEFT JOIN tbl_inventario a ON h.id_inventario = a.id
                            LEFT JOIN tbl_cata_hidra_tipo b ON h.id_tipo_elemento = b.id
                            LEFT JOIN vw_catalogo_hidraulica c ON h.id_catalogo_elemento = c.id
                            LEFT JOIN tbl_inv_orientacion d ON h.id_orientacion = d.id
                            LEFT JOIN tbl_inv_material e ON h.id_material = e.id
                            WHERE h.id_tipo = 2;
                        """)
        conexion.commit()
        cursor.close()
        # Cerrar conexión
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#CREA CLAVES FORANEAS PARA RELACIONAR TABLAS DEL PROYECTO
def create_fk(user,password, code_project):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password,
        database=code_project
    )

    try:
        conexion.start_transaction()
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        # Ejecutar la consulta asiganr claves foraneas a tablas
        cursor.execute(f""" ALTER TABLE `tbl_presupuesto` 
                            ADD CONSTRAINT `fk_pres_precios`
                              FOREIGN KEY (`id_partida`)
                              REFERENCES `tbl_pres_precios` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE,
                            ADD CONSTRAINT `fk_inventario`
                              FOREIGN KEY (`id_arqueta`)
                              REFERENCES `tbl_inventario` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE;
                            
                            ALTER TABLE `tbl_pres_precios` 
                            ADD CONSTRAINT `fk_naturaleza`
                              FOREIGN KEY (`id_naturaleza`)
                              REFERENCES `tbl_pres_naturaleza` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE,
                            ADD CONSTRAINT `fk_unidades`
                              FOREIGN KEY (`id_unidades`)
                              REFERENCES `tbl_pres_unidades` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE,
                            ADD CONSTRAINT `fk_capitulo`
                              FOREIGN KEY (`id_capitulo`)
                              REFERENCES `tbl_pres_capitulos` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE;
                            
                            ALTER TABLE `tbl_pres_grupo_partidas` 
                            ADD CONSTRAINT `fk_naturaleza_grupo`
                              FOREIGN KEY (`id_naturaleza`)
                              REFERENCES `tbl_pres_naturaleza` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE,
                            ADD CONSTRAINT `fk_unidades_grupo`
                              FOREIGN KEY (`id_unidades`)
                              REFERENCES `tbl_pres_unidades` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE,
                            ADD CONSTRAINT `fk_capitulo_grupo`
                              FOREIGN KEY (`id_capitulo`)
                              REFERENCES `tbl_pres_capitulos` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE;
                            
                            ALTER TABLE `tbl_pres_grupo_elementos` 
                            ADD CONSTRAINT `fk_grupo`
                              FOREIGN KEY (`id_grupo`)
                              REFERENCES `tbl_pres_grupo_partidas` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE,
                            ADD CONSTRAINT `fk_partida_grupo`
                              FOREIGN KEY (`id_partida`)
                              REFERENCES `tbl_pres_precios` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE;
                            
                            ALTER TABLE `tbl_pres_certificacion` 
                            ADD CONSTRAINT `fk_partida_certificacion`
                              FOREIGN KEY (`id_partida`)
                              REFERENCES `tbl_pres_precios` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE,
                            ADD CONSTRAINT `fk_inventario_certificacion`
                              FOREIGN KEY (`id_arqueta`)
                              REFERENCES `tbl_inventario` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE;
                            
                            ALTER TABLE `tbl_pres_capitulos` 
                            ADD CONSTRAINT `fk_naturaleza_capitulos`
                              FOREIGN KEY (`id_naturaleza`)
                              REFERENCES `tbl_pres_naturaleza` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE;
                            
                            ALTER TABLE `tbl_inventario` 
                            ADD CONSTRAINT `fk_municipio_inventario`
                              FOREIGN KEY (`id_municipio`)
                              REFERENCES `tbl_municipios` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE,
                            ADD CONSTRAINT `fk_estado_inventario`
                              FOREIGN KEY (`id_estado`)
                              REFERENCES `tbl_inv_estado` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE,
                            ADD CONSTRAINT `fk_certificacion_inventario`
                              FOREIGN KEY (`id_certificacion`)
                              REFERENCES `tbl_inv_certificado` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE;
                            
                            ALTER TABLE `tbl_inv_fotografias` 
                            ADD CONSTRAINT `fk_inventario_foto`
                              FOREIGN KEY (`id_inventario`)
                              REFERENCES `tbl_inventario` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE,
                            ADD CONSTRAINT `fk_tipo_foto`
                              FOREIGN KEY (`id_tipo_foto`)
                              REFERENCES `tbl_inv_foto_tipo` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE;
                            
                            ALTER TABLE `tbl_catalogo_registros` 
                            ADD CONSTRAINT `fk_tipo_registro`
                              FOREIGN KEY (`id_tipo_registro`)
                              REFERENCES `tbl_cata_regis_tipo` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE,
                            ADD CONSTRAINT `fk_proveedor_registro`
                              FOREIGN KEY (`id_proveedor`)
                              REFERENCES `tbl_cata_regis_proveedor` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE;
                            
                            ALTER TABLE `tbl_catalogo_hidraulica` 
                            ADD CONSTRAINT `fk_familia_hidro`
                              FOREIGN KEY (`id_familia`)
                              REFERENCES `tbl_cata_hidra_familia` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE,
                            ADD CONSTRAINT `fk_tipo_hidro`
                              FOREIGN KEY (`id_tipo_hidraulica`)
                              REFERENCES `tbl_cata_hidra_tipo` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE,
                            ADD CONSTRAINT `fk_marca_hidro`
                              FOREIGN KEY (`id_marca`)
                              REFERENCES `tbl_cata_hidra_marcas` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE,
                            ADD CONSTRAINT `fk_caracteristica_hidro`
                              FOREIGN KEY (`id_caracteristica`)
                              REFERENCES `tbl_cata_hidra_caracteristica` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE,
                            ADD CONSTRAINT `fk_dni_hidro`
                              FOREIGN KEY (`id_dni`)
                              REFERENCES `tbl_cata_hidra_dni` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE,
                            ADD CONSTRAINT `fk_dnf_hidro`
                              FOREIGN KEY (`id_dnf`)
                              REFERENCES `tbl_cata_hidra_dnf` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE,
                            ADD CONSTRAINT `fk_pn_hidro`
                              FOREIGN KEY (`id_pn`)
                              REFERENCES `tbl_cata_hidra_pn` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE,
                            ADD CONSTRAINT `fk_angulo_hidro`
                              FOREIGN KEY (`id_angulo`)
                              REFERENCES `tbl_cata_hidra_angulo` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE;
                            
                            ALTER TABLE `tbl_cata_hidra_tipo` 
                            ADD CONSTRAINT `fk_familia_tipo`
                              FOREIGN KEY (`id_familia`)
                              REFERENCES `tbl_cata_hidra_familia` (`id`)
                              ON DELETE NO ACTION
                              ON UPDATE CASCADE;
                        """)
        conexion.commit()
        cursor.close()
        # Cerrar conexión
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#ACTUALIZA LAS REFERENCIAS DEL PROYECTO SEGUN SU DIRECTORIO
def update_reference(user,password,code_project,path_reference):
    reference_files = []

    # Recorrer todos los niveles de subdirectorios
    for subdir, dirs, files in os.walk(path_reference):
        for file in files:
            if file.endswith('.dwg'):
                subpath = os.path.relpath(subdir, path_reference)  # Ruta relativa desde la carpeta raíz
                name_file = os.path.splitext(file)[0]
                path_file=os.path.join(subpath, name_file)
                reference_files.append((subpath , name_file, path_file))

    try:
        # Conectar a la base de datos MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            user=user,
            password=password,
            database=code_project
        )
        cursor =  conexion.cursor()

        # borrar los registros existentes en la base de datos
        cursor.execute("DELETE FROM tbl_cata_hidra_referencias_cad")
        conexion.commit()

        conexion.start_transaction()
        # Obtener los registros existentes en la base de datos
        cursor.execute("ALTER TABLE tbl_cata_hidra_referencias_cad AUTO_INCREMENT = 1;")
        conexion.commit()

        conexion.start_transaction()
        # Si hay nuevos archivos, insertarlos en la base de datos
        if reference_files:
            cursor.executemany("""
            INSERT INTO tbl_cata_hidra_referencias_cad (directorio, referencia, ruta)
            VALUES (%s, %s, %s)
            """, list(reference_files))

        conexion.commit()
        cursor.close()
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#AÑADIR PRIVILEGIOS A USUARIO PARA UN ESQUEMA DETERMINADO
def add_privileges(user,password,code_project, user_bd, type_privilege):
    try:
        # Conectar a la base de datos MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            port=3307,
            user=user,
            password=password,
            database=code_project
        )
        cursor =  conexion.cursor()

        privileges_query=""
        # Asignar permisos según el nivel seleccionado
        if type_privilege == "Solo lectura":
            privileges_query = f"GRANT SELECT ON {code_project}.* TO '{user_bd}'@'%';"
        elif type_privilege == "Escritura y lectura":
            privileges_query = f"GRANT SELECT, INSERT, UPDATE, DELETE,ALTER ON {code_project}.* TO '{user_bd}'@'%';"
        elif type_privilege == "Administrador":
            privileges_query = f"GRANT ALL PRIVILEGES ON *.* TO '{user_bd}'@'%' WITH GRANT OPTION;"
            cursor.execute(privileges_query)
            privileges_query = f"GRANT ALL PRIVILEGES ON {code_project}.* TO '{user_bd}'@'%';"

        cursor.execute(privileges_query)

        query = f"FLUSH PRIVILEGES;"
        cursor.execute(query)

        # Confirmar los cambios
        conexion.commit()
        cursor.close()
        conexion.close()
        return "ok"

    except mysql.connector.Error as e:
        return e


# VERIFICA SI EXISTE EL USUARIO
def user_verfication(cursor, user, host='%'):
    query = f"SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = '{user}' AND host = '{host}');"
    cursor.execute(query)
    return cursor.fetchone()[0]


# ELIMINA LOS PERMISOS PARA UN ESQUEMA Y UN USUARIO
def revoke_privileges(user,password, user_db, schema):
    # Conectar a la base de datos MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )
    cursor = conexion.cursor()
    query = f"REVOKE ALL PRIVILEGES ON {schema}.* FROM '{user_db}'@'%';"
    cursor.execute(query)

    query = f"FLUSH PRIVILEGES;"
    cursor.execute(query)

    cursor.close()
    conexion.close()


# ACTUALIZA CONTRASEÑA DE UN USUARIO
def change_pass_user(user,password, user_db, newpassword):
    # Conectar a la base de datos MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )
    cursor = conexion.cursor()
    query = f"ALTER USER'{user_db}'@'%' IDENTIFIED BY '{newpassword}';"
    cursor.execute(query)

    cursor.close()
    conexion.close()


#DEVUELVE TODOS LOS REGISTROS FILTRADOS DE UNA TABLA
def get_all_bd(user, password, table, schema):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )
    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Ejecutar la consulta para obtener el campo requerido
    sql_query = "SELECT * FROM " + schema + "." + table
    cursor.execute(sql_query)
    # Obtener el resultado
    records = cursor.fetchall()
    option_items = sum([list(elem) for elem in records], [])
    # Cerrar conexión
    conexion.close()

    return records


#DEVUELVE FILTRADO LOS REGISTROS DE UNA TABLA
def get_filter_data_bd(user, password, table, schema, field,item):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )

    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Ejecutar la consulta para obtener el campo requerido
    sql_query = "SELECT * FROM " + schema + "." + table + " WHERE " + field + " = '" + item +"'"
    cursor.execute(sql_query)
    # Obtener el resultado
    records = cursor.fetchall()
    # Cerrar conexión
    conexion.close()

    return records


#DEVUELVE FILTRADO LOS REGISTROS DE UNA TABLA
def get_multifilter_data_bd(user, password, table, schema, field1,item1,field2,item2):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )

    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Ejecutar la consulta para obtener el campo requerido
    sql_query = "SELECT * FROM " + schema + "." + table + " WHERE " + field1 + " = '" + item1 +"' AND "+ field2 + " = '" + item2 +"'"
    cursor.execute(sql_query)
    # Obtener el resultado
    records = cursor.fetchall()
    # Cerrar conexión
    conexion.close()

    return records


#DEVUELVE CAMPOS DE UNA TABLA
def get_field_bd(user, password, table, schema):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )

    # Crear un cursor para ejecutar la consulta
    cursor = conexion.cursor()
    # Ejecutar la consulta para obtener el campo requerido
    sql_query = f"SHOW COLUMNS FROM {schema}.{table}"
    cursor.execute(sql_query)
    # Obtener el resultado
    records = cursor.fetchall()
    fields = sum([list(elem[:1]) for elem in records], [])
    # Cerrar conexión
    conexion.close()

    return fields


#AÑADE ITEM EN UN CAMPO DE UNA TABLA
def add_item_aux(user,password,table,schema,field,item):
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
        sql_query = f"INSERT INTO {schema}.{table} ({field}) VALUES ('{item}')"
        # Ejecutar la consulta
        cursor.execute(sql_query)
        # Confirmar la transacción
        conexion.commit()
        print("Registro insertado exitosamente.")
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#AÑADE ITEM CON SUBTIPO EN UN CAMPO DE UNA TABLA
def add_item_type_aux(user,password,table,schema,field1, item1, field2, item2):
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
        sql_query = f"INSERT INTO {schema}.{table} ({field1}, {field2}) VALUES ('{item1}','{item2}')"
        # Ejecutar la consulta
        cursor.execute(sql_query)
        # Confirmar la transacción
        conexion.commit()
        print("Registro insertado exitosamente.")
        conexion.close()
        return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


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


#MODIFICA ITEM EN UN CAMPO DE UNA TABLA
def mod_item_aux(user,password,table,schema,field,item,id_item):
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
        sql_query = f"UPDATE {schema}.{table} SET {field} = '{item}' WHERE id = {id_item}"
        # Ejecutar la consulta
        cursor.execute(sql_query)
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


#SUMATORIO TOTAL POR PROYECTO
def sum_field_bd(user, password, fieldSum, fieldGroup, schema, table):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )


    cursor = conexion.cursor()
    # Consulta SQL con parámetros para evitar SQL Injection
    sql_query = f"SELECT SUM({fieldSum}) as total FROM {schema}.{table} GROUP BY {fieldGroup}"
    # Ejecutar la consulta
    cursor.execute(sql_query)
    resultados = cursor.fetchall()
    conexion.close()
    return resultados

#SUMATORIO TOTAL POR ARQEUTA DEL PROYECTO
def sum_field_filter_bd(user, password, field, fieldGroup, schema, table, fieldFilter, itemFilter):
    # Establecer la conexión con el servidor MySQL
    conexion = mysql.connector.connect(
        host='localhost',
        port=3307,
        user=user,
        password=password
    )

    cursor = conexion.cursor()
    # Consulta SQL con parámetros para evitar SQL Injection
    sql_query = f"SELECT SUM({field}) as total  FROM {schema}.{table}  WHERE {fieldFilter} = '{itemFilter}' GROUP BY {fieldGroup}"
    # Ejecutar la consulta
    cursor.execute(sql_query)
    resultados = cursor.fetchall()
    conexion.close()

    return resultados

# -------------------- Dimensiones de certificación (OT/RED/TIPO/CÓDIGO) --------------------

def _guess_text_column(user: str, password: str, schema: str, table: str, port: int = 3307):
    """
    Intenta detectar automáticamente la columna 'de texto' para mostrar en menús.
    Estrategia:
      1) Preferir nombres que contengan alguna keyword según tabla: 
         - dim_ot:         ['ot','nombre','desc','texto','codigo','cod']
         - dim_red:        ['red','nombre','desc','texto','codigo','cod']
         - dim_tipo_trabajo: ['tipo','nombre','desc','texto','codigo','cod']
      2) Si no hay match por nombre, elegir la primera columna tipo VARCHAR/TEXT distinta de 'id'.
    Devuelve nombre de columna o None si no encuentra.
    """
    import mysql.connector as mysql
    keywords_map = {
        'dim_ot': ['ot','nombre','desc','texto','codigo','cod'],
        'dim_red': ['red','nombre','desc','texto','codigo','cod'],
        'dim_tipo_trabajo': ['tipo','nombre','desc','texto','codigo','cod'],
        'dim_codigo_trabajo': ['cod_trabajo','codigo','cod','nombre','desc','texto'],
    }
    try:
        cn = mysql.connect(host='127.0.0.1', port=port, user=user, password=password, database=schema)
        cur = cn.cursor()
        cur.execute(
            "SELECT COLUMN_NAME, DATA_TYPE FROM information_schema.COLUMNS "
            "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s ORDER BY ORDINAL_POSITION",
            (schema, table)
        )
        cols = cur.fetchall()  # [(col, type), ...]
        cur.close(); cn.close()
    except Exception:
        return None

    # 1) por keywords
    keys = keywords_map.get(table, ['nombre','desc','texto','codigo','cod'])
    names = [c[0].lower() for c in cols]
    for k in keys:
        for col, dtype in cols:
            if col.lower() == 'id': 
                continue
            if k in col.lower():  # match por substring
                return col

    # 2) primera VARCHAR/TEXT distinta de id
    for col, dtype in cols:
        if col.lower() == 'id': 
            continue
        if dtype and dtype.lower() in ('varchar','text','char','tinytext','mediumtext','longtext'):
            return col

    # 3) fallback: primera que no sea id
    for col, dtype in cols:
        if col.lower() != 'id':
            return col

    return None


def _fetch_dim_list_guess(user: str, password: str, schema: str, table: str, port: int = 3307):
    """
    Devuelve lista de 'id - texto' detectando automáticamente la columna de texto.
    """
    import mysql.connector as mysql
    text_col = _guess_text_column(user, password, schema, table, port=port)
    if not text_col:
        return []
    rows = []
    try:
        cn = mysql.connect(host='127.0.0.1', port=port, user=user, password=password, database=schema)
        cur = cn.cursor()
        cur.execute(f"SELECT id, {text_col} FROM {schema}.{table} ORDER BY {text_col}")
        for rid, txt in cur.fetchall():
            rows.append(f"{rid} - {txt}")
        cur.close(); cn.close()
    except Exception:
        pass
    return rows


def get_dim_all(user: str, password: str, schema: str):
    """
    Devuelve dict con las 4 listas de dimensiones para la UI,
    detectando automáticamente la columna visible:
      - dim_ot
      - dim_red
      - dim_tipo_trabajo
      - dim_codigo_trabajo
    """
    return {
        'OT': _fetch_dim_list_guess(user, password, schema, 'dim_ot'),
        'RED': _fetch_dim_list_guess(user, password, schema, 'dim_red'),
        'TIPO_TRABAJO': _fetch_dim_list_guess(user, password, schema, 'dim_tipo_trabajo'),
        'COD_TRABAJO': _fetch_dim_list_guess(user, password, schema, 'dim_codigo_trabajo'),
    }

def add_parte_with_code(user, password, schema, ot_id, red_id, tipo_trabajo_id, cod_trabajo_id, descripcion):
    """
    Inserta un parte y genera el código automático (PT-00001).
    Devuelve (id, codigo).
    """
    import mysql.connector
    cn = mysql.connector.connect(
        host='127.0.0.1', port=3307, user=user, password=password, database=schema
    )
    try:
        cur = cn.cursor()
        cur.execute(
            "INSERT INTO tbl_partes (ot_id, red_id, tipo_trabajo_id, cod_trabajo_id, descripcion) "
            "VALUES (%s,%s,%s,%s,%s)",
            (ot_id, red_id, tipo_trabajo_id, cod_trabajo_id, descripcion)
        )
        new_id = cur.lastrowid
        codigo = f"PT-{new_id:05d}"
        cur.execute("UPDATE tbl_partes SET codigo=%s WHERE id=%s", (codigo, new_id))
        cn.commit()
        return new_id, codigo
    finally:
        cn.close()

# ---------- PARTES: lectura listado ----------
def list_partes(user: str, password: str, schema: str, limit: int = 200):
    """
    Devuelve una lista de dicts con los partes más recientes.
    Campos: id, codigo, ot, red, tipo, cod_trabajo, descripcion, created_at
    """
    import mysql.connector as m
    cn = m.connect(host='127.0.0.1', port=3307, user=user, password=password, database=schema)
    cur = cn.cursor()
    cur.execute("""
        SELECT  p.id,
                p.codigo,
                COALESCE(ot.ot_codigo, '')         AS ot,
                COALESCE(rd.red_codigo, '')        AS red,
                COALESCE(tt.tipo_codigo, '')       AS tipo,
                COALESCE(ct.cod_trabajo,'')        AS cod_trabajo,
                p.descripcion,
                p.creado_en
        FROM tbl_partes p
        LEFT JOIN dim_ot             ot ON ot.id = p.ot_id
        LEFT JOIN dim_red            rd ON rd.id = p.red_id
        LEFT JOIN dim_tipo_trabajo   tt ON tt.id = p.tipo_trabajo_id
        LEFT JOIN dim_codigo_trabajo ct ON ct.id = p.cod_trabajo_id
        ORDER BY p.id DESC
        LIMIT %s
    """, (limit,))
    rows = cur.fetchall()
    cur.close(); cn.close()

    cols = ["id","codigo","ot","red","tipo","cod_trabajo","descripcion","created_at"]
    return [dict(zip(cols, r)) for r in rows]

def get_parts_list(user, password, schema, limit=100):
    import mysql.connector
    cn = mysql.connector.connect(
        host='127.0.0.1',
        port=3307,
        user=user,
        password=password,
        database=schema
    )
    cur = cn.cursor()
    cur.execute("""
        SELECT
            p.id,
            p.codigo,
            COALESCE(ot.ot_codigo, '')         AS ot,
            COALESCE(rd.red_codigo, '')        AS red,
            COALESCE(tt.tipo_codigo, '')       AS tipo,
            COALESCE(ct.cod_trabajo, '')       AS cod_trabajo,
            p.descripcion,
            p.creado_en
        FROM tbl_partes p
        LEFT JOIN dim_ot             ot ON ot.id = p.ot_id
        LEFT JOIN dim_red            rd ON rd.id = p.red_id
        LEFT JOIN dim_tipo_trabajo   tt ON tt.id = p.tipo_trabajo_id
        LEFT JOIN dim_codigo_trabajo ct ON ct.id = p.cod_trabajo_id
        ORDER BY p.id DESC
        LIMIT %s
    """, (limit,))
    rows = cur.fetchall()
    cur.close()
    cn.close()
    return rows

def delete_parte(user: str, password: str, schema: str, parte_id: int):
    """
    Elimina un parte por su ID
    """
    import mysql.connector as m
    try:
        cn = m.connect(host='127.0.0.1', port=3307, user=user, password=password, database=schema)
        cur = cn.cursor()
        cur.execute("DELETE FROM tbl_partes WHERE id = %s", (parte_id,))
        cn.commit()
        cur.close()
        cn.close()
        return "ok"
    except Exception as e:
        return str(e)

# ==================== GESTIÓN DE PARTES ====================

def get_partes_resumen(user: str, password: str, schema: str):
    """
    Devuelve lista de partes con totales de presupuesto y certificación.
    Usa la vista vw_partes_resumen.
    """
    import mysql.connector as m
    cn = m.connect(host='127.0.0.1', port=3307, user=user, password=password, database=schema)
    cur = cn.cursor()
    cur.execute("""
        SELECT 
            id, codigo, descripcion, estado, ot, red, tipo, cod_trabajo,
            total_presupuesto, total_certificado, total_pendiente,
            creado_en, actualizado_en
        FROM vw_partes_resumen
        ORDER BY id DESC
    """)
    rows = cur.fetchall()
    cur.close()
    cn.close()
    return rows


def get_parte_detail(user: str, password: str, schema: str, parte_id: int):
    """
    Devuelve todos los datos de un parte específico.
    """
    import mysql.connector as m
    cn = m.connect(host='127.0.0.1', port=3307, user=user, password=password, database=schema)
    cur = cn.cursor()

    # Verificar qué columnas existen
    cur.execute(f"DESCRIBE {schema}.tbl_partes")
    columns = [row[0] for row in cur.fetchall()]

    # Construir SELECT dinámicamente
    select_cols = ['id', 'codigo', 'descripcion', 'estado',
                   'ot_id', 'red_id', 'tipo_trabajo_id', 'cod_trabajo_id']

    # Añadir columnas opcionales si existen
    if 'municipio_id' in columns:
        select_cols.append('municipio_id')
    else:
        select_cols.append('NULL as municipio_id')

    if 'observaciones' in columns:
        select_cols.append('observaciones')
    else:
        select_cols.append('NULL as observaciones')

    select_cols.extend(['creado_en', 'actualizado_en'])

    query = f"SELECT {', '.join(select_cols)} FROM tbl_partes WHERE id = %s"
    cur.execute(query, (parte_id,))
    row = cur.fetchone()
    cur.close()
    cn.close()
    return row


def mod_parte_item(user: str, password: str, schema: str, parte_id: int,
                   ot_id: int, red_id: int, tipo_trabajo_id: int, cod_trabajo_id: int,
                   descripcion: str = None, estado: str = 'Pendiente', observaciones: str = None):
    """
    Modifica los datos de un parte existente.
    """
    import mysql.connector as m
    try:
        cn = m.connect(host='127.0.0.1', port=3307, user=user, password=password, database=schema)
        cur = cn.cursor()

        # Verificar si existe la columna observaciones
        cur.execute(f"DESCRIBE {schema}.tbl_partes")
        columns = [row[0] for row in cur.fetchall()]

        if 'observaciones' in columns:
            cur.execute("""
                        UPDATE tbl_partes
                        SET ot_id           = %s,
                            red_id          = %s,
                            tipo_trabajo_id = %s,
                            cod_trabajo_id  = %s,
                            descripcion     = %s,
                            estado          = %s,
                            observaciones   = %s,
                            actualizado_en  = NOW()
                        WHERE id = %s
                        """,
                        (ot_id, red_id, tipo_trabajo_id, cod_trabajo_id, descripcion, estado, observaciones, parte_id))
        else:
            cur.execute("""
                        UPDATE tbl_partes
                        SET ot_id           = %s,
                            red_id          = %s,
                            tipo_trabajo_id = %s,
                            cod_trabajo_id  = %s,
                            descripcion     = %s,
                            estado          = %s,
                            actualizado_en  = NOW()
                        WHERE id = %s
                        """, (ot_id, red_id, tipo_trabajo_id, cod_trabajo_id, descripcion, estado, parte_id))

        cn.commit()
        cur.close()
        cn.close()
        return "ok"
    except Exception as e:
        return str(e)

# ==================== PRESUPUESTO DE PARTES ====================

def get_part_presupuesto(user: str, password: str, schema: str, parte_id: int):
    """
    Devuelve el presupuesto de un parte (partidas añadidas).
    """
    import mysql.connector as m
    cn = m.connect(host='127.0.0.1', port=3307, user=user, password=password, database=schema)
    cur = cn.cursor()
    cur.execute("""
        SELECT id, parte_id, codigo_parte, codigo_partida, resumen, 
               descripcion, unidad, cantidad, precio_unit, coste
        FROM vw_part_presupuesto
        WHERE parte_id = %s
        ORDER BY codigo_partida
    """, (parte_id,))
    rows = cur.fetchall()
    cur.close()
    cn.close()
    return rows


def add_part_presupuesto_item(user: str, password: str, schema: str,
                               parte_id: int, precio_id: int, cantidad: float, precio_unit: float):
    """
    Añade una partida al presupuesto de un parte.
    """
    import mysql.connector as m
    try:
        cn = m.connect(host='127.0.0.1', port=3307, user=user, password=password, database=schema)
        cur = cn.cursor()
        cur.execute("""
            INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, precio_unit)
            VALUES (%s, %s, %s, %s)
        """, (parte_id, precio_id, cantidad, precio_unit))
        cn.commit()
        cur.close()
        cn.close()
        return "ok"
    except Exception as e:
        return str(e)


def mod_amount_part_budget_item(user: str, password: str, schema: str, item_id: int, cantidad: float):
    """
    Modifica la cantidad de una partida en el presupuesto de un parte.
    """
    import mysql.connector as m
    try:
        cn = m.connect(host='127.0.0.1', port=3307, user=user, password=password, database=schema)
        cur = cn.cursor()
        cur.execute("""
            UPDATE tbl_part_presupuesto
            SET cantidad = %s
            WHERE id = %s
        """, (cantidad, item_id))
        cn.commit()
        cur.close()
        cn.close()
        return "ok"
    except Exception as e:
        return str(e)


def delete_part_presupuesto_item(user: str, password: str, schema: str, item_id: int):
    """
    Elimina una partida del presupuesto de un parte.
    """
    import mysql.connector as m
    try:
        cn = m.connect(host='127.0.0.1', port=3307, user=user, password=password, database=schema)
        cur = cn.cursor()
        cur.execute("DELETE FROM tbl_part_presupuesto WHERE id = %s", (item_id,))
        cn.commit()
        cur.close()
        cn.close()
        return "ok"
    except Exception as e:
        return str(e)


# ==================== CERTIFICACIONES DE PARTES ====================

def get_part_cert_pendientes(user: str, password: str, schema: str, parte_id: int):
    """
    Devuelve las partidas NO certificadas de un parte.
    Calcula: presupuesto - suma(certificado).
    """
    import mysql.connector as m
    cn = m.connect(host='127.0.0.1', port=3307, user=user, password=password, database=schema)
    cur = cn.cursor()
    cur.execute("""
        SELECT 
            pp.id AS presupuesto_id,
            pp.precio_id,
            pr.codigo AS codigo_partida,
            pr.resumen,
            u.unidad,
            pp.cantidad AS cantidad_presupuesto,
            COALESCE(SUM(pc.cantidad_cert), 0) AS cantidad_certificada,
            (pp.cantidad - COALESCE(SUM(pc.cantidad_cert), 0)) AS cantidad_pendiente,
            pp.precio_unit
        FROM tbl_part_presupuesto pp
        INNER JOIN tbl_pres_precios pr ON pr.id = pp.precio_id
        LEFT JOIN tbl_pres_unidades u ON u.id = pr.id_unidades
        LEFT JOIN tbl_part_certificacion pc ON pc.parte_id = pp.parte_id 
                                             AND pc.precio_id = pp.precio_id
        WHERE pp.parte_id = %s
        GROUP BY pp.id, pp.precio_id, pr.codigo, pr.resumen, u.unidad, 
                 pp.cantidad, pp.precio_unit
        HAVING cantidad_pendiente > 0
        ORDER BY pr.codigo
    """, (parte_id,))
    rows = cur.fetchall()
    cur.close()
    cn.close()
    return rows


def get_part_cert_certificadas(user: str, password: str, schema: str, parte_id: int):
    """
    Devuelve las certificaciones YA certificadas de un parte.
    """
    import mysql.connector as m
    cn = m.connect(host='127.0.0.1', port=3307, user=user, password=password, database=schema)
    cur = cn.cursor()
    cur.execute("""
        SELECT id, parte_id, codigo_parte, codigo_partida, resumen, unidad,
               cantidad_cert, precio_unit, coste_cert, fecha_certificacion, 
               certificada, ot, red, tipo, cod_trabajo, creado_en
        FROM vw_part_certificaciones
        WHERE parte_id = %s AND certificada = 1
        ORDER BY fecha_certificacion DESC, codigo_partida
    """, (parte_id,))
    rows = cur.fetchall()
    cur.close()
    cn.close()
    return rows


def add_part_cert_item(user: str, password: str, schema: str,
                       parte_id: int, precio_id: int, cantidad_cert: float,
                       precio_unit: float, fecha_certificacion: str,
                       certificada: int = 0):
    """
    Añade una certificación (certificada o pendiente) a un parte.
    fecha_certificacion: formato 'YYYY-MM-DD'
    certificada: 0=pendiente, 1=certificada
    """
    import mysql.connector as m
    try:
        cn = m.connect(host='127.0.0.1', port=3307, user=user, password=password, database=schema)
        cur = cn.cursor()
        cur.execute("""
            INSERT INTO tbl_part_certificacion 
            (parte_id, precio_id, cantidad_cert, precio_unit, fecha_certificacion, certificada)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (parte_id, precio_id, cantidad_cert, precio_unit, fecha_certificacion, certificada))
        cn.commit()
        cur.close()
        cn.close()
        return "ok"
    except Exception as e:
        return str(e)


def cert_part_item(user: str, password: str, schema: str, cert_id: int, fecha_certificacion: str):
    """
    Marca una certificación como certificada (certificada=1) y actualiza su fecha.
    """
    import mysql.connector as m
    try:
        cn = m.connect(host='127.0.0.1', port=3307, user=user, password=password, database=schema)
        cur = cn.cursor()
        cur.execute("""
            UPDATE tbl_part_certificacion
            SET certificada = 1, fecha_certificacion = %s
            WHERE id = %s
        """, (fecha_certificacion, cert_id))
        cn.commit()
        cur.close()
        cn.close()
        return "ok"
    except Exception as e:
        return str(e)


def delete_part_cert_item(user: str, password: str, schema: str, cert_id: int):
    """
    Elimina una certificación.
    """
    import mysql.connector as m
    try:
        cn = m.connect(host='127.0.0.1', port=3307, user=user, password=password, database=schema)
        cur = cn.cursor()
        cur.execute("DELETE FROM tbl_part_certificacion WHERE id = %s", (cert_id,))
        cn.commit()
        cur.close()
        cn.close()
        return "ok"
    except Exception as e:
        return str(e)