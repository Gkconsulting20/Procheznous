#!/usr/bin/env python3
"""
Script pour créer un compte administrateur PRO CHEZ NOUS
"""

import sqlite3
import bcrypt
from utils import normalize_phone_number

def create_admin(email, phone, password, name="Administrateur"):
    """Crée un compte administrateur"""
    
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Vérifier si un admin existe déjà
    cursor.execute("SELECT * FROM users WHERE role = 'admin'")
    existing_admin = cursor.fetchone()
    
    if existing_admin:
        print(f"⚠️  Un administrateur existe déjà: {existing_admin['email']}")
        response = input("Voulez-vous créer un autre admin? (oui/non): ").strip().lower()
        if response not in ['oui', 'o', 'yes', 'y']:
            print("❌ Création annulée")
            conn.close()
            return False
    
    # Normaliser le numéro de téléphone
    normalized_phone = normalize_phone_number(phone) if phone else None
    
    # Vérifier si l'email existe déjà
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    if cursor.fetchone():
        print(f"❌ Erreur: L'email {email} est déjà utilisé")
        conn.close()
        return False
    
    # Vérifier si le téléphone existe déjà
    if normalized_phone:
        cursor.execute("SELECT * FROM users WHERE phone = ?", (normalized_phone,))
        if cursor.fetchone():
            print(f"❌ Erreur: Le numéro {normalized_phone} est déjà utilisé")
            conn.close()
            return False
    
    # Hasher le mot de passe
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Insérer l'administrateur
    try:
        cursor.execute('''
            INSERT INTO users (name, email, phone, password, role, plan, statut_verification)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, email, normalized_phone, hashed_password, 'admin', 'premium', 'verifie'))
        
        conn.commit()
        
        print("\n" + "=" * 50)
        print("✅ Compte administrateur créé avec succès!")
        print("=" * 50)
        print(f"Nom:       {name}")
        print(f"Email:     {email}")
        if normalized_phone:
            print(f"Téléphone: {normalized_phone}")
        print(f"Rôle:      admin")
        print(f"Plan:      premium")
        print("=" * 50)
        print("\n💡 Vous pouvez maintenant vous connecter avec ces identifiants.")
        print("   L'onglet 🔐 Admin sera visible uniquement pour vous.")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        conn.rollback()
        return False
    
    finally:
        conn.close()

if __name__ == '__main__':
    print("=" * 50)
    print("🔐 CRÉATION COMPTE ADMINISTRATEUR")
    print("=" * 50)
    print()
    
    name = input("Nom de l'administrateur: ").strip()
    email = input("Email: ").strip()
    phone = input("Téléphone (optionnel): ").strip()
    password = input("Mot de passe: ").strip()
    
    if not name or not email or not password:
        print("❌ Le nom, l'email et le mot de passe sont obligatoires")
    elif len(password) < 6:
        print("❌ Le mot de passe doit contenir au moins 6 caractères")
    else:
        create_admin(email, phone, password, name)
