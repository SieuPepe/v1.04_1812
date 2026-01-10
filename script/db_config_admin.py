"""
Módulo de funciones CRUD para la configuración del sistema.
Gestiona tablas de dimensiones y catálogo de partidas.
"""

from script.db_connector import get_project_connection


# =============================================================================
# FUNCIONES GENÉRICAS PARA TABLAS DE DIMENSIONES
# =============================================================================

def get_dimension_columns(user: str, password: str, schema: str, table_name: str) -> dict:
    """
    Detecta las columnas disponibles en una tabla de dimensiones.

    Returns:
        dict con las columnas encontradas: {'id': 'id', 'codigo': 'codigo'|None, 'descripcion': 'descripcion', 'activo': 'activo'|None}
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()
            cur.execute(f"""
                SELECT COLUMN_NAME FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
            """, (schema, table_name))
            columns = [row[0].lower() for row in cur.fetchall()]
            cur.close()

            result = {'id': 'id'}

            # Detectar columna de código
            for col in ['codigo', 'cod', 'code']:
                if col in columns:
                    result['codigo'] = col
                    break
            else:
                result['codigo'] = None

            # Detectar columna de descripción
            for col in ['descripcion', 'nombre', 'description', 'desc']:
                if col in columns:
                    result['descripcion'] = col
                    break
            else:
                result['descripcion'] = columns[1] if len(columns) > 1 else None

            # Detectar columna activo
            result['activo'] = 'activo' if 'activo' in columns else None

            return result
    except Exception as e:
        print(f"Error detectando columnas de {table_name}: {e}")
        return {'id': 'id', 'codigo': 'codigo', 'descripcion': 'descripcion', 'activo': 'activo'}


def get_dimension_records(user: str, password: str, schema: str, table_name: str) -> list:
    """
    Obtiene todos los registros de una tabla de dimensiones.
    """
    valid_tables = ['dim_red', 'dim_tipos_rep', 'dim_codigo_trabajo']
    if table_name not in valid_tables:
        raise ValueError(f"Tabla no válida: {table_name}")

    try:
        # Detectar columnas disponibles
        cols = get_dimension_columns(user, password, schema, table_name)

        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()

            # Construir query dinámicamente
            select_cols = ['id']
            if cols['codigo']:
                select_cols.append(cols['codigo'])
            else:
                select_cols.append("'' as codigo")

            select_cols.append(cols['descripcion'] if cols['descripcion'] else "'' as descripcion")

            if cols['activo']:
                select_cols.append(cols['activo'])
            else:
                select_cols.append("1 as activo")

            query = f"SELECT {', '.join(select_cols)} FROM {schema}.{table_name} ORDER BY id ASC"
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()
            return rows
    except Exception as e:
        print(f"Error al obtener registros de {table_name}: {e}")
        import traceback
        traceback.print_exc()
        return []


def add_dimension_record(user: str, password: str, schema: str, table_name: str,
                         codigo: str, descripcion: str) -> dict:
    """Añade un nuevo registro a una tabla de dimensiones."""
    valid_tables = ['dim_red', 'dim_tipos_rep', 'dim_codigo_trabajo']
    if table_name not in valid_tables:
        return {'success': False, 'message': f"Tabla no válida: {table_name}", 'id': None}

    try:
        cols = get_dimension_columns(user, password, schema, table_name)

        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()

            # Verificar si ya existe el código (si la tabla tiene columna codigo)
            if cols['codigo']:
                cur.execute(f"SELECT id FROM {schema}.{table_name} WHERE {cols['codigo']} = %s", (codigo,))
                if cur.fetchone():
                    cur.close()
                    return {'success': False, 'message': f"Ya existe un registro con el código '{codigo}'", 'id': None}

            # Construir INSERT dinámicamente
            insert_cols = []
            insert_vals = []

            if cols['codigo']:
                insert_cols.append(cols['codigo'])
                insert_vals.append(codigo)

            if cols['descripcion']:
                insert_cols.append(cols['descripcion'])
                insert_vals.append(descripcion)

            if cols['activo']:
                insert_cols.append(cols['activo'])
                insert_vals.append(1)

            placeholders = ', '.join(['%s'] * len(insert_vals))
            query = f"INSERT INTO {schema}.{table_name} ({', '.join(insert_cols)}) VALUES ({placeholders})"

            cur.execute(query, insert_vals)
            cn.commit()
            new_id = cur.lastrowid
            cur.close()

            return {'success': True, 'message': 'Registro añadido correctamente', 'id': new_id}
    except Exception as e:
        return {'success': False, 'message': f"Error al añadir registro: {e}", 'id': None}


def update_dimension_record(user: str, password: str, schema: str, table_name: str,
                            record_id: int, codigo: str, descripcion: str, activo: int) -> dict:
    """Actualiza un registro existente en una tabla de dimensiones."""
    valid_tables = ['dim_red', 'dim_tipos_rep', 'dim_codigo_trabajo']
    if table_name not in valid_tables:
        return {'success': False, 'message': f"Tabla no válida: {table_name}"}

    try:
        cols = get_dimension_columns(user, password, schema, table_name)

        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()

            # Verificar duplicado de código
            if cols['codigo']:
                cur.execute(f"SELECT id FROM {schema}.{table_name} WHERE {cols['codigo']} = %s AND id != %s",
                           (codigo, record_id))
                if cur.fetchone():
                    cur.close()
                    return {'success': False, 'message': f"Ya existe otro registro con el código '{codigo}'"}

            # Construir UPDATE dinámicamente
            set_parts = []
            set_vals = []

            if cols['codigo']:
                set_parts.append(f"{cols['codigo']} = %s")
                set_vals.append(codigo)

            if cols['descripcion']:
                set_parts.append(f"{cols['descripcion']} = %s")
                set_vals.append(descripcion)

            if cols['activo']:
                set_parts.append(f"{cols['activo']} = %s")
                set_vals.append(activo)

            set_vals.append(record_id)
            query = f"UPDATE {schema}.{table_name} SET {', '.join(set_parts)} WHERE id = %s"

            cur.execute(query, set_vals)
            cn.commit()
            cur.close()

            return {'success': True, 'message': 'Registro actualizado correctamente'}
    except Exception as e:
        return {'success': False, 'message': f"Error al actualizar registro: {e}"}


def delete_dimension_record(user: str, password: str, schema: str, table_name: str,
                            record_id: int) -> dict:
    """Elimina un registro de una tabla de dimensiones."""
    valid_tables = ['dim_red', 'dim_tipos_rep', 'dim_codigo_trabajo']
    if table_name not in valid_tables:
        return {'success': False, 'message': f"Tabla no válida: {table_name}"}

    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()

            # Verificar si el registro está siendo usado
            if table_name == 'dim_red':
                cur.execute(f"SELECT COUNT(*) FROM {schema}.tbl_partes WHERE red_id = %s", (record_id,))
                count = cur.fetchone()[0]
                if count > 0:
                    cur.close()
                    return {'success': False, 'message': f"No se puede eliminar: {count} partes usan esta red"}

            elif table_name == 'dim_tipos_rep':
                cur.execute(f"SELECT COUNT(*) FROM {schema}.tbl_partes WHERE tipo_rep_id = %s", (record_id,))
                count = cur.fetchone()[0]
                if count > 0:
                    cur.close()
                    return {'success': False, 'message': f"No se puede eliminar: {count} partes usan este tipo"}

            elif table_name == 'dim_codigo_trabajo':
                cur.execute(f"SELECT COUNT(*) FROM {schema}.tbl_partes WHERE cod_trabajo_id = %s", (record_id,))
                count = cur.fetchone()[0]
                if count > 0:
                    cur.close()
                    return {'success': False, 'message': f"No se puede eliminar: {count} partes usan este código"}

            cur.execute(f"DELETE FROM {schema}.{table_name} WHERE id = %s", (record_id,))
            cn.commit()
            cur.close()

            return {'success': True, 'message': 'Registro eliminado correctamente'}
    except Exception as e:
        return {'success': False, 'message': f"Error al eliminar registro: {e}"}


def toggle_dimension_active(user: str, password: str, schema: str, table_name: str,
                            record_id: int) -> dict:
    """Alterna el estado activo/inactivo de un registro."""
    valid_tables = ['dim_red', 'dim_tipos_rep', 'dim_codigo_trabajo']
    if table_name not in valid_tables:
        return {'success': False, 'message': f"Tabla no válida: {table_name}", 'new_state': None}

    try:
        cols = get_dimension_columns(user, password, schema, table_name)

        if not cols['activo']:
            return {'success': False, 'message': 'Esta tabla no tiene columna activo', 'new_state': None}

        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()

            cur.execute(f"SELECT {cols['activo']} FROM {schema}.{table_name} WHERE id = %s", (record_id,))
            result = cur.fetchone()
            if not result:
                cur.close()
                return {'success': False, 'message': 'Registro no encontrado', 'new_state': None}

            new_state = 0 if result[0] == 1 else 1
            cur.execute(f"UPDATE {schema}.{table_name} SET {cols['activo']} = %s WHERE id = %s", (new_state, record_id))
            cn.commit()
            cur.close()

            estado_texto = "activado" if new_state == 1 else "desactivado"
            return {'success': True, 'message': f'Registro {estado_texto}', 'new_state': new_state}
    except Exception as e:
        return {'success': False, 'message': f"Error al cambiar estado: {e}", 'new_state': None}


# =============================================================================
# FUNCIONES PARA CATÁLOGO DE PARTIDAS (tbl_pres_capitulos + tbl_pres_precios)
# =============================================================================

def get_catalogo_capitulos(user: str, password: str, schema: str) -> list:
    """
    Obtiene los capítulos del catálogo (tbl_pres_capitulos).

    Returns:
        list: Lista de tuplas (id, codigo_capitulo, capitulo)
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()
            cur.execute(f"""
                SELECT id, codigo_capitulo, capitulo
                FROM {schema}.tbl_pres_capitulos
                ORDER BY codigo_capitulo
            """)
            rows = cur.fetchall()
            cur.close()
            return rows
    except Exception as e:
        print(f"Error al obtener capítulos: {e}")
        return []


def get_catalogo_partidas(user: str, password: str, schema: str,
                          capitulo_id: int = None, search_text: str = None) -> list:
    """
    Obtiene partidas del catálogo (tbl_pres_precios) con filtros opcionales.
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()

            query = f"""
                SELECT p.id, p.codigo, p.resumen, p.coste,
                       c.codigo_capitulo, c.capitulo,
                       COALESCE(u.unidad, '') as unidad
                FROM {schema}.tbl_pres_precios p
                LEFT JOIN {schema}.tbl_pres_capitulos c ON p.id_capitulo = c.id
                LEFT JOIN {schema}.tbl_pres_unidades u ON p.id_unidades = u.id
                WHERE 1=1
            """
            params = []

            if capitulo_id:
                query += " AND p.id_capitulo = %s"
                params.append(capitulo_id)

            if search_text:
                query += " AND (p.codigo LIKE %s OR p.resumen LIKE %s)"
                params.extend([f"%{search_text}%", f"%{search_text}%"])

            query += " ORDER BY c.codigo_capitulo, p.codigo"

            cur.execute(query, params)
            rows = cur.fetchall()
            cur.close()
            return rows

    except Exception as e:
        print(f"Error al obtener catálogo: {e}")
        import traceback
        traceback.print_exc()
        return []


def add_catalogo_partida(user: str, password: str, schema: str,
                         codigo: str, resumen: str, coste: float,
                         capitulo_id: int, unidad_id: int = None) -> dict:
    """Añade una nueva partida al catálogo."""
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()

            # Verificar si ya existe el código
            cur.execute(f"SELECT id FROM {schema}.tbl_pres_precios WHERE codigo = %s", (codigo,))
            if cur.fetchone():
                cur.close()
                return {'success': False, 'message': f"Ya existe una partida con el código '{codigo}'", 'id': None}

            cur.execute(f"""
                INSERT INTO {schema}.tbl_pres_precios
                (codigo, resumen, coste, id_capitulo, id_unidades)
                VALUES (%s, %s, %s, %s, %s)
            """, (codigo, resumen, coste, capitulo_id, unidad_id))
            cn.commit()
            new_id = cur.lastrowid
            cur.close()
            return {'success': True, 'message': 'Partida añadida correctamente', 'id': new_id}

    except Exception as e:
        return {'success': False, 'message': f"Error al añadir partida: {e}", 'id': None}


def update_catalogo_partida(user: str, password: str, schema: str,
                            partida_id: int, codigo: str, resumen: str,
                            coste: float) -> dict:
    """Actualiza una partida existente del catálogo."""
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()

            # Verificar duplicado de código
            cur.execute(f"""
                SELECT id FROM {schema}.tbl_pres_precios
                WHERE codigo = %s AND id != %s
            """, (codigo, partida_id))
            if cur.fetchone():
                cur.close()
                return {'success': False, 'message': f"Ya existe otra partida con el código '{codigo}'"}

            cur.execute(f"""
                UPDATE {schema}.tbl_pres_precios
                SET codigo = %s, resumen = %s, coste = %s
                WHERE id = %s
            """, (codigo, resumen, coste, partida_id))
            cn.commit()
            cur.close()

            return {'success': True, 'message': 'Partida actualizada correctamente'}
    except Exception as e:
        return {'success': False, 'message': f"Error al actualizar partida: {e}"}


def delete_catalogo_partida(user: str, password: str, schema: str, partida_id: int) -> dict:
    """Elimina una partida del catálogo."""
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()

            # Verificar si la partida está siendo usada en presupuestos
            cur.execute(f"""
                SELECT COUNT(*) FROM {schema}.tbl_parte_presupuesto
                WHERE partida_id = %s
            """, (partida_id,))
            count = cur.fetchone()[0]
            if count > 0:
                cur.close()
                return {'success': False, 'message': f"No se puede eliminar: la partida está usada en {count} presupuestos"}

            cur.execute(f"DELETE FROM {schema}.tbl_pres_precios WHERE id = %s", (partida_id,))
            cn.commit()
            cur.close()

            return {'success': True, 'message': 'Partida eliminada correctamente'}
    except Exception as e:
        return {'success': False, 'message': f"Error al eliminar partida: {e}"}


# =============================================================================
# FUNCIONES DE VALIDACIÓN DE FORMATO
# =============================================================================

def validar_codigo_dimension(codigo: str, table_name: str) -> str:
    """Valida y formatea el código según la tabla de destino."""
    codigo = codigo.strip()
    if table_name == 'dim_red':
        return codigo.upper()[:10]
    elif table_name == 'dim_tipos_rep':
        return codigo.upper()[:20]
    elif table_name == 'dim_codigo_trabajo':
        return codigo.upper()[:50]
    return codigo


def validar_descripcion(descripcion: str) -> str:
    """Valida y formatea la descripción."""
    descripcion = descripcion.strip()
    if descripcion:
        return descripcion[0].upper() + descripcion[1:] if len(descripcion) > 1 else descripcion.upper()
    return descripcion


def validar_precio(precio_str: str) -> tuple:
    """Valida y formatea el precio."""
    try:
        precio_str = precio_str.replace(',', '.').strip()
        precio = float(precio_str)
        if precio < 0:
            return (False, 0.0, "El precio no puede ser negativo")
        return (True, round(precio, 2), "")
    except ValueError:
        return (False, 0.0, "El precio debe ser un número válido")
