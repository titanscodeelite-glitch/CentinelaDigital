from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_sentinela_2026'

# Configuración de la Base de Datos MySQL (usando variables de entorno o valores por defecto para pruebas locales)
mysql_user = os.environ.get('MYSQL_USER', 'tu_usuario')
mysql_password = os.environ.get('MYSQL_PASSWORD', 'tu_contrasena')
mysql_host = os.environ.get('MYSQL_HOST', 'localhost')
mysql_db = os.environ.get('MYSQL_DB', 'sentinela_db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo para guardar los reportes o mensajes de ayuda de forma segura en MySQL
class Reporte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=True)
    contacto = db.Column(db.String(150), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)

# Crear las tablas automáticamente al iniciar la app si no existen
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reportar', methods=['POST'])
def reportar():
    nombre = request.form.get('nombre', 'Anónimo')
    contacto = request.form.get('contacto')
    mensaje = request.form.get('mensaje')

    if not contacto or not mensaje:
        return "Por favor completa los campos obligatorios.", 400

    nuevo_reporte = Reporte(nombre=nombre, contacto=contacto, mensaje=mensaje)
    db.session.add(nuevo_reporte)
    db.session.commit()

    return render_template('index.html', enviado=True)

if __name__ == '__main__':
    app.run(debug=True)
