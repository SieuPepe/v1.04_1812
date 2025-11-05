"""
Módulo de base de datos refactorizado.

Este archivo mantiene compatibilidad con el código existente re-exportando
todas las funciones de los módulos especializados:
- db_core.py: Funciones de conexión, autenticación y gestión base
- db_projects.py: Gestión de proyectos, clientes y presupuestos
- db_partes.py: Gestión de partes de trabajo

Para usar las funciones directamente desde los módulos especializados:
    from script.db_core import login_db, get_schemas_db
    from script.db_projects import add_project_item
    from script.db_partes import add_parte_with_code

Para mantener compatibilidad con código existente:
    from script.modulo_db import login_db, add_project_item
"""

# Re-exportar todas las funciones de db_core
from .db_core import (
    # Autenticación y conexión
    login_db,
    manager_db,
    user_db,

    # Gestión de esquemas
    get_schemas_db,
    get_table_schemas_db,
    create_schemas_db,
    create_tables_schema_db,
    copy_tables_schema_db,
    create_locality_schema_db,
    create_view_projects,
    create_view_catalog,
    create_view_economic,
    create_view_inventory,
    create_view_partes,
    create_fk,
    update_reference,

    # Gestión de ubicaciones
    get_ccaa_bd,
    get_id_ccaa_bd,
    get_id_province_bd,
    get_code_ccaa_bd,
    get_province_bd,

    # Funciones genéricas CRUD
    get_id_item_bd,
    get_id_item_sub_bd,
    get_item_id_bd,
    get_option_item_bd,
    get_option_item_sub_bd,
    get_all_bd,
    get_filter_data_bd,
    get_multifilter_data_bd,
    get_field_bd,
    add_item_aux,
    add_item_type_aux,
    mod_item_aux,
    sum_field_bd,
    sum_field_filter_bd,

    # Gestión de usuarios BD
    get_user_db,
    create_user_bd,
    create_pass,
    user_verfication,
    change_pass_user,

    # Gestión de privilegios
    add_privileges,
    revoke_privileges,
)

# Re-exportar todas las funciones de db_projects
from .db_projects import (
    # Proyectos
    project_directory_db,
    add_project_item,
    add_economic_project_item,
    mod_project_item,

    # Clientes
    add_customer_item,
    get_customer_data,
    mod_customer_item,

    # Usuarios de clientes
    get_user_customer_data,
    get_id_user_customer,
    add_user_customer_item,
    mod_user_customer_item,

    # Usuarios de empresa
    get_id_user_company,
    add_user_company_item,
    mod_user_company_item,
    get_user_company_data,

    # Catálogos
    add_catalog_hidro_item,
    mod_catalog_hidro_item,
    add_catalog_regis_item,
    mod_catalog_regis_item,

    # Registros/Inventario
    add_register_item,
    mod_register_item,
    add_register_elements,
    delete_register_item,
    delete_register_budget_items,
    mod_register_data,
    close_register_data,

    # Fotografías
    add_photo_register,
    add_photo_site_register,
    mod_photo_site_register,

    # Presupuestos
    mod_amount_budget_item,
    add_budget_item,
    import_budget_items,
    delete_budget_item,
    mod_amount_cost_item,
    delete_cost_item,
    cert_cost_item,
    add_cost_item,
    mod_item_budget,
    add_item_chapter,
    add_item_budget,
    add_group_budget,
    add_item_group_budget,
    mod_amount_group_item,
    delete_group_item,
)

# Re-exportar todas las funciones de db_partes
from .db_partes import (
    # Dimensiones
    get_dim_all,
    _guess_text_column,
    _fetch_dim_list_guess,
    add_dim_ot,
    get_all_dim_ot,
    delete_dim_ot,

    # Gestión de partes
    add_parte_with_code,
    list_partes,
    get_parts_list,
    delete_parte,
    get_partes_resumen,
    get_parte_detail,
    mod_parte_item,

    # Presupuesto de partes
    get_part_presupuesto,
    add_part_presupuesto_item,
    mod_amount_part_budget_item,
    delete_part_presupuesto_item,

    # Certificaciones de partes
    get_part_cert_pendientes,
    get_part_cert_certificadas,
    add_part_cert_item,
    cert_part_item,
    delete_part_cert_item,
    cert_parte_completo,

    # Formulario mejorado de partes
    add_parte_mejorado,
    get_estados_parte,
    get_provincias,
    get_comarcas_by_provincia,
    get_municipios_by_provincia,
    _get_tipo_trabajo_prefix,
)

# Lista de todas las funciones exportadas (útil para debugging)
__all__ = [
    # db_core
    'login_db', 'manager_db', 'user_db',
    'get_schemas_db', 'get_table_schemas_db', 'create_schemas_db',
    'create_tables_schema_db', 'copy_tables_schema_db', 'create_locality_schema_db',
    'create_view_projects', 'create_view_catalog', 'create_view_economic',
    'create_view_inventory', 'create_fk', 'update_reference',
    'get_ccaa_bd', 'get_id_ccaa_bd', 'get_id_province_bd',
    'get_code_ccaa_bd', 'get_province_bd',
    'get_id_item_bd', 'get_id_item_sub_bd', 'get_item_id_bd',
    'get_option_item_bd', 'get_option_item_sub_bd', 'get_all_bd',
    'get_filter_data_bd', 'get_multifilter_data_bd', 'get_field_bd',
    'add_item_aux', 'add_item_type_aux', 'mod_item_aux',
    'sum_field_bd', 'sum_field_filter_bd',
    'get_user_db', 'create_user_bd', 'create_pass',
    'user_verfication', 'change_pass_user',
    'add_privileges', 'revoke_privileges',

    # db_projects
    'project_directory_db', 'add_project_item', 'add_economic_project_item',
    'mod_project_item', 'add_customer_item', 'get_customer_data',
    'mod_customer_item', 'get_user_customer_data', 'get_id_user_customer',
    'add_user_customer_item', 'mod_user_customer_item', 'get_id_user_company',
    'add_user_company_item', 'mod_user_company_item', 'get_user_company_data',
    'add_catalog_hidro_item', 'mod_catalog_hidro_item', 'add_catalog_regis_item',
    'mod_catalog_regis_item', 'add_register_item', 'mod_register_item',
    'add_register_elements', 'delete_register_item', 'delete_register_budget_items',
    'mod_register_data', 'close_register_data', 'add_photo_register',
    'add_photo_site_register', 'mod_photo_site_register', 'mod_amount_budget_item',
    'add_budget_item', 'import_budget_items', 'delete_budget_item',
    'mod_amount_cost_item', 'delete_cost_item', 'cert_cost_item',
    'add_cost_item', 'mod_item_budget', 'add_item_chapter',
    'add_item_budget', 'add_group_budget', 'add_item_group_budget',
    'mod_amount_group_item', 'delete_group_item',

    # db_partes
    'get_dim_all', '_guess_text_column', '_fetch_dim_list_guess',
    'add_dim_ot', 'get_all_dim_ot', 'delete_dim_ot',
    'add_parte_with_code', 'list_partes', 'get_parts_list',
    'delete_parte', 'get_partes_resumen', 'get_parte_detail',
    'mod_parte_item', 'get_part_presupuesto', 'add_part_presupuesto_item',
    'mod_amount_part_budget_item', 'delete_part_presupuesto_item',
    'get_part_cert_pendientes', 'get_part_cert_certificadas', 'add_part_cert_item',
    'cert_part_item', 'delete_part_cert_item', 'cert_parte_completo',
    'add_parte_mejorado', 'get_estados_parte', 'get_provincias',
    'get_municipios_by_provincia', '_get_tipo_trabajo_prefix',
]
