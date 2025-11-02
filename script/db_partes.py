import mysql.connector
from .db_config import get_config
from .db_connection import get_connection, get_project_connection


# ==================== DIMENSIONES DE CERTIFICACIÓN (OT/RED/TIPO/CÓDIGO) ====================

def _guess_text_column(user: str, password: str, schema: str, table: str):
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
    keywords_map = {
        'dim_ot': ['ot','nombre','desc','texto','codigo','cod'],
        'dim_red': ['red','nombre','desc','texto','codigo','cod'],
        'dim_tipo_trabajo': ['tipo','nombre','desc','texto','codigo','cod'],
        'dim_codigo_trabajo': ['cod_trabajo','codigo','cod','nombre','desc','texto'],
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


def add_dim_ot(user: str, password: str, schema: str, ot_codigo: str, descripcion: str = None):
    """
    Añade un nuevo código de OT a la tabla dim_ot.
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()
            # Detectar la columna de texto
            text_col = _guess_text_column(user, password, schema, 'dim_ot')
            if text_col:
                cur.execute(f"INSERT INTO dim_ot (ot_codigo, {text_col}) VALUES (%s, %s)", (ot_codigo, descripcion or ot_codigo))
            else:
                cur.execute("INSERT INTO dim_ot (ot_codigo) VALUES (%s)", (ot_codigo,))
            cn.commit()
            cur.close()
            return "ok"
    except Exception as e:
        return str(e)


def get_all_dim_ot(user: str, password: str, schema: str):
    """
    Devuelve todos los registros de dim_ot.
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()
            text_col = _guess_text_column(user, password, schema, 'dim_ot')
            if text_col:
                cur.execute(f"SELECT id, ot_codigo, {text_col} FROM dim_ot ORDER BY ot_codigo")
            else:
                cur.execute("SELECT id, ot_codigo FROM dim_ot ORDER BY ot_codigo")
            rows = cur.fetchall()
            cur.close()
            return rows
    except Exception as e:
        return []


def delete_dim_ot(user: str, password: str, schema: str, ot_id: int):
    """
    Elimina un código de OT.
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()
            cur.execute("DELETE FROM dim_ot WHERE id = %s", (ot_id,))
            cn.commit()
            cur.close()
            return "ok"
    except Exception as e:
        return str(e)


# ==================== GESTIÓN DE PARTES ====================

def add_parte_with_code(user, password, schema, ot_id, red_id, tipo_trabajo_id, cod_trabajo_id, descripcion):
    """
    Inserta un parte y genera el código automático (PT-00001).
    Devuelve (id, codigo).
    """
    with get_project_connection(user, password, schema) as cn:
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
        cur.close()
        return new_id, codigo


def list_partes(user: str, password: str, schema: str, limit: int = 200):
    """
    Devuelve una lista de dicts con los partes más recientes.
    Campos: id, codigo, ot, red, tipo, cod_trabajo, descripcion, created_at
    """
    with get_project_connection(user, password, schema) as cn:
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
        cur.close()

        cols = ["id","codigo","ot","red","tipo","cod_trabajo","descripcion","created_at"]
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

        # Intentar con las columnas timestamp
        try:
            cur.execute("""
                SELECT
                    id, codigo, descripcion, estado, ot, red, tipo, cod_trabajo,
                    total_presupuesto, total_certificado, total_pendiente,
                    creado_en, actualizado_en
                FROM vw_partes_resumen
                ORDER BY id DESC
            """)
            rows = cur.fetchall()
        except Exception:
            # Si falla (columnas no existen), intentar sin ellas
            cur.execute("""
                SELECT
                    id, codigo, descripcion, estado, ot, red, tipo, cod_trabajo,
                    total_presupuesto, total_certificado, total_pendiente,
                    NULL as creado_en, NULL as actualizado_en
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

        # Añadir columnas de timestamp si existen
        if 'creado_en' in columns:
            select_cols.append('creado_en')
        else:
            select_cols.append('NULL as creado_en')

        if 'actualizado_en' in columns:
            select_cols.append('actualizado_en')
        else:
            select_cols.append('NULL as actualizado_en')

        query = f"SELECT {', '.join(select_cols)} FROM tbl_partes WHERE id = %s"
        cur.execute(query, (parte_id,))
        row = cur.fetchone()
        cur.close()
        return row


def mod_parte_item(user: str, password: str, schema: str, parte_id: int,
                   ot_id: int, red_id: int, tipo_trabajo_id: int, cod_trabajo_id: int,
                   descripcion: str = None, estado: str = 'Pendiente', observaciones: str = None):
    """
    Modifica los datos de un parte existente.
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()

            # Verificar si existen las columnas opcionales
            cur.execute(f"DESCRIBE {schema}.tbl_partes")
            columns = [row[0] for row in cur.fetchall()]

            has_observaciones = 'observaciones' in columns
            has_actualizado_en = 'actualizado_en' in columns

            # Construir UPDATE dinámicamente
            set_clauses = [
                "ot_id = %s",
                "red_id = %s",
                "tipo_trabajo_id = %s",
                "cod_trabajo_id = %s",
                "descripcion = %s",
                "estado = %s"
            ]
            params = [ot_id, red_id, tipo_trabajo_id, cod_trabajo_id, descripcion, estado]

            if has_observaciones:
                set_clauses.append("observaciones = %s")
                params.append(observaciones)

            if has_actualizado_en:
                set_clauses.append("actualizado_en = NOW()")

            params.append(parte_id)

            query = f"""
                UPDATE tbl_partes
                SET {', '.join(set_clauses)}
                WHERE id = %s
            """
            cur.execute(query, params)

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

        # Intentar con la columna creado_en
        try:
            cur.execute("""
                SELECT id, parte_id, codigo_parte, codigo_partida, resumen, unidad,
                       cantidad_cert, precio_unit, coste_cert, fecha_certificacion,
                       certificada, ot, red, tipo, cod_trabajo, creado_en
                FROM vw_part_certificaciones
                WHERE parte_id = %s AND certificada = 1
                ORDER BY fecha_certificacion DESC, codigo_partida
            """, (parte_id,))
            rows = cur.fetchall()
        except Exception:
            # Si falla (columna no existe), intentar sin ella
            cur.execute("""
                SELECT id, parte_id, codigo_parte, codigo_partida, resumen, unidad,
                       cantidad_cert, precio_unit, coste_cert, fecha_certificacion,
                       certificada, ot, red, tipo, cod_trabajo, NULL as creado_en
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
