#!/usr/bin/env python3
"""
Script de migration standalone pour ajouter le système d'expiration d'abonnement
Peut être exécuté avec: python migrate_subscription_system.py
"""

import sqlite3
from datetime import datetime

def migrate_database():
    """Applique la migration pour le système d'expiration"""
    print("🚀 Début de la migration du système d'expiration d'abonnement...")
    print("="*70)
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    try:
        # 1. Ajouter subscription_started_at
        print("\n1️⃣ Ajout de la colonne subscription_started_at...")
        try:
            cursor.execute('ALTER TABLE users ADD COLUMN subscription_started_at TEXT')
            print("   ✅ Colonne subscription_started_at ajoutée")
        except sqlite3.OperationalError as e:
            if 'duplicate column' in str(e).lower():
                print("   ⚠️  Colonne subscription_started_at déjà existante")
            else:
                raise
        
        # 2. Ajouter subscription_expires_at
        print("\n2️⃣ Ajout de la colonne subscription_expires_at...")
        try:
            cursor.execute('ALTER TABLE users ADD COLUMN subscription_expires_at TEXT')
            print("   ✅ Colonne subscription_expires_at ajoutée")
        except sqlite3.OperationalError as e:
            if 'duplicate column' in str(e).lower():
                print("   ⚠️  Colonne subscription_expires_at déjà existante")
            else:
                raise
        
        # 3. Ajouter subscription_status
        print("\n3️⃣ Ajout de la colonne subscription_status...")
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN subscription_status TEXT DEFAULT 'active'")
            print("   ✅ Colonne subscription_status ajoutée")
        except sqlite3.OperationalError as e:
            if 'duplicate column' in str(e).lower():
                print("   ⚠️  Colonne subscription_status déjà existante")
            else:
                raise
        
        # 4. Créer table subscription_history
        print("\n4️⃣ Création de la table subscription_history...")
        try:
            cursor.execute('''
                CREATE TABLE subscription_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    plan TEXT NOT NULL,
                    period_start TEXT NOT NULL,
                    period_end TEXT NOT NULL,
                    amount REAL,
                    payment_reference TEXT,
                    status TEXT DEFAULT 'completed',
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            print("   ✅ Table subscription_history créée")
        except sqlite3.OperationalError as e:
            if 'already exists' in str(e).lower():
                print("   ⚠️  Table subscription_history déjà existante")
            else:
                raise
        
        # 5. Créer table notifications
        print("\n5️⃣ Création de la table notifications...")
        try:
            cursor.execute('''
                CREATE TABLE notifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    type TEXT NOT NULL,
                    message TEXT NOT NULL,
                    sent_at TEXT NOT NULL,
                    read_at TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            print("   ✅ Table notifications créée")
        except sqlite3.OperationalError as e:
            if 'already exists' in str(e).lower():
                print("   ⚠️  Table notifications déjà existante")
            else:
                raise
        
        # 6. Initialiser les utilisateurs Premium existants
        print("\n6️⃣ Initialisation des utilisateurs Premium avec 30 jours...")
        cursor.execute('''
            UPDATE users 
            SET 
                subscription_started_at = datetime('now'),
                subscription_expires_at = datetime('now', '+30 days'),
                subscription_status = 'active'
            WHERE plan = 'premium' AND subscription_expires_at IS NULL
        ''')
        premium_count = cursor.rowcount
        print(f"   ✅ {premium_count} utilisateurs Premium initialisés")
        
        # 7. Initialiser les utilisateurs gratuits
        print("\n7️⃣ Initialisation des utilisateurs gratuits...")
        cursor.execute('''
            UPDATE users 
            SET subscription_status = 'inactive'
            WHERE (plan = 'gratuit' OR plan IS NULL) AND subscription_status IS NULL
        ''')
        free_count = cursor.rowcount
        print(f"   ✅ {free_count} utilisateurs gratuits initialisés")
        
        conn.commit()
        
        # Rapport final
        print("\n" + "="*70)
        print("✅ MIGRATION TERMINÉE AVEC SUCCÈS!")
        print("="*70)
        
        # Afficher un résumé
        cursor.execute("SELECT COUNT(*) FROM users WHERE plan='premium'")
        total_premium = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE plan='gratuit' OR plan IS NULL")
        total_free = cursor.fetchone()[0]
        
        print(f"\n📊 RÉSUMÉ:")
        print(f"   👥 Total utilisateurs Premium: {total_premium}")
        print(f"   👥 Total utilisateurs Gratuits: {total_free}")
        print(f"\n✅ Le système d'expiration est maintenant actif!")
        print(f"   - Les abonnements Premium expirent après 30 jours")
        print(f"   - Des alertes seront affichées à J-7, J-3 et J-1")
        print(f"   - Les fonctionnalités Premium seront bloquées après expiration")
        
    except Exception as e:
        print(f"\n❌ ERREUR lors de la migration: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_database()
