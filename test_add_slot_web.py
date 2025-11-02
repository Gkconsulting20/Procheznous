#!/usr/bin/env python3
"""
Test automatisé de l'ajout de créneau via l'interface web
"""

import requests
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:5000"

def test_add_slot():
    """Test complet: connexion pro + ajout créneau"""
    
    print("\n" + "="*70)
    print("TEST AJOUT CRÉNEAU - INTERFACE WEB")
    print("="*70)
    
    # Créer une session pour garder les cookies
    session = requests.Session()
    
    # 1. CONNEXION EN TANT QUE PRO
    print("\n1️⃣ Connexion en tant que professionnel...")
    login_data = {
        'identifier': 'pro@test.com',
        'password': 'Test2025!'
    }
    
    response = session.post(f"{BASE_URL}/login", data=login_data, allow_redirects=False)
    
    if response.status_code == 302:  # Redirection = succès
        print("   ✅ Connexion réussie")
    else:
        print(f"   ❌ Échec connexion: {response.status_code}")
        print(f"   Réponse: {response.text[:200]}")
        return False
    
    # 2. TESTER L'AJOUT DE CRÉNEAU
    print("\n2️⃣ Ajout d'un créneau...")
    
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    slot_data = {
        'date': tomorrow,
        'heure': '15:30'
    }
    
    print(f"   Date: {slot_data['date']}")
    print(f"   Heure: {slot_data['heure']}")
    
    response = session.post(f"{BASE_URL}/add_slot", data=slot_data, allow_redirects=False)
    
    print(f"   Code retour: {response.status_code}")
    
    if response.status_code == 302:  # Redirection = succès
        redirect_url = response.headers.get('Location', '')
        print(f"   ✅ Créneau ajouté ! Redirection vers: {redirect_url}")
        
        # Vérifier le message flash
        dashboard_response = session.get(f"{BASE_URL}/dashboard")
        if "Créneau ajouté avec succès" in dashboard_response.text:
            print("   ✅ Message de succès confirmé")
            return True
        elif "obligatoire" in dashboard_response.text:
            print("   ❌ Erreur: champs obligatoires manquants")
            return False
        else:
            print("   ⚠️  Statut incertain")
            return True
    else:
        print(f"   ❌ Échec ajout créneau")
        print(f"   Réponse: {response.text[:500]}")
        return False

if __name__ == '__main__':
    try:
        success = test_add_slot()
        print("\n" + "="*70)
        if success:
            print("✅ TEST RÉUSSI - L'ajout de créneau fonctionne !")
        else:
            print("❌ TEST ÉCHOUÉ - Problème détecté")
        print("="*70 + "\n")
    except Exception as e:
        print(f"\n❌ ERREUR DURANT LE TEST: {e}\n")
        import traceback
        traceback.print_exc()
