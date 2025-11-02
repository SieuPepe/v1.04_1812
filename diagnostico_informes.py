"""
Script de diagnóstico para el módulo de informes
Verifica datos y queries SQL
"""

from script.db_connection import get_project_connection
from script.informes import ejecutar_informe, build_query
from script.informes_config import INFORMES_DEFINICIONES

# Credenciales
USER = "aperez"
PASSWORD = "WGueXNk9"
SCHEMA = "HFM"

def verificar_datos_partes():
    """Verifica cuántos partes hay en la base de datos"""
    print("\n" + "="*70)
    print("VERIFICANDO DATOS EN tbl_partes")
    print("="*70)

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # Contar total de partes
            cursor.execute(f"SELECT COUNT(*) FROM {SCHEMA}.tbl_partes")
            total = cursor.fetchone()[0]
            print(f"✓ Total de partes en la tabla: {total}")

            # Verificar estados
            cursor.execute(f"""
                SELECT estado, COUNT(*) as cantidad
                FROM {SCHEMA}.tbl_partes
                GROUP BY estado
            """)
            estados = cursor.fetchall()
            print(f"\n✓ Distribución por estado:")
            for estado, cantidad in estados:
                print(f"  - {estado}: {cantidad} partes")

            # Verificar algunos datos de los primeros 5 partes
            cursor.execute(f"""
                SELECT id, codigo, descripcion, estado, red_id, provincia_id
                FROM {SCHEMA}.tbl_partes
                LIMIT 5
            """)
            partes = cursor.fetchall()
            print(f"\n✓ Muestra de los primeros 5 partes:")
            for parte in partes:
                print(f"  - ID: {parte[0]}, Código: {parte[1]}, Estado: {parte[3]}")

            return total > 0

    except Exception as e:
        print(f"✗ ERROR al verificar datos: {e}")
        import traceback
        traceback.print_exc()
        return False


def verificar_query_informe():
    """Verifica la query SQL generada para el informe"""
    print("\n" + "="*70)
    print("VERIFICANDO QUERY SQL DEL INFORME 'Resumen de Partes'")
    print("="*70)

    try:
        # Obtener definición del informe
        definicion = INFORMES_DEFINICIONES.get("Resumen de Partes")
        if not definicion:
            print("✗ No se encontró la definición del informe")
            return False

        # Campos por defecto
        campos_default = definicion.get('campos_default', [])
        print(f"\n✓ Campos por defecto ({len(campos_default)}):")
        for campo in campos_default:
            print(f"  - {campo}")

        # Construir query sin filtros ni clasificaciones
        query = build_query(
            "Resumen de Partes",
            filtros=None,
            clasificaciones=None,
            campos_seleccionados=None,  # Usará los campos por defecto
            schema=SCHEMA
        )

        print(f"\n✓ Query SQL generada:")
        print("-" * 70)
        print(query)
        print("-" * 70)

        # Ejecutar la query
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            datos = cursor.fetchall()

            print(f"\n✓ Resultados de la query: {len(datos)} registros")

            if len(datos) > 0:
                print(f"\n✓ Primeros 3 registros:")
                for i, fila in enumerate(datos[:3], 1):
                    print(f"  Registro {i}: {fila[:5]}...")  # Mostrar primeros 5 campos
            else:
                print("\n✗ ¡NO SE ENCONTRARON DATOS!")
                print("\nPosibles causas:")
                print("  1. Problema con los JOINs de dimensiones")
                print("  2. Valores NULL en campos de dimensión")
                print("  3. Referencias incorrectas a tablas de dimensión")

                # Verificar que existan las tablas de dimensión
                print("\n✓ Verificando tablas de dimensión:")
                tablas = ["dim_red", "dim_tipo_trabajo", "dim_provincias"]
                for tabla in tablas:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {SCHEMA}.{tabla}")
                        count = cursor.fetchone()[0]
                        print(f"  - {tabla}: {count} registros")
                    except Exception as e:
                        print(f"  - {tabla}: ERROR - {e}")

            return len(datos) > 0

    except Exception as e:
        print(f"\n✗ ERROR al verificar query: {e}")
        import traceback
        traceback.print_exc()
        return False


def verificar_dimensiones_partes():
    """Verifica que los partes tengan valores correctos en los campos de dimensión"""
    print("\n" + "="*70)
    print("VERIFICANDO VALORES DE DIMENSIONES EN PARTES")
    print("="*70)

    try:
        with get_project_connection(USER, PASSWORD, SCHEMA) as conn:
            cursor = conn.cursor()

            # Verificar cuántos partes tienen NULL en red_id
            cursor.execute(f"""
                SELECT COUNT(*)
                FROM {SCHEMA}.tbl_partes
                WHERE red_id IS NULL
            """)
            null_red = cursor.fetchone()[0]
            print(f"✓ Partes con red_id NULL: {null_red}")

            # Verificar cuántos partes tienen NULL en tipo_trabajo_id
            cursor.execute(f"""
                SELECT COUNT(*)
                FROM {SCHEMA}.tbl_partes
                WHERE tipo_trabajo_id IS NULL
            """)
            null_tipo = cursor.fetchone()[0]
            print(f"✓ Partes con tipo_trabajo_id NULL: {null_tipo}")

            # Verificar cuántos partes tienen NULL en provincia_id
            cursor.execute(f"""
                SELECT COUNT(*)
                FROM {SCHEMA}.tbl_partes
                WHERE provincia_id IS NULL
            """)
            null_provincia = cursor.fetchone()[0]
            print(f"✓ Partes con provincia_id NULL: {null_provincia}")

            # Verificar IDs que no coinciden con las dimensiones
            cursor.execute(f"""
                SELECT COUNT(*)
                FROM {SCHEMA}.tbl_partes p
                LEFT JOIN {SCHEMA}.dim_red r ON p.red_id = r.id
                WHERE p.red_id IS NOT NULL AND r.id IS NULL
            """)
            red_invalidos = cursor.fetchone()[0]
            print(f"✓ Partes con red_id inválido (no existe en dim_red): {red_invalidos}")

            cursor.execute(f"""
                SELECT COUNT(*)
                FROM {SCHEMA}.tbl_partes p
                LEFT JOIN {SCHEMA}.dim_tipo_trabajo t ON p.tipo_trabajo_id = t.id
                WHERE p.tipo_trabajo_id IS NOT NULL AND t.id IS NULL
            """)
            tipo_invalidos = cursor.fetchone()[0]
            print(f"✓ Partes con tipo_trabajo_id inválido: {tipo_invalidos}")

            cursor.execute(f"""
                SELECT COUNT(*)
                FROM {SCHEMA}.tbl_partes p
                LEFT JOIN {SCHEMA}.dim_provincias prov ON p.provincia_id = prov.id
                WHERE p.provincia_id IS NOT NULL AND prov.id IS NULL
            """)
            provincia_invalidos = cursor.fetchone()[0]
            print(f"✓ Partes con provincia_id inválido: {provincia_invalidos}")

            if red_invalidos > 0 or tipo_invalidos > 0 or provincia_invalidos > 0:
                print("\n⚠️  HAY VALORES INVÁLIDOS EN LOS CAMPOS DE DIMENSIÓN")
                print("   Esto puede causar que los JOINs filtren incorrectamente los datos")
            else:
                print("\n✓ Todos los valores de dimensión son válidos")

    except Exception as e:
        print(f"\n✗ ERROR al verificar dimensiones: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("\n" + "="*70)
    print(" DIAGNÓSTICO DEL MÓDULO DE INFORMES")
    print("="*70)

    # 1. Verificar que haya datos
    hay_datos = verificar_datos_partes()

    if not hay_datos:
        print("\n⚠️  No hay datos en tbl_partes. El informe no puede devolver resultados.")
    else:
        # 2. Verificar dimensiones
        verificar_dimensiones_partes()

        # 3. Verificar query del informe
        query_ok = verificar_query_informe()

        if query_ok:
            print("\n" + "="*70)
            print("✓ DIAGNÓSTICO EXITOSO - El informe funciona correctamente")
            print("="*70)
        else:
            print("\n" + "="*70)
            print("✗ PROBLEMA IDENTIFICADO - El informe no devuelve datos")
            print("="*70)
            print("\nRevisa los mensajes de error arriba para más detalles.")

    print("\n")
