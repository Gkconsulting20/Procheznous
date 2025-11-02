"""
Service de gestion des abonnements Premium
Gère l'expiration, les notifications et le renouvellement
"""

from datetime import datetime, timedelta
import sqlite3

def get_db():
    """Connexion à la base de données"""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def check_subscription_status(user_id):
    """
    Vérifie et met à jour le statut d'abonnement d'un utilisateur
    Retourne: dict avec statut, plan, jours_restants, etc.
    """
    conn = get_db()
    
    try:
        user_row = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        
        if not user_row:
            return None
        
        # Convertir Row en dict pour accès sûr
        user = dict(user_row)
        
        result = {
            'user_id': user_id,
            'plan': user.get('plan', 'gratuit'),
            'subscription_status': user.get('subscription_status', 'inactive'),
            'is_premium_active': False,
            'days_until_expiry': None,
            'expires_at': None,
            'needs_warning': False,
            'warning_level': None
        }
        
        # Si pas premium, retour rapide
        if user.get('plan') != 'premium':
            return result
        
        # Vérifier la date d'expiration
        expires_at = user.get('subscription_expires_at')
        
        if not expires_at:
            # Premium mais pas de date d'expiration (ancien système)
            # On peut leur donner 30 jours de grâce
            expires_at = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
            conn.execute(
                'UPDATE users SET subscription_started_at = ?, subscription_expires_at = ?, subscription_status = ? WHERE id = ?',
                (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), expires_at, 'active', user_id)
            )
            conn.commit()
        
        # Parser la date d'expiration
        try:
            expiry_date = datetime.strptime(expires_at, '%Y-%m-%d %H:%M:%S')
        except:
            # Format alternatif
            try:
                expiry_date = datetime.strptime(expires_at, '%Y-%m-%d')
            except:
                return result
        
        now = datetime.now()
        days_left = (expiry_date - now).days
        
        result['expires_at'] = expiry_date.strftime('%Y-%m-%d')
        result['days_until_expiry'] = days_left
        
        # Déterminer le statut
        if days_left < 0:
            # Expiré
            new_status = 'expired'
            result['is_premium_active'] = False
            result['needs_warning'] = True
            result['warning_level'] = 'expired'
        elif days_left <= 1:
            # Dernier jour
            new_status = 'grace'
            result['is_premium_active'] = True
            result['needs_warning'] = True
            result['warning_level'] = 'urgent'
        elif days_left <= 3:
            # 3 jours ou moins
            new_status = 'grace'
            result['is_premium_active'] = True
            result['needs_warning'] = True
            result['warning_level'] = 'warning'
        elif days_left <= 7:
            # 7 jours ou moins
            new_status = 'active'
            result['is_premium_active'] = True
            result['needs_warning'] = True
            result['warning_level'] = 'info'
        else:
            # Plus de 7 jours
            new_status = 'active'
            result['is_premium_active'] = True
            result['needs_warning'] = False
        
        result['subscription_status'] = new_status
        
        # Mettre à jour le statut dans la DB si changé
        if user.get('subscription_status') != new_status:
            conn.execute(
                'UPDATE users SET subscription_status = ? WHERE id = ?',
                (new_status, user_id)
            )
            conn.commit()
        
        return result
    
    finally:
        conn.close()

def is_premium_active(user_id):
    """
    Vérifie si l'abonnement Premium est actif (non expiré)
    Retourne: True/False
    """
    status = check_subscription_status(user_id)
    return status['is_premium_active'] if status else False

def get_days_until_expiry(user_id):
    """
    Retourne le nombre de jours avant expiration
    Retourne: int (négatif si expiré)
    """
    status = check_subscription_status(user_id)
    return status['days_until_expiry'] if status else None

def get_warning_message(status_info):
    """
    Génère le message d'avertissement approprié
    """
    if not status_info or not status_info['needs_warning']:
        return None
    
    days = status_info['days_until_expiry']
    level = status_info['warning_level']
    
    # Préparer les textes dynamiques
    aujourdhui = "aujourd'hui"
    demain = "demain"
    expire_quand = aujourdhui if days == 0 else demain
    acces = "l'accès"
    
    messages = {
        'expired': {
            'text': '⚠️ Votre abonnement Premium a expiré. Renouvelez maintenant pour continuer à profiter de toutes les fonctionnalités !',
            'class': 'alert-danger',
            'cta': 'Renouveler maintenant'
        },
        'urgent': {
            'text': f'🔔 Attention ! Votre abonnement expire {expire_quand} ! Renouvelez dès maintenant.',
            'class': 'alert-warning',
            'cta': 'Renouveler'
        },
        'warning': {
            'text': f'⏰ Votre abonnement Premium expire dans {days} jours. Renouvelez pour ne pas perdre {acces}.',
            'class': 'alert-warning',
            'cta': 'Renouveler'
        },
        'info': {
            'text': f'💡 Votre abonnement Premium expire dans {days} jours.',
            'class': 'alert-info',
            'cta': 'Voir mon abonnement'
        }
    }
    
    return messages.get(level)

def renew_subscription(user_id, duration_days=30, payment_reference=None, amount=1000):
    """
    Renouvelle l'abonnement Premium
    """
    conn = get_db()
    
    try:
        now = datetime.now()
        
        # Vérifier si l'utilisateur a déjà un abonnement actif
        user_row = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        
        if not user_row:
            return {'success': False, 'error': 'Utilisateur introuvable'}
        
        # Convertir Row en dict pour accès sûr
        user = dict(user_row)
        
        # Calculer les nouvelles dates
        expires_at = user.get('subscription_expires_at')
        
        if expires_at:
            try:
                # Partir de la date d'expiration existante si elle est dans le futur
                current_expiry = datetime.strptime(expires_at, '%Y-%m-%d %H:%M:%S')
                if current_expiry > now:
                    new_expiry = current_expiry + timedelta(days=duration_days)
                else:
                    new_expiry = now + timedelta(days=duration_days)
            except:
                new_expiry = now + timedelta(days=duration_days)
        else:
            new_expiry = now + timedelta(days=duration_days)
        
        start_date = now.strftime('%Y-%m-%d %H:%M:%S')
        end_date = new_expiry.strftime('%Y-%m-%d %H:%M:%S')
        
        # Mettre à jour l'utilisateur
        conn.execute('''
            UPDATE users 
            SET plan = 'premium',
                subscription_started_at = ?,
                subscription_expires_at = ?,
                subscription_status = 'active'
            WHERE id = ?
        ''', (start_date, end_date, user_id))
        
        # Enregistrer dans l'historique
        conn.execute('''
            INSERT INTO subscription_history 
            (user_id, plan, period_start, period_end, amount, payment_reference, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, 'premium', start_date, end_date, amount, payment_reference, 'completed', start_date))
        
        conn.commit()
        
        return {
            'success': True,
            'expires_at': end_date,
            'days_added': duration_days
        }
    
    finally:
        conn.close()

def expire_subscription(user_id):
    """
    Fait expirer l'abonnement (passe en gratuit mais garde l'historique)
    """
    conn = get_db()
    
    try:
        conn.execute('''
            UPDATE users 
            SET plan = 'gratuit',
                subscription_status = 'expired'
            WHERE id = ?
        ''', (user_id,))
        
        conn.commit()
        
        return {'success': True}
    
    finally:
        conn.close()

def get_subscription_history(user_id):
    """
    Récupère l'historique des abonnements
    """
    conn = get_db()
    
    try:
        history = conn.execute('''
            SELECT * FROM subscription_history 
            WHERE user_id = ? 
            ORDER BY created_at DESC
        ''', (user_id,)).fetchall()
        
        return [dict(h) for h in history]
    
    finally:
        conn.close()
