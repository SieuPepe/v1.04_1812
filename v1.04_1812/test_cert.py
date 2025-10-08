from script.modulo_db import list_certifications, create_new_certification

USER = "root"            # tu usuario MySQL de dev
PASS = "NuevaPass!2025"    # tu contraseña MySQL
SCHEMA = "manager"      # AJUSTA al esquema real que tienes (usa SHOW DATABASES; en MySQL)

print("Antes:", list_certifications(USER, PASS, SCHEMA))

name = "certification_prueba01"
try:
    print("Creando:", name)
    created = create_new_certification(USER, PASS, SCHEMA, name, gg_pct=13.0, bi_pct=6.0)
    print("Creada:", created)
except Exception as e:
    print("Error al crear:", e)

print("Después:", list_certifications(USER, PASS, SCHEMA))
