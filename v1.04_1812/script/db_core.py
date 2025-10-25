import mysql.connector
from mysql.connector import Error
import secrets
import string
import os
from .db_config import get_config
from .db_connection import (
    get_connection,
    get_manager_connection,
    get_project_connection,
    execute_query,
    execute_insert,
    execute_update
)


# ==================== FUNCIONES DE CONEXIÓN Y AUTENTICACIÓN ====================

#COMPRUEBA LOGIN EN BBDD PARA DAR ACCESO A LA APP
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
        # Usar la configuración centralizada y context manager
        with get_connection(user, password) as conn:
            print("Conexión exitosa al servidor MySQL.")
            # La conexión se cierra automáticamente al salir del with
            return conn, None
    except Exception as e:
        print(f"Error al conectar a MySQL: {e}")
        return None, e



#COMPRUEBA SI ERES MANAGER PARA DEJARTE ENTRAR EN EL MODULO DE MANAGER
def manager_db(user, password):
    """
    Comprueba si el usuario tiene acceso al módulo de manager.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario

    Returns:
        tuple: (connection, error) - connection si exitoso, error si falla
    """
    try:
        # Usar el helper para esquema manager
        with get_manager_connection(user, password) as conn:
            print("Conexión exitosa al servidor MySQL.")
            return conn, None
    except Exception as e:
        print(f"Error al conectar a MySQL: {e}")
        return None, e


#COMPRUEBA SI ERES MANAGER PARA DEJARTE ENTRAR EN EL MODULO DE USUARIOS
def user_db(user, password):
    """
    Comprueba si el usuario tiene acceso al módulo de usuarios.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario

    Returns:
        tuple: (connection, error) - connection si exitoso, error si falla
    """
    try:
        # Usar la configuración centralizada y context manager
        with get_connection(user, password) as conn:
            print("Conexión exitosa al servidor MySQL.")
            return conn, None
    except Exception as e:
        print(f"Error al conectar a MySQL: {e}")
        return None, e


# ==================== GESTIÓN DE ESQUEMAS Y BASES DE DATOS ====================

#DEVUELVE LOS ESQUEMAS DE LA BBDD A LOS QUE TIENE EL USUARIO ACCESO
def get_schemas_db(user, password):
    """
    Devuelve los esquemas de la BBDD a los que tiene acceso el usuario.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario

    Returns:
        list: Lista de nombres de esquemas
    """
    with get_connection(user, password) as conn:
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        records = cursor.fetchall()
        schemas = sum([list(elem) for elem in records], [])
        cursor.close()
        return schemas


#DEVUELVE LAS TABLAS DE UN ESQUEMA DE LA BBDD A LOS QUE TIENE EL USUARIO ACCESO
def get_table_schemas_db(user, password, schema):
    """
    Devuelve las tablas de un esquema de la BBDD.

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


#CREA EL ESQUEMA DEL PROYECTO
def create_schemas_db(user, password, db_name):
    """
    Crea el esquema del proyecto.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario
        db_name: Nombre del esquema a crear

    Returns:
        str: 'ok' si exitoso, error si falla
    """
    with get_connection(user, password) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"CREATE SCHEMA {db_name}")
            cursor.close()
            return "ok"
        except Error as e:
            cursor.close()
            print(f"Error al conectarse a MySQL: {e}")
            return e


#COPIAR TABLAS VACIAS DEL PROYECTO TIPO A ESQUEMA PROYECTO
def create_tables_schema_db(user, password, new, example):
    """
    Copiar tablas vacías del proyecto tipo a esquema proyecto.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario
        new: Lista de nombres de tablas nuevas
        example: Lista de nombres de tablas de ejemplo

    Returns:
        str: 'ok' si exitoso, error si falla
    """
    with get_connection(user, password) as conn:
        cursor = conn.cursor()
        try:
            conn.start_transaction()
            for i in range(len(new)):
                new_table = new[i]
                example_table = example[i]
                cursor.execute(f"CREATE TABLE {new_table} LIKE {example_table}")
            conn.commit()
            cursor.close()
            return "ok"
        except Error as e:
            conn.rollback()
            cursor.close()
            print(f"Error al conectarse a MySQL: {e}")
            return e


#COPIAR CONTENIDO DE TABLAS DEL PROYECTO TIPO A ESQUEMA PROYECTO
def copy_tables_schema_db(user, password, code_project, table):
    """
    Copiar contenido de tablas del proyecto tipo a esquema proyecto.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario
        code_project: Código del proyecto destino
        table: Nombre de la tabla

    Returns:
        str: 'ok' si exitoso, error si falla
    """
    config = get_config()
    with get_connection(user, password) as conn:
        cursor = conn.cursor()
        try:
            conn.start_transaction()
            cursor.execute(f"INSERT INTO {code_project}.{table} SELECT * FROM {config.example_schema}.{table}")
            conn.commit()
            cursor.close()
            return "ok"
        except Error as e:
            conn.rollback()
            cursor.close()
            print(f"Error al conectarse a MySQL: {e}")
            return e


#CREAR TABLA DE MUNICIPIOS PARA PROYECTO
def create_locality_schema_db(user, password, code_project, cod_province):
    """
    Crear tabla de municipios para proyecto.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario
        code_project: Código del proyecto
        cod_province: Código de la provincia

    Returns:
        str: 'ok' si exitoso, error si falla
    """
    config = get_config()
    with get_connection(user, password) as conn:
        cursor = conn.cursor()
        try:
            conn.start_transaction()
            cursor.execute(f"INSERT INTO {code_project}.tbl_municipios SELECT * FROM {config.manager_schema}.list_municipios WHERE CODNUT3 = '{cod_province}'")
            conn.commit()
            cursor.close()
            return "ok"

    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e


#CREA VISTA TBL DE PROYECTOS PARA QUE PUEDAS ACCEDER AL ID DESDE EL ESQUEMA SIN SER ADMINISTRADOR
def create_view_projects(user, password, code_project):
    """
    Crea vista tbl de proyectos para acceder al ID desde el esquema sin ser administrador.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario
        code_project: Código del proyecto

    Returns:
        str: 'ok' si exitoso, error si falla
    """
    config = get_config()
    with get_project_connection(user, password, code_project) as conn:
        cursor = conn.cursor()
        try:
            conn.start_transaction()
            cursor.execute(f"CREATE VIEW tbl_proyectos AS SELECT * FROM {config.manager_schema}.tbl_proyectos")
            conn.commit()
            cursor.close()
            return "ok"
        except Error as e:
            conn.rollback()
            cursor.close()
            print(f"Error al conectarse a MySQL: {e}")
            return e


#CREA VISTA DE LOS CATÁLOGOS PARA OPTIMIZAR VISUALIZACIÓN LAS TABLAS DE LA APLICACIÓN
def create_view_catalog(user, password, code_project):
    """
    Crea vista de los catálogos para optimizar visualización de las tablas de la aplicación.

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
            # Crear vista del catálogo de hidráulica
            cursor.execute(""" CREATE VIEW vw_catalogo_hidraulica AS
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
            # Crear vista del catálogo de registros
            cursor.execute(""" CREATE VIEW vw_catalogo_registros AS
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
            conn.commit()
            cursor.close()
            return "ok"
        except Error as e:
            conn.rollback()
            cursor.close()
            print(f"Error al conectarse a MySQL: {e}")
            return e


#CREA VISTA DEL PRESUPUESTO Y CERTIFICACION DEL PROYECTO
def create_view_economic(user, password, code_project):
    """
    Crea vista del presupuesto y certificación del proyecto.

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
            # Crear vista del presupuesto
            cursor.execute(""" CREATE VIEW vw_presupuesto AS
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
            # Crear vista de certificaciones
            cursor.execute(""" CREATE VIEW vw_certificaciones AS
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
            conn.commit()
            cursor.close()
            return "ok"
        except Error as e:
            conn.rollback()
            cursor.close()
            print(f"Error al conectarse a MySQL: {e}")
            return e


#CREA VISTA DE LOS REGISTROS DEL INVENTARIO  PARA DYNAMO
def create_view_inventory(user, password, code_project):
    """
    Crea vista de los registros del inventario para Dynamo.

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
            cursor.execute(""" CREATE VIEW vw_inv_elementos AS
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
            conn.commit()
            cursor.close()
            return "ok"
        except Error as e:
            conn.rollback()
            cursor.close()
            print(f"Error al conectarse a MySQL: {e}")
            return e


#CREA CLAVES FORANEAS PARA RELACIONAR TABLAS DEL PROYECTO
def create_fk(user, password, code_project):
    """
    Crea claves foráneas para relacionar tablas del proyecto.

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
            # Ejecutar la consulta asiganr claves foraneas a tablas
            cursor.execute(""" ALTER TABLE `tbl_presupuesto`
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
            conn.commit()
            cursor.close()
            return "ok"
        except Error as e:
            conn.rollback()
            cursor.close()
            print(f"Error al conectarse a MySQL: {e}")
            return e


#ACTUALIZA LAS REFERENCIAS DEL PROYECTO SEGUN SU DIRECTORIO
def update_reference(user, password, code_project, path_reference):
    """
    Actualiza las referencias del proyecto según su directorio.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario
        code_project: Código del proyecto
        path_reference: Ruta del directorio de referencias

    Returns:
        str: 'ok' si exitoso, error si falla
    """
    reference_files = []

    # Recorrer todos los niveles de subdirectorios
    for subdir, dirs, files in os.walk(path_reference):
        for file in files:
            if file.endswith('.dwg'):
                subpath = os.path.relpath(subdir, path_reference)
                name_file = os.path.splitext(file)[0]
                path_file = os.path.join(subpath, name_file)
                reference_files.append((subpath, name_file, path_file))

    with get_project_connection(user, password, code_project) as conn:
        cursor = conn.cursor()
        try:
            # Borrar los registros existentes
            cursor.execute("DELETE FROM tbl_cata_hidra_referencias_cad")
            conn.commit()

            # Resetear AUTO_INCREMENT
            cursor.execute("ALTER TABLE tbl_cata_hidra_referencias_cad AUTO_INCREMENT = 1;")
            conn.commit()

            # Insertar nuevos archivos si existen
            if reference_files:
                conn.start_transaction()
                cursor.executemany("""
                INSERT INTO tbl_cata_hidra_referencias_cad (directorio, referencia, ruta)
                VALUES (%s, %s, %s)
                """, list(reference_files))
                conn.commit()

            cursor.close()
            return "ok"
        except Error as e:
            conn.rollback()
            cursor.close()
            print(f"Error al conectarse a MySQL: {e}")
            return e


# ==================== GESTIÓN DE UBICACIONES (CCAA, PROVINCIAS) ====================

#DEVUELVE LAS CCAA DE LA BBDD PARA OPCIONES EN APP
def get_ccaa_bd(user, password):
    """
    Devuelve las CCAA de la BBDD para opciones en APP.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario

    Returns:
        list: Lista de nombres de CCAA
    """
    config = get_config()
    with get_manager_connection(user, password) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT NAMEUNIT FROM {config.manager_schema}.list_ccaa")
        records = cursor.fetchall()
        ccaa = sum([list(elem) for elem in records], [])
        cursor.close()
        return ccaa


#DEVUELVE CODIGO DE LA PROVINCIA
def get_id_ccaa_bd(user, password, select_ccaa):
    """
    Devuelve código de la CCAA.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario
        select_ccaa: Nombre de la CCAA

    Returns:
        int: ID de la CCAA
    """
    config = get_config()
    with get_manager_connection(user, password) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT id FROM {config.manager_schema}.list_ccaa WHERE NAMEUNIT='{select_ccaa}'")
        records = cursor.fetchall()
        code_ccaa = sum([list(elem) for elem in records], [])
        cursor.close()
        return code_ccaa[0]


#DEVUELVE CODIGO DE LA PROVINCIA
def get_id_province_bd(user, password, select_province):
    """
    Devuelve código de la provincia.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario
        select_province: Nombre de la provincia

    Returns:
        int: ID de la provincia
    """
    config = get_config()
    with get_manager_connection(user, password) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT id FROM {config.manager_schema}.list_provincias WHERE NAMEUNIT='{select_province}'")
        records = cursor.fetchall()
        code_province = sum([list(elem) for elem in records], [])
        cursor.close()
        return code_province[0]


#DEVUELVE CODIGO DE LA CCAA DE LA BBDD PARA OPCIONES DE PROVINCIA EN APP
def get_code_ccaa_bd(user, password, select_ccaa):
    """
    Devuelve código de la CCAA de la BBDD para opciones de provincia en APP.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario
        select_ccaa: Nombre de la CCAA

    Returns:
        str: Código NUT2 de la CCAA
    """
    config = get_config()
    with get_manager_connection(user, password) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT CODNUT2 FROM {config.manager_schema}.list_ccaa WHERE NAMEUNIT='{select_ccaa}'")
        records = cursor.fetchall()
        code_ccaa = sum([list(elem) for elem in records], [])
        cursor.close()
        return code_ccaa[0]


#DEVUELVE LAS PROVINCIAS FILTRADAS POR CCAA DE LA BBDD PARA OPCIONES EN APP
def get_province_bd(user, password, code_ccaa):
    """
    Devuelve las provincias filtradas por CCAA de la BBDD para opciones en APP.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario
        code_ccaa: Código NUT2 de la CCAA

    Returns:
        list: Lista de nombres de provincias
    """
    config = get_config()
    with get_manager_connection(user, password) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT NAMEUNIT FROM {config.manager_schema}.list_provincias WHERE CODNUT2='{code_ccaa}'")
        records = cursor.fetchall()
        province = sum([list(elem) for elem in records], [])
        cursor.close()
        return province


# ==================== FUNCIONES GENÉRICAS CRUD ====================

#DEVUELVE EL ID DE UN ELEMENTO DE UNA TABLA DE LA BBDD
def get_id_item_bd(user, password, table, schema, field, item):
    """
    Devuelve el ID de un elemento de una tabla de la BBDD.

    Args:
        user: Usuario de la base de datos
        password: Contraseña del usuario
        table: Nombre de la tabla
        schema: Nombre del esquema
        field: Campo por el que filtrar
        item: Valor del campo

    Returns:
        int: ID del elemento
    """
    with get_connection(user, password) as conn:
        cursor = conn.cursor()
        sql_query = f"SELECT id FROM {schema}.{table} WHERE {field} = '{item}'"
        cursor.execute(sql_query)
        records = cursor.fetchall()
        option_items = sum([list(elem) for elem in records], [])
        id_item = option_items[0]
        cursor.close()
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


# ==================== GESTIÓN DE USUARIOS BD ====================

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


# VERIFICA SI EXISTE EL USUARIO
def user_verfication(cursor, user, host='%'):
    query = f"SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = '{user}' AND host = '{host}');"
    cursor.execute(query)
    return cursor.fetchone()[0]


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


# ==================== GESTIÓN DE PRIVILEGIOS ====================

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
