#!/usr/bin/env python3
"""
Script para ejecutar la migración manualmente en un esquema específico.
Usa el script SQL compatible con MySQL.

Uso:
    python script/ejecutar_migracion_manual.py --user root --password PASS --schema cert_dev
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from script.db_config import get_config
import mysql.connector


def ejecutar_sql_archivo(user: str, password: str, schema: str, archivo_sql: Path):
    """Ejecuta un archivo SQL línea por línea."""
    print(f"\n📄 Leyendo archivo SQL: {archivo_sql}")

    with open(archivo_sql, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    print(f"✅ Archivo cargado ({len(sql_content)} caracteres)")

    config = get_config()

    try:
        conn = mysql.connector.connect(
            host=config.host,
            port=config.port,
            user=user,
            password=password,
            database=schema
        )

        cursor = conn.cursor()

        print(f"\n🚀 Ejecutando migración en esquema '{schema}'...\n")

        # Dividir por comandos (usando ; como delimitador, pero respetando DELIMITER)
        comandos = []
        buffer = []
        delimiter = ';'
        in_delimiter_block = False

        for linea in sql_content.split('\n'):
            linea_stripped = linea.strip()

            # Detectar cambio de DELIMITER
            if linea_stripped.upper().startswith('DELIMITER'):
                if 'DELIMITER ;' in linea_stripped:
                    delimiter = ';'
                    in_delimiter_block = False
                else:
                    delimiter = '//'
                    in_delimiter_block = True
                continue

            # Ignorar líneas vacías y comentarios
            if not linea_stripped or linea_stripped.startswith('--'):
                continue

            buffer.append(linea)

            # Si la línea termina con el delimiter actual
            if linea_stripped.endswith(delimiter):
                comando = '\n'.join(buffer)
                comando = comando.rstrip(delimiter).strip()
                if comando:
                    comandos.append(comando)
                buffer = []

        # Agregar cualquier comando restante
        if buffer:
            comando = '\n'.join(buffer).strip()
            if comando:
                comandos.append(comando)

        print(f"📋 Se ejecutarán {len(comandos)} comandos SQL\n")

        exitos = 0
        advertencias = 0
        errores_criticos = []

        for i, comando in enumerate(comandos, 1):
            try:
                # Mostrar resumen del comando
                primera_linea = comando.split('\n')[0][:60]
                print(f"[{i}/{len(comandos)}] {primera_linea}...", end=' ')

                cursor.execute(comando)

                # Obtener resultados si los hay
                if cursor.with_rows:
                    resultados = cursor.fetchall()
                    if resultados and len(resultados) > 0:
                        # Mostrar primer resultado si es un mensaje
                        primer_resultado = resultados[0]
                        if isinstance(primer_resultado, tuple) and len(primer_resultado) > 0:
                            mensaje = primer_resultado[0]
                            if isinstance(mensaje, str) and ('✓' in mensaje or '⚠' in mensaje or 'ℹ' in mensaje):
                                print(f"→ {mensaje}")
                            else:
                                print("✓")
                        else:
                            print("✓")
                    else:
                        print("✓")
                else:
                    print("✓")

                exitos += 1

            except mysql.connector.Error as err:
                error_msg = str(err)

                # Clasificar error
                if 'Duplicate' in error_msg or 'already exists' in error_msg:
                    print(f"⚠ Ya existe")
                    advertencias += 1
                elif 'doesn\'t exist' in error_msg and 'dim_' in comando:
                    print(f"ℹ Tabla opcional no existe")
                    advertencias += 1
                else:
                    print(f"\n  ❌ ERROR: {error_msg}")
                    errores_criticos.append((i, comando[:100], error_msg))

        conn.commit()
        cursor.close()
        conn.close()

        # Resumen
        print(f"\n" + "=" * 80)
        print(f"📊 RESUMEN DE EJECUCIÓN")
        print("=" * 80)
        print(f"✅ Comandos exitosos: {exitos}")
        print(f"⚠️  Advertencias: {advertencias}")
        print(f"❌ Errores críticos: {len(errores_criticos)}")

        if errores_criticos:
            print(f"\n⚠️  ERRORES CRÍTICOS ENCONTRADOS:")
            for num, cmd, error in errores_criticos:
                print(f"\n  Comando #{num}: {cmd}...")
                print(f"  Error: {error}")
            return False
        else:
            print(f"\n🎉 ¡MIGRACIÓN COMPLETADA CON ÉXITO!")
            return True

    except Exception as e:
        print(f"\n❌ ERROR FATAL: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Ejecutar migración manual de mejoras de partes'
    )
    parser.add_argument('--user', required=True, help='Usuario de MySQL')
    parser.add_argument('--password', required=True, help='Contraseña de MySQL')
    parser.add_argument('--schema', required=True, help='Esquema donde ejecutar (ej: cert_dev)')

    args = parser.parse_args()

    print("=" * 80)
    print("  MIGRACIÓN MANUAL - MEJORAS DE PARTES")
    print("=" * 80)
    print(f"\n🎯 Esquema objetivo: {args.schema}")
    print(f"👤 Usuario: {args.user}")

    # Buscar archivo SQL
    script_dir = Path(__file__).parent
    archivo_sql = script_dir / 'mejoras_tabla_partes_mysql.sql'

    if not archivo_sql.exists():
        print(f"\n❌ ERROR: No se encontró el archivo {archivo_sql}")
        sys.exit(1)

    # Ejecutar
    exito = ejecutar_sql_archivo(args.user, args.password, args.schema, archivo_sql)

    if exito:
        print(f"\n✅ La migración se completó correctamente en '{args.schema}'")
        print(f"\n📝 Próximos pasos:")
        print(f"   1. Verificar los cambios con: python script/test_migration_complete.py --user {args.user} --password *** --schema {args.schema} --skip-migration")
        print(f"   2. Probar las funciones Python con datos reales")
        print(f"   3. Aplicar a otros esquemas si es necesario")
        sys.exit(0)
    else:
        print(f"\n❌ La migración falló. Revisa los errores anteriores.")
        print(f"\n🔄 Para revertir, restaura desde el backup:")
        print(f"   mysql -u {args.user} -p {args.schema} < backup_{args.schema}_antes_migracion.sql")
        sys.exit(1)


if __name__ == '__main__':
    main()
