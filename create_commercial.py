#!/usr/bin/env python3
"""
Script pour créer un compte COMMERCIAL sur PRO CHEZ NOUS
Les commerciaux peuvent inscrire des professionnels et des clients et suivre leurs performances
"""

import sqlite3
import bcrypt
import secrets
import string

def generate_code_commercial():
    """Génère un code commercial unique (8 caractères alphanumériques)"""
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))

def create_commercial():
    print("=" * 60)
    print("  CRÉATION D'UN COMPTE COMMERCIAL - PRO CHEZ NOUS")
    print("=" * 60)
    print()
    
    # Collecter les informations
    name = input("Nom complet du commercial : ").strip()
    email = input("Email du commercial : ").strip().lower()
    phone = input("Téléphone (optionnel, ex: +22890123456) : ").strip()
    password = input("Mot de passe : ").strip()
    
    if not name or not email or not password:
        print("\n❌ ERREUR : Le nom, l'email et le mot de passe sont obligatoires!")
        return
    
    # Générer un code commercial unique
    code_commercial = generate_code_commercial()
    
    # Connexion à la base de données
    try:
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Vérifier si l'email existe déjà
        existing = cursor.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        if existing:
            print(f"\n❌ ERREUR : Un utilisateur avec l'email '{email}' existe déjà!")
            conn.close()
            return
        
        # Hasher le mot de passe
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Créer le compte commercial
        cursor.execute('''
            INSERT INTO users (name, email, phone, password, role, plan, code_commercial, statut_compte)
            VALUES (?, ?, ?, ?, 'commercial', 'premium', ?, 'actif')
        ''', (name, email, phone if phone else None, hashed_password, code_commercial))
        
        conn.commit()
        commercial_id = cursor.lastrowid
        
        print("\n" + "=" * 60)
        print("✅ COMPTE COMMERCIAL CRÉÉ AVEC SUCCÈS!")
        print("=" * 60)
        print(f"\n📋 INFORMATIONS DU COMMERCIAL:")
        print(f"   ID             : {commercial_id}")
        print(f"   Nom            : {name}")
        print(f"   Email          : {email}")
        print(f"   Téléphone      : {phone if phone else 'Non renseigné'}")
        print(f"   Rôle           : COMMERCIAL")
        print(f"   Plan           : Premium (inclus)")
        print(f"   Code Commercial: {code_commercial}")
        print(f"\n🔗 LIEN DE PARRAINAGE:")
        print(f"   Inscription Client:")
        print(f"   https://www.pro-chez-nous.com/register?ref={code_commercial}")
        print(f"\n   Inscription Professionnel:")
        print(f"   https://www.pro-chez-nous.com/register?ref={code_commercial}")
        print(f"\n💡 UTILISATION:")
        print(f"   - Le commercial partage son lien de parrainage")
        print(f"   - Les inscriptions via ce lien sont automatiquement liées à ce commercial")
        print(f"   - Toutes les stats sont disponibles dans le dashboard commercial")
        print(f"\n🔐 CONNEXION:")
        print(f"   URL      : https://www.pro-chez-nous.com/login")
        print(f"   Email    : {email}")
        print(f"   Password : (celui que vous avez saisi)")
        print("=" * 60)
        
        conn.close()
        
    except Exception as e:
        print(f"\n❌ ERREUR : {str(e)}")
        return

if __name__ == '__main__':
    create_commercial()
