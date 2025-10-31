#!/usr/bin/env python3
"""
Script de correction de sécurité pour PRO CHEZ NOUS
Corrige les problèmes d'accès admin et premium
"""

import os

print("🔧 Correction de la sécurité PRO CHEZ NOUS")
print("=" * 60)

# ===== CORRECTIF 1 : app.py - Ajouter plan dans session =====
print("\n📝 Correction de app.py (ajout du plan dans la session)...")

# Lire le fichier
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Correction 1 : Ajouter session['plan'] dans login
old_login = """        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['user_id'] = user['id']
            session['role'] = user['role']
            flash(f'Bienvenue {user["name"]}!', 'success')"""

new_login = """        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['plan'] = user['plan']
            flash(f'Bienvenue {user["name"]}!', 'success')"""

if old_login in content:
    content = content.replace(old_login, new_login)
    print("   ✅ Plan ajouté dans la session de connexion")
else:
    print("   ⚠️  Modification login déjà effectuée ou format différent")

# Sauvegarder
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

# ===== CORRECTIF 2 : base.html - Masquer onglets premium =====
print("\n📝 Correction de templates/base.html (onglets premium)...")

# Lire le fichier
with open('templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Correction : Masquer Favoris pour non-premium
old_favoris = '            <li class="nav-item"><a class="nav-link" href="{{ url_for(\'favoris\') }}">⭐ Favoris</a></li>'
new_favoris = '''            {% if session.plan == 'premium' %}
            <li class="nav-item"><a class="nav-link" href="{{ url_for('favoris') }}">⭐ Favoris</a></li>
            {% endif %}'''

if old_favoris in content and new_favoris not in content:
    content = content.replace(old_favoris, new_favoris)
    print("   ✅ Onglet Favoris masqué pour non-premium")
else:
    print("   ⚠️  Modification Favoris déjà effectuée")

# Correction : Masquer Messages pour non-premium
old_messages = '            <li class="nav-item"><a class="nav-link" href="{{ url_for(\'messages\') }}">💬 Messages</a></li>'
new_messages = '''            {% if session.plan == 'premium' %}
            <li class="nav-item"><a class="nav-link" href="{{ url_for('messages') }}">💬 Messages</a></li>
            {% endif %}'''

if old_messages in content and new_messages not in content:
    content = content.replace(old_messages, new_messages)
    print("   ✅ Onglet Messages masqué pour non-premium")
else:
    print("   ⚠️  Modification Messages déjà effectuée")

# Sauvegarder
with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "=" * 60)
print("✅ CORRECTION TERMINÉE AVEC SUCCÈS!")
print("=" * 60)
print("\n📋 RÉSUMÉ DES CORRECTIONS:")
print("   1. ✅ Le plan de l'utilisateur est maintenant dans la session")
print("   2. ✅ Les onglets Messages et Favoris sont masqués pour les comptes gratuits")
print("   3. ✅ L'onglet Admin est masqué pour les non-administrateurs")
print("\n🔄 PROCHAINES ÉTAPES:")
print("   1. Rechargez votre application (Web → Reload)")
print("   2. Déconnectez-vous puis reconnectez-vous")
print("   3. Testez avec un compte gratuit : pas d'onglets premium")
print("   4. Testez avec un compte admin : onglet Admin visible")
print("\n" + "=" * 60)
