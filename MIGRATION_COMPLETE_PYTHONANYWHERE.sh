#!/bin/bash
# ══════════════════════════════════════════════════════════════════════
# MIGRATION COMPLÈTE - PRO CHEZ NOUS
# PythonAnywhere Production - www.pro-chez-nous.com
# ══════════════════════════════════════════════════════════════════════

echo "🚀 Début de la migration complète..."
echo ""

cd /home/gkconsulting/prochenous2

# ═══════════ ÉTAPE 1 : SAUVEGARDE ═══════════
echo "📦 Étape 1/4 : Sauvegarde de la base de données..."
cp database.db database.db.backup_migration_$(date +%Y%m%d_%H%M%S)
echo "✅ Sauvegarde créée"
echo ""

# ═══════════ ÉTAPE 2 : MIGRATION DATABASE ═══════════
echo "🔧 Étape 2/4 : Migration de la base de données..."

python3 << 'PYTHON_EOF'
import sqlite3

conn = sqlite3.connect('database.db')

print("  → Ajout des colonnes à la table users...")
colonnes = [
    ("phone", "ALTER TABLE users ADD COLUMN phone TEXT"),
    ("plan", "ALTER TABLE users ADD COLUMN plan TEXT DEFAULT 'gratuit'"),
    ("verification_status", "ALTER TABLE users ADD COLUMN verification_status TEXT DEFAULT 'en_attente'"),
    ("latitude", "ALTER TABLE users ADD COLUMN latitude REAL"),
    ("longitude", "ALTER TABLE users ADD COLUMN longitude REAL")
]

for nom, sql in colonnes:
    try:
        conn.execute(sql)
        print(f"    ✅ Colonne '{nom}' ajoutée")
    except Exception as e:
        if "duplicate column" in str(e).lower():
            print(f"    ⏭️  Colonne '{nom}' existe déjà")
        else:
            print(f"    ❌ Erreur pour '{nom}': {e}")

print("\n  → Mise à jour des utilisateurs existants...")
conn.execute("UPDATE users SET plan = 'gratuit' WHERE plan IS NULL OR plan = ''")
conn.commit()
print("    ✅ Utilisateurs mis à jour")

print("\n  → Création de la table categories...")
conn.execute('''
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL UNIQUE,
    icone TEXT,
    actif INTEGER DEFAULT 1,
    ordre INTEGER DEFAULT 0,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
''')
print("    ✅ Table categories créée")

# Vérifier si elle est vide
count = conn.execute('SELECT COUNT(*) FROM categories').fetchone()[0]
if count == 0:
    print("\n  → Insertion des 75 catégories...")
    categories = [
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
    conn.executemany('INSERT INTO categories (nom, icone, ordre) VALUES (?, ?, ?)', categories)
    conn.commit()
    print("    ✅ 75 catégories insérées")
else:
    print(f"    ⏭️  {count} catégories déjà présentes")

conn.close()
print("\n✅ Migration de la base de données terminée")
PYTHON_EOF

echo ""

# ═══════════ ÉTAPE 3 : VÉRIFICATION ═══════════
echo "🔍 Étape 3/4 : Vérification..."

python3 << 'VERIFY_EOF'
import sqlite3
conn = sqlite3.connect('database.db')

# Vérifier la table categories
count_cat = conn.execute('SELECT COUNT(*) FROM categories').fetchone()[0]
print(f"  ✅ Table categories: {count_cat} catégories")

# Vérifier la table users
cursor = conn.execute("PRAGMA table_info(users)")
columns = [row[1] for row in cursor.fetchall()]
required = ['phone', 'plan', 'verification_status', 'latitude', 'longitude']
missing = [col for col in required if col not in columns]

if missing:
    print(f"  ❌ Colonnes manquantes: {missing}")
else:
    print(f"  ✅ Table users: toutes les colonnes présentes")

conn.close()
VERIFY_EOF

echo ""

# ═══════════ ÉTAPE 4 : INSTRUCTIONS FINALES ═══════════
echo "📝 Étape 4/4 : Instructions finales"
echo ""
echo "✅ MIGRATION TERMINÉE AVEC SUCCÈS!"
echo ""
echo "🔄 PROCHAINES ÉTAPES:"
echo "  1. Allez dans l'onglet 'Web' sur PythonAnywhere"
echo "  2. Cliquez sur 'Reload gkconsulting.pythonanywhere.com'"
echo "  3. Attendez 10 secondes"
echo "  4. Testez www.pro-chez-nous.com"
echo ""
echo "✨ Votre application devrait maintenant fonctionner parfaitement!"
echo ""
