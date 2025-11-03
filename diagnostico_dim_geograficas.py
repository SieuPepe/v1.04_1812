#!/usr/bin/env python3
"""
Script de diagnóstico para verificar la estructura de tablas de dimensiones geográficas
"""

import sys
from script.db_connection import get_project_connection

def diagnosticar_tablas_geograficas(user, password, schema):
    """
    Verifica la estructura de las tablas dim_provincias, dim_comarcas y dim_municipios
    """
    tablas = ['dim_provincias', 'dim_comarcas', 'dim_municipios']

    print("="*80)
    print("DIAGNÓSTICO DE TABLAS DE DIMENSIONES GEOGRÁFICAS")
    print("="*80)
    print(f"Schema: {schema}\n")

    with get_project_connection(user, password, schema) as conn:
        cursor = conn.cursor()

        for tabla in tablas:
            print(f"\n{'='*80}")
            print(f"Tabla: {tabla}")
            print(f"{'='*80}")

            try:
                # Obtener estructura de la tabla
                cursor.execute(f"DESCRIBE {schema}.{tabla}")
                columnas = cursor.fetchall()

                print("\nColumnas encontradas:")
                print(f"{'Campo':<30} {'Tipo':<20} {'Null':<10} {'Key':<10}")
                print("-"*80)
                for col in columnas:
                    print(f"{col[0]:<30} {col[1]:<20} {col[2]:<10} {col[3]:<10}")

                # Buscar columnas candidatas para mostrar
                columnas_texto = []
                for col in columnas:
                    col_name = col[0].lower()
                    col_type = col[1].lower()

                    if col_name != 'id' and ('varchar' in col_type or 'text' in col_type or 'char' in col_type):
                        columnas_texto.append(col[0])

                print(f"\nColumnas de texto (candidatas para mostrar): {', '.join(columnas_texto)}")

                # Intentar obtener algunos registros de ejemplo
                if columnas_texto:
                    col_principal = columnas_texto[0]
                    cursor.execute(f"SELECT id, {col_principal} FROM {schema}.{tabla} LIMIT 5")
                    ejemplos = cursor.fetchall()

                    if ejemplos:
                        print(f"\nEjemplos de datos (usando columna '{col_principal}'):")
                        print(f"{'ID':<10} {col_principal}")
                        print("-"*50)
                        for ejemplo in ejemplos:
                            print(f"{ejemplo[0]:<10} {ejemplo[1]}")
                    else:
                        print(f"\n⚠ La tabla está vacía")

            except Exception as e:
                print(f"\n❌ Error al analizar tabla {tabla}: {e}")

        cursor.close()

    print("\n" + "="*80)
    print("FIN DEL DIAGNÓSTICO")
    print("="*80)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python diagnostico_dim_geograficas.py <usuario> <password> <schema>")
        print("Ejemplo: python diagnostico_dim_geograficas.py root mypass cert_dev")
        sys.exit(1)

    user = sys.argv[1]
    password = sys.argv[2]
    schema = sys.argv[3]

    try:
        diagnosticar_tablas_geograficas(user, password, schema)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
