import pymysql

def obtener_conexion():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='', # Cambia esto si tu MySQL tiene contraseña
        database='centinela_db',
        cursorclass=pymysql.cursors.DictCursor
    )