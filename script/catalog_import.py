import pandas as pd
import mysql.connector
from mysql.connector import Error
from .db_config import get_config


def catalog_import(user, password, schema,file_path):
    # Leer el archivo Excel
    xl = pd.ExcelFile(file_path)

    # Leer las hojas del Excel
    df_cata_hidra = xl.parse("tbl_catalogo_hidraulica")
    df_cata_hidra_familia = xl.parse("tbl_cata_hidra_familia")
    df_cata_hidra_tipo = xl.parse("tbl_cata_hidra_tipo")
    df_cata_hidra_marcas = xl.parse("tbl_cata_hidra_marcas")
    df_cata_hidra_caracteristica = xl.parse("tbl_cata_hidra_caracteristica")
    df_cata_hidra_dni = xl.parse("tbl_cata_hidra_dni")
    df_cata_hidra_dnf = xl.parse("tbl_cata_hidra_dnf")
    df_cata_hidra_pn = xl.parse("tbl_cata_hidra_pn")
    df_cata_hidra_angulo = xl.parse("tbl_cata_hidra_angulo")
    df_cata_regis = xl.parse("tbl_catalogo_registros")
    df_cata_regis_tipo = xl.parse("tbl_cata_regis_tipo")
    df_cata_regis_proveedor = xl.parse("tbl_cata_regis_proveedor")

    df_cata_hidra = df_cata_hidra.fillna('-')
    df_cata_regis = df_cata_regis.fillna('-')

    # Crear diccionarios para mapear naturaleza y unidades
    hidra_familia_dict = {row['familia']: idx + 1 for idx, row in df_cata_hidra_familia.iterrows()}
    hidra_tipo_dict = {row['elemento']: idx + 1 for idx, row in df_cata_hidra_tipo.iterrows()}
    hidra_marcas_dict =  {row['marca']: idx + 1 for idx, row in df_cata_hidra_marcas.iterrows()}
    hidra_caracteristica_dict = {row['caracteristica']: idx + 1 for idx, row in df_cata_hidra_caracteristica.iterrows()}
    hidra_dni_dict = {row['dni']: idx + 1 for idx, row in df_cata_hidra_dni.iterrows()}
    hidra_dnf_dict = {row['dnf']: idx + 1 for idx, row in df_cata_hidra_dnf.iterrows()}
    hidra_pn_dict = {row['pn']: idx + 1 for idx, row in df_cata_hidra_pn.iterrows()}
    hidra_angulo_dict = {row['angulo']: idx + 1 for idx, row in df_cata_hidra_angulo.iterrows()}
    regis_tipo_dict = {row['tipo']: idx + 1 for idx, row in df_cata_regis_tipo.iterrows()}
    regis_proveedor_dict = {row['proveedor']: idx + 1 for idx, row in df_cata_regis_proveedor.iterrows()}


    # Reemplazar familia en tbl_cata_hidra_tipo
    df_cata_hidra_tipo['id_familia'] = df_cata_hidra_tipo['familia'].map(hidra_familia_dict)
    df_cata_hidra_tipo = df_cata_hidra_tipo.drop(columns=['familia'])

    # Reemplazar familia, tipo, marca, caracteristica, dni, dnf, pn y angulo  en tbl_catalogo_hidraulica
    df_cata_hidra['id_familia'] = df_cata_hidra['familia'].map(hidra_familia_dict)
    df_cata_hidra['id_tipo'] = df_cata_hidra['tipo'].map(hidra_tipo_dict)
    df_cata_hidra['id_marca'] = df_cata_hidra['marca'].map(hidra_marcas_dict)
    df_cata_hidra['id_caracteristica'] = df_cata_hidra['caracteristica'].map(hidra_caracteristica_dict)
    df_cata_hidra['id_dni'] = df_cata_hidra['dni'].map(hidra_dni_dict)
    df_cata_hidra['id_dnf'] = df_cata_hidra['dnf'].map(hidra_dnf_dict)
    df_cata_hidra['id_pn'] = df_cata_hidra['pn'].map(hidra_pn_dict)
    df_cata_hidra['id_angulo'] = df_cata_hidra['angulo'].map(hidra_angulo_dict)
    df_cata_hidra = df_cata_hidra.drop(columns=['familia', 'tipo', 'marca', 'caracteristica', 'dni', 'dnf', 'pn', 'angulo'])

    # Reemplazar  tipo,y proveedor  en tbl_catalogo_hidraulica
    df_cata_regis['id_tipo'] = df_cata_regis['tipo'].map(regis_tipo_dict)
    df_cata_regis['id_proveedor'] = df_cata_regis['proveedor'].map(regis_proveedor_dict)
    df_cata_regis = df_cata_regis.drop(columns=['tipo','proveedor'])


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

        cursor.execute("ALTER TABLE tbl_catalogo_hidraulica AUTO_INCREMENT = 1;")
        # Insertar datos en tbl_catalogo_hidraulica
        for index, row in df_cata_hidra.iterrows():
            print(row)
            cursor.execute("""INSERT INTO tbl_catalogo_hidraulica (id_familia, id_tipo_hidraulica, id_marca, id_caracteristica, modelo, referencia, id_dni, id_dnf, id_pn, id_angulo, longitud,long_extremos, altura_eje, altura_total, peso, bloque_ref, descripcion, cod_partida) 
                           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (row['id_familia'],row['id_tipo'],row['id_marca'],row['id_caracteristica'],row['modelo'],row['referencia'],row['id_dni'],row['id_dnf'],row['id_pn'],row['id_angulo'],row['longitud'],row['long_extremos'],row['altura_eje'],row['altura_total'],row['peso'],row['bloque_ref'],row['descripcion'],row['cod_partida']))

        cursor.execute("ALTER TABLE tbl_cata_hidra_familia AUTO_INCREMENT = 1;")
        # Insertar datos en tbl_cata_hidra_familia
        for index, row in df_cata_hidra_familia.iterrows():
            cursor.execute("INSERT INTO tbl_cata_hidra_familia (familia) VALUES (%s)", (row['familia'],))

        cursor.execute("ALTER TABLE tbl_cata_hidra_tipo AUTO_INCREMENT = 1;")
        # Insertar datos en tbl_cata_hidra_tipo
        for index, row in df_cata_hidra_tipo.iterrows():
            cursor.execute("INSERT INTO tbl_cata_hidra_tipo (id_familia, tipo_elemento) VALUES (%s, %s)",
                           (row['id_familia'], row['elemento'],))

        cursor.execute("ALTER TABLE tbl_cata_hidra_marcas AUTO_INCREMENT = 1;")
        # Insertar datos en tbl_cata_hidra_marcas
        for index, row in df_cata_hidra_marcas.iterrows():
            cursor.execute("INSERT INTO tbl_cata_hidra_marcas (marca) VALUES (%s)", (row['marca'],))

        cursor.execute("ALTER TABLE tbl_cata_hidra_caracteristica AUTO_INCREMENT = 1;")
        # Insertar datos en tbl_cata_hidra_caracteristica
        for index, row in df_cata_hidra_caracteristica.iterrows():
            cursor.execute("INSERT INTO tbl_cata_hidra_caracteristica (caracteristica) VALUES (%s)", (row['caracteristica'],))

        cursor.execute("ALTER TABLE tbl_cata_hidra_dni AUTO_INCREMENT = 1;")
        # Insertar datos en tbl_cata_hidra_dni
        for index, row in df_cata_hidra_dni.iterrows():
            cursor.execute("INSERT INTO tbl_cata_hidra_dni (dni) VALUES (%s)", (row['dni'],))

        cursor.execute("ALTER TABLE tbl_cata_hidra_dnf AUTO_INCREMENT = 1;")
        # Insertar datos en tbl_cata_hidra_dnf
        for index, row in df_cata_hidra_dnf.iterrows():
            cursor.execute("INSERT INTO tbl_cata_hidra_dnf (dnf) VALUES (%s)", (row['dnf'],))

        cursor.execute("ALTER TABLE tbl_cata_hidra_pn AUTO_INCREMENT = 1;")
        # Insertar datos en tbl_cata_hidra_pn
        for index, row in df_cata_hidra_pn.iterrows():
            cursor.execute("INSERT INTO tbl_cata_hidra_pn (pn) VALUES (%s)", (row['pn'],))

        cursor.execute("ALTER TABLE tbl_cata_hidra_angulo AUTO_INCREMENT = 1;")
        # Insertar datos en tbl_cata_hidra_pn
        for index, row in df_cata_hidra_angulo.iterrows():
            cursor.execute("INSERT INTO tbl_cata_hidra_angulo (angulo) VALUES (%s)", (row['angulo'],))

        cursor.execute("ALTER TABLE tbl_catalogo_registros AUTO_INCREMENT = 1;")
        # Insertar datos en tbl_catalogo_registros
        for index, row in df_cata_regis.iterrows():
            cursor.execute("""INSERT INTO tbl_catalogo_registros (id_tipo_registro, id_proveedor, modelo, referencia, dimensionA, dimensionB, dimensionC, descripcion, cod_partida) 
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (row['id_tipo'], row['id_proveedor'], row['modelo'], row['referencia'], row['dimensionA'], row['dimensionB'], row['dimensionC'], row['descripcion'],row['cod_partida']))

        cursor.execute("ALTER TABLE tbl_cata_regis_tipo AUTO_INCREMENT = 1;")
        # Insertar datos en tbl_cata_regis_tipo
        for index, row in df_cata_regis_tipo.iterrows():
            cursor.execute("INSERT INTO tbl_cata_regis_tipo (tipo) VALUES (%s)", (row['tipo'],))

        cursor.execute("ALTER TABLE tbl_cata_regis_proveedor AUTO_INCREMENT = 1;")
        # Insertar datos en tbl_cata_regis_proveedor
        for index, row in df_cata_regis_proveedor.iterrows():
            cursor.execute("INSERT INTO tbl_cata_regis_proveedor (proveedor) VALUES (%s)", (row['proveedor'],))


        # Confirmar los cambios y cerrar la conexión
        conn.commit()
        cursor.close()
        conn.close()
        return "ok"
    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return e

