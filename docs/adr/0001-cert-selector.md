# ADR 0001 — Selector de certificación y creación desde la UI

## Contexto
La app usa/crea la certificación del mes activo sin permitir elegir ni crear manualmente.

## Decisión
- Añadir un **ComboBox** en la UI para elegir certificación.
- Opción **“➕ Nueva certificación…”** en el combo.
- Backend:
  - `list_certifications(user, password, schema)`
  - `create_new_certification(user, password, schema, cert_name, gg_pct, bi_pct)`

## Consecuencias
- Permite certificar meses anteriores o escenarios alternativos.
- A corto plazo, mantenemos “una tabla por certificación”.
- A medio plazo, evaluar modelo normalizado (tabla `cert` + `cert_line`).
