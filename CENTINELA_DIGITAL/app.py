import os
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)

# Llave secreta configurable por variables de entorno para producción
app.secret_key = os.environ.get('SECRET_KEY', 'centinela_digital_secret_key_2026')

# Base de datos en memoria (Sustituir por base de datos SQL en etapa avanzada)
ALERTAS_RECIENTES = [
    {
        "id": 1,
        "titulo": "Campaña masiva de Phishing bancario vía SMS",
        "categoria": "Fraude Financiero",
        "nivel": "Alto",
        "fecha": "2026-10-01",
        "descripcion": "Mensajes falsos solicitando verificación urgente de cuenta bancaria mediante un enlace malicioso."
    },
    {
        "id": 2,
        "titulo": "Robo de cuentas de WhatsApp mediante código de verificación",
        "categoria": "Suplantación de Identidad",
        "nivel": "Medio",
        "fecha": "2026-09-30",
        "descripcion": "Llamadas solicitando un código enviado por SMS para supuestamente confirmar un servicio o entrega."
    }
]

REPORTES_CIUDADANOS = []

@app.route('/')
def index():
    """Página principal con Dashboard de alertas y estadísticas."""
    total_reportes = len(REPORTES_CIUDADANOS) + 128
    return render_template('index.html', alertas=ALERTAS_RECIENTES, total_reportes=total_reportes)

@app.route('/reportar', methods=['GET', 'POST'])
def reportar():
    """Ruta para recibir y procesar los reportes ciudadanos."""
    if request.method == 'POST':
        tipo_incidente = request.form.get('tipo_incidente')
        descripcion = request.form.get('descripcion')
        contacto = request.form.get('contacto', 'Anónimo')
        
        nuevo_reporte = {
            "id": len(REPORTES_CIUDADANOS) + 1,
            "tipo": tipo_incidente,
            "descripcion": descripcion,
            "contacto": contacto if contacto.strip() else 'Anónimo',
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        REPORTES_CIUDADANOS.append(nuevo_reporte)
        flash('¡Reporte registrado exitosamente! El equipo técnico revisará el incidente.', 'success')
        return redirect(url_for('reportar'))

    return render_template('reportar.html')

@app.route('/educacion')
def educacion():
    """Portal educativo de prevención y ciberseguridad."""
    return render_template('educacion.html')

if __name__ == '__main__':
    # Obtener el puerto desde el entorno de Render o usar 5000 por defecto
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)