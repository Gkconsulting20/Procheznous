#!/usr/bin/env python3
"""
Script de nettoyage de la base de données PRO CHEZ NOUS
Efface toutes les données de test tout en gardant la structure
"""

import sqlite3
import os

def clean_database():
    """Nettoie toutes les données de test de la base de données"""
    
    db_path = 'database.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Erreur: Base de données '{db_path}' introuvable")
        return False
    
    # Créer une sauvegarde avant nettoyage
    backup_path = 'database_backup.db'
    print(f"📦 Création d'une sauvegarde: {backup_path}")
    
    import shutil
    shutil.copy2(db_path, backup_path)
    print(f"✅ Sauvegarde créée avec succès")
    
    # Connexion à la base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\n🧹 Nettoyage de la base de données...")
    print("=" * 50)
    
    # Liste des tables à nettoyer (dans l'ordre pour respecter les contraintes)
    tables_to_clean = [
        'messages',
        'favoris',
        'avis',
        'rendezvous',
        'slots',
        'profils_pro',
        'documents_verification',
        'password_reset_tokens',
        'sms_verifications',
        'users'
    ]
    
    try:
        for table in tables_to_clean:
            # Vérifier si la table existe
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name=?
            """, (table,))
            
            if cursor.fetchone():
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                
                if count > 0:
                    cursor.execute(f"DELETE FROM {table}")
                    print(f"✅ Table '{table}': {count} enregistrement(s) supprimé(s)")
                else:
                    print(f"⚪ Table '{table}': Déjà vide")
            else:
                print(f"⚠️  Table '{table}': N'existe pas")
        
        # Réinitialiser les séquences auto-increment
        cursor.execute("DELETE FROM sqlite_sequence")
        print(f"✅ Séquences auto-increment réinitialisées")
        
        # Valider les changements
        conn.commit()
        print("\n" + "=" * 50)
        print("✅ Base de données nettoyée avec succès !")
        print(f"📦 Sauvegarde disponible: {backup_path}")
        print("\n💡 Pour restaurer la sauvegarde en cas de problème:")
        print(f"   cp {backup_path} {db_path}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du nettoyage: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

def verify_structure():
    """Vérifie que la structure de la base de données est intacte"""
    
    db_path = 'database.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\n🔍 Vérification de la structure de la base de données...")
    print("=" * 50)
    
    # Liste des tables essentielles
    required_tables = [
        'users',
        'slots',
        'rendezvous',
        'avis',
        'profils_pro',
        'messages',
        'favoris',
        'documents_verification',
        'password_reset_tokens'
    ]
    
    all_ok = True
    for table in required_tables:
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name=?
        """, (table,))
        
        if cursor.fetchone():
            print(f"✅ Table '{table}': OK")
        else:
            print(f"❌ Table '{table}': MANQUANTE")
            all_ok = False
    
    conn.close()
    
    if all_ok:
        print("\n✅ Structure de la base de données: OK")
    else:
        print("\n⚠️  Certaines tables sont manquantes")
    
    return all_ok

if __name__ == '__main__':
    print("=" * 50)
    print("🧹 NETTOYAGE BASE DE DONNÉES - PRO CHEZ NOUS")
    print("=" * 50)
    print("\n⚠️  ATTENTION: Ce script va supprimer TOUTES les données de test")
    print("Une sauvegarde sera créée automatiquement.")
    
    response = input("\n❓ Voulez-vous continuer? (oui/non): ").strip().lower()
    
    if response in ['oui', 'o', 'yes', 'y']:
        print("\n🚀 Démarrage du nettoyage...")
        
        if clean_database():
            verify_structure()
            print("\n🎉 Nettoyage terminé ! Votre base de données est prête pour la production.")
        else:
            print("\n❌ Le nettoyage a échoué. Vérifiez les erreurs ci-dessus.")
    else:
        print("\n❌ Nettoyage annulé par l'utilisateur.")
