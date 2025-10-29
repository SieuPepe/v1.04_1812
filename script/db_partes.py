import mysql.connector
from .db_config import get_config
from .db_connection import get_connection, get_project_connection


# ==================== DIMENSIONES DE CERTIFICACIÓN (OT/RED/TIPO/CÓDIGO) ====================

def _guess_text_column(user: str, password: str, schema: str, table: str):
    """
    Intenta detectar automáticamente la columna 'de texto' para mostrar en menús.
    Estrategia:
      1) Preferir nombres que contengan alguna keyword según tabla:
         - dim_red:        ['red','nombre','desc','texto','codigo','cod']
         - dim_tipo_trabajo: ['tipo','nombre','desc','texto','codigo','cod']
         - dim_codigo_trabajo: ['cod_trabajo','nombre','desc','texto','codigo','cod']
      2) Si no hay match por nombre, elegir la primera columna tipo VARCHAR/TEXT distinta de 'id'.
    Devuelve nombre de columna o None si no encuentra.
    """
    keywords_map = {
        'dim_red': ['descripcion','desc','nombre','texto','red','codigo','cod'],
        'dim_tipo_trabajo': ['descripcion','desc','nombre','texto','tipo','codigo','cod'],
        'dim_codigo_trabajo': ['descripcion','desc','nombre','texto','cod_trabajo','codigo','cod'],
    }
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()
            cur.execute(
                "SELECT COLUMN_NAME, DATA_TYPE FROM information_schema.COLUMNS "
                "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s ORDER BY ORDINAL_POSITION",
                (schema, table)
            )
            cols = cur.fetchall()  # [(col, type), ...]
            cur.close()
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


def _fetch_dim_list_guess(user: str, password: str, schema: str, table: str):
    """
    Devuelve lista de 'id - texto' detectando automáticamente la columna de texto.
    """
    text_col = _guess_text_column(user, password, schema, table)
    if not text_col:
        return []
    rows = []
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()
            cur.execute(f"SELECT id, {text_col} FROM {schema}.{table} ORDER BY {text_col}")
            for rid, txt in cur.fetchall():
                rows.append(f"{rid} - {txt}")
            cur.close()
    except Exception:
        pass
    return rows


def get_dim_all(user: str, password: str, schema: str):
    """
    Devuelve dict con las 3 listas de dimensiones para la UI,
    detectando automáticamente la columna visible:
      - dim_red
      - dim_tipo_trabajo
      - dim_codigo_trabajo
    """
    return {
        'RED': _fetch_dim_list_guess(user, password, schema, 'dim_red'),
        'TIPO_TRABAJO': _fetch_dim_list_guess(user, password, schema, 'dim_tipo_trabajo'),
        'COD_TRABAJO': _fetch_dim_list_guess(user, password, schema, 'dim_codigo_trabajo'),
    }


# ==================== GESTIÓN DE PARTES ====================

def _get_tipo_trabajo_prefix(user, password, schema, tipo_trabajo_id):
    """
    Determina el prefijo del código según el tipo de trabajo:
    - Gastos Fijos → GF
    - Orden de Trabajo → OT
    - Trabajos Programados → TP
    - Por defecto → PT
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()
            # Detectar columna de texto en dim_tipo_trabajo
            text_col = _guess_text_column(user, password, schema, 'dim_tipo_trabajo')
            if text_col:
                cur.execute(f"SELECT {text_col} FROM dim_tipo_trabajo WHERE id = %s", (tipo_trabajo_id,))
            else:
                cur.execute("SELECT tipo_codigo FROM dim_tipo_trabajo WHERE id = %s", (tipo_trabajo_id,))

            result = cur.fetchone()
            cur.close()

            if result:
                tipo_nombre = result[0].lower() if result[0] else ""
                # Determinar prefijo según el nombre
                if "gastos" in tipo_nombre or "gf" in tipo_nombre:
                    return "GF"
                elif "orden" in tipo_nombre or "ot" == tipo_nombre:
                    return "OT"
                elif "programado" in tipo_nombre or "tp" in tipo_nombre:
                    return "TP"

            # Por defecto
            return "PT"
    except Exception:
        return "PT"


def add_parte_with_code(user, password, schema, red_id, tipo_trabajo_id, cod_trabajo_id, descripcion):
    """
    Inserta un parte y genera el código automático según el tipo de trabajo:
    - GF-00001 (Gastos Fijos)
    - OT-00001 (Orden de Trabajo)
    - TP-00001 (Trabajos Programados)
    Devuelve (id, codigo).
    """
    with get_project_connection(user, password, schema) as cn:
        cur = cn.cursor()
        cur.execute(
            "INSERT INTO tbl_partes (red_id, tipo_trabajo_id, cod_trabajo_id, descripcion) "
            "VALUES (%s,%s,%s,%s)",
            (red_id, tipo_trabajo_id, cod_trabajo_id, descripcion)
        )
        new_id = cur.lastrowid

        # Obtener prefijo según tipo de trabajo
        prefix = _get_tipo_trabajo_prefix(user, password, schema, tipo_trabajo_id)
        codigo = f"{prefix}-{new_id:05d}"

        cur.execute("UPDATE tbl_partes SET codigo=%s WHERE id=%s", (codigo, new_id))
        cn.commit()
        cur.close()
        return new_id, codigo


def list_partes(user: str, password: str, schema: str, limit: int = 200):
    """
    Devuelve una lista de dicts con los partes más recientes.
    Campos: id, codigo, red, tipo, cod_trabajo, descripcion, created_at
    """
    with get_project_connection(user, password, schema) as cn:
        cur = cn.cursor()
        cur.execute("""
            SELECT  p.id,
                    p.codigo,
                    COALESCE(rd.red_codigo, '')        AS red,
                    COALESCE(tt.tipo_codigo, '')       AS tipo,
                    COALESCE(ct.cod_trabajo,'')        AS cod_trabajo,
                    p.descripcion,
                    p.creado_en
            FROM tbl_partes p
            LEFT JOIN dim_red            rd ON rd.id = p.red_id
            LEFT JOIN dim_tipo_trabajo   tt ON tt.id = p.tipo_trabajo_id
            LEFT JOIN dim_codigo_trabajo ct ON ct.id = p.cod_trabajo_id
            ORDER BY p.id DESC
            LIMIT %s
        """, (limit,))
        rows = cur.fetchall()
        cur.close()

        cols = ["id","codigo","red","tipo","cod_trabajo","descripcion","created_at"]
        return [dict(zip(cols, r)) for r in rows]


def get_parts_list(user, password, schema, limit=100):
    """
    Devuelve lista de partes.
    """
    with get_project_connection(user, password, schema) as cn:
        cur = cn.cursor()
        cur.execute("""
            SELECT
                p.id,
                p.codigo,
                COALESCE(rd.red_codigo, '')        AS red,
                COALESCE(tt.tipo_codigo, '')       AS tipo,
                COALESCE(ct.cod_trabajo, '')       AS cod_trabajo,
                p.descripcion,
                p.creado_en
            FROM tbl_partes p
            LEFT JOIN dim_red            rd ON rd.id = p.red_id
            LEFT JOIN dim_tipo_trabajo   tt ON tt.id = p.tipo_trabajo_id
            LEFT JOIN dim_codigo_trabajo ct ON ct.id = p.cod_trabajo_id
            ORDER BY p.id DESC
            LIMIT %s
        """, (limit,))
        rows = cur.fetchall()
        cur.close()
        return rows


def delete_parte(user: str, password: str, schema: str, parte_id: int):
    """
    Elimina un parte por su ID
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()
            cur.execute("DELETE FROM tbl_partes WHERE id = %s", (parte_id,))
            cn.commit()
            cur.close()
            return "ok"
    except Exception as e:
        return str(e)


def get_partes_resumen(user: str, password: str, schema: str):
    """
    Devuelve lista de partes con totales de presupuesto y certificación.
    Usa la vista vw_partes_resumen.
    """
    with get_project_connection(user, password, schema) as cn:
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
        return rows


def get_parte_detail(user: str, password: str, schema: str, parte_id: int):
    """
    Devuelve todos los datos de un parte específico.
    """
    with get_project_connection(user, password, schema) as cn:
        cur = cn.cursor()

        # Verificar qué columnas existen
        cur.execute(f"DESCRIBE {schema}.tbl_partes")
        columns = [row[0] for row in cur.fetchall()]

        # Construir SELECT dinámicamente
        select_cols = ['id', 'codigo', 'descripcion', 'estado',
                       'red_id', 'tipo_trabajo_id', 'cod_trabajo_id']

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
        return row


def mod_parte_item(user: str, password: str, schema: str, parte_id: int,
                   red_id: int, tipo_trabajo_id: int, cod_trabajo_id: int,
                   descripcion: str = None, estado: str = 'Pendiente', observaciones: str = None):
    """
    Modifica los datos de un parte existente.
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()

            # Verificar si existe la columna observaciones
            cur.execute(f"DESCRIBE {schema}.tbl_partes")
            columns = [row[0] for row in cur.fetchall()]

            if 'observaciones' in columns:
                cur.execute("""
                            UPDATE tbl_partes
                            SET red_id          = %s,
                                tipo_trabajo_id = %s,
                                cod_trabajo_id  = %s,
                                descripcion     = %s,
                                estado          = %s,
                                observaciones   = %s,
                                actualizado_en  = NOW()
                            WHERE id = %s
                            """,
                            (red_id, tipo_trabajo_id, cod_trabajo_id, descripcion, estado, observaciones, parte_id))
            else:
                cur.execute("""
                            UPDATE tbl_partes
                            SET red_id          = %s,
                                tipo_trabajo_id = %s,
                                cod_trabajo_id  = %s,
                                descripcion     = %s,
                                estado          = %s,
                                actualizado_en  = NOW()
                            WHERE id = %s
                            """, (red_id, tipo_trabajo_id, cod_trabajo_id, descripcion, estado, parte_id))

            cn.commit()
            cur.close()
            return "ok"
    except Exception as e:
        return str(e)


# ==================== PRESUPUESTO DE PARTES ====================

def get_part_presupuesto(user: str, password: str, schema: str, parte_id: int):
    """
    Devuelve el presupuesto de un parte (partidas añadidas).
    """
    with get_project_connection(user, password, schema) as cn:
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
        return rows


def add_part_presupuesto_item(user: str, password: str, schema: str,
                               parte_id: int, precio_id: int, cantidad: float, precio_unit: float):
    """
    Añade una partida al presupuesto de un parte.
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()
            cur.execute("""
                INSERT INTO tbl_part_presupuesto (parte_id, precio_id, cantidad, precio_unit)
                VALUES (%s, %s, %s, %s)
            """, (parte_id, precio_id, cantidad, precio_unit))
            cn.commit()
            cur.close()
            return "ok"
    except Exception as e:
        return str(e)


def mod_amount_part_budget_item(user: str, password: str, schema: str, item_id: int, cantidad: float):
    """
    Modifica la cantidad de una partida en el presupuesto de un parte.
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()
            cur.execute("""
                UPDATE tbl_part_presupuesto
                SET cantidad = %s
                WHERE id = %s
            """, (cantidad, item_id))
            cn.commit()
            cur.close()
            return "ok"
    except Exception as e:
        return str(e)


def delete_part_presupuesto_item(user: str, password: str, schema: str, item_id: int):
    """
    Elimina una partida del presupuesto de un parte.
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()
            cur.execute("DELETE FROM tbl_part_presupuesto WHERE id = %s", (item_id,))
            cn.commit()
            cur.close()
            return "ok"
    except Exception as e:
        return str(e)


# ==================== CERTIFICACIONES DE PARTES ====================

def get_part_cert_pendientes(user: str, password: str, schema: str, parte_id: int):
    """
    Devuelve las partidas NO certificadas de un parte.
    Calcula: presupuesto - suma(certificado).
    """
    with get_project_connection(user, password, schema) as cn:
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
        return rows


def get_part_cert_certificadas(user: str, password: str, schema: str, parte_id: int):
    """
    Devuelve las certificaciones YA certificadas de un parte.
    """
    with get_project_connection(user, password, schema) as cn:
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
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()
            cur.execute("""
                INSERT INTO tbl_part_certificacion
                (parte_id, precio_id, cantidad_cert, precio_unit, fecha_certificacion, certificada)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (parte_id, precio_id, cantidad_cert, precio_unit, fecha_certificacion, certificada))
            cn.commit()
            cur.close()
            return "ok"
    except Exception as e:
        return str(e)


def cert_part_item(user: str, password: str, schema: str, cert_id: int, fecha_certificacion: str):
    """
    Marca una certificación como certificada (certificada=1) y actualiza su fecha.
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()
            cur.execute("""
                UPDATE tbl_part_certificacion
                SET certificada = 1, fecha_certificacion = %s
                WHERE id = %s
            """, (fecha_certificacion, cert_id))
            cn.commit()
            cur.close()
            return "ok"
    except Exception as e:
        return str(e)


def delete_part_cert_item(user: str, password: str, schema: str, cert_id: int):
    """
    Elimina una certificación.
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()
            cur.execute("DELETE FROM tbl_part_certificacion WHERE id = %s", (cert_id,))
            cn.commit()
            cur.close()
            return "ok"
    except Exception as e:
        return str(e)


# ==================== FUNCIONES MEJORADAS CON NUEVOS CAMPOS ====================

def add_parte_mejorado(user: str, password: str, schema: str,
                       red_id: int, tipo_trabajo_id: int, cod_trabajo_id: int,
                       titulo: str = None,
                       descripcion: str = None,
                       descripcion_larga: str = None,
                       descripcion_corta: str = None,
                       fecha_inicio: str = None,
                       fecha_fin: str = None,
                       fecha_prevista_fin: str = None,
                       id_estado: int = 1,
                       finalizada: bool = False,
                       localizacion: str = None,
                       id_municipio: int = None):
    """
    Inserta un parte con los campos mejorados y genera el código automático según tipo:
    GF-00001 (Gastos Fijos), OT-00001 (Orden de Trabajo), TP-00001 (Trabajos Programados).

    Args:
        user: Usuario de BD
        password: Contraseña
        schema: Esquema del proyecto
        red_id: ID de red (FK)
        tipo_trabajo_id: ID de tipo de trabajo (FK)
        cod_trabajo_id: ID de código de trabajo (FK)
        titulo: Título descriptivo del parte (obligatorio conceptualmente)
        descripcion: Descripción original (compatible con versión anterior)
        descripcion_larga: Descripción detallada del trabajo
        descripcion_corta: Resumen breve para listados
        fecha_inicio: Fecha de inicio (formato 'YYYY-MM-DD')
        fecha_fin: Fecha de finalización (formato 'YYYY-MM-DD')
        fecha_prevista_fin: Fecha prevista de finalización
        id_estado: ID del estado (1=Pendiente por defecto)
        finalizada: Booleano de finalización (sincronizado con estado)
        localizacion: Ubicación textual
        id_municipio: ID del municipio (FK)

    Returns:
        tuple: (id, codigo) del parte creado

    Raises:
        Exception: Si hay error en la inserción
    """
    with get_project_connection(user, password, schema) as cn:
        cur = cn.cursor()

        # Verificar qué columnas existen en tbl_partes
        cur.execute(f"DESCRIBE {schema}.tbl_partes")
        columns = {row[0] for row in cur.fetchall()}

        # Construir INSERT dinámicamente según columnas disponibles
        insert_cols = ['red_id', 'tipo_trabajo_id', 'cod_trabajo_id']
        insert_vals = [red_id, tipo_trabajo_id, cod_trabajo_id]

        # Campos nuevos (añadir solo si la columna existe)
        if 'titulo' in columns and titulo:
            insert_cols.append('titulo')
            insert_vals.append(titulo)

        if 'descripcion' in columns and descripcion:
            insert_cols.append('descripcion')
            insert_vals.append(descripcion)

        if 'descripcion_larga' in columns and descripcion_larga:
            insert_cols.append('descripcion_larga')
            insert_vals.append(descripcion_larga)

        if 'descripcion_corta' in columns and descripcion_corta:
            insert_cols.append('descripcion_corta')
            insert_vals.append(descripcion_corta)

        if 'fecha_inicio' in columns and fecha_inicio:
            insert_cols.append('fecha_inicio')
            insert_vals.append(fecha_inicio)

        if 'fecha_fin' in columns and fecha_fin:
            insert_cols.append('fecha_fin')
            insert_vals.append(fecha_fin)

        if 'fecha_prevista_fin' in columns and fecha_prevista_fin:
            insert_cols.append('fecha_prevista_fin')
            insert_vals.append(fecha_prevista_fin)

        if 'id_estado' in columns:
            insert_cols.append('id_estado')
            insert_vals.append(id_estado)

        if 'finalizada' in columns:
            insert_cols.append('finalizada')
            insert_vals.append(1 if finalizada else 0)

        if 'localizacion' in columns and localizacion:
            insert_cols.append('localizacion')
            insert_vals.append(localizacion)

        if 'id_municipio' in columns and id_municipio:
            insert_cols.append('id_municipio')
            insert_vals.append(id_municipio)

        # Construir query
        placeholders = ', '.join(['%s'] * len(insert_vals))
        query = f"INSERT INTO tbl_partes ({', '.join(insert_cols)}) VALUES ({placeholders})"

        cur.execute(query, tuple(insert_vals))
        new_id = cur.lastrowid

        # Generar código según tipo de trabajo
        prefix = _get_tipo_trabajo_prefix(user, password, schema, tipo_trabajo_id)
        codigo = f"{prefix}-{new_id:05d}"
        cur.execute("UPDATE tbl_partes SET codigo=%s WHERE id=%s", (codigo, new_id))

        cn.commit()
        cur.close()
        return new_id, codigo


def mod_parte_mejorado(user: str, password: str, schema: str,
                       parte_id: int,
                       red_id: int = None,
                       tipo_trabajo_id: int = None,
                       cod_trabajo_id: int = None,
                       titulo: str = None,
                       descripcion: str = None,
                       descripcion_larga: str = None,
                       descripcion_corta: str = None,
                       fecha_inicio: str = None,
                       fecha_fin: str = None,
                       fecha_prevista_fin: str = None,
                       id_estado: int = None,
                       finalizada: bool = None,
                       localizacion: str = None,
                       id_municipio: int = None):
    """
    Modifica un parte existente con los campos mejorados.
    Solo actualiza los campos que se pasan (los que son None se ignoran).

    Args:
        user: Usuario de BD
        password: Contraseña
        schema: Esquema del proyecto
        parte_id: ID del parte a modificar
        Resto de parámetros: ver add_parte_mejorado()

    Returns:
        str: "ok" si exitoso, mensaje de error si falla
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()

            # Verificar qué columnas existen
            cur.execute(f"DESCRIBE {schema}.tbl_partes")
            columns = {row[0] for row in cur.fetchall()}

            # Construir UPDATE dinámicamente
            update_parts = []
            update_vals = []

            # Campos obligatorios (solo actualizar si se pasan)
            if red_id is not None:
                update_parts.append('red_id = %s')
                update_vals.append(red_id)

            if tipo_trabajo_id is not None:
                update_parts.append('tipo_trabajo_id = %s')
                update_vals.append(tipo_trabajo_id)

            if cod_trabajo_id is not None:
                update_parts.append('cod_trabajo_id = %s')
                update_vals.append(cod_trabajo_id)

            # Campos nuevos
            if 'titulo' in columns and titulo is not None:
                update_parts.append('titulo = %s')
                update_vals.append(titulo)

            if 'descripcion' in columns and descripcion is not None:
                update_parts.append('descripcion = %s')
                update_vals.append(descripcion)

            if 'descripcion_larga' in columns and descripcion_larga is not None:
                update_parts.append('descripcion_larga = %s')
                update_vals.append(descripcion_larga)

            if 'descripcion_corta' in columns and descripcion_corta is not None:
                update_parts.append('descripcion_corta = %s')
                update_vals.append(descripcion_corta)

            if 'fecha_inicio' in columns and fecha_inicio is not None:
                update_parts.append('fecha_inicio = %s')
                update_vals.append(fecha_inicio)

            if 'fecha_fin' in columns and fecha_fin is not None:
                update_parts.append('fecha_fin = %s')
                update_vals.append(fecha_fin)

            if 'fecha_prevista_fin' in columns and fecha_prevista_fin is not None:
                update_parts.append('fecha_prevista_fin = %s')
                update_vals.append(fecha_prevista_fin)

            if 'id_estado' in columns and id_estado is not None:
                update_parts.append('id_estado = %s')
                update_vals.append(id_estado)

            if 'finalizada' in columns and finalizada is not None:
                update_parts.append('finalizada = %s')
                update_vals.append(1 if finalizada else 0)

            if 'localizacion' in columns and localizacion is not None:
                update_parts.append('localizacion = %s')
                update_vals.append(localizacion)

            if 'id_municipio' in columns and id_municipio is not None:
                update_parts.append('id_municipio = %s')
                update_vals.append(id_municipio)

            # Añadir fecha de actualización si existe
            if 'fecha_modificacion' in columns or 'actualizado_en' in columns:
                update_parts.append('actualizado_en = NOW()')

            if not update_parts:
                return "No hay campos para actualizar"

            # Construir y ejecutar query
            update_vals.append(parte_id)
            query = f"UPDATE tbl_partes SET {', '.join(update_parts)} WHERE id = %s"

            cur.execute(query, tuple(update_vals))
            cn.commit()
            cur.close()
            return "ok"
    except Exception as e:
        return str(e)


def get_estados_parte(user: str, password: str, schema: str):
    """
    Obtiene la lista de estados disponibles para los partes.

    Returns:
        list: Lista de diccionarios con keys: id, nombre, descripcion, orden
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()
            cur.execute("""
                SELECT id, nombre, descripcion, orden
                FROM tbl_parte_estados
                WHERE activo = TRUE
                ORDER BY orden
            """)
            rows = cur.fetchall()
            cur.close()

            # Convertir tuplas a diccionarios
            return [
                {
                    'id': row[0],
                    'nombre': row[1],
                    'descripcion': row[2],
                    'orden': row[3]
                }
                for row in rows
            ]
    except Exception:
        # Si la tabla no existe, devolver estados por defecto
        return [
            {'id': 1, 'nombre': 'Pendiente', 'descripcion': 'Parte pendiente de iniciar', 'orden': 1},
            {'id': 2, 'nombre': 'En curso', 'descripcion': 'Parte en ejecución', 'orden': 2},
            {'id': 3, 'nombre': 'Finalizada', 'descripcion': 'Parte completada con éxito', 'orden': 3},
            {'id': 4, 'nombre': 'Cancelada', 'descripcion': 'Parte cancelada', 'orden': 4},
        ]


def list_partes_mejorado(user: str, password: str, schema: str, limit: int = 200):
    """
    Devuelve una lista de dicts con los partes más recientes, incluyendo nuevos campos.

    Returns:
        list: Lista de dicts con todos los campos del parte
    """
    with get_project_connection(user, password, schema) as cn:
        cur = cn.cursor()

        # Verificar si existe la vista mejorada
        cur.execute(f"""
            SELECT COUNT(*)
            FROM information_schema.VIEWS
            WHERE TABLE_SCHEMA = '{schema}'
            AND TABLE_NAME = 'vw_partes_completo'
        """)

        if cur.fetchone()[0] > 0:
            # Usar vista mejorada si existe
            cur.execute(f"""
                SELECT *
                FROM vw_partes_completo
                ORDER BY fecha_inicio DESC, id DESC
                LIMIT %s
            """, (limit,))
        else:
            # Fallback a consulta manual
            cur.execute(f"""
                SELECT
                    p.id,
                    p.codigo,
                    p.titulo,
                    p.descripcion,
                    p.descripcion_larga,
                    p.descripcion_corta,
                    p.fecha_inicio,
                    p.fecha_fin,
                    p.fecha_prevista_fin,
                    CASE
                        WHEN p.fecha_fin IS NOT NULL AND p.fecha_inicio IS NOT NULL
                        THEN DATEDIFF(p.fecha_fin, p.fecha_inicio)
                        ELSE NULL
                    END AS dias_duracion,
                    pe.nombre AS estado,
                    p.finalizada,
                    p.localizacion,
                    m.nombre AS municipio,
                    r.red_codigo AS red,
                    tt.tipo_codigo AS tipo_trabajo,
                    ct.cod_trabajo AS cod_trabajo
                FROM tbl_partes p
                LEFT JOIN tbl_parte_estados pe ON p.id_estado = pe.id
                LEFT JOIN tbl_municipios m ON p.id_municipio = m.id
                LEFT JOIN dim_red r ON p.red_id = r.id
                LEFT JOIN dim_tipo_trabajo tt ON p.tipo_trabajo_id = tt.id
                LEFT JOIN dim_codigo_trabajo ct ON p.cod_trabajo_id = ct.id
                ORDER BY p.fecha_inicio DESC, p.id DESC
                LIMIT %s
            """, (limit,))

        # Obtener nombres de columnas
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        cur.close()

        # Convertir a lista de dicts
        return [dict(zip(columns, row)) for row in rows]
