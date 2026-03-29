import os
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from models import db, Device, User
from flask_cors import CORS
from datetime import datetime
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'devnet-secret-key-123')
CORS(app)

# Database configuration
db_user = os.getenv('POSTGRES_USER', 'user')
db_password = os.getenv('POSTGRES_PASSWORD', 'password')
db_name = os.getenv('POSTGRES_DB', 'netmon_db')
db_host = os.getenv('DB_HOST', 'db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Login Manager configuration
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize database
with app.app_context():
    db.create_all()
    # Create a default admin user if none exists
    if User.query.filter_by(username='admin').first() is None:
        admin = User(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        
    # Add some default devices for testing if none exist
    if Device.query.count() == 0:
        default_devices = [
            Device(name="Google DNS", ip_address="8.8.8.8"),
            Device(name="Cloudflare DNS", ip_address="1.1.1.1"),
            Device(name="ISI Keur Massar", ip_address="isi.sn")
        ]
        db.session.add_all(default_devices)
        db.session.commit()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html', user=current_user)

@app.route('/api/devices', methods=['GET'])
@login_required
def get_devices():
    devices = Device.query.all()
    return jsonify([device.to_dict() for device in devices])

@app.route('/api/devices', methods=['POST'])
@login_required
def add_device():
    data = request.get_json()
    new_device = Device(name=data['name'], ip_address=data['ip_address'])
    db.session.add(new_device)
    db.session.commit()
    return jsonify(new_device.to_dict()), 201

@app.route('/api/devices/<int:device_id>', methods=['DELETE'])
@login_required
def delete_device(device_id):
    device = Device.query.get_or_404(device_id)
    db.session.delete(device)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
