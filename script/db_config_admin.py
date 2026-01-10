"""
Módulo de funciones CRUD para la configuración del sistema.
Gestiona tablas de dimensiones y catálogo de partidas.
"""

from script.db_connector import get_project_connection


# =============================================================================
# FUNCIONES GENÉRICAS PARA TABLAS DE DIMENSIONES
# =============================================================================

def get_dimension_records(user: str, password: str, schema: str, table_name: str) -> list:
    """
    Obtiene todos los registros de una tabla de dimensiones.

    Args:
        user: Usuario de BD
        password: Contraseña
        schema: Esquema del proyecto
        table_name: Nombre de la tabla (dim_red, dim_tipos_rep, dim_codigo_trabajo)

    Returns:
        list: Lista de tuplas (id, codigo, descripcion, activo)
    """
    # Validar nombre de tabla para evitar SQL injection
    valid_tables = ['dim_red', 'dim_tipos_rep', 'dim_codigo_trabajo']
    if table_name not in valid_tables:
        raise ValueError(f"Tabla no válida: {table_name}")

    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()
            cur.execute(f"""
                SELECT id, codigo, descripcion, activo
                FROM {schema}.{table_name}
                ORDER BY id ASC
            """)
            rows = cur.fetchall()
            cur.close()
            return rows
    except Exception as e:
        print(f"Error al obtener registros de {table_name}: {e}")
        return []


def add_dimension_record(user: str, password: str, schema: str, table_name: str,
                         codigo: str, descripcion: str) -> dict:
    """
    Añade un nuevo registro a una tabla de dimensiones.

    Args:
        user: Usuario de BD
        password: Contraseña
        schema: Esquema del proyecto
        table_name: Nombre de la tabla
        codigo: Código del registro
        descripcion: Descripción del registro

    Returns:
        dict: {'success': bool, 'message': str, 'id': int|None}
    """
    valid_tables = ['dim_red', 'dim_tipos_rep', 'dim_codigo_trabajo']
    if table_name not in valid_tables:
        return {'success': False, 'message': f"Tabla no válida: {table_name}", 'id': None}

    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()

            # Verificar si ya existe el código
            cur.execute(f"""
                SELECT id FROM {schema}.{table_name} WHERE codigo = %s
            """, (codigo,))
            if cur.fetchone():
                cur.close()
                return {'success': False, 'message': f"Ya existe un registro con el código '{codigo}'", 'id': None}

            # Insertar nuevo registro
            cur.execute(f"""
                INSERT INTO {schema}.{table_name} (codigo, descripcion, activo)
                VALUES (%s, %s, 1)
            """, (codigo, descripcion))
            cn.commit()
            new_id = cur.lastrowid
            cur.close()

            return {'success': True, 'message': 'Registro añadido correctamente', 'id': new_id}
    except Exception as e:
        return {'success': False, 'message': f"Error al añadir registro: {e}", 'id': None}


def update_dimension_record(user: str, password: str, schema: str, table_name: str,
                            record_id: int, codigo: str, descripcion: str, activo: int) -> dict:
    """
    Actualiza un registro existente en una tabla de dimensiones.

    Args:
        user: Usuario de BD
        password: Contraseña
        schema: Esquema del proyecto
        table_name: Nombre de la tabla
        record_id: ID del registro a actualizar
        codigo: Nuevo código
        descripcion: Nueva descripción
        activo: Estado activo (1) o inactivo (0)

    Returns:
        dict: {'success': bool, 'message': str}
    """
    valid_tables = ['dim_red', 'dim_tipos_rep', 'dim_codigo_trabajo']
    if table_name not in valid_tables:
        return {'success': False, 'message': f"Tabla no válida: {table_name}"}

    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()

            # Verificar si el código ya existe en otro registro
            cur.execute(f"""
                SELECT id FROM {schema}.{table_name} WHERE codigo = %s AND id != %s
            """, (codigo, record_id))
            if cur.fetchone():
                cur.close()
                return {'success': False, 'message': f"Ya existe otro registro con el código '{codigo}'"}

            # Actualizar registro
            cur.execute(f"""
                UPDATE {schema}.{table_name}
                SET codigo = %s, descripcion = %s, activo = %s
                WHERE id = %s
            """, (codigo, descripcion, activo, record_id))
            cn.commit()
            cur.close()

            return {'success': True, 'message': 'Registro actualizado correctamente'}
    except Exception as e:
        return {'success': False, 'message': f"Error al actualizar registro: {e}"}


def delete_dimension_record(user: str, password: str, schema: str, table_name: str,
                            record_id: int) -> dict:
    """
    Elimina un registro de una tabla de dimensiones.

    Args:
        user: Usuario de BD
        password: Contraseña
        schema: Esquema del proyecto
        table_name: Nombre de la tabla
        record_id: ID del registro a eliminar

    Returns:
        dict: {'success': bool, 'message': str}
    """
    valid_tables = ['dim_red', 'dim_tipos_rep', 'dim_codigo_trabajo']
    if table_name not in valid_tables:
        return {'success': False, 'message': f"Tabla no válida: {table_name}"}

    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()

            # Verificar si el registro está siendo usado
            # Para dim_red, verificar en tbl_partes
            if table_name == 'dim_red':
                cur.execute(f"SELECT COUNT(*) FROM {schema}.tbl_partes WHERE red_id = %s", (record_id,))
                count = cur.fetchone()[0]
                if count > 0:
                    cur.close()
                    return {'success': False, 'message': f"No se puede eliminar: {count} partes usan esta red"}

            # Para dim_tipos_rep, verificar en tbl_partes
            elif table_name == 'dim_tipos_rep':
                cur.execute(f"SELECT COUNT(*) FROM {schema}.tbl_partes WHERE tipo_rep_id = %s", (record_id,))
                count = cur.fetchone()[0]
                if count > 0:
                    cur.close()
                    return {'success': False, 'message': f"No se puede eliminar: {count} partes usan este tipo"}

            # Para dim_codigo_trabajo, verificar en tbl_partes
            elif table_name == 'dim_codigo_trabajo':
                cur.execute(f"SELECT COUNT(*) FROM {schema}.tbl_partes WHERE cod_trabajo_id = %s", (record_id,))
                count = cur.fetchone()[0]
                if count > 0:
                    cur.close()
                    return {'success': False, 'message': f"No se puede eliminar: {count} partes usan este código"}

            # Eliminar registro
            cur.execute(f"DELETE FROM {schema}.{table_name} WHERE id = %s", (record_id,))
            cn.commit()
            cur.close()

            return {'success': True, 'message': 'Registro eliminado correctamente'}
    except Exception as e:
        return {'success': False, 'message': f"Error al eliminar registro: {e}"}


def toggle_dimension_active(user: str, password: str, schema: str, table_name: str,
                            record_id: int) -> dict:
    """
    Alterna el estado activo/inactivo de un registro.

    Args:
        user: Usuario de BD
        password: Contraseña
        schema: Esquema del proyecto
        table_name: Nombre de la tabla
        record_id: ID del registro

    Returns:
        dict: {'success': bool, 'message': str, 'new_state': int|None}
    """
    valid_tables = ['dim_red', 'dim_tipos_rep', 'dim_codigo_trabajo']
    if table_name not in valid_tables:
        return {'success': False, 'message': f"Tabla no válida: {table_name}", 'new_state': None}

    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()

            # Obtener estado actual
            cur.execute(f"SELECT activo FROM {schema}.{table_name} WHERE id = %s", (record_id,))
            result = cur.fetchone()
            if not result:
                cur.close()
                return {'success': False, 'message': 'Registro no encontrado', 'new_state': None}

            new_state = 0 if result[0] == 1 else 1

            # Actualizar estado
            cur.execute(f"UPDATE {schema}.{table_name} SET activo = %s WHERE id = %s", (new_state, record_id))
            cn.commit()
            cur.close()

            estado_texto = "activado" if new_state == 1 else "desactivado"
            return {'success': True, 'message': f'Registro {estado_texto}', 'new_state': new_state}
    except Exception as e:
        return {'success': False, 'message': f"Error al cambiar estado: {e}", 'new_state': None}


# =============================================================================
# FUNCIONES PARA CATÁLOGO DE PARTIDAS
# =============================================================================

def get_catalogo_partidas(user: str, password: str, schema: str,
                          familia_id: int = None, tipo_id: int = None,
                          search_text: str = None) -> list:
    """
    Obtiene partidas del catálogo con filtros opcionales.

    Args:
        user: Usuario de BD
        password: Contraseña
        schema: Esquema del proyecto
        familia_id: ID de familia para filtrar (opcional)
        tipo_id: ID de tipo para filtrar (opcional)
        search_text: Texto para buscar en código/descripción (opcional)

    Returns:
        list: Lista de tuplas con datos de partidas
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()

            # Verificar si existe la tabla de catálogo
            cur.execute(f"""
                SELECT COUNT(*) FROM information_schema.tables
                WHERE table_schema = %s AND table_name = 'tbl_catalogo'
            """, (schema,))

            if cur.fetchone()[0] == 0:
                # Intentar con tabla alternativa
                cur.execute(f"""
                    SELECT COUNT(*) FROM information_schema.tables
                    WHERE table_schema = %s AND table_name = 'tbl_cata_hidra_tipo'
                """, (schema,))

                if cur.fetchone()[0] == 0:
                    cur.close()
                    return []

                # Usar catálogo hidráulico
                query = f"""
                    SELECT t.id, t.codigo, t.descripcion,
                           COALESCE(t.precio, 0) as precio,
                           f.descripcion as familia,
                           t.activo
                    FROM {schema}.tbl_cata_hidra_tipo t
                    LEFT JOIN {schema}.tbl_cata_hidra_familia f ON t.familia_id = f.id
                    WHERE 1=1
                """
                params = []

                if familia_id:
                    query += " AND t.familia_id = %s"
                    params.append(familia_id)

                if search_text:
                    query += " AND (t.codigo LIKE %s OR t.descripcion LIKE %s)"
                    params.extend([f"%{search_text}%", f"%{search_text}%"])

                query += " ORDER BY f.descripcion, t.codigo"

                cur.execute(query, params)
                rows = cur.fetchall()
                cur.close()
                return rows

            # Usar tbl_catalogo si existe
            query = f"""
                SELECT id, codigo, descripcion, precio, categoria, activo
                FROM {schema}.tbl_catalogo
                WHERE 1=1
            """
            params = []

            if search_text:
                query += " AND (codigo LIKE %s OR descripcion LIKE %s)"
                params.extend([f"%{search_text}%", f"%{search_text}%"])

            query += " ORDER BY codigo"

            cur.execute(query, params)
            rows = cur.fetchall()
            cur.close()
            return rows

    except Exception as e:
        print(f"Error al obtener catálogo: {e}")
        return []


def get_catalogo_familias(user: str, password: str, schema: str) -> list:
    """
    Obtiene las familias del catálogo hidráulico.

    Returns:
        list: Lista de tuplas (id, descripcion)
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()
            cur.execute(f"""
                SELECT id, descripcion FROM {schema}.tbl_cata_hidra_familia
                ORDER BY descripcion
            """)
            rows = cur.fetchall()
            cur.close()
            return rows
    except Exception as e:
        print(f"Error al obtener familias: {e}")
        return []


def add_catalogo_partida(user: str, password: str, schema: str,
                         codigo: str, descripcion: str, precio: float,
                         familia_id: int = None, unidad: str = 'ud') -> dict:
    """
    Añade una nueva partida al catálogo.

    Returns:
        dict: {'success': bool, 'message': str, 'id': int|None}
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()

            # Verificar si existe tbl_cata_hidra_tipo
            cur.execute(f"""
                SELECT COUNT(*) FROM information_schema.tables
                WHERE table_schema = %s AND table_name = 'tbl_cata_hidra_tipo'
            """, (schema,))

            if cur.fetchone()[0] > 0:
                # Usar catálogo hidráulico
                cur.execute(f"""
                    SELECT id FROM {schema}.tbl_cata_hidra_tipo WHERE codigo = %s
                """, (codigo,))
                if cur.fetchone():
                    cur.close()
                    return {'success': False, 'message': f"Ya existe una partida con el código '{codigo}'", 'id': None}

                cur.execute(f"""
                    INSERT INTO {schema}.tbl_cata_hidra_tipo
                    (codigo, descripcion, precio, familia_id, unidad, activo)
                    VALUES (%s, %s, %s, %s, %s, 1)
                """, (codigo, descripcion, precio, familia_id, unidad))
                cn.commit()
                new_id = cur.lastrowid
                cur.close()
                return {'success': True, 'message': 'Partida añadida correctamente', 'id': new_id}

            cur.close()
            return {'success': False, 'message': 'No se encontró tabla de catálogo', 'id': None}

    except Exception as e:
        return {'success': False, 'message': f"Error al añadir partida: {e}", 'id': None}


def update_catalogo_partida(user: str, password: str, schema: str,
                            partida_id: int, codigo: str, descripcion: str,
                            precio: float, activo: int = 1) -> dict:
    """
    Actualiza una partida existente del catálogo.

    Returns:
        dict: {'success': bool, 'message': str}
    """
    try:
        with get_project_connection(user, password, schema) as cn:
            cur = cn.cursor()

            # Verificar si el código ya existe en otra partida
            cur.execute(f"""
                SELECT id FROM {schema}.tbl_cata_hidra_tipo
                WHERE codigo = %s AND id != %s
            """, (codigo, partida_id))
            if cur.fetchone():
                cur.close()
                return {'success': False, 'message': f"Ya existe otra partida con el código '{codigo}'"}

            cur.execute(f"""
                UPDATE {schema}.tbl_cata_hidra_tipo
                SET codigo = %s, descripcion = %s, precio = %s, activo = %s
                WHERE id = %s
            """, (codigo, descripcion, precio, activo, partida_id))
            cn.commit()
            cur.close()

            return {'success': True, 'message': 'Partida actualizada correctamente'}
    except Exception as e:
        return {'success': False, 'message': f"Error al actualizar partida: {e}"}


def delete_catalogo_partida(user: str, password: str, schema: str, partida_id: int) -> dict:
    """
    Elimina una partida del catálogo.

    Returns:
        dict: {'success': bool, 'message': str}
    """
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

            cur.execute(f"DELETE FROM {schema}.tbl_cata_hidra_tipo WHERE id = %s", (partida_id,))
            cn.commit()
            cur.close()

            return {'success': True, 'message': 'Partida eliminada correctamente'}
    except Exception as e:
        return {'success': False, 'message': f"Error al eliminar partida: {e}"}


# =============================================================================
# FUNCIONES DE VALIDACIÓN DE FORMATO
# =============================================================================

def validar_codigo_dimension(codigo: str, table_name: str) -> str:
    """
    Valida y formatea el código según la tabla de destino.

    - dim_red: MAYÚSCULAS, 2-10 caracteres
    - dim_tipos_rep: MAYÚSCULAS, 2-20 caracteres
    - dim_codigo_trabajo: Numérico o alfanumérico en MAYÚSCULAS

    Returns:
        str: Código validado y formateado
    """
    codigo = codigo.strip()

    if table_name == 'dim_red':
        # Código de red: MAYÚSCULAS, máximo 10 chars
        return codigo.upper()[:10]

    elif table_name == 'dim_tipos_rep':
        # Tipo de reparación: MAYÚSCULAS
        return codigo.upper()[:20]

    elif table_name == 'dim_codigo_trabajo':
        # Código de trabajo: puede ser numérico o alfanumérico
        return codigo.upper()[:50]

    return codigo


def validar_descripcion(descripcion: str) -> str:
    """
    Valida y formatea la descripción.
    Primera letra en mayúscula, resto respetado.

    Returns:
        str: Descripción formateada
    """
    descripcion = descripcion.strip()
    if descripcion:
        return descripcion[0].upper() + descripcion[1:] if len(descripcion) > 1 else descripcion.upper()
    return descripcion


def validar_precio(precio_str: str) -> tuple:
    """
    Valida y formatea el precio.

    Returns:
        tuple: (success: bool, value: float, message: str)
    """
    try:
        # Reemplazar coma por punto para decimales
        precio_str = precio_str.replace(',', '.').strip()
        precio = float(precio_str)
        if precio < 0:
            return (False, 0.0, "El precio no puede ser negativo")
        return (True, round(precio, 2), "")
    except ValueError:
        return (False, 0.0, "El precio debe ser un número válido")
