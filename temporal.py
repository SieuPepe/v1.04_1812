python -c "
import mysql.connector
cn = mysql.connector.connect(host='localhost', port=3307, user='root', password='NuevaPass!2025', database='cert_dev')
cur = cn.cursor()

# Leer el archivo SQL
with open('script/eliminar_dim_ot.sql', 'r', encoding='utf-8') as f:
    sql_script = f.read()

# Ejecutar cada comando
for statement in sql_script.split(';'):
    statement = statement.strip()
    if statement and not statement.startswith('--'):
        try:
            cur.execute(statement)
            print(f'✓ Ejecutado: {statement[:50]}...')
        except Exception as e:
            print(f'✗ Error: {e}')

cn.commit()
cur.close()
cn.close()
print('\\n✅ Script SQL ejecutado correctamente')
"
