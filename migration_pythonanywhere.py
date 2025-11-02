#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DE MIGRATION SÉCURISÉ POUR PYTHONANYWHERE
Ajoute les nouvelles fonctionnalités sans toucher aux données existantes
"""

import sqlite3
import os

def migration_securisee():
    """Migration progressive et sécurisée"""
    
    # Chemin de la base de données
    db_path = 'pro_chez_nous.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Erreur : Fichier {db_path} introuvable")
        return
    
    print(f"📂 Connexion à {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\n" + "="*60)
    print("🔍 ANALYSE DE LA BASE DE DONNÉES ACTUELLE")
    print("="*60)
    
    # 1. Vérifier les tables existantes
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"\n✅ Tables existantes : {', '.join(tables)}")
    
    # 2. Créer la table categories si elle n'existe pas
    if 'categories' not in tables:
        print("\n📝 Création de la table 'categories'...")
        cursor.execute('''
            CREATE TABLE categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL UNIQUE,
                icone TEXT,
                actif INTEGER DEFAULT 1,
                ordre INTEGER DEFAULT 0,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Ajouter les 75 catégories par défaut
        categories_defaut = [
            ('Plomberie', '🔧', 1, 1), ('Électricité', '⚡', 1, 2), ('Peinture', '🎨', 1, 3),
            ('Menuiserie', '🪚', 1, 4), ('Maçonnerie', '🧱', 1, 5), ('Carrelage', '🏗️', 1, 6),
            ('Climatisation', '❄️', 1, 7), ('Jardinage', '🌿', 1, 8), ('Nettoyage', '🧹', 1, 9),
            ('Déménagement', '📦', 1, 10), ('Sécurité', '🔒', 1, 11), ('Rénovation', '🏠', 1, 12),
            ('Toiture', '🏚️', 1, 13), ('Vitrerie', '🪟', 1, 14), ('Serrurerie', '🔑', 1, 15),
            ('Chauffage', '🔥', 1, 16), ('Soudure', '🔥', 1, 17), ('Ferronnerie', '⚒️', 1, 18),
            ('Couture', '🧵', 1, 19), ('Coiffure', '✂️', 1, 20), ('Esthétique', '💅', 1, 21),
            ('Mécanique Auto', '🚗', 1, 22), ('Mécanique Moto', '🏍️', 1, 23), ('Réparation Électronique', '📱', 1, 24),
            ('Informatique', '💻', 1, 25), ('Photographie', '📸', 1, 26), ('Vidéographie', '🎥', 1, 27),
            ('Cuisine', '👨‍🍳', 1, 28), ('Pâtisserie', '🧁', 1, 29), ('Traiteur', '🍽️', 1, 30),
            ('Boulangerie', '🥖', 1, 31), ('Cordonnerie', '👞', 1, 32), ('Tapisserie', '🛋️', 1, 33),
            ('Décoration', '🎨', 1, 34), ('Architecture', '📐', 1, 35), ('Design', '✨', 1, 36),
            ('Soudure Aluminium', '⚡', 1, 37), ('Soudure Inox', '🔩', 1, 38), ('Charpentier', '🪵', 1, 39),
            ('Ébéniste', '🪑', 1, 40), ('Forgeron', '🔨', 1, 41), ('Tailleur', '👔', 1, 42),
            ('Broderie', '🧵', 1, 43), ('Pressing', '👗', 1, 44), ('Cordonnerie', '👢', 1, 45),
            ('Réparation Vélo', '🚴', 1, 46), ('Vulcanisation', '🛞', 1, 47), ('Peinture Auto', '🚙', 1, 48),
            ('Carrosserie', '🚗', 1, 49), ('Vitrerie Auto', '🚕', 1, 50), ('Installation Solaire', '☀️', 1, 51),
            ('Climatisation Auto', '❄️', 1, 52), ('Lavage Auto', '🧽', 1, 53), ('Paysagiste', '🌳', 1, 54),
            ('Élagage', '🌲', 1, 55), ('Arrosage', '💧', 1, 56), ('Désinsectisation', '🦟', 1, 57),
            ('Dératisation', '🐀', 1, 58), ('Entretien Piscine', '🏊', 1, 59), ('Ramonage', '🔥', 1, 60),
            ('Ascenseurs', '🛗', 1, 61), ('Portails', '🚪', 1, 62), ('Stores', '🪟', 1, 63),
            ('Volets', '🏠', 1, 64), ('Parquets', '🪵', 1, 65), ('Isolation', '🧱', 1, 66),
            ('Étanchéité', '💧', 1, 67), ('Gouttières', '🌧️', 1, 68), ('Cheminées', '🔥', 1, 69),
            ('Alarmes', '🚨', 1, 70), ('Vidéosurveillance', '📹', 1, 71), ('Télésurveillance', '👁️', 1, 72),
            ('Domotique', '🏡', 1, 73), ('Photovoltaïque', '☀️', 1, 74), ('Éolien', '💨', 1, 75)
        ]
        
        cursor.executemany('INSERT INTO categories (nom, icone, actif, ordre) VALUES (?, ?, ?, ?)', categories_defaut)
        print(f"✅ Table 'categories' créée avec {len(categories_defaut)} catégories")
    else:
        print("\nℹ️ Table 'categories' existe déjà")
    
    # 3. Créer la table devis si elle n'existe pas
    if 'devis' not in tables:
        print("\n📝 Création de la table 'devis'...")
        cursor.execute('''
            CREATE TABLE devis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pro_id INTEGER NOT NULL,
                client_id INTEGER NOT NULL,
                titre TEXT NOT NULL,
                description TEXT NOT NULL,
                montant REAL NOT NULL,
                statut TEXT DEFAULT 'en_attente',
                type_devis TEXT DEFAULT 'demande_client',
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_reponse TIMESTAMP,
                FOREIGN KEY (pro_id) REFERENCES users (id),
                FOREIGN KEY (client_id) REFERENCES users (id)
            )
        ''')
        print("✅ Table 'devis' créée")
    else:
        print("\nℹ️ Table 'devis' existe déjà")
    
    # 4. Vérifier la structure de la table messages
    if 'messages' in tables:
        cursor.execute(f"PRAGMA table_info(messages)")
        colonnes_messages = [row[1] for row in cursor.fetchall()]
        print(f"\n📋 Colonnes de 'messages' : {', '.join(colonnes_messages)}")
        
        # Si la table utilise les anciens noms (expediteur_id, destinataire_id)
        if 'expediteur_id' in colonnes_messages and 'sender_id' not in colonnes_messages:
            print("\n⚠️ Détection de l'ancien format de 'messages' (expediteur_id/destinataire_id)")
            print("🔄 Renommage des colonnes...")
            
            # SQLite ne supporte pas ALTER COLUMN RENAME directement
            # On doit recréer la table
            cursor.execute('''
                CREATE TABLE messages_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender_id INTEGER NOT NULL,
                    receiver_id INTEGER NOT NULL,
                    contenu TEXT NOT NULL,
                    date_envoi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    lu INTEGER DEFAULT 0,
                    FOREIGN KEY (sender_id) REFERENCES users (id),
                    FOREIGN KEY (receiver_id) REFERENCES users (id)
                )
            ''')
            
            # Copier les données
            cursor.execute('''
                INSERT INTO messages_new (id, sender_id, receiver_id, contenu, date_envoi, lu)
                SELECT id, expediteur_id, destinataire_id, contenu, date_envoi, lu
                FROM messages
            ''')
            
            # Supprimer l'ancienne table et renommer
            cursor.execute('DROP TABLE messages')
            cursor.execute('ALTER TABLE messages_new RENAME TO messages')
            
            print("✅ Colonnes 'messages' renommées : expediteur_id → sender_id, destinataire_id → receiver_id")
    
    # 5. Ajouter la colonne statut_compte si manquante
    cursor.execute("PRAGMA table_info(users)")
    colonnes_users = [row[1] for row in cursor.fetchall()]
    
    if 'statut_compte' not in colonnes_users:
        print("\n📝 Ajout de la colonne 'statut_compte' à 'users'...")
        cursor.execute('ALTER TABLE users ADD COLUMN statut_compte TEXT DEFAULT "actif"')
        print("✅ Colonne 'statut_compte' ajoutée")
    else:
        print("\nℹ️ Colonne 'statut_compte' existe déjà")
    
    # 6. Vérifier la colonne type_devis dans devis
    if 'devis' in tables or 'devis' not in tables:  # Si on vient de la créer
        cursor.execute("PRAGMA table_info(devis)")
        colonnes_devis = [row[1] for row in cursor.fetchall()]
        
        if 'type_devis' not in colonnes_devis and 'devis' in tables:
            print("\n📝 Ajout de la colonne 'type_devis' à 'devis'...")
            cursor.execute('ALTER TABLE devis ADD COLUMN type_devis TEXT DEFAULT "demande_client"')
            print("✅ Colonne 'type_devis' ajoutée")
    
    # Valider les changements
    conn.commit()
    
    print("\n" + "="*60)
    print("✅ MIGRATION TERMINÉE AVEC SUCCÈS")
    print("="*60)
    
    # Afficher un résumé
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables_finales = [row[0] for row in cursor.fetchall()]
    print(f"\n📊 Tables finales : {', '.join(tables_finales)}")
    
    # Compter les données
    cursor.execute("SELECT COUNT(*) FROM users")
    nb_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM categories")
    nb_categories = cursor.fetchone()[0]
    
    print(f"\n📈 Statistiques :")
    print(f"   👥 Utilisateurs : {nb_users}")
    print(f"   📂 Catégories : {nb_categories}")
    
    if 'messages' in tables_finales:
        cursor.execute("SELECT COUNT(*) FROM messages")
        nb_messages = cursor.fetchone()[0]
        print(f"   💬 Messages : {nb_messages}")
    
    if 'devis' in tables_finales:
        cursor.execute("SELECT COUNT(*) FROM devis")
        nb_devis = cursor.fetchone()[0]
        print(f"   📝 Devis : {nb_devis}")
    
    conn.close()
    print("\n✅ Base de données fermée")
    print("\n🚀 Vous pouvez maintenant recharger l'application sur PythonAnywhere!")

if __name__ == '__main__':
    print("="*60)
    print("🔧 MIGRATION SÉCURISÉE - PRO CHEZ NOUS")
    print("="*60)
    migration_securisee()
