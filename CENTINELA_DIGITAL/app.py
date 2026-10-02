from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_sentinela_2026'

# Configuración de PostgreSQL (Render provee la variable DATABASE_URL automáticamente)
database_url = os.environ.get('DATABASE_URL', 'sqlite:///sentinela.db')

# Corrección de compatibilidad para URLs de PostgreSQL en Render
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo para guardar los reportes de incidentes en PostgreSQL
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

@app.route('/educacion')
def educacion():
    return render_template('educacion.html')

@app.route('/reportar', methods=['GET', 'POST'])
def reportar():
    if request.method == 'POST':
        nombre = request.form.get('nombre', 'Anónimo')
        contacto = request.form.get('contacto')
        mensaje = request.form.get('mensaje')

        if not contacto or not mensaje:
            return "Por favor completa los campos obligatorios.", 400

        nuevo_reporte = Reporte(nombre=nombre, contacto=contacto, mensaje=mensaje)
        db.session.add(nuevo_reporte)
        db.session.commit()

        return render_template('reportar.html', enviado=True)
    
    return render_template('reportar.html')

if __name__ == '__main__':
    app.run(debug=True)
