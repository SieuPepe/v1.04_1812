import pandas as pd
import mysql.connector
from mysql.connector import Error
from .db_config import get_config


def budget_import(user, password, schema,file_path):
    # Leer el archivo Excel
    xl = pd.ExcelFile(file_path)

    # Leer las hojas del Excel
    df_capitulos = xl.parse("tbl_pres_capitulos")
    df_precios = xl.parse("tbl_pres_precios")
    df_naturaleza = xl.parse("tbl_pres_naturaleza")
    df_unidades = xl.parse("tbl_pres_unidades")

    #rellenar nulos
    df_capitulos = df_capitulos.fillna('-')
    df_precios = df_precios.fillna('-')

    # Crear diccionarios para mapear naturaleza y unidades
    naturaleza_dict = {row['tipo']: idx + 1 for idx, row in df_naturaleza.iterrows()}
    unidades_dict = {row['unidad']: idx + 1 for idx, row in df_unidades.iterrows()}

    # Reemplazar naturaleza en tbl_pres_capitulos
    df_capitulos['id_naturaleza'] = df_capitulos['naturaleza'].map(naturaleza_dict)
    df_capitulos = df_capitulos.drop(columns=['naturaleza'])

    # Reemplazar naturaleza, unidades y codigo_capitulo en tbl_pres_precios
    df_precios['id_naturaleza'] = df_precios['naturaleza'].map(naturaleza_dict)
    df_precios['id_unidades'] = df_precios['unidades'].map(unidades_dict)
    df_precios = df_precios.drop(columns=['naturaleza', 'unidades'])

    # Ahora relacionamos el código de capítulo con el ID
    capitulos_dict = {row['codigo_capitulo']: idx + 1 for idx, row in df_capitulos.iterrows()}
    df_precios['id_capitulo'] = df_precios['codigo_capitulo'].map(capitulos_dict)
    df_precios = df_precios.drop(columns=['codigo_capitulo'])
    try:
        # Conectar a la base de datos MySQL usando configuración centralizada
        config = get_config()
        conn = mysql.connector.connect(
            host=config.host,
            database=schema,
            port=config.port,
            user=user,
            password=password
        )
        cursor = conn.cursor()

        cursor.execute("ALTER TABLE tbl_pres_naturaleza AUTO_INCREMENT = 1;")
        # Insertar datos en tbl_pres_naturaleza
        for index, row in df_naturaleza.iterrows():
            cursor.execute("INSERT INTO tbl_pres_naturaleza (tipo) VALUES (%s)", (row['tipo'],))

        cursor.execute("ALTER TABLE tbl_pres_unidades AUTO_INCREMENT = 1;")
        # Insertar datos en tbl_pres_unidades
        for index, row in df_unidades.iterrows():
            cursor.execute("INSERT INTO tbl_pres_unidades (unidad) VALUES (%s)", (row['unidad'],))

        cursor.execute("ALTER TABLE tbl_pres_capitulos AUTO_INCREMENT = 1;")
        # Insertar datos en tbl_pres_capitulos
        for index, row in df_capitulos.iterrows():
            cursor.execute("INSERT INTO tbl_pres_capitulos (codigo_capitulo, id_naturaleza, capitulo) VALUES (%s, %s, %s)",
                           (row['codigo_capitulo'], row['id_naturaleza'], row['capitulo']))

        cursor.execute("ALTER TABLE tbl_pres_precios AUTO_INCREMENT = 1;")
        # Insertar datos en tbl_pres_precios
        for index, row in df_precios.iterrows():
            cursor.execute("INSERT INTO tbl_pres_precios (codigo, id_naturaleza, id_unidades, resumen, descripcion, coste, id_capitulo) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (row['codigo_partida'], row['id_naturaleza'], row['id_unidades'], row['resumen'], row['descripcion'], row['coste'], row['id_capitulo']))

        # Confirmar los cambios y cerrar la conexión
        conn.commit()
        cursor.close()
        conn.close()
        return "ok"
    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e