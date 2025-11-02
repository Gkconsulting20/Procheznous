#!/usr/bin/env python3
"""
Script de test pour le système d'expiration d'abonnement
Permet de simuler différents scénarios d'expiration
"""

import sqlite3
from datetime import datetime, timedelta

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def list_premium_users():
    """Liste tous les utilisateurs Premium avec leurs dates"""
    conn = get_db()
    users = conn.execute('''
        SELECT id, name, email, plan, subscription_status, 
               subscription_started_at, subscription_expires_at
        FROM users 
        WHERE plan = 'premium'
    ''').fetchall()
    
    print("\n" + "="*80)
    print("📋 UTILISATEURS PREMIUM")
    print("="*80)
    
    for user in users:
        print(f"\n👤 {user['name']} (ID: {user['id']})")
        print(f"   Email: {user['email']}")
        print(f"   Statut: {user['subscription_status']}")
        print(f"   Début: {user['subscription_started_at']}")
        print(f"   Expiration: {user['subscription_expires_at']}")
        
        if user['subscription_expires_at']:
            try:
                expiry = datetime.strptime(user['subscription_expires_at'], '%Y-%m-%d %H:%M:%S')
                days_left = (expiry - datetime.now()).days
                print(f"   ⏱️  Jours restants: {days_left}")
            except:
                print(f"   ⏱️  Jours restants: Erreur de format")
    
    conn.close()
    print("\n" + "="*80 + "\n")

def set_expiry_scenario(user_id, scenario):
    """
    Configure un scénario d'expiration pour un utilisateur
    
    Scénarios:
    - 'active_30': Actif, expire dans 30 jours
    - 'warning_7': Avertissement, expire dans 7 jours
    - 'warning_3': Avertissement, expire dans 3 jours
    - 'urgent_1': Urgent, expire demain
    - 'urgent_0': Urgent, expire aujourd'hui
    - 'expired_1': Expiré depuis 1 jour
    - 'expired_7': Expiré depuis 7 jours
    """
    conn = get_db()
    
    scenarios = {
        'active_30': 30,
        'warning_7': 7,
        'warning_3': 3,
        'urgent_1': 1,
        'urgent_0': 0,
        'expired_1': -1,
        'expired_7': -7
    }
    
    if scenario not in scenarios:
        print(f"❌ Scénario invalide. Choisissez parmi: {list(scenarios.keys())}")
        return
    
    days = scenarios[scenario]
    now = datetime.now()
    started_at = (now - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
    expires_at = (now + timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
    
    # Déterminer le statut
    if days < 0:
        status = 'expired'
    elif days <= 1:
        status = 'grace'
    else:
        status = 'active'
    
    conn.execute('''
        UPDATE users 
        SET subscription_started_at = ?,
            subscription_expires_at = ?,
            subscription_status = ?
        WHERE id = ?
    ''', (started_at, expires_at, status, user_id))
    
    conn.commit()
    
    user = conn.execute('SELECT name FROM users WHERE id = ?', (user_id,)).fetchone()
    
    print(f"\n✅ Scénario '{scenario}' appliqué à {user['name']}")
    print(f"   Début: {started_at}")
    print(f"   Expiration: {expires_at}")
    print(f"   Statut: {status}")
    print(f"   Jours restants: {days}")
    
    conn.close()

def test_all_scenarios():
    """Test tous les scénarios avec les utilisateurs existants"""
    conn = get_db()
    premium_users = conn.execute('''
        SELECT id, name FROM users WHERE plan = 'premium' ORDER BY id LIMIT 3
    ''').fetchall()
    conn.close()
    
    if len(premium_users) < 3:
        print("❌ Pas assez d'utilisateurs Premium (minimum 3 requis)")
        return
    
    scenarios = [
        ('warning_7', '7 jours - Alerte info'),
        ('warning_3', '3 jours - Alerte warning'),
        ('urgent_0', "Aujourd'hui - Alerte urgente")
    ]
    
    print("\n" + "="*80)
    print("🧪 TEST DE TOUS LES SCÉNARIOS")
    print("="*80)
    
    for i, (scenario, description) in enumerate(scenarios):
        if i < len(premium_users):
            user = premium_users[i]
            print(f"\n{i+1}. {user['name']} → {description}")
            set_expiry_scenario(user['id'], scenario)
    
    print("\n" + "="*80)
    print("✅ Tests configurés ! Connectez-vous pour voir les alertes:")
    print("="*80)
    for i, (scenario, description) in enumerate(scenarios):
        if i < len(premium_users):
            user = premium_users[i]
            print(f"   - {user['name']}: {description}")
    print("\n")

def reset_all_premium():
    """Réinitialise tous les Premium à 30 jours actifs"""
    conn = get_db()
    
    now = datetime.now()
    started_at = now.strftime('%Y-%m-%d %H:%M:%S')
    expires_at = (now + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
    
    conn.execute('''
        UPDATE users 
        SET subscription_started_at = ?,
            subscription_expires_at = ?,
            subscription_status = 'active'
        WHERE plan = 'premium'
    ''', (started_at, expires_at))
    
    count = conn.total_changes
    conn.commit()
    conn.close()
    
    print(f"\n✅ {count} utilisateurs Premium réinitialisés à 30 jours actifs")

def main():
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                  TEST SYSTÈME D'EXPIRATION D'ABONNEMENT                    ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    while True:
        print("\nOptions:")
        print("  1. Lister les utilisateurs Premium")
        print("  2. Configurer un scénario pour un utilisateur")
        print("  3. Tester tous les scénarios (auto)")
        print("  4. Réinitialiser tous les Premium (30 jours)")
        print("  0. Quitter")
        
        choice = input("\nVotre choix: ").strip()
        
        if choice == '1':
            list_premium_users()
        
        elif choice == '2':
            list_premium_users()
            user_id = input("\nID utilisateur: ").strip()
            print("\nScénarios disponibles:")
            print("  active_30   : Actif, 30 jours restants")
            print("  warning_7   : Alerte info, 7 jours restants")
            print("  warning_3   : Alerte warning, 3 jours restants")
            print("  urgent_1    : Urgent, expire demain")
            print("  urgent_0    : Urgent, expire aujourd'hui")
            print("  expired_1   : Expiré depuis 1 jour")
            print("  expired_7   : Expiré depuis 7 jours")
            scenario = input("\nScénario: ").strip()
            
            if user_id.isdigit():
                set_expiry_scenario(int(user_id), scenario)
            else:
                print("❌ ID invalide")
        
        elif choice == '3':
            test_all_scenarios()
        
        elif choice == '4':
            confirm = input("\n⚠️  Réinitialiser TOUS les Premium à 30 jours? (oui/non): ").strip().lower()
            if confirm == 'oui':
                reset_all_premium()
        
        elif choice == '0':
            print("\n👋 Au revoir!\n")
            break
        
        else:
            print("❌ Choix invalide")

if __name__ == '__main__':
    main()
