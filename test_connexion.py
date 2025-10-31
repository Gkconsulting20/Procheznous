#!/usr/bin/env python3
"""
Script de test de connexion et vérification des onglets
"""

import sqlite3
import bcrypt

print("=" * 70)
print("🧪 TEST DE DIAGNOSTIC - PRO CHEZ NOUS")
print("=" * 70)

conn = sqlite3.connect('database.db')

# Test 1: Vérifier que app.py ajoute bien le plan dans la session
print("\n📝 TEST 1: Vérification du code dans app.py")
print("-" * 70)

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
if "session['plan'] = user['plan']" in content:
    print("✅ Le plan est bien ajouté à la session dans app.py")
else:
    print("❌ PROBLÈME: Le plan n'est PAS ajouté à la session!")
    print("   → Il faut ajouter: session['plan'] = user['plan']")

# Test 2: Vérifier que base.html masque bien les onglets
print("\n📝 TEST 2: Vérification du code dans base.html")
print("-" * 70)

with open('templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

if "{% if session.plan == 'premium' %}" in content:
    print("✅ Les onglets premium sont bien protégés dans base.html")
else:
    print("❌ PROBLÈME: Les onglets premium ne sont PAS protégés!")

if "{% if session.role == 'admin' %}" in content:
    print("✅ L'onglet admin est bien protégé dans base.html")
else:
    print("❌ PROBLÈME: L'onglet admin n'est PAS protégé!")

# Test 3: Simuler une connexion
print("\n📝 TEST 3: Simulation de connexion")
print("-" * 70)

test_accounts = [
    ('gratuit@test.com', 'Test123!', 'gratuit', 'user'),
    ('premium@test.com', 'Test123!', 'premium', 'user'),
    ('admin@test.com', 'Admin123!', 'premium', 'admin')
]

for email, password, plan_attendu, role_attendu in test_accounts:
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    
    if user:
        # Vérifier le mot de passe
        pwd_ok = bcrypt.checkpw(password.encode('utf-8'), user['password'])
        
        print(f"\n👤 {user['name']}")
        print(f"   Email: {email}")
        print(f"   Mot de passe: {'✅ Correct' if pwd_ok else '❌ Incorrect'}")
        print(f"   Rôle DB: {user['role']} (attendu: {role_attendu})")
        print(f"   Plan DB: {user['plan']} (attendu: {plan_attendu})")
        
        # Simuler ce qui serait en session
        print(f"   SESSION attendue:")
        print(f"     - user_id: {user['id']}")
        print(f"     - role: {user['role']}")
        print(f"     - plan: {user['plan']}")
        
        # Déterminer quels onglets doivent être visibles
        print(f"   ONGLETS visibles:")
        print(f"     - Tableau de bord: ✅ Toujours")
        if user['role'] == 'user':
            print(f"     - Professionnels: ✅")
            if user['plan'] == 'premium':
                print(f"     - Favoris: ✅ (premium)")
            else:
                print(f"     - Favoris: ❌ (gratuit)")
        elif user['role'] == 'pro':
            print(f"     - Vérification: ✅")
        
        if user['plan'] == 'premium':
            print(f"     - Messages: ✅ (premium)")
        else:
            print(f"     - Messages: ❌ (gratuit)")
            
        print(f"     - Abonnement: ✅ Toujours")
        
        if user['role'] == 'admin':
            print(f"     - Admin: ✅ (administrateur)")
        else:
            print(f"     - Admin: ❌ (pas admin)")
    else:
        print(f"\n❌ Compte {email} introuvable")

conn.close()

print("\n" + "=" * 70)
print("📋 INSTRUCTIONS POUR TESTER MANUELLEMENT:")
print("=" * 70)
print("\n1. Ouvrez l'application dans votre navigateur")
print("2. Connectez-vous avec un des comptes ci-dessus")
print("3. Regardez la barre de navigation en haut")
print("4. Comparez avec les onglets attendus ci-dessus")
print("\n" + "=" * 70)
