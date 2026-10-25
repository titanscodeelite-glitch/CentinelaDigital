import os
from flask import Flask, render_template, request, redirect, url_for
from database.bd import obtener_conexion

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')
STATIC_DIR = os.path.join(BASE_DIR, 'frontend', 'static')

app = Flask(__name__, template_folder=FRONTEND_DIR, static_folder=STATIC_DIR)

# 1. La ruta raíz ahora muestra el Dashboard/Bienvenida principal con los botones
@app.route('/')
def inicio():
    return render_template('dashboard_inicio.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']
        
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE correo = %s AND password = %s", (correo, password))
            usuario = cursor.fetchone()
        conexion.close()
        
        if usuario:
            return redirect(url_for('panel_reportes'))
        else:
            return "Datos incorrectos. <a href='/login'>Volver</a>"
            
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        password = request.form['password']
        
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO usuarios (nombre, correo, password) VALUES (%s, %s, %s)", (nombre, correo, password))
            conexion.commit()
        conexion.close()
        
        return redirect(url_for('login'))
        
    return render_template('registro.html')

# Panel de reportes interno una vez logueado
@app.route('/dashboard', methods=['GET', 'POST'])
def panel_reportes():
    conexion = obtener_conexion()
    
    if request.method == 'POST':
        incidente = request.form['incidente']
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO reportes (incidente) VALUES (%s)", (incidente,))
            conexion.commit()
            
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM reportes ORDER BY id DESC")
        reportes = cursor.fetchall()
    conexion.close()
    
    return render_template('dashboard_inicio.html', reportes=reportes)

if __name__ == '__main__':
    app.run(debug=True, port=5000)