import pymysql

host = '193.144.42.124'
usuario = 'Vanesa'
contraseña = '1Super-Password'
base_de_datos = 'inferno'
puerto = 33306

def showTable(table_name):
    conexion = pymysql.connect(
    host=host,
    port=puerto,
    user=usuario,
    password=contraseña,
    database=base_de_datos
    )

    try:
        with conexion.cursor() as cursor:
            cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            nombres_columnas = [columna[0] for columna in cursor.fetchall()]
            print(", ".join(nombres_columnas))

            cursor.execute(f"SELECT * FROM {table_name}")
            resultados = cursor.fetchall()
            for fila in resultados:
                print(fila)
    finally:
        conexion.close()

def getDestinyLevel(name):
    conexion = pymysql.connect(
    host=host,
    port=puerto,
    user=usuario,
    password=contraseña,
    database=base_de_datos
    )

    try:
        with conexion.cursor() as cursor:
            sql = f"SELECT nivel, nome_nivel FROM admision WHERE nome LIKE '{name}'"
            cursor.execute(sql)
            resultados = cursor.fetchall()
            for resultado in resultados:
                return resultado
    finally:
        conexion.close()

def showDestiny(name):
    nivel, nome_nivel = getDestinyLevel(name)
    return f'O teu nivel no inferno é o {nivel}, pecas de {nome_nivel}.' if nivel != 1 else f'O teu nivel no inferno é o {nivel}, estás no {nome_nivel}.'