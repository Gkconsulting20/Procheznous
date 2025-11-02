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
    # Chemin absolu pour PythonAnywhere
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    # OPTIMISATIONS PRODUCTION
    conn.execute("PRAGMA journal_mode = WAL")      # Lecture/Écriture simultanées
    conn.execute("PRAGMA synchronous = NORMAL")    # Balance vitesse/sécurité
    conn.execute("PRAGMA cache_size = -64000")     # Cache 64MB
    conn.execute("PRAGMA temp_store = MEMORY")     # Stockage RAM
    
    return conn

def get_categories():
    """Récupère les catégories actives depuis la base de données"""
    conn = get_db()
    categories = conn.execute('SELECT nom FROM categories WHERE actif = 1 ORDER BY ordre ASC').fetchall()
    return [cat['nom'] for cat in categories]

@app.context_processor
def inject_user_features():
    """Injecte les informations sur les fonctionnalités disponibles pour l'utilisateur"""
    has_messages = False
    has_devis = False
    
    if 'user_id' in session:
        try:
            conn = get_db()
            user_id = session['user_id']
            
            # Vérifier si l'utilisateur a des conversations actives (compatible ancien/nouveau format)
            try:
                # Essayer nouveau format (sender_id/receiver_id)
                conversations = conn.execute('''
                    SELECT COUNT(*) as count FROM messages 
                    WHERE sender_id = ? OR receiver_id = ?
                ''', (user_id, user_id)).fetchone()
                has_messages = conversations['count'] > 0
            except:
                # Fallback ancien format (expediteur_id/destinataire_id)
                try:
                    conversations = conn.execute('''
                        SELECT COUNT(*) as count FROM messages 
                        WHERE expediteur_id = ? OR destinataire_id = ?
                    ''', (user_id, user_id)).fetchone()
                    has_messages = conversations['count'] > 0
                except:
                    has_messages = False
            
            # Vérifier si l'utilisateur a des devis
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
        
        normalized_phone = normalize_phone_number(identifier) if '@' not in identifier else None
        
        conn = get_db()
        
        if normalized_phone:
            user = conn.execute('SELECT * FROM users WHERE email = ? OR phone = ? OR phone = ?', 
                              (identifier, identifier, normalized_phone)).fetchone()
        else:
            user = conn.execute('SELECT * FROM users WHERE email = ? OR phone = ?', 
                              (identifier, identifier)).fetchone()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8') if isinstance(user['password'], str) else user['password']):
            # Vérifier si le compte est bloqué
            statut = user['statut_compte'] if 'statut_compte' in user.keys() else 'actif'
            if statut == 'bloque':
                flash('Votre compte a été bloqué. Veuillez contacter l\'administrateur.', 'error')
                return render_template('login.html')
            
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['plan'] = user['plan']
            flash(f'Bienvenue {user["name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email/Téléphone ou mot de passe incorrect', 'error')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: return redirect(url_for('login'))
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    if user['role'] == 'pro':
        rdvs = conn.execute('''
            SELECT r.id, s.date, s.heure, u.name as client 
            FROM rendezvous r
            JOIN slots s ON r.slot_id = s.id
            JOIN users u ON r.client_id = u.id 
            WHERE s.user_id = ?
            ORDER BY s.date DESC, s.heure DESC
        ''', (user['id'],)).fetchall()
        return render_template('dashboard_pro.html', user=user, rdvs=rdvs)
    else:
        rdvs = conn.execute('''
            SELECT r.id, s.date, s.heure, u.name as pro_name 
            FROM rendezvous r
            JOIN slots s ON r.slot_id = s.id
            JOIN users u ON s.user_id = u.id 
            WHERE r.client_id = ?
            ORDER BY s.date DESC, s.heure DESC
        ''', (user['id'],)).fetchall()
        return render_template('dashboard_user.html', user=user, rdvs=rdvs)

@app.route('/professionals')
def view_professionals():
    conn = get_db()
    categories = get_categories()
    
    search = request.args.get('search', '').strip()
    ville = request.args.get('ville', '').strip()
    note_min = request.args.get('note_min', '').strip()
    categorie = request.args.get('categorie', '').strip()
    
    query = '''
        SELECT u.id, u.name, u.localisation, u.categorie, u.plan, u.statut_verification,
               COALESCE(AVG(a.note), 0) as note_moyenne,
               COUNT(a.id) as nb_avis
        FROM users u
        LEFT JOIN avis a ON u.id = a.pro_id
        WHERE u.role = 'pro'
    '''
    
    params = []
    
    if search:
        query += ' AND u.name LIKE ?'
        params.append(f'%{search}%')
    
    if ville:
        query += ' AND u.localisation LIKE ?'
        params.append(f'%{ville}%')
    
    if categorie:
        query += ' AND u.categorie = ?'
        params.append(categorie)
    
    query += ' GROUP BY u.id'
    
    if note_min:
        query += ' HAVING note_moyenne >= ?'
        params.append(float(note_min))
    
    query += ' ORDER BY note_moyenne DESC'
    
    pros = conn.execute(query, params).fetchall()
    
    user = None
    if 'user_id' in session:
        user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    
    return render_template('professionals.html', professionals=pros, categories=categories, user=user)

@app.route('/professionals_nearby')
def professionals_nearby():
    if 'user_id' not in session:
        flash('Veuillez vous connecter pour accéder à cette fonctionnalité', 'error')
        return redirect(url_for('login'))
    
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    
    if user['plan'] != 'premium':
        flash('La géolocalisation est réservée aux membres Premium! Passez à Premium pour trouver les professionnels près de vous 📍', 'error')
        return redirect(url_for('subscription'))
    
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    
    if not lat or not lon:
        flash('Impossible de récupérer votre position', 'error')
        return redirect(url_for('view_professionals'))
    
    import math
    
    def calculate_distance(lat1, lon1, lat2, lon2):
        if lat2 is None or lon2 is None:
            return float('inf')
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
    
    categories = get_categories()
    
    pros = conn.execute('''
        SELECT u.id, u.name, u.localisation, u.categorie, u.plan, u.statut_verification, u.latitude, u.longitude,
               COALESCE(AVG(a.note), 0) as note_moyenne,
               COUNT(a.id) as nb_avis
        FROM users u
        LEFT JOIN avis a ON u.id = a.pro_id
        WHERE u.role = 'pro'
        GROUP BY u.id
    ''').fetchall()
    
    pros_with_distance = []
    for pro in pros:
        distance = calculate_distance(lat, lon, pro['latitude'], pro['longitude'])
        pros_with_distance.append({
            'id': pro['id'],
            'name': pro['name'],
            'localisation': pro['localisation'],
            'categorie': pro['categorie'],
            'plan': pro['plan'],
            'statut_verification': pro['statut_verification'],
            'note_moyenne': pro['note_moyenne'],
            'nb_avis': pro['nb_avis'],
            'distance': distance
        })
    
    pros_with_distance.sort(key=lambda x: x['distance'])
    
    return render_template('professionals.html', professionals=pros_with_distance, categories=categories, user=user, nearby_mode=True)

@app.route('/book/<int:pro_id>', methods=['GET', 'POST'])
def book(pro_id):
    if 'user_id' not in session: return redirect(url_for('login'))
    conn = get_db()
    if request.method == 'POST':
        slot_id = request.form['slot_id']
        conn.execute('INSERT INTO rendezvous (pro_id, client_id, date) SELECT pro_id, ?, date FROM slots WHERE id = ?',
                     (session['user_id'], slot_id))
        conn.execute('DELETE FROM slots WHERE id = ?', (slot_id,))
        conn.commit()
        flash('Rendez-vous réservé avec succès!', 'success')
        return redirect(url_for('dashboard'))
    pro = conn.execute('SELECT * FROM users WHERE id = ?', (pro_id,)).fetchone()
    slots = conn.execute('SELECT * FROM slots WHERE pro_id = ?', (pro_id,)).fetchall()
    return render_template('book.html', pro=pro, slots=slots)

@app.route('/add_slot', methods=['GET', 'POST'])
def add_slot():
    if 'user_id' not in session or session['role'] != 'pro':
        return redirect(url_for('login'))
    if request.method == 'POST':
        conn = get_db()
        conn.execute('INSERT INTO slots (pro_id, date) VALUES (?, ?)',
                     (session['user_id'], request.form['date']))
        conn.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_slot.html')

@app.route('/rate/<int:pro_id>', methods=['GET', 'POST'])
def rate(pro_id):
    if 'user_id' not in session or session['role'] != 'user':
        return redirect(url_for('login'))
    conn = get_db()
    if request.method == 'POST':
        from datetime import datetime
        note = request.form['note']
        commentaire = request.form.get('commentaire', '')
        conn.execute('INSERT INTO avis (pro_id, client_id, note, commentaire, date) VALUES (?, ?, ?, ?, ?)',
                     (pro_id, session['user_id'], note, commentaire, datetime.now().strftime('%Y-%m-%d')))
        conn.commit()
        return redirect(url_for('view_professionals'))
    pro = conn.execute('SELECT * FROM users WHERE id = ?', (pro_id,)).fetchone()
    return render_template('rate.html', pro=pro)

@app.route('/cancel_rdv/<int:rdv_id>', methods=['POST'])
def cancel_rdv(rdv_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    rdv = conn.execute('SELECT * FROM rendezvous WHERE id = ?', (rdv_id,)).fetchone()
    
    if rdv and (rdv['client_id'] == session['user_id'] or rdv['pro_id'] == session['user_id']):
        conn.execute('INSERT INTO slots (pro_id, date) VALUES (?, ?)', (rdv['pro_id'], rdv['date']))
        conn.execute('DELETE FROM rendezvous WHERE id = ?', (rdv_id,))
        conn.commit()
        flash('Rendez-vous annulé avec succès. Le créneau est à nouveau disponible.', 'success')
    else:
        flash('Impossible d\'annuler ce rendez-vous', 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/subscription')
def subscription():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    return render_template('subscription.html', user=user)

@app.route('/upgrade_premium', methods=['GET', 'POST'])
def upgrade_premium():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    
    if request.method == 'POST':
        if not fedapay_service.is_configured():
            flash('⚠️ Les paiements sont temporairement désactivés. Nous configurons actuellement FedaPay pour accepter T-Money, Flooz et autres moyens de paiement. Revenez bientôt !', 'warning')
            return redirect(url_for('subscription'))
        
        user_data = {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'phone': user['phone']
        }
        
        callback_url = url_for('fedapay_callback', _external=True)
        
        result = fedapay_service.create_transaction(
            user_data, 
            amount=1000,
            description="Abonnement Premium PRO CHEZ NOUS - 1000 FCFA/mois",
            callback_url=callback_url
        )
        
        if result['success']:
            return render_template('payment_redirect.html', 
                                 payment_url=result['payment_url'],
                                 transaction_id=result['transaction_id'])
        else:
            flash(f"Erreur lors de la création du paiement: {result['error']}", 'error')
            return redirect(url_for('subscription'))
    
    fedapay_configured = fedapay_service.is_configured()
    return render_template('upgrade_premium.html', user=user, fedapay_configured=fedapay_configured)

@app.route('/profil/<int:pro_id>')
def profil(pro_id):
    conn = get_db()
    pro = conn.execute('SELECT * FROM users WHERE id = ? AND role = ?', (pro_id, 'pro')).fetchone()
    if not pro:
        flash('Professionnel introuvable', 'error')
        return redirect(url_for('view_professionals'))
    
    profil_enrichi = conn.execute('SELECT * FROM profils_pro WHERE pro_id = ?', (pro_id,)).fetchone()
    avis = conn.execute('''
        SELECT a.*, u.name as client_name FROM avis a
        JOIN users u ON a.client_id = u.id
        WHERE a.pro_id = ? ORDER BY a.date DESC
    ''', (pro_id,)).fetchall()
    
    note_moyenne = conn.execute('SELECT AVG(note) as moyenne FROM avis WHERE pro_id = ?', (pro_id,)).fetchone()
    
    is_favori = False
    if 'user_id' in session:
        favori = conn.execute('SELECT * FROM favoris WHERE client_id = ? AND pro_id = ?', 
                            (session['user_id'], pro_id)).fetchone()
        is_favori = favori is not None
    
    return render_template('profil.html', pro=pro, profil=profil_enrichi, avis=avis, 
                         note_moyenne=note_moyenne, is_favori=is_favori)

@app.route('/messages')
def messages():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    user_plan = user['plan'] if 'plan' in user.keys() else 'gratuit'
    
    # Récupérer les messages où AU MOINS UN est Premium (expéditeur OU destinataire)
    received = conn.execute('''
        SELECT m.*, u.name as expediteur_name, u.plan as expediteur_plan FROM messages m
        JOIN users u ON m.expediteur_id = u.id
        WHERE m.destinataire_id = ?
        ORDER BY m.date DESC
    ''', (session['user_id'],)).fetchall()
    
    sent = conn.execute('''
        SELECT m.*, u.name as destinataire_name, u.plan as destinataire_plan FROM messages m
        JOIN users u ON m.destinataire_id = u.id
        WHERE m.expediteur_id = ?
        ORDER BY m.date DESC
    ''', (session['user_id'],)).fetchall()
    
    # Filtrer: afficher seulement si l'utilisateur OU son interlocuteur est Premium
    received_premium = [msg for msg in received if user_plan == 'premium' or msg['expediteur_plan'] == 'premium']
    sent_premium = [msg for msg in sent if user_plan == 'premium' or msg['destinataire_plan'] == 'premium']
    
    return render_template('messages.html', received=received_premium, sent=sent_premium, user_plan=user_plan)

@app.route('/send_message/<int:dest_id>', methods=['GET', 'POST'])
def send_message(dest_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    destinataire = conn.execute('SELECT * FROM users WHERE id = ?', (dest_id,)).fetchone()
    
    if not destinataire:
        flash('Utilisateur introuvable', 'error')
        return redirect(url_for('view_professionals'))
    
    user_plan = user['plan'] if 'plan' in user.keys() else 'gratuit'
    dest_plan = destinataire['plan'] if 'plan' in destinataire.keys() else 'gratuit'
    
    # Autoriser si AU MOINS UN des deux est Premium
    if user_plan != 'premium' and dest_plan != 'premium':
        flash('La messagerie nécessite qu\'au moins un des deux utilisateurs soit Premium. Passez à Premium pour débloquer cette fonctionnalité!', 'error')
        return redirect(url_for('subscription'))
    
    if request.method == 'POST':
        from datetime import datetime
        contenu = request.form.get('contenu', '').strip()
        if contenu:
            conn.execute('INSERT INTO messages (expediteur_id, destinataire_id, contenu, date) VALUES (?, ?, ?, ?)',
                       (session['user_id'], dest_id, contenu, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            flash('Message envoyé avec succès!', 'success')
            return redirect(url_for('messages'))
    
    return render_template('send_message.html', destinataire=destinataire)

@app.route('/favoris')
def favoris():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    
    if user['plan'] != 'premium':
        flash('Les favoris sont réservés aux membres Premium!', 'error')
        return redirect(url_for('subscription'))
    
    favs = conn.execute('''
        SELECT u.*, f.date_ajout,
               COALESCE(AVG(a.note), 0) as note_moyenne,
               COUNT(a.id) as nb_avis
        FROM favoris f
        JOIN users u ON f.pro_id = u.id
        LEFT JOIN avis a ON u.id = a.pro_id
        WHERE f.client_id = ?
        GROUP BY u.id
        ORDER BY f.date_ajout DESC
    ''', (session['user_id'],)).fetchall()
    
    return render_template('favoris.html', favoris=favs)

@app.route('/add_favori/<int:pro_id>', methods=['POST'])
def add_favori(pro_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    
    if user['plan'] != 'premium':
        flash('Les favoris sont réservés aux membres Premium!', 'error')
        return redirect(url_for('subscription'))
    
    from datetime import datetime
    existing = conn.execute('SELECT * FROM favoris WHERE client_id = ? AND pro_id = ?', 
                          (session['user_id'], pro_id)).fetchone()
    
    if existing:
        conn.execute('DELETE FROM favoris WHERE client_id = ? AND pro_id = ?', 
                   (session['user_id'], pro_id))
        flash('Retiré des favoris', 'info')
    else:
        conn.execute('INSERT INTO favoris (client_id, pro_id, date_ajout) VALUES (?, ?, ?)',
                   (session['user_id'], pro_id, datetime.now().strftime('%Y-%m-%d')))
        flash('Ajouté aux favoris! ⭐', 'success')
    
    conn.commit()
    return redirect(request.referrer or url_for('view_professionals'))

@app.route('/devis')
def devis():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    user_plan = user['plan'] if 'plan' in user.keys() else 'gratuit'
    user_role = user['role']
    
    if user_role == 'user':
        # Clients: voir leurs demandes de devis
        mes_devis = conn.execute('''
            SELECT d.*, u.name as pro_name, u.categorie, u.plan as pro_plan
            FROM devis d
            JOIN users u ON d.pro_id = u.id
            WHERE d.client_id = ?
            ORDER BY d.date_demande DESC
        ''', (session['user_id'],)).fetchall()
        
        # Filtrer: afficher seulement si client OU pro est Premium
        devis_premium = [d for d in mes_devis if user_plan == 'premium' or d['pro_plan'] == 'premium']
        return render_template('devis_client.html', devis=devis_premium, user_plan=user_plan)
    
    else:  # pro
        # Pros: voir les demandes reçues
        devis_recus = conn.execute('''
            SELECT d.*, u.name as client_name, u.plan as client_plan
            FROM devis d
            JOIN users u ON d.client_id = u.id
            WHERE d.pro_id = ?
            ORDER BY d.date_demande DESC
        ''', (session['user_id'],)).fetchall()
        
        # Filtrer: afficher seulement si pro OU client est Premium
        devis_premium = [d for d in devis_recus if user_plan == 'premium' or d['client_plan'] == 'premium']
        return render_template('devis_pro.html', devis=devis_premium, user_plan=user_plan)

@app.route('/demander_devis/<int:pro_id>', methods=['GET', 'POST'])
def demander_devis(pro_id):
    if 'user_id' not in session or session.get('role') != 'user':
        return redirect(url_for('login'))
    
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    pro = conn.execute('SELECT * FROM users WHERE id = ? AND role = "pro"', (pro_id,)).fetchone()
    
    if not pro:
        flash('Professionnel introuvable', 'error')
        return redirect(url_for('view_professionals'))
    
    user_plan = user['plan'] if 'plan' in user.keys() else 'gratuit'
    pro_plan = pro['plan'] if 'plan' in pro.keys() else 'gratuit'
    
    # Autoriser si AU MOINS UN des deux est Premium
    if user_plan != 'premium' and pro_plan != 'premium':
        flash('La gestion de devis nécessite qu\'au moins un des deux utilisateurs soit Premium. Passez à Premium pour débloquer cette fonctionnalité!', 'error')
        return redirect(url_for('subscription'))
    
    if request.method == 'POST':
        titre = request.form.get('titre', '').strip()
        description = request.form.get('description', '').strip()
        
        if not titre:
            flash('Le titre du devis est obligatoire', 'error')
            return render_template('demander_devis.html', pro=pro)
        
        conn.execute('''
            INSERT INTO devis (client_id, pro_id, titre, description)
            VALUES (?, ?, ?, ?)
        ''', (session['user_id'], pro_id, titre, description))
        conn.commit()
        
        flash(f'Demande de devis envoyée à {pro["name"]} avec succès!', 'success')
        return redirect(url_for('devis'))
    
    return render_template('demander_devis.html', pro=pro)

@app.route('/repondre_devis/<int:devis_id>', methods=['GET', 'POST'])
def repondre_devis(devis_id):
    if 'user_id' not in session or session.get('role') != 'pro':
        return redirect(url_for('login'))
    
    conn = get_db()
    devis_item = conn.execute('''
        SELECT d.*, u.name as client_name
        FROM devis d
        JOIN users u ON d.client_id = u.id
        WHERE d.id = ? AND d.pro_id = ?
    ''', (devis_id, session['user_id'])).fetchone()
    
    if not devis_item:
        flash('Devis introuvable', 'error')
        return redirect(url_for('devis'))
    
    if request.method == 'POST':
        montant = request.form.get('montant', '').strip()
        delai = request.form.get('delai', '').strip()
        notes_pro = request.form.get('notes_pro', '').strip()
        
        if not montant:
            flash('Le montant est obligatoire', 'error')
            return render_template('repondre_devis.html', devis=devis_item)
        
        from datetime import datetime
        conn.execute('''
            UPDATE devis
            SET montant = ?, delai = ?, notes_pro = ?, statut = 'repondu', date_reponse = ?
            WHERE id = ?
        ''', (float(montant), delai, notes_pro, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), devis_id))
        conn.commit()
        
        flash(f'Devis répondu avec succès!', 'success')
        return redirect(url_for('devis'))
    
    return render_template('repondre_devis.html', devis=devis_item)

@app.route('/creer_devis', methods=['GET', 'POST'])
def creer_devis():
    if 'user_id' not in session or session.get('role') != 'pro':
        flash('Cette fonctionnalité est réservée aux professionnels', 'error')
        return redirect(url_for('login'))
    
    conn = get_db()
    user_plan = conn.execute('SELECT plan FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    
    if request.method == 'POST':
        client_id = request.form.get('client_id', '').strip()
        titre = request.form.get('titre', '').strip()
        description = request.form.get('description', '').strip()
        montant = request.form.get('montant', '').strip()
        delai = request.form.get('delai', '').strip()
        notes_pro = request.form.get('notes_pro', '').strip()
        
        if not client_id or not titre or not montant:
            flash('Le client, le titre et le montant sont obligatoires', 'error')
            clients = conn.execute('SELECT id, name, email, phone, plan FROM users WHERE role = "user" ORDER BY name').fetchall()
            return render_template('creer_devis.html', clients=clients, user_plan=user_plan['plan'] if user_plan else 'gratuit')
        
        client = conn.execute('SELECT plan FROM users WHERE id = ?', (client_id,)).fetchone()
        
        if user_plan['plan'] != 'premium' and client['plan'] != 'premium':
            flash('La gestion de devis nécessite qu\'au moins l\'un de vous soit Premium. Passez à Premium pour débloquer cette fonctionnalité!', 'error')
            return redirect(url_for('subscription'))
        
        from datetime import datetime
        conn.execute('''
            INSERT INTO devis (client_id, pro_id, titre, description, statut, montant, delai, notes_pro, date_demande, date_reponse, type_devis)
            VALUES (?, ?, ?, ?, 'repondu', ?, ?, ?, ?, ?, 'creation_pro')
        ''', (client_id, session['user_id'], titre, description, float(montant), delai, notes_pro, 
              datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
              datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        
        flash(f'Devis créé et envoyé avec succès!', 'success')
        return redirect(url_for('devis'))
    
    clients = conn.execute('SELECT id, name, email, phone, plan FROM users WHERE role = "user" ORDER BY name').fetchall()
    return render_template('creer_devis.html', clients=clients, user_plan=user_plan['plan'] if user_plan else 'gratuit')

@app.route('/logout')
def logout():
    session.clear()
    flash('Vous êtes déconnecté', 'info')
    return redirect(url_for('index'))

@app.route('/verification')
def verification():
    if 'user_id' not in session or session.get('role') != 'pro':
        flash('Cette page est réservée aux professionnels', 'error')
        return redirect(url_for('index'))
    
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    documents = conn.execute('''
        SELECT * FROM documents_verification 
        WHERE user_id = ? 
        ORDER BY date_upload DESC
    ''', (session['user_id'],)).fetchall()
    
    return render_template('verification.html', user=user, documents=documents)

@app.route('/upload_document', methods=['POST'])
def upload_document():
    if 'user_id' not in session or session.get('role') != 'pro':
        flash('Cette page est réservée aux professionnels', 'error')
        return redirect(url_for('index'))
    
    if 'document' not in request.files:
        flash('Aucun fichier sélectionné', 'error')
        return redirect(url_for('verification'))
    
    file = request.files['document']
    type_document = request.form.get('type_document', '').strip()
    
    if not file.filename or file.filename == '':
        flash('Aucun fichier sélectionné', 'error')
        return redirect(url_for('verification'))
    
    if not type_document:
        flash('Veuillez sélectionner le type de document', 'error')
        return redirect(url_for('verification'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        new_filename = f"{session['user_id']}_{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        file.save(filepath)
        
        conn = get_db()
        conn.execute('''
            INSERT INTO documents_verification (user_id, type_document, chemin_fichier, statut)
            VALUES (?, ?, ?, ?)
        ''', (session['user_id'], type_document, new_filename, 'en_attente'))
        conn.commit()
        
        flash('Document uploadé avec succès! Il sera vérifié prochainement.', 'success')
    else:
        flash('Type de fichier non autorisé. Formats acceptés: PDF, JPG, JPEG, PNG', 'error')
    
    return redirect(url_for('verification'))

@app.route('/valider_verification/<int:pro_id>')
def valider_verification(pro_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    documents = conn.execute('SELECT COUNT(*) as nb FROM documents_verification WHERE user_id = ? AND statut = "valide"', (pro_id,)).fetchone()
    
    if documents['nb'] > 0:
        conn.execute('UPDATE users SET statut_verification = ? WHERE id = ?', ('verifie', pro_id))
        conn.commit()
        flash('Professionnel vérifié avec succès!', 'success')
    
    return redirect(url_for('profil', pro_id=pro_id))

@app.route('/admin_verification')
def admin_verification():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session.get('role') != 'admin':
        flash('Accès refusé. Cette page est réservée aux administrateurs.', 'error')
        return redirect(url_for('dashboard'))
    
    conn = get_db()
    documents_attente = conn.execute('''
        SELECT d.*, u.name, u.email, u.categorie
        FROM documents_verification d
        JOIN users u ON d.user_id = u.id
        WHERE d.statut = 'en_attente'
        ORDER BY d.date_upload DESC
    ''').fetchall()
    
    return render_template('admin_verification.html', documents=documents_attente)

@app.route('/valider_document/<int:doc_id>', methods=['POST'])
def valider_document(doc_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session.get('role') != 'admin':
        flash('Accès refusé. Cette action est réservée aux administrateurs.', 'error')
        return redirect(url_for('dashboard'))
    
    action = request.form.get('action')
    conn = get_db()
    
    if action == 'valider':
        conn.execute('UPDATE documents_verification SET statut = ? WHERE id = ?', ('valide', doc_id))
        document = conn.execute('SELECT user_id FROM documents_verification WHERE id = ?', (doc_id,)).fetchone()
        if document:
            conn.execute('UPDATE users SET statut_verification = ? WHERE id = ?', ('verifie', document['user_id']))
        flash('Document validé avec succès!', 'success')
    elif action == 'refuser':
        conn.execute('UPDATE documents_verification SET statut = ? WHERE id = ?', ('refuse', doc_id))
        flash('Document refusé', 'info')
    
    conn.commit()
    return redirect(url_for('admin_verification'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        
        if not identifier:
            flash('Veuillez entrer votre email ou numéro de téléphone', 'error')
            return render_template('forgot_password.html')
        
        normalized_phone = normalize_phone_number(identifier) if '@' not in identifier else None
        
        conn = get_db()
        if normalized_phone:
            user = conn.execute('SELECT * FROM users WHERE email = ? OR phone = ? OR phone = ?', 
                              (identifier, identifier, normalized_phone)).fetchone()
        else:
            user = conn.execute('SELECT * FROM users WHERE email = ? OR phone = ?', 
                              (identifier, identifier)).fetchone()
        
        if not user:
            flash('Aucun compte trouvé avec cet email ou ce numéro de téléphone', 'error')
            return render_template('forgot_password.html')
        
        token = secrets.token_urlsafe(32)
        expiration = (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
        
        conn.execute('''
            INSERT INTO password_reset_tokens (user_id, token, expiration, used)
            VALUES (?, ?, ?, 0)
        ''', (user['id'], token, expiration))
        conn.commit()
        
        reset_url = url_for('reset_password', token=token, _external=True)
        
        if user['email'] and email_service.is_configured():
            result = email_service.send_password_reset_email(
                user['email'], 
                reset_url, 
                user['name']
            )
            if result['success']:
                flash('Un email de réinitialisation a été envoyé à votre adresse!', 'success')
                return redirect(url_for('login'))
            else:
                flash(f"Erreur lors de l'envoi de l'email. Voici votre lien: {reset_url}", 'warning')
        
        return render_template('reset_link_sent.html', reset_url=reset_url, identifier=identifier)
    
    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    conn = get_db()
    
    reset_token = conn.execute('''
        SELECT * FROM password_reset_tokens 
        WHERE token = ? AND used = 0
    ''', (token,)).fetchone()
    
    if not reset_token:
        flash('Lien de réinitialisation invalide ou déjà utilisé', 'error')
        return redirect(url_for('login'))
    
    expiration = datetime.strptime(reset_token['expiration'], '%Y-%m-%d %H:%M:%S')
    if datetime.now() > expiration:
        flash('Ce lien de réinitialisation a expiré. Veuillez en demander un nouveau.', 'error')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        if not password or len(password) < 6:
            flash('Le mot de passe doit contenir au moins 6 caractères', 'error')
            return render_template('reset_password.html', token=token)
        
        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas', 'error')
            return render_template('reset_password.html', token=token)
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        conn.execute('UPDATE users SET password = ? WHERE id = ?', 
                    (hashed_password, reset_token['user_id']))
        
        conn.execute('UPDATE password_reset_tokens SET used = 1 WHERE id = ?', 
                    (reset_token['id'],))
        
        conn.commit()
        
        flash('Votre mot de passe a été réinitialisé avec succès! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html', token=token)

@app.route('/fedapay/callback', methods=['POST', 'GET'])
def fedapay_callback():
    """
    Callback/Webhook FedaPay pour confirmer les paiements
    """
    if request.method == 'GET':
        transaction_id = request.args.get('id')
        status = request.args.get('status', 'unknown')
        
        if not transaction_id:
            flash('Erreur : ID de transaction manquant', 'error')
            return redirect(url_for('dashboard'))
        
        if fedapay_service.is_configured():
            result = fedapay_service.get_transaction(transaction_id)
            
            if result['success']:
                transaction = result['transaction']
                trans_status = transaction.get('status', 'unknown')
                
                if trans_status == 'approved':
                    user_id = session.get('user_id')
                    if user_id:
                        conn = get_db()
                        conn.execute('UPDATE users SET plan = ? WHERE id = ?', ('premium', user_id))
                        conn.commit()
                        flash('Paiement confirmé ! Vous êtes maintenant membre Premium 🌟', 'success')
                    return redirect(url_for('dashboard'))
                elif trans_status == 'declined':
                    flash('Paiement refusé. Veuillez réessayer.', 'error')
                    return redirect(url_for('subscription'))
                elif trans_status == 'canceled':
                    flash('Paiement annulé.', 'warning')
                    return redirect(url_for('subscription'))
                else:
                    flash(f'Paiement en attente (statut: {trans_status})', 'info')
                    return redirect(url_for('dashboard'))
            else:
                flash(f'Erreur lors de la vérification du paiement: {result["error"]}', 'error')
                return redirect(url_for('subscription'))
        
        if status == 'approved' and 'user_id' in session:
            conn = get_db()
            conn.execute('UPDATE users SET plan = ? WHERE id = ?', ('premium', session['user_id']))
            conn.commit()
            flash('Vous êtes maintenant membre Premium 🌟 (Mode démo - sans vérification FedaPay)', 'success')
        else:
            flash('Mode démo : FedaPay non configuré', 'warning')
        
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        payload = request.get_json()
        
        if fedapay_service.is_configured():
            signature = request.headers.get('X-FedaPay-Signature', '')
            
            if not fedapay_service.verify_webhook_signature(request.data, signature):
                return jsonify({'error': 'Invalid signature'}), 401
            
            event = payload.get('entity', {})
            transaction_id = event.get('id')
            status = event.get('status')
            
            if status == 'approved' and transaction_id:
                conn = get_db()
                user = conn.execute('''
                    SELECT id FROM users WHERE id IN (
                        SELECT user_id FROM rendezvous WHERE id = ?
                    )
                ''', (transaction_id,)).fetchone()
                
                if user:
                    conn.execute('UPDATE users SET plan = ? WHERE id = ?', ('premium', user['id']))
                    conn.commit()
            
            return jsonify({'status': 'success'}), 200
        
        return jsonify({'error': 'FedaPay not configured'}), 400

@app.route('/admin/categories')
def admin_categories():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Accès refusé. Vous devez être administrateur.', 'error')
        return redirect(url_for('login'))
    
    conn = get_db()
    categories = conn.execute('''
        SELECT c.*, COUNT(u.id) as nb_pros
        FROM categories c
        LEFT JOIN users u ON c.nom = u.categorie AND u.role = 'pro'
        GROUP BY c.id
        ORDER BY c.ordre ASC
    ''').fetchall()
    return render_template('admin_categories.html', categories=categories)

@app.route('/admin/categories/add', methods=['GET', 'POST'])
def admin_add_category():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Accès refusé. Vous devez être administrateur.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nom = request.form.get('nom', '').strip()
        icone = request.form.get('icone', '').strip()
        ordre = request.form.get('ordre', 0)
        
        if not nom:
            flash('Le nom de la catégorie est obligatoire', 'error')
            return render_template('admin_category_form.html', action='add')
        
        conn = get_db()
        try:
            conn.execute('INSERT INTO categories (nom, icone, ordre) VALUES (?, ?, ?)', (nom, icone, ordre))
            conn.commit()
            flash(f'Catégorie "{nom}" ajoutée avec succès!', 'success')
            return redirect(url_for('admin_categories'))
        except sqlite3.IntegrityError:
            flash('Cette catégorie existe déjà', 'error')
            return render_template('admin_category_form.html', action='add', nom=nom, icone=icone, ordre=ordre)
    
    return render_template('admin_category_form.html', action='add')

@app.route('/admin/categories/edit/<int:id>', methods=['GET', 'POST'])
def admin_edit_category(id):
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Accès refusé. Vous devez être administrateur.', 'error')
        return redirect(url_for('login'))
    
    conn = get_db()
    category = conn.execute('SELECT * FROM categories WHERE id = ?', (id,)).fetchone()
    
    if not category:
        flash('Catégorie introuvable', 'error')
        return redirect(url_for('admin_categories'))
    
    if request.method == 'POST':
        nom = request.form.get('nom', '').strip()
        icone = request.form.get('icone', '').strip()
        ordre = request.form.get('ordre', 0)
        
        if not nom:
            flash('Le nom de la catégorie est obligatoire', 'error')
            return render_template('admin_category_form.html', action='edit', category=category)
        
        try:
            conn.execute('UPDATE categories SET nom = ?, icone = ?, ordre = ? WHERE id = ?', (nom, icone, ordre, id))
            conn.commit()
            flash(f'Catégorie "{nom}" modifiée avec succès!', 'success')
            return redirect(url_for('admin_categories'))
        except sqlite3.IntegrityError:
            flash('Cette catégorie existe déjà', 'error')
            return render_template('admin_category_form.html', action='edit', category=category, nom=nom, icone=icone, ordre=ordre)
    
    return render_template('admin_category_form.html', action='edit', category=category)

@app.route('/admin/categories/delete/<int:id>', methods=['POST'])
def admin_delete_category(id):
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Accès refusé. Vous devez être administrateur.', 'error')
        return redirect(url_for('login'))
    
    conn = get_db()
    category = conn.execute('SELECT * FROM categories WHERE id = ?', (id,)).fetchone()
    
    if not category:
        flash('Catégorie introuvable', 'error')
        return redirect(url_for('admin_categories'))
    
    pros_using = conn.execute('SELECT COUNT(*) as count FROM users WHERE categorie = ? AND role = "pro"', (category['nom'],)).fetchone()
    
    if pros_using['count'] > 0:
        flash(f'Impossible de supprimer cette catégorie car {pros_using["count"]} professionnel(s) l\'utilisent. Désactivez-la plutôt.', 'error')
        return redirect(url_for('admin_categories'))
    
    conn.execute('DELETE FROM categories WHERE id = ?', (id,))
    conn.commit()
    flash(f'Catégorie "{category["nom"]}" supprimée avec succès!', 'success')
    return redirect(url_for('admin_categories'))

@app.route('/admin/categories/toggle/<int:id>', methods=['POST'])
def admin_toggle_category(id):
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Accès refusé. Vous devez être administrateur.', 'error')
        return redirect(url_for('login'))
    
    conn = get_db()
    category = conn.execute('SELECT * FROM categories WHERE id = ?', (id,)).fetchone()
    
    if not category:
        flash('Catégorie introuvable', 'error')
        return redirect(url_for('admin_categories'))
    
    new_status = 0 if category['actif'] == 1 else 1
    conn.execute('UPDATE categories SET actif = ? WHERE id = ?', (new_status, id))
    conn.commit()
    
    status_text = 'activée' if new_status == 1 else 'désactivée'
    flash(f'Catégorie "{category["nom"]}" {status_text} avec succès!', 'success')
    return redirect(url_for('admin_categories'))

@app.route('/admin/users')
def admin_users():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Accès refusé. Vous devez être administrateur.', 'error')
        return redirect(url_for('login'))
    
    conn = get_db()
    users = conn.execute('''
        SELECT id, name, email, phone, role, localisation, pays, categorie, plan, statut_verification, statut_compte
        FROM users
        ORDER BY id DESC
    ''').fetchall()
    return render_template('admin_users.html', users=users)

@app.route('/admin/users/add', methods=['GET', 'POST'])
def admin_add_user():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Accès refusé. Vous devez être administrateur.', 'error')
        return redirect(url_for('login'))
    
    categories = get_categories()
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '').strip()
        role = request.form.get('role', '').strip()
        localisation = request.form.get('localisation', '').strip()
        pays = request.form.get('pays', 'Togo').strip()
        plan = request.form.get('plan', 'gratuit').strip()
        categorie = request.form.get('categorie', '').strip() if role == 'pro' else None
        
        if not name or not password or not role:
            flash('Le nom, mot de passe et rôle sont obligatoires', 'error')
            return render_template('admin_user_form.html', action='add', categories=categories)
        
        if not email and not phone:
            flash('Veuillez fournir un email OU un numéro de téléphone', 'error')
            return render_template('admin_user_form.html', action='add', categories=categories)
        
        if phone:
            if not validate_phone_number(phone):
                flash('Numéro de téléphone invalide', 'error')
                return render_template('admin_user_form.html', action='add', categories=categories)
            phone = normalize_phone_number(phone)
        
        conn = get_db()
        
        if email:
            existing = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
            if existing:
                flash('Cette adresse email est déjà utilisée', 'error')
                return render_template('admin_user_form.html', action='add', categories=categories)
        
        if phone:
            existing = conn.execute('SELECT * FROM users WHERE phone = ?', (phone,)).fetchone()
            if existing:
                flash('Ce numéro de téléphone est déjà utilisé', 'error')
                return render_template('admin_user_form.html', action='add', categories=categories)
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        conn.execute('''
            INSERT INTO users (name, email, phone, password, role, localisation, pays, categorie, plan, statut_verification)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, email if email else None, phone if phone else None, hashed_password, role, localisation, pays, categorie, plan, 'en_attente'))
        conn.commit()
        
        flash(f'Utilisateur "{name}" créé avec succès!', 'success')
        return redirect(url_for('admin_users'))
    
    return render_template('admin_user_form.html', action='add', categories=categories)

@app.route('/admin/users/delete/<int:id>', methods=['POST'])
def admin_delete_user(id):
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Accès refusé. Vous devez être administrateur.', 'error')
        return redirect(url_for('login'))
    
    if id == session.get('user_id'):
        flash('Vous ne pouvez pas supprimer votre propre compte!', 'error')
        return redirect(url_for('admin_users'))
    
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
    
    if not user:
        flash('Utilisateur introuvable', 'error')
        return redirect(url_for('admin_users'))
    
    # Supprimer toutes les données liées (avec gestion d'erreur pour tables manquantes)
    try:
        conn.execute('DELETE FROM rendezvous WHERE client_id = ? OR pro_id = ?', (id, id))
    except: pass
    
    try:
        conn.execute('DELETE FROM slots WHERE pro_id = ?', (id,))
    except: pass
    
    try:
        conn.execute('DELETE FROM avis WHERE client_id = ? OR pro_id = ?', (id, id))
    except: pass
    
    try:
        conn.execute('DELETE FROM documents_verification WHERE user_id = ?', (id,))
    except: pass
    
    try:
        conn.execute('DELETE FROM devis WHERE client_id = ? OR pro_id = ?', (id, id))
    except: pass
    
    try:
        # Essayer nouveau format (sender_id/receiver_id)
        conn.execute('DELETE FROM messages WHERE sender_id = ? OR receiver_id = ?', (id, id))
    except:
        # Fallback ancien format (expediteur_id/destinataire_id)
        try:
            conn.execute('DELETE FROM messages WHERE expediteur_id = ? OR destinataire_id = ?', (id, id))
        except: pass
    
    try:
        conn.execute('DELETE FROM favoris WHERE client_id = ? OR pro_id = ?', (id, id))
    except: pass
    
    try:
        conn.execute('DELETE FROM profils_pro WHERE user_id = ?', (id,))
    except: pass
    
    # Supprimer l'utilisateur
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    
    flash(f'Utilisateur "{user["name"]}" supprimé avec succès!', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/users/toggle_status/<int:id>', methods=['POST'])
def admin_toggle_user_status(id):
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Accès refusé. Vous devez être administrateur.', 'error')
        return redirect(url_for('login'))
    
    if id == session.get('user_id'):
        flash('Vous ne pouvez pas modifier le statut de votre propre compte!', 'error')
        return redirect(url_for('admin_users'))
    
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
    
    if not user:
        flash('Utilisateur introuvable', 'error')
        return redirect(url_for('admin_users'))
    
    # Basculer le statut
    current_status = user['statut_compte'] if 'statut_compte' in user.keys() else 'actif'
    new_status = 'bloque' if current_status == 'actif' else 'actif'
    
    conn.execute('UPDATE users SET statut_compte = ? WHERE id = ?', (new_status, id))
    conn.commit()
    
    action = 'bloqué' if new_status == 'bloque' else 'débloqué'
    flash(f'Utilisateur "{user["name"]}" {action} avec succès!', 'success')
    return redirect(url_for('admin_users'))

def init_db():
    conn = get_db()
    conn.executescript('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT, email TEXT, password TEXT, role TEXT, localisation TEXT, categorie TEXT
    );
    CREATE TABLE IF NOT EXISTS slots (
        id INTEGER PRIMARY KEY,
        pro_id INTEGER, date TEXT
    );
    CREATE TABLE IF NOT EXISTS rendezvous (
        id INTEGER PRIMARY KEY,
        pro_id INTEGER, client_id INTEGER, date TEXT
    );
    CREATE TABLE IF NOT EXISTS avis (
        id INTEGER PRIMARY KEY,
        pro_id INTEGER,
        client_id INTEGER,
        note INTEGER,
        commentaire TEXT,
        date TEXT,
        FOREIGN KEY (pro_id) REFERENCES users(id),
        FOREIGN KEY (client_id) REFERENCES users(id)
    );
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL UNIQUE,
        icone TEXT,
        actif INTEGER DEFAULT 1,
        ordre INTEGER DEFAULT 0,
        date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS devis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER NOT NULL,
        pro_id INTEGER NOT NULL,
        titre TEXT NOT NULL,
        description TEXT,
        date_demande TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        statut TEXT DEFAULT 'en_attente',
        montant REAL,
        delai TEXT,
        notes_pro TEXT,
        date_reponse TIMESTAMP,
        type_devis TEXT DEFAULT 'demande_client',
        FOREIGN KEY (client_id) REFERENCES users(id),
        FOREIGN KEY (pro_id) REFERENCES users(id)
    );
    ''')
    try:
        conn.execute('ALTER TABLE users ADD COLUMN localisation TEXT')
        conn.commit()
    except:
        pass
    try:
        conn.execute('ALTER TABLE users ADD COLUMN categorie TEXT')
        conn.commit()
    except:
        pass
    try:
        conn.execute('ALTER TABLE users ADD COLUMN phone TEXT')
        conn.commit()
    except:
        pass
    try:
        conn.execute('ALTER TABLE users ADD COLUMN plan TEXT DEFAULT "gratuit"')
        conn.commit()
    except:
        pass
    try:
        conn.execute('ALTER TABLE users ADD COLUMN verification_status TEXT DEFAULT "en_attente"')
        conn.commit()
    except:
        pass
    try:
        conn.execute('ALTER TABLE users ADD COLUMN latitude REAL')
        conn.commit()
    except:
        pass
    try:
        conn.execute('ALTER TABLE users ADD COLUMN longitude REAL')
        conn.commit()
    except:
        pass
    try:
        conn.execute('ALTER TABLE users ADD COLUMN pays TEXT DEFAULT "Togo"')
        conn.commit()
    except:
        pass
    try:
        conn.execute('ALTER TABLE users ADD COLUMN statut_compte TEXT DEFAULT "actif"')
        conn.commit()
    except:
        pass
    
    try:
        conn.execute('ALTER TABLE devis ADD COLUMN type_devis TEXT DEFAULT "demande_client"')
        conn.commit()
    except:
        pass
    
    # Mettre à jour les utilisateurs existants sans plan
    try:
        conn.execute('UPDATE users SET plan = "gratuit" WHERE plan IS NULL')
        conn.commit()
    except:
        pass
    
    # Migrer les catégories hardcodées vers la base de données
    existing_cats = conn.execute('SELECT COUNT(*) as count FROM categories').fetchone()
    if existing_cats['count'] == 0:
        default_categories = [
            ('🔧 Plomberie', '🔧', 1), ('⚡ Électricité', '⚡', 2), ('🎨 Peinture', '🎨', 3),
            ('🪚 Menuiserie', '🪚', 4), ('🧱 Maçonnerie', '🧱', 5), ('🏗️ Rénovation', '🏗️', 6),
            ('🪟 Vitrerie', '🪟', 7), ('🔐 Serrurerie', '🔐', 8), ('🏠 Toiture', '🏠', 9),
            ('🪜 Couverture', '🪜', 10), ('🌳 Jardinage', '🌳', 11), ('🌱 Paysagiste', '🌱', 12),
            ('🌿 Élagage', '🌿', 13), ('💧 Piscine', '💧', 14), ('❄️ Climatisation', '❄️', 15),
            ('🔥 Chauffage', '🔥', 16), ('📡 Antenne/Parabole', '📡', 17), ('🚪 Portail/Clôture', '🚪', 18),
            ('🧹 Nettoyage', '🧹', 19), ('🧽 Ménage à domicile', '🧽', 20), ('🪟 Lavage vitres', '🪟', 21),
            ('🧼 Pressing/Repassage', '🧼', 22), ('🚚 Déménagement', '🚚', 23), ('📦 Livraison', '📦', 24),
            ('🚗 Transport', '🚗', 25), ('🛵 Coursier', '🛵', 26), ('🔨 Bricolage', '🔨', 27),
            ('⚙️ Dépannage', '⚙️', 28), ('🔧 Réparation électroménager', '🔧', 29), ('📱 Réparation téléphone', '📱', 30),
            ('💻 Informatique', '💻', 31), ('🖥️ Maintenance PC', '🖥️', 32), ('📶 Installation internet', '📶', 33),
            ('✂️ Coiffure à domicile', '✂️', 34), ('💅 Manucure', '💅', 35), ('💆 Massage', '💆', 36),
            ('👗 Couture/Retouche', '👗', 37), ('🍳 Cuisinier à domicile', '🍳', 38), ('🎂 Pâtisserie', '🎂', 39),
            ('🍕 Traiteur', '🍕', 40), ('☕ Barista', '☕', 41), ('👶 Garde d\'enfants', '👶', 42),
            ('🧓 Aide à domicile', '🧓', 43), ('🐕 Garde animaux', '🐕', 44), ('🚶 Promenade chiens', '🚶', 45),
            ('🚗 Mécanicien auto', '🚗', 46), ('🏍️ Mécanicien moto', '🏍️', 47), ('🔧 Carrosserie', '🔧', 48),
            ('🚙 Lavage auto', '🚙', 49), ('📚 Soutien scolaire', '📚', 50), ('🎓 Formation', '🎓', 51),
            ('🎸 Cours de musique', '🎸', 52), ('🎨 Cours d\'art', '🎨', 53), ('📸 Photographe', '📸', 54),
            ('🎥 Vidéaste', '🎥', 55), ('🎤 DJ/Sonorisation', '🎤', 56), ('🎪 Animation événements', '🎪', 57),
            ('👔 Repassage', '👔', 58), ('🧺 Blanchisserie', '🧺', 59), ('🪡 Tapissier', '🪡', 60),
            ('🛋️ Rénovation meuble', '🛋️', 61), ('🪴 Fleuriste', '🪴', 62), ('🌺 Décoration florale', '🌺', 63),
            ('🎀 Décoration événements', '🎀', 64), ('🔒 Sécurité', '🔒', 65), ('👮 Gardiennage', '👮', 66),
            ('📹 Installation alarme', '📹', 67), ('🏋️ Coach sportif', '🏋️', 68), ('🧘 Yoga/Pilates', '🧘', 69),
            ('💪 Personal trainer', '💪', 70), ('🐝 Apiculture', '🐝', 71), ('🐓 Élevage', '🐓', 72),
            ('🌾 Agriculture', '🌾', 73), ('🥕 Maraîchage', '🥕', 74), ('🎪 Autres services', '🎪', 75)
        ]
        conn.executemany('INSERT INTO categories (nom, icone, ordre) VALUES (?, ?, ?)', default_categories)
        conn.commit()



@app.route('/debug_session')
def debug_session():
    """Route temporaire pour debug"""
    import json
    session_data = {
        'user_id': session.get('user_id'),
        'role': session.get('role'),
        'plan': session.get('plan'),
        'all_keys': list(session.keys())
    }
    return f"<pre>{json.dumps(session_data, indent=2)}</pre>"


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)