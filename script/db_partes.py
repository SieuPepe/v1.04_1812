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


def _fetch_ot_list_by_code(user: str, password: str, schema: str):
    """
    Devuelve lista de 'ot_codigo - descripcion' para dim_ot.
    Formato especial para OT que usa codigo en lugar de ID numérico.
    Ejemplo: "OT-001 - Orden de Trabajo 001"
    """
    rows = []
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()
            text_col = _guess_text_column(user, password, schema, 'dim_ot')
            if not text_col:
                text_col = 'descripcion'

            cur.execute(f"SELECT ot_codigo, {text_col} FROM {schema}.dim_ot ORDER BY ot_codigo")
            for codigo, txt in cur.fetchall():
                if codigo:  # Solo si tiene código
                    rows.append(f"{codigo} - {txt}")
            cur.close()
    except Exception as e:
        print(f"Error en _fetch_ot_list_by_code: {e}")
        pass
    return rows


def get_dim_all(user: str, password: str, schema: str):
    """
    Devuelve dict con las 4 listas de dimensiones para la UI,
    detectando automáticamente la columna visible:
      - dim_ot (formato especial: ot_codigo - descripcion)
      - dim_red (formato: id - texto)
      - dim_tipo_trabajo (formato: id - texto)
      - dim_codigo_trabajo (formato: id - texto)
    """
    return {
        'OT': _fetch_ot_list_by_code(user, password, schema),
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

        # Obtener prefijo según tipo de trabajo y numeración independiente
        prefix = _get_tipo_trabajo_prefix(user, password, schema, tipo_trabajo_id)

        # Obtener el siguiente número para este prefijo específico
        # Más robusto: maneja NULLs y códigos vacíos
        cur.execute("""
            SELECT COALESCE(
                MAX(
                    CAST(
                        REPLACE(codigo, %s, '') AS UNSIGNED
                    )
                ),
                0
            ) + 1
            FROM tbl_partes
            WHERE codigo IS NOT NULL
              AND codigo LIKE %s
        """, (prefix + '-', prefix + '-%'))
        next_num = int(cur.fetchone()[0])  # Convertir a int para evitar ValueError con Decimal

        codigo = f"{prefix}-{next_num:05d}"

        cur.execute("UPDATE tbl_partes SET codigo=%s WHERE id=%s", (codigo, new_id))
        cn.commit()
        cur.close()
        return new_id, codigo


def list_partes(user: str, password: str, schema: str, limit: int = 200):
    """
    Devuelve una lista de dicts con los partes más recientes.
    Campos: id, codigo, red, tipo, cod_trabajo, descripcion, creado_en
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

        cols = ["id","codigo","red","tipo","cod_trabajo","descripcion","creado_en"]
        return [dict(zip(cols, r)) for r in rows]


def get_parts_list(user, password, schema, limit=100):
    """
    Devuelve lista de partes.
    Retorna: id, codigo, codigo_ot, red, tipo, cod_trabajo, descripcion, creado_en
    """
    with get_project_connection(user, password, schema) as cn:
        cur = cn.cursor()
        cur.execute("""
            SELECT
                p.id,
                p.codigo,
                COALESCE(p.codigo_ot, '')          AS ot,
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
    Retorna tupla con índices:
      0: id, 1: codigo, 2: descripcion, 3: estado, 4: codigo_ot,
      5: red_id, 6: tipo_trabajo_id, 7: cod_trabajo_id, 8: municipio_id,
      9: observaciones, 10: creado_en, 11: actualizado_en,
      12: titulo, 13: fecha_inicio, 14: fecha_fin, 15: fecha_prevista_fin,
      16: localizacion, 17: latitud, 18: longitud, 19: trabajadores,
      20: descripcion_corta, 21: descripcion_larga, 22: comarca_id, 23: id_municipio
    """
    with get_project_connection(user, password, schema) as cn:
        cur = cn.cursor()

        # Verificar qué columnas existen
        cur.execute(f"DESCRIBE {schema}.tbl_partes")
        columns = [row[0] for row in cur.fetchall()]

        # Construir SELECT dinámicamente - ORDEN IMPORTANTE para parts_manager_interfaz.py
        select_cols = ['id', 'codigo', 'descripcion', 'estado']

        # Añadir codigo_ot (la tabla usa codigo_ot en lugar de ot_id)
        if 'codigo_ot' in columns:
            select_cols.append('codigo_ot')
        elif 'ot_id' in columns:
            select_cols.append('ot_id')
        else:
            select_cols.append('NULL as codigo_ot')

        # Continuar con red, tipo, cod
        select_cols.extend(['red_id', 'tipo_trabajo_id', 'cod_trabajo_id'])

        # Añadir municipio_id
        if 'municipio_id' in columns:
            select_cols.append('municipio_id')
        else:
            select_cols.append('NULL as municipio_id')

        # Añadir observaciones
        if 'observaciones' in columns:
            select_cols.append('observaciones')
        else:
            select_cols.append('NULL as observaciones')

        # Fechas de auditoría
        select_cols.extend(['creado_en', 'actualizado_en'])

        # NUEVOS CAMPOS AMPLIADOS
        # Título
        if 'titulo' in columns:
            select_cols.append('titulo')
        else:
            select_cols.append('NULL as titulo')

        # Fechas del trabajo
        for col in ['fecha_inicio', 'fecha_fin', 'fecha_prevista_fin']:
            if col in columns:
                select_cols.append(col)
            else:
                select_cols.append(f'NULL as {col}')

        # Localización
        if 'localizacion' in columns:
            select_cols.append('localizacion')
        else:
            select_cols.append('NULL as localizacion')

        # Coordenadas GPS
        if 'latitud' in columns:
            select_cols.append('latitud')
        else:
            select_cols.append('NULL as latitud')

        if 'longitud' in columns:
            select_cols.append('longitud')
        else:
            select_cols.append('NULL as longitud')

        # Trabajadores
        if 'trabajadores' in columns:
            select_cols.append('trabajadores')
        else:
            select_cols.append('NULL as trabajadores')

        # Descripciones adicionales
        if 'descripcion_corta' in columns:
            select_cols.append('descripcion_corta')
        else:
            select_cols.append('NULL as descripcion_corta')

        if 'descripcion_larga' in columns:
            select_cols.append('descripcion_larga')
        else:
            select_cols.append('NULL as descripcion_larga')

        # Comarca (provincia)
        if 'comarca_id' in columns:
            select_cols.append('comarca_id')
        else:
            select_cols.append('NULL as comarca_id')

        # id_municipio (puede ser diferente de municipio_id)
        if 'id_municipio' in columns:
            select_cols.append('id_municipio')
        else:
            select_cols.append('NULL as id_municipio')

        query = f"SELECT {', '.join(select_cols)} FROM tbl_partes WHERE id = %s"
        cur.execute(query, (parte_id,))
        row = cur.fetchone()
        cur.close()
        return row


def mod_parte_item(user: str, password: str, schema: str, parte_id: int,
                   red_id: int, tipo_trabajo_id: int, cod_trabajo_id: int,
                   descripcion: str = None, estado: str = 'Pendiente', observaciones: str = None,
                   municipio_id: int = None,
                   titulo: str = None, fecha_fin=None, fecha_prevista_fin=None,
                   trabajadores: str = None, localizacion: str = None,
                   latitud: float = None, longitud: float = None):
    """
    Modifica los datos de un parte existente.
    Args:
        red_id, tipo_trabajo_id, cod_trabajo_id: IDs numéricos de dimensiones
        descripcion, estado, observaciones: Campos básicos
        municipio_id: ID del municipio
        titulo, trabajadores, localizacion: Campos de texto
        fecha_fin, fecha_prevista_fin: Fechas (date o str)
        latitud, longitud: Coordenadas GPS (float)

    Nota: codigo_ot y fecha_inicio NO se modifican (se asignan solo al crear)
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()

            # Verificar columnas disponibles
            cur.execute(f"DESCRIBE {schema}.tbl_partes")
            columns = [row[0] for row in cur.fetchall()]

            # Construir UPDATE dinámicamente
            set_clauses = [
                "red_id = %s",
                "tipo_trabajo_id = %s",
                "cod_trabajo_id = %s",
                "descripcion = %s",
                "estado = %s",
                "actualizado_en = NOW()"
            ]
            values = [red_id, tipo_trabajo_id, cod_trabajo_id, descripcion, estado]

            # Campos opcionales
            if 'observaciones' in columns:
                set_clauses.append("observaciones = %s")
                values.append(observaciones)

            if 'municipio_id' in columns:
                set_clauses.append("municipio_id = %s")
                values.append(municipio_id)

            if 'titulo' in columns:
                set_clauses.append("titulo = %s")
                values.append(titulo)

            if 'fecha_fin' in columns:
                set_clauses.append("fecha_fin = %s")
                values.append(fecha_fin)

            if 'fecha_prevista_fin' in columns:
                set_clauses.append("fecha_prevista_fin = %s")
                values.append(fecha_prevista_fin)

            if 'trabajadores' in columns:
                set_clauses.append("trabajadores = %s")
                values.append(trabajadores)

            if 'localizacion' in columns:
                set_clauses.append("localizacion = %s")
                values.append(localizacion)

            if 'latitud' in columns:
                set_clauses.append("latitud = %s")
                values.append(latitud)

            if 'longitud' in columns:
                set_clauses.append("longitud = %s")
                values.append(longitud)

            # Agregar parte_id al final
            values.append(parte_id)

            query = f"UPDATE tbl_partes SET {', '.join(set_clauses)} WHERE id = %s"
            cur.execute(query, tuple(values))

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
    Retorna: id, parte_id, codigo_parte, codigo_partida, resumen, unidad,
             cantidad_cert, precio_unit, coste_cert, fecha_certificacion,
             certificada, ot, red, tipo, cod_trabajo
    """
    with get_project_connection(user, password, schema) as cn:
        cur = cn.cursor()
        cur.execute("""
            SELECT id, parte_id, codigo_parte, codigo_partida, resumen, unidad,
                   cantidad_cert, precio_unit, coste_cert, fecha_certificacion,
                   certificada, ot, red, tipo, cod_trabajo
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
                       id_municipio: int = None,
                       trabajadores: str = None,
                       latitud: float = None,
                       longitud: float = None):
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
        trabajadores: Nombres de trabajadores (texto libre)
        latitud: Latitud GPS en grados decimales (WGS84, -90 a 90)
        longitud: Longitud GPS en grados decimales (WGS84, -180 a 180)

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

        if 'trabajadores' in columns and trabajadores:
            insert_cols.append('trabajadores')
            insert_vals.append(trabajadores)

        if 'latitud' in columns and latitud is not None:
            insert_cols.append('latitud')
            insert_vals.append(latitud)

        if 'longitud' in columns and longitud is not None:
            insert_cols.append('longitud')
            insert_vals.append(longitud)

        # Construir query
        placeholders = ', '.join(['%s'] * len(insert_vals))
        query = f"INSERT INTO tbl_partes ({', '.join(insert_cols)}) VALUES ({placeholders})"

        cur.execute(query, tuple(insert_vals))
        new_id = cur.lastrowid

        # Generar código con numeración independiente por prefijo
        prefix = _get_tipo_trabajo_prefix(user, password, schema, tipo_trabajo_id)

        # Obtener el siguiente número para este prefijo específico
        # Más robusto: maneja NULLs y códigos vacíos
        cur.execute("""
            SELECT COALESCE(
                MAX(
                    CAST(
                        REPLACE(codigo, %s, '') AS UNSIGNED
                    )
                ),
                0
            ) + 1
            FROM tbl_partes
            WHERE codigo IS NOT NULL
              AND codigo LIKE %s
        """, (prefix + '-', prefix + '-%'))
        next_num = int(cur.fetchone()[0])  # Convertir a int para evitar ValueError con Decimal

        codigo = f"{prefix}-{next_num:05d}"
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
                       id_municipio: int = None,
                       trabajadores: str = None,
                       latitud: float = None,
                       longitud: float = None):
    """
    Modifica un parte existente con los campos mejorados.
    Solo actualiza los campos que se pasan (los que son None se ignoran).

    Args:
        user: Usuario de BD
        password: Contraseña
        schema: Esquema del proyecto
        parte_id: ID del parte a modificar
        red_id: ID de red (FK)
        tipo_trabajo_id: ID de tipo de trabajo (FK)
        cod_trabajo_id: ID de código de trabajo (FK)
        titulo: Título descriptivo
        descripcion: Descripción original
        descripcion_larga: Descripción detallada
        descripcion_corta: Resumen breve
        fecha_inicio: Fecha de inicio (formato 'YYYY-MM-DD')
        fecha_fin: Fecha de finalización
        fecha_prevista_fin: Fecha prevista de finalización
        id_estado: ID del estado
        finalizada: Booleano de finalización
        localizacion: Ubicación textual
        id_municipio: ID del municipio (FK)
        trabajadores: Nombres de trabajadores (texto libre)
        latitud: Latitud GPS (WGS84, -90 a 90)
        longitud: Longitud GPS (WGS84, -180 a 180)

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

            if 'trabajadores' in columns and trabajadores is not None:
                update_parts.append('trabajadores = %s')
                update_vals.append(trabajadores)

            if 'latitud' in columns and latitud is not None:
                update_parts.append('latitud = %s')
                update_vals.append(latitud)

            if 'longitud' in columns and longitud is not None:
                update_parts.append('longitud = %s')
                update_vals.append(longitud)

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


# ==================== PROVINCIAS Y MUNICIPIOS ====================

def get_provincias(user: str, password: str, schema: str):
    """
    Obtiene lista de provincias en formato "id - nombre"

    Returns:
        list: Lista de strings formato "id - nombre"
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()
            cur.execute("""
                SELECT id, nombre
                FROM dim_provincias
                ORDER BY codigo
            """)
            rows = cur.fetchall()
            cur.close()
            return [f"{row[0]} - {row[1]}" for row in rows]
    except Exception as e:
        print(f"Error al obtener provincias: {e}")
        return []


def get_municipios_by_provincia(user: str, password: str, schema: str, provincia_id: int = None):
    """
    Obtiene lista de municipios filtrados por provincia

    Args:
        user: Usuario de BD
        password: Contraseña
        schema: Esquema del proyecto
        provincia_id: ID de provincia para filtrar (None = todos)

    Returns:
        list: Lista de strings formato "id - nombre"
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()

            # Detectar columna de nombre
            cur.execute(f"""
                SELECT COLUMN_NAME
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = %s
                AND TABLE_NAME = 'tbl_municipios'
                AND COLUMN_NAME IN ('nombre', 'municipio', 'descripcion', 'NAMEUNIT')
                ORDER BY FIELD(COLUMN_NAME, 'nombre', 'municipio', 'descripcion', 'NAMEUNIT')
                LIMIT 1
            """, (schema,))
            col_result = cur.fetchone()
            col_name = col_result[0] if col_result else 'id'

            # Construir query con filtro opcional
            if provincia_id:
                query = f"""
                    SELECT id, {col_name}
                    FROM tbl_municipios
                    WHERE provincia_id = %s
                    ORDER BY {col_name}
                """
                cur.execute(query, (provincia_id,))
            else:
                query = f"""
                    SELECT id, {col_name}
                    FROM tbl_municipios
                    ORDER BY {col_name}
                """
                cur.execute(query)

            rows = cur.fetchall()
            cur.close()
            return [f"{row[0]} - {row[1]}" for row in rows]
    except Exception as e:
        print(f"Error al obtener municipios: {e}")
        return []


# ==================== CATÁLOGOS FASE 3: TIPOS DE TRABAJO Y RED ====================

def get_categorias_trabajo(user: str, password: str, schema: str):
    """
    Obtiene lista de categorías de trabajo (Fugas, Atascos, Mantenimiento, etc.)

    Returns:
        list: Lista de diccionarios con keys: id, codigo, nombre, descripcion, orden
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()
            cur.execute("""
                SELECT id, codigo, nombre, descripcion, orden
                FROM tbl_categoria_trabajo
                WHERE activo = TRUE
                ORDER BY orden
            """)
            rows = cur.fetchall()
            cur.close()

            return [
                {
                    'id': row[0],
                    'codigo': row[1],
                    'nombre': row[2],
                    'descripcion': row[3],
                    'orden': row[4]
                }
                for row in rows
            ]
    except Exception as e:
        print(f"Error al obtener categorías de trabajo: {e}")
        return []


def get_tipos_trabajo_catalogo(user: str, password: str, schema: str, id_categoria: int = None):
    """
    Obtiene lista de tipos de trabajo del catálogo, opcionalmente filtrados por categoría

    Args:
        id_categoria: ID de categoría para filtrar (None = todos)

    Returns:
        list: Lista de diccionarios con información completa del tipo de trabajo
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()

            if id_categoria:
                query = """
                    SELECT ttc.id, ttc.codigo, ttc.nombre, ttc.descripcion,
                           ttc.id_categoria, cat.nombre AS categoria_nombre,
                           ttc.requiere_urgencia, ttc.tiempo_respuesta_max,
                           ttc.orden
                    FROM tbl_tipo_trabajo_catalogo ttc
                    INNER JOIN tbl_categoria_trabajo cat ON ttc.id_categoria = cat.id
                    WHERE ttc.activo = TRUE AND ttc.id_categoria = %s
                    ORDER BY ttc.orden
                """
                cur.execute(query, (id_categoria,))
            else:
                query = """
                    SELECT ttc.id, ttc.codigo, ttc.nombre, ttc.descripcion,
                           ttc.id_categoria, cat.nombre AS categoria_nombre,
                           ttc.requiere_urgencia, ttc.tiempo_respuesta_max,
                           ttc.orden
                    FROM tbl_tipo_trabajo_catalogo ttc
                    INNER JOIN tbl_categoria_trabajo cat ON ttc.id_categoria = cat.id
                    WHERE ttc.activo = TRUE
                    ORDER BY cat.orden, ttc.orden
                """
                cur.execute(query)

            rows = cur.fetchall()
            cur.close()

            return [
                {
                    'id': row[0],
                    'codigo': row[1],
                    'nombre': row[2],
                    'descripcion': row[3],
                    'id_categoria': row[4],
                    'categoria_nombre': row[5],
                    'requiere_urgencia': bool(row[6]),
                    'tiempo_respuesta_max': row[7],
                    'orden': row[8]
                }
                for row in rows
            ]
    except Exception as e:
        print(f"Error al obtener tipos de trabajo: {e}")
        return []


def get_tipos_trabajo_catalogo_simple(user: str, password: str, schema: str, id_categoria: int = None):
    """
    Obtiene lista de tipos de trabajo en formato "id - nombre" para combobox

    Args:
        id_categoria: ID de categoría para filtrar (None = todos)

    Returns:
        list: Lista de strings formato "id - nombre"
    """
    try:
        tipos = get_tipos_trabajo_catalogo(user, password, schema, id_categoria)
        return [f"{t['id']} - {t['nombre']}" for t in tipos]
    except Exception as e:
        print(f"Error: {e}")
        return []


def get_tipos_red(user: str, password: str, schema: str):
    """
    Obtiene lista de tipos de red (Distribución, Saneamiento, Depuración, etc.)

    Returns:
        list: Lista de diccionarios con keys: id, codigo, nombre, descripcion, color_hex, orden
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()
            cur.execute("""
                SELECT id, codigo, nombre, descripcion, color_hex, orden
                FROM tbl_tipo_red
                WHERE activo = TRUE
                ORDER BY orden
            """)
            rows = cur.fetchall()
            cur.close()

            return [
                {
                    'id': row[0],
                    'codigo': row[1],
                    'nombre': row[2],
                    'descripcion': row[3],
                    'color_hex': row[4],
                    'orden': row[5]
                }
                for row in rows
            ]
    except Exception as e:
        print(f"Error al obtener tipos de red: {e}")
        return []


def get_tipos_red_simple(user: str, password: str, schema: str):
    """
    Obtiene lista de tipos de red en formato "id - nombre" para combobox

    Returns:
        list: Lista de strings formato "id - nombre"
    """
    try:
        tipos = get_tipos_red(user, password, schema)
        return [f"{t['id']} - {t['nombre']}" for t in tipos]
    except Exception as e:
        print(f"Error: {e}")
        return []


def get_trabajo_by_codigo(user: str, password: str, schema: str, codigo: str):
    """
    Obtiene información de un tipo de trabajo por su código

    Args:
        codigo: Código del tipo de trabajo (ej: 'REP_FUG_COND')

    Returns:
        dict or None: Diccionario con información del tipo de trabajo o None si no existe
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()
            cur.execute("""
                SELECT ttc.id, ttc.codigo, ttc.nombre, ttc.descripcion,
                       ttc.id_categoria, cat.nombre AS categoria_nombre,
                       ttc.requiere_urgencia, ttc.tiempo_respuesta_max
                FROM tbl_tipo_trabajo_catalogo ttc
                INNER JOIN tbl_categoria_trabajo cat ON ttc.id_categoria = cat.id
                WHERE ttc.codigo = %s AND ttc.activo = TRUE
            """, (codigo,))

            row = cur.fetchone()
            cur.close()

            if row:
                return {
                    'id': row[0],
                    'codigo': row[1],
                    'nombre': row[2],
                    'descripcion': row[3],
                    'id_categoria': row[4],
                    'categoria_nombre': row[5],
                    'requiere_urgencia': bool(row[6]),
                    'tiempo_respuesta_max': row[7]
                }
            return None
    except Exception as e:
        print(f"Error al buscar tipo de trabajo: {e}")
        return None


def get_estadisticas_por_categoria(user: str, password: str, schema: str, fecha_desde: str = None, fecha_hasta: str = None):
    """
    Obtiene estadísticas de partes agrupadas por categoría de trabajo

    Args:
        fecha_desde: Fecha inicio en formato 'YYYY-MM-DD' (None = sin filtro)
        fecha_hasta: Fecha fin en formato 'YYYY-MM-DD' (None = sin filtro)

    Returns:
        list: Lista de diccionarios con estadísticas por categoría
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()

            # Construir query con filtros opcionales
            where_clauses = ["ttc.activo = TRUE"]
            params = []

            if fecha_desde:
                where_clauses.append("p.fecha_inicio >= %s")
                params.append(fecha_desde)

            if fecha_hasta:
                where_clauses.append("p.fecha_inicio <= %s")
                params.append(fecha_hasta)

            where_sql = " AND ".join(where_clauses)

            query = f"""
                SELECT
                    cat.id,
                    cat.codigo,
                    cat.nombre AS categoria,
                    COUNT(DISTINCT p.id) AS total_partes,
                    SUM(CASE WHEN p.finalizada = TRUE THEN 1 ELSE 0 END) AS partes_finalizadas,
                    SUM(CASE WHEN p.id_estado = 1 THEN 1 ELSE 0 END) AS partes_pendientes,
                    SUM(CASE WHEN p.id_estado = 2 THEN 1 ELSE 0 END) AS partes_en_curso,
                    COUNT(DISTINCT ttc.id) AS tipos_usados
                FROM tbl_categoria_trabajo cat
                LEFT JOIN tbl_tipo_trabajo_catalogo ttc ON cat.id = ttc.id_categoria AND ttc.activo = TRUE
                LEFT JOIN dim_tipo_trabajo dt ON ttc.id = dt.id_tipo_catalogo
                LEFT JOIN tbl_partes p ON dt.id = p.tipo_trabajo_id
                WHERE {where_sql}
                GROUP BY cat.id, cat.codigo, cat.nombre
                ORDER BY cat.orden
            """

            cur.execute(query, tuple(params))
            rows = cur.fetchall()
            cur.close()

            return [
                {
                    'id': row[0],
                    'codigo': row[1],
                    'categoria': row[2],
                    'total_partes': row[3] or 0,
                    'partes_finalizadas': row[4] or 0,
                    'partes_pendientes': row[5] or 0,
                    'partes_en_curso': row[6] or 0,
                    'tipos_usados': row[7] or 0
                }
                for row in rows
            ]
    except Exception as e:
        print(f"Error al obtener estadísticas: {e}")
        return []


def get_estadisticas_por_tipo_red(user: str, password: str, schema: str, fecha_desde: str = None, fecha_hasta: str = None):
    """
    Obtiene estadísticas de partes agrupadas por tipo de red

    Args:
        fecha_desde: Fecha inicio en formato 'YYYY-MM-DD' (None = sin filtro)
        fecha_hasta: Fecha fin en formato 'YYYY-MM-DD' (None = sin filtro)

    Returns:
        list: Lista de diccionarios con estadísticas por tipo de red
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()

            # Construir query con filtros opcionales
            where_clauses = ["tr.activo = TRUE"]
            params = []

            if fecha_desde:
                where_clauses.append("p.fecha_inicio >= %s")
                params.append(fecha_desde)

            if fecha_hasta:
                where_clauses.append("p.fecha_inicio <= %s")
                params.append(fecha_hasta)

            where_sql = " AND ".join(where_clauses)

            query = f"""
                SELECT
                    tr.id,
                    tr.codigo,
                    tr.nombre AS tipo_red,
                    COUNT(DISTINCT p.id) AS total_partes,
                    SUM(CASE WHEN p.finalizada = TRUE THEN 1 ELSE 0 END) AS partes_finalizadas,
                    SUM(CASE WHEN p.id_estado = 1 THEN 1 ELSE 0 END) AS partes_pendientes,
                    SUM(CASE WHEN p.id_estado = 2 THEN 1 ELSE 0 END) AS partes_en_curso
                FROM tbl_tipo_red tr
                LEFT JOIN dim_red dr ON tr.id = dr.id_tipo_red
                LEFT JOIN tbl_partes p ON dr.id = p.red_id
                WHERE {where_sql}
                GROUP BY tr.id, tr.codigo, tr.nombre
                ORDER BY tr.orden
            """

            cur.execute(query, tuple(params))
            rows = cur.fetchall()
            cur.close()

            return [
                {
                    'id': row[0],
                    'codigo': row[1],
                    'tipo_red': row[2],
                    'total_partes': row[3] or 0,
                    'partes_finalizadas': row[4] or 0,
                    'partes_pendientes': row[5] or 0,
                    'partes_en_curso': row[6] or 0
                }
                for row in rows
            ]
    except Exception as e:
        print(f"Error al obtener estadísticas por tipo de red: {e}")
        return []
