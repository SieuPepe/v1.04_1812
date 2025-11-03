═══════════════════════════════════════════════════════════════════
   CONFIGURACIONES GUARDADAS DE INFORMES
   HydroFlow Manager v1.04
═══════════════════════════════════════════════════════════════════

Este directorio contiene las configuraciones guardadas de informes
personalizados creados por los usuarios.

FUNCIONAMIENTO:
---------------
Cuando un usuario configura un informe (filtros, clasificaciones, campos)
y hace clic en "💾 Guardar Config", la configuración se guarda como un
archivo JSON en este directorio.

Posteriormente, puede recuperar la configuración haciendo clic en
"📂 Cargar Config" y seleccionando el informe guardado de la lista.

ARCHIVOS:
---------
Cada configuración se guarda como:
  nombre_configuracion.json

Ejemplo:
  partes_en_curso_por_ot.json
  resumen_economico_comarca.json
  certificaciones_pendientes_2024.json

CONTENIDO DE ARCHIVOS:
----------------------
Cada archivo JSON contiene:
- Nombre y descripción de la configuración
- Tipo de informe base
- Filtros aplicados (campo, operador, valor, lógica AND/OR)
- Clasificaciones (ordenamiento)
- Campos seleccionados para mostrar
- Fechas de creación y modificación

GESTIÓN:
--------
- Los archivos pueden compartirse entre usuarios copiándolos
- Para eliminar una configuración, usar el botón 🗑️ en la interfaz
- También pueden eliminarse manualmente borrando el archivo .json

BACKUP:
-------
Se recomienda hacer backup periódico de este directorio para preservar
las configuraciones personalizadas creadas por los usuarios.

═══════════════════════════════════════════════════════════════════
