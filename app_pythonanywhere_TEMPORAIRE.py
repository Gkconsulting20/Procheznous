from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import sqlite3
import bcrypt
import os
import secrets
from datetime import datetime, timedelta
from utils import normalize_phone_number, validate_phone_number, format_phone_display
from fedapay_service import fedapay_service
from email_service import email_service
from sms_service import sms_service

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

UPLOAD_FOLDER = 'static/documents_verification'
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db():
    # Chemin pour PythonAnywhere
    db_path = 'pro_chez_nous.db'  # NOM DU FICHIER SUR PYTHONANYWHERE
    if not os.path.exists(db_path):
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def get_categories():
    """TEMPORAIRE : Liste hardcodée compatible avec l'ancienne base"""
    try:
        conn = get_db()
        categories = conn.execute('SELECT nom FROM categories WHERE actif = 1 ORDER BY ordre ASC').fetchall()
        return [cat['nom'] for cat in categories]
    except:
        # Fallback si table categories n'existe pas
        return [
            'Plomberie', 'Électricité', 'Peinture', 'Menuiserie', 
            'Maçonnerie', 'Carrelage', 'Climatisation', 'Jardinage',
            'Nettoyage', 'Déménagement', 'Sécurité', 'Rénovation'
        ]

@app.context_processor
def inject_user_features():
    """TEMPORAIRE : Compatible avec ancienne et nouvelle base"""
    has_messages = False
    has_devis = False
    
    if 'user_id' in session:
        try:
            conn = get_db()
            user_id = session['user_id']
            
            # Essayer avec nouveaux noms de colonnes
            try:
                conversations = conn.execute('''
                    SELECT COUNT(*) as count FROM messages 
                    WHERE sender_id = ? OR receiver_id = ?
                ''', (user_id, user_id)).fetchone()
                has_messages = conversations['count'] > 0
            except:
                # Fallback avec anciens noms
                try:
                    conversations = conn.execute('''
                        SELECT COUNT(*) as count FROM messages 
                        WHERE expediteur_id = ? OR destinataire_id = ?
                    ''', (user_id, user_id)).fetchone()
                    has_messages = conversations['count'] > 0
                except:
                    pass
            
            # Vérifier table devis si elle existe
            try:
                devis_count = conn.execute('''
                    SELECT COUNT(*) as count FROM devis 
                    WHERE client_id = ? OR pro_id = ?
                ''', (user_id, user_id)).fetchone()
                has_devis = devis_count['count'] > 0
            except:
                has_devis = False
        except:
            pass
    
    return dict(has_messages=has_messages, has_devis=has_devis)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    categories = get_categories()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '').strip()
        role = request.form.get('role', '').strip()
        localisation = request.form.get('localisation', '').strip()
        pays = request.form.get('pays', 'Togo').strip()
        categorie = request.form.get('categorie', '').strip() if role == 'pro' else None
        
        if not name or not password or not role:
            flash('Tous les champs obligatoires doivent être remplis', 'error')
            return render_template('register.html', categories=categories)
        
        if not email and not phone:
            flash('Veuillez fournir un email OU un numéro de téléphone', 'error')
            return render_template('register.html', categories=categories)
        
        if phone:
            if not validate_phone_number(phone):
                flash('Numéro de téléphone invalide. Format attendu: +228XXXXXXXX ou 90XXXXXX', 'error')
                return render_template('register.html', categories=categories)
            phone = normalize_phone_number(phone)
        
        conn = get_db()
        
        if email:
            existing_user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
            if existing_user:
                flash('Cette adresse email est déjà utilisée', 'error')
                return render_template('register.html', categories=categories)
        
        if phone:
            existing_user = conn.execute('SELECT * FROM users WHERE phone = ?', (phone,)).fetchone()
            if existing_user:
                flash('Ce numéro de téléphone est déjà utilisé', 'error')
                return render_template('register.html', categories=categories)
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        conn.execute('INSERT INTO users (name, email, phone, password, role, localisation, pays, categorie) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                     (name, email if email else None, phone if phone else None, hashed_password, role, localisation, pays, categorie))
        conn.commit()
        flash('Inscription réussie! Vous pouvez maintenant vous connecter', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', categories=categories)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        password = request.form.get('password', '').strip()
        
        if not identifier or not password:
            flash('Veuillez remplir tous les champs', 'error')
            return render_template('login.html')
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE email = ? OR phone = ?', (identifier, identifier)).fetchone()
        
        if user:
            # Vérifier statut_compte si la colonne existe
            try:
                if user['statut_compte'] == 'bloque':
                    flash('Votre compte a été bloqué. Contactez l\'administrateur.', 'error')
                    return render_template('login.html')
            except:
                pass  # Colonne n'existe pas encore
            
            if bcrypt.checkpw(password.encode('utf-8'), user['password']):
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                session['role'] = user['role']
                session['plan'] = user.get('plan', 'gratuit')  # Défaut gratuit
                flash(f'Bienvenue {user["name"]} !', 'success')
                return redirect(url_for('dashboard'))
        
        flash('Identifiant ou mot de passe incorrect', 'error')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    user_id = session['user_id']
    
    if session['role'] == 'user':
        # COMPATIBLE avec ancienne structure
        rdvs = conn.execute('''
            SELECT r.id, r.date, s.heure_debut, s.heure_fin, u.name as pro_name, u.categorie
            FROM rendezvous r
            JOIN slots s ON r.slot_id = s.id
            JOIN users u ON s.pro_id = u.id
            WHERE r.client_id = ?
            ORDER BY r.date DESC
        ''', (user_id,)).fetchall()
        return render_template('dashboard_user.html', rendezvous=rdvs)
    
    else:
        slots = conn.execute('SELECT * FROM slots WHERE pro_id = ? ORDER BY date DESC', (user_id,)).fetchall()
        rdvs = conn.execute('''
            SELECT r.id, r.date, s.heure_debut, s.heure_fin, u.name as client_name, u.email, u.phone
            FROM rendezvous r
            JOIN slots s ON r.slot_id = s.id
            JOIN users u ON r.client_id = u.id
            WHERE s.pro_id = ?
            ORDER BY r.date DESC
        ''', (user_id,)).fetchall()
        
        # Stats basiques
        total_rdv = len(rdvs)
        
        return render_template('dashboard_pro.html', slots=slots, rendezvous=rdvs, total_rdv=total_rdv)

# COPIER LE RESTE DES ROUTES DEPUIS L'ANCIEN app.py de PythonAnywhere
# Cette version temporaire corrige uniquement les incompatibilités critiques

if __name__ == '__main__':
    app.run(debug=True)
