#!/usr/bin/env python3
"""
Script de verificación de integridad de datos
Verifica la integridad de partes y presupuestos en la base de datos
"""
import mysql.connector
from datetime import datetime
from typing import Dict, List, Tuple
import sys


class IntegrityChecker:
    """Verificador de integridad de datos"""

    def __init__(self, host='localhost', port=3307, user='root', password='Cretus2021*', schema='cert_dev'):
        """
        Inicializa el verificador de integridad

        Args:
            host: Host de la base de datos
            port: Puerto de la base de datos
            user: Usuario
            password: Contraseña
            schema: Esquema a verificar
        """
        self.connection_params = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': schema
        }
        self.schema = schema
        self.errors = []
        self.warnings = []
        self.stats = {}

    def connect(self):
        """Establece conexión con la base de datos"""
        try:
            self.conn = mysql.connector.connect(**self.connection_params)
            self.cursor = self.conn.cursor(dictionary=True)
            print(f"✓ Conectado al esquema: {self.schema}")
            return True
        except Exception as e:
            print(f"✗ Error de conexión: {e}")
            return False

    def close(self):
        """Cierra la conexión"""
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'conn'):
            self.conn.close()

    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """
        Ejecuta una consulta y retorna los resultados

        Args:
            query: Consulta SQL
            params: Parámetros de la consulta

        Returns:
            Lista de diccionarios con los resultados
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            self.errors.append(f"Error ejecutando query: {str(e)}")
            return []

    def verify_tables_exist(self) -> bool:
        """Verifica que existan las tablas requeridas"""
        print("\n=== VERIFICANDO EXISTENCIA DE TABLAS ===")

        required_tables = [
            'tbl_partes',
            'tbl_part_presupuesto',
            'tbl_presupuesto',
            'tbl_pres_precios',
            'tbl_parte_estados',
            'dim_municipios'
        ]

        query = """
            SELECT TABLE_NAME
            FROM information_schema.TABLES
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME IN (%s)
        """

        placeholders = ','.join(['%s'] * len(required_tables))
        query = query.replace('(%s)', f'({placeholders})')
        params = (self.schema,) + tuple(required_tables)

        results = self.execute_query(query, params)
        existing_tables = [r['TABLE_NAME'] for r in results]

        all_exist = True
        for table in required_tables:
            if table in existing_tables:
                print(f"  ✓ {table}")
            else:
                print(f"  ✗ {table} - NO EXISTE")
                self.errors.append(f"Tabla {table} no existe")
                all_exist = False

        return all_exist

    def get_table_stats(self):
        """Obtiene estadísticas básicas de las tablas"""
        print("\n=== ESTADÍSTICAS DE TABLAS ===")

        tables = {
            'tbl_partes': 'Partes',
            'tbl_part_presupuesto': 'Partes-Presupuesto (relación)',
            'tbl_presupuesto': 'Presupuesto',
            'tbl_pres_precios': 'Precios de partidas'
        }

        for table, description in tables.items():
            try:
                result = self.execute_query(f"SELECT COUNT(*) as total FROM {table}")
                count = result[0]['total'] if result else 0
                self.stats[table] = count
                print(f"  {description:35s}: {count:>6,} registros")
            except Exception as e:
                print(f"  {description:35s}: ERROR - {e}")
                self.stats[table] = 0

    def verify_partes_integrity(self):
        """Verifica integridad de la tabla de partes"""
        print("\n=== VERIFICANDO INTEGRIDAD DE PARTES ===")

        # 1. Partes sin código
        print("\n1. Verificando códigos de partes...")
        query = "SELECT COUNT(*) as total FROM tbl_partes WHERE codigo IS NULL OR codigo = ''"
        result = self.execute_query(query)
        if result and result[0]['total'] > 0:
            self.warnings.append(f"Encontrados {result[0]['total']} partes sin código")
            print(f"  ⚠ {result[0]['total']} partes sin código")
        else:
            print(f"  ✓ Todos los partes tienen código")

        # 2. Partes con fechas inconsistentes
        print("\n2. Verificando fechas...")
        query = """
            SELECT COUNT(*) as total
            FROM tbl_partes
            WHERE fecha_inicio IS NOT NULL
              AND fecha_fin IS NOT NULL
              AND fecha_fin < fecha_inicio
        """
        result = self.execute_query(query)
        if result and result[0]['total'] > 0:
            self.errors.append(f"{result[0]['total']} partes con fecha_fin anterior a fecha_inicio")
            print(f"  ✗ {result[0]['total']} partes con fechas inconsistentes")
        else:
            print(f"  ✓ Todas las fechas son consistentes")

        # 3. Partes sin municipio
        print("\n3. Verificando municipios...")
        query = "SELECT COUNT(*) as total FROM tbl_partes WHERE id_municipio IS NULL"
        result = self.execute_query(query)
        if result and result[0]['total'] > 0:
            self.warnings.append(f"{result[0]['total']} partes sin municipio asignado")
            print(f"  ⚠ {result[0]['total']} partes sin municipio")
        else:
            print(f"  ✓ Todos los partes tienen municipio")

        # 4. Partes con municipio inexistente
        print("\n4. Verificando referencias a municipios...")
        query = """
            SELECT COUNT(*) as total
            FROM tbl_partes p
            LEFT JOIN dim_municipios m ON p.id_municipio = m.id
            WHERE p.id_municipio IS NOT NULL AND m.id IS NULL
        """
        result = self.execute_query(query)
        if result and result[0]['total'] > 0:
            self.errors.append(f"{result[0]['total']} partes referencian municipios inexistentes")
            print(f"  ✗ {result[0]['total']} partes con municipios inexistentes")

            # Mostrar detalle
            query_detail = """
                SELECT p.id, p.codigo, p.id_municipio
                FROM tbl_partes p
                LEFT JOIN dim_municipios m ON p.id_municipio = m.id
                WHERE p.id_municipio IS NOT NULL AND m.id IS NULL
                LIMIT 5
            """
            details = self.execute_query(query_detail)
            if details:
                print("  Ejemplos:")
                for d in details:
                    print(f"    - Parte {d['codigo']} (id={d['id']}) → municipio_id={d['id_municipio']}")
        else:
            print(f"  ✓ Todas las referencias a municipios son válidas")

        # 5. Partes con estado inválido
        print("\n5. Verificando estados...")
        query = """
            SELECT COUNT(*) as total
            FROM tbl_partes p
            LEFT JOIN tbl_parte_estados e ON p.id_estado = e.id
            WHERE p.id_estado IS NOT NULL AND e.id IS NULL
        """
        result = self.execute_query(query)
        if result and result[0]['total'] > 0:
            self.errors.append(f"{result[0]['total']} partes con estado inválido")
            print(f"  ✗ {result[0]['total']} partes con estado inválido")
        else:
            print(f"  ✓ Todos los estados son válidos")

        # 6. Distribución por estado
        print("\n6. Distribución de partes por estado...")
        query = """
            SELECT
                COALESCE(e.nombre, 'SIN ESTADO') as estado,
                COUNT(*) as total
            FROM tbl_partes p
            LEFT JOIN tbl_parte_estados e ON p.id_estado = e.id
            GROUP BY estado
            ORDER BY total DESC
        """
        results = self.execute_query(query)
        if results:
            for r in results:
                print(f"  - {r['estado']:20s}: {r['total']:>6,} partes")

    def verify_presupuesto_integrity(self):
        """Verifica integridad de presupuestos"""
        print("\n=== VERIFICANDO INTEGRIDAD DE PRESUPUESTOS ===")

        # 1. Presupuestos sin partida
        print("\n1. Verificando partidas...")
        query = "SELECT COUNT(*) as total FROM tbl_presupuesto WHERE id_partida IS NULL"
        result = self.execute_query(query)
        if result and result[0]['total'] > 0:
            self.errors.append(f"{result[0]['total']} presupuestos sin partida")
            print(f"  ✗ {result[0]['total']} presupuestos sin partida")
        else:
            print(f"  ✓ Todos los presupuestos tienen partida")

        # 2. Presupuestos con partida inexistente
        print("\n2. Verificando referencias a partidas...")
        query = """
            SELECT COUNT(*) as total
            FROM tbl_presupuesto p
            LEFT JOIN tbl_pres_precios pp ON p.id_partida = pp.id
            WHERE p.id_partida IS NOT NULL AND pp.id IS NULL
        """
        result = self.execute_query(query)
        if result and result[0]['total'] > 0:
            self.errors.append(f"{result[0]['total']} presupuestos referencian partidas inexistentes")
            print(f"  ✗ {result[0]['total']} presupuestos con partidas inexistentes")
        else:
            print(f"  ✓ Todas las referencias a partidas son válidas")

        # 3. Presupuestos con cantidad negativa o cero
        print("\n3. Verificando cantidades...")
        query = """
            SELECT COUNT(*) as total
            FROM tbl_presupuesto
            WHERE cantidad IS NULL OR cantidad <= 0
        """
        result = self.execute_query(query)
        if result and result[0]['total'] > 0:
            self.warnings.append(f"{result[0]['total']} presupuestos con cantidad inválida")
            print(f"  ⚠ {result[0]['total']} presupuestos con cantidad <= 0 o NULL")
        else:
            print(f"  ✓ Todas las cantidades son válidas")

        # 4. Presupuestos sin grupo
        print("\n4. Verificando grupos...")
        query = "SELECT COUNT(*) as total FROM tbl_presupuesto WHERE grupo IS NULL"
        result = self.execute_query(query)
        if result and result[0]['total'] > 0:
            self.warnings.append(f"{result[0]['total']} presupuestos sin grupo asignado")
            print(f"  ⚠ {result[0]['total']} presupuestos sin grupo")
        else:
            print(f"  ✓ Todos los presupuestos tienen grupo")

    def verify_part_presupuesto_integrity(self):
        """Verifica integridad de la relación partes-presupuesto"""
        print("\n=== VERIFICANDO INTEGRIDAD DE RELACIÓN PARTES-PRESUPUESTO ===")

        # 1. Registros con parte inexistente
        print("\n1. Verificando referencias a partes...")
        query = """
            SELECT COUNT(*) as total
            FROM tbl_part_presupuesto pp
            LEFT JOIN tbl_partes p ON pp.id_parte = p.id
            WHERE pp.id_parte IS NOT NULL AND p.id IS NULL
        """
        result = self.execute_query(query)
        if result and result[0]['total'] > 0:
            self.errors.append(f"{result[0]['total']} registros referencian partes inexistentes")
            print(f"  ✗ {result[0]['total']} registros con partes inexistentes")
        else:
            print(f"  ✓ Todas las referencias a partes son válidas")

        # 2. Registros con presupuesto inexistente
        print("\n2. Verificando referencias a presupuestos...")
        query = """
            SELECT COUNT(*) as total
            FROM tbl_part_presupuesto pp
            LEFT JOIN tbl_presupuesto p ON pp.id_presupuesto = p.id
            WHERE pp.id_presupuesto IS NOT NULL AND p.id IS NULL
        """
        result = self.execute_query(query)
        if result and result[0]['total'] > 0:
            self.errors.append(f"{result[0]['total']} registros referencian presupuestos inexistentes")
            print(f"  ✗ {result[0]['total']} registros con presupuestos inexistentes")
        else:
            print(f"  ✓ Todas las referencias a presupuestos son válidas")

        # 3. Cantidad certificada sin fecha
        print("\n3. Verificando fechas de certificación...")
        query = """
            SELECT COUNT(*) as total
            FROM tbl_part_presupuesto
            WHERE cantidad_certificada > 0 AND fecha IS NULL
        """
        result = self.execute_query(query)
        if result and result[0]['total'] > 0:
            self.warnings.append(f"{result[0]['total']} certificaciones sin fecha")
            print(f"  ⚠ {result[0]['total']} certificaciones sin fecha")
        else:
            print(f"  ✓ Todas las certificaciones tienen fecha")

        # 4. Cantidad certificada mayor que cantidad presupuestada
        print("\n4. Verificando cantidades certificadas vs presupuestadas...")
        query = """
            SELECT COUNT(*) as total
            FROM tbl_part_presupuesto pp
            INNER JOIN tbl_presupuesto p ON pp.id_presupuesto = p.id
            WHERE pp.cantidad_certificada > p.cantidad
        """
        result = self.execute_query(query)
        if result and result[0]['total'] > 0:
            self.warnings.append(f"{result[0]['total']} certificaciones exceden cantidad presupuestada")
            print(f"  ⚠ {result[0]['total']} certificaciones exceden presupuesto")

            # Mostrar detalle
            query_detail = """
                SELECT
                    pt.codigo as parte,
                    pp.cantidad_certificada,
                    p.cantidad as cantidad_presupuesto,
                    (pp.cantidad_certificada - p.cantidad) as exceso
                FROM tbl_part_presupuesto pp
                INNER JOIN tbl_presupuesto p ON pp.id_presupuesto = p.id
                INNER JOIN tbl_partes pt ON pp.id_parte = pt.id
                WHERE pp.cantidad_certificada > p.cantidad
                ORDER BY exceso DESC
                LIMIT 5
            """
            details = self.execute_query(query_detail)
            if details:
                print("  Ejemplos de excesos:")
                for d in details:
                    print(f"    - Parte {d['parte']}: certificado={d['cantidad_certificada']:.2f}, "
                          f"presupuesto={d['cantidad_presupuesto']:.2f}, exceso={d['exceso']:.2f}")
        else:
            print(f"  ✓ Todas las certificaciones están dentro del presupuesto")

        # 5. Partes sin presupuesto asignado
        print("\n5. Verificando partes con/sin presupuesto...")
        query = """
            SELECT COUNT(*) as total
            FROM tbl_partes p
            LEFT JOIN tbl_part_presupuesto pp ON p.id = pp.id_parte
            WHERE pp.id IS NULL
        """
        result = self.execute_query(query)
        if result and result[0]['total'] > 0:
            print(f"  ℹ {result[0]['total']} partes sin presupuesto asignado")
        else:
            print(f"  ✓ Todos los partes tienen presupuesto")

    def verify_data_consistency(self):
        """Verifica consistencia general de datos"""
        print("\n=== VERIFICANDO CONSISTENCIA DE DATOS ===")

        # 1. Verificar duplicados en códigos de partes
        print("\n1. Verificando duplicados en códigos de partes...")
        query = """
            SELECT codigo, COUNT(*) as total
            FROM tbl_partes
            WHERE codigo IS NOT NULL AND codigo != ''
            GROUP BY codigo
            HAVING COUNT(*) > 1
        """
        results = self.execute_query(query)
        if results:
            self.errors.append(f"{len(results)} códigos de partes duplicados")
            print(f"  ✗ {len(results)} códigos duplicados encontrados")
            for r in results[:5]:
                print(f"    - Código '{r['codigo']}': {r['total']} veces")
        else:
            print(f"  ✓ No hay códigos duplicados")

        # 2. Verificar rango de fechas
        print("\n2. Verificando rango de fechas...")
        query = """
            SELECT
                MIN(fecha_inicio) as fecha_min,
                MAX(fecha_fin) as fecha_max
            FROM tbl_partes
            WHERE fecha_inicio IS NOT NULL OR fecha_fin IS NOT NULL
        """
        result = self.execute_query(query)
        if result and result[0]['fecha_min']:
            print(f"  ℹ Rango de fechas: {result[0]['fecha_min']} a {result[0]['fecha_max']}")

    def generate_report(self):
        """Genera un reporte final"""
        print("\n" + "="*70)
        print("RESUMEN DE VERIFICACIÓN DE INTEGRIDAD")
        print("="*70)

        print(f"\nEsquema verificado: {self.schema}")
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        print("\n--- ESTADÍSTICAS ---")
        for table, count in self.stats.items():
            print(f"  {table:35s}: {count:>6,} registros")

        print("\n--- RESULTADOS ---")

        if not self.errors and not self.warnings:
            print("  ✓ ¡NO SE ENCONTRARON PROBLEMAS!")
            print("  ✓ La integridad de los datos es correcta")
        else:
            if self.errors:
                print(f"\n  ✗ ERRORES CRÍTICOS: {len(self.errors)}")
                for i, error in enumerate(self.errors, 1):
                    print(f"    {i}. {error}")

            if self.warnings:
                print(f"\n  ⚠ ADVERTENCIAS: {len(self.warnings)}")
                for i, warning in enumerate(self.warnings, 1):
                    print(f"    {i}. {warning}")

        print("\n" + "="*70)

        return len(self.errors) == 0

    def run_all_checks(self):
        """Ejecuta todas las verificaciones"""
        if not self.connect():
            return False

        try:
            # Verificar existencia de tablas
            if not self.verify_tables_exist():
                print("\n⚠ Faltan tablas requeridas. Abortando verificación.")
                return False

            # Estadísticas
            self.get_table_stats()

            # Verificaciones de integridad
            self.verify_partes_integrity()
            self.verify_presupuesto_integrity()
            self.verify_part_presupuesto_integrity()
            self.verify_data_consistency()

            # Generar reporte
            return self.generate_report()

        finally:
            self.close()


def main():
    """Función principal"""
    print("="*70)
    print("VERIFICACIÓN DE INTEGRIDAD DE DATOS")
    print("Partes y Presupuestos")
    print("="*70)

    # Verificar esquema
    schema = 'cert_dev'
    if len(sys.argv) > 1:
        schema = sys.argv[1]

    print(f"\nEsquema a verificar: {schema}")

    # Crear verificador y ejecutar
    checker = IntegrityChecker(schema=schema)
    success = checker.run_all_checks()

    # Retornar código de salida
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
