# 📍 GÉOLOCALISATION À L'INSCRIPTION

## 🎯 Objectif
Permettre à **TOUS les utilisateurs** (clients ET professionnels) de se géolocaliser dès l'inscription pour améliorer la recherche de proximité.

---

## ✅ Modifications Apportées

### 1. **Formulaire d'inscription** (`templates/register.html`)

#### Champs ajoutés/modifiés :
- **Ville** : Maintenant **obligatoire pour TOUS** (pas seulement les pros)
- **Bouton de géolocalisation** : "📍 Utiliser ma position actuelle"
- **Latitude/Longitude** : Champs cachés pour stocker les coordonnées GPS

#### Interface utilisateur :
```html
<div class="mb-3">
    <label>Ville *</label>
    <input name="localisation" required>
</div>

<div class="mb-3">
    <label>📍 Géolocalisation</label>
    <button type="button" onclick="getLocation()">
        📍 Utiliser ma position actuelle
    </button>
    <input type="hidden" name="latitude">
    <input type="hidden" name="longitude">
</div>
```

#### Fonctionnalités JavaScript :
- **API HTML5 Geolocation** : Demande l'accès à la position
- **Feedback visuel** : États du bouton (En cours, Réussi, Erreur)
- **Gestion des erreurs** :
  - Permission refusée
  - Position indisponible
  - Timeout

### 2. **Route d'inscription** (`app.py`)

#### Modifications (lignes 168-174) :
```python
latitude = request.form.get('latitude', '').strip()
longitude = request.form.get('longitude', '').strip()

latitude = float(latitude) if latitude else None
longitude = float(longitude) if longitude else None

if not name or not password or not role or not localisation:
    flash('Tous les champs obligatoires doivent être remplis')
```

#### Sauvegarde en base (lignes 209-219) :
```python
INSERT INTO users 
(name, email, phone, password, role, localisation, pays, categorie, 
 latitude, longitude,
 plan, subscription_started_at, subscription_expires_at, subscription_status) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'premium', ?, ?, 'trial')
```

---

## 📊 Exemple de Données Enregistrées

### Utilisateur avec géolocalisation :
```
Nom: Test Géolocalisation
Email: geo_test@example.com
Ville: Lomé
Pays: Togo
Latitude: 6.1319
Longitude: 1.2228
```

### Utilisateur sans géolocalisation :
```
Nom: Test Sans Géo
Email: no_geo@example.com
Ville: Cotonou
Pays: Bénin
Latitude: NULL
Longitude: NULL
```

---

## 🎨 Expérience Utilisateur

### Étape 1 : Remplir le formulaire
- Nom, Email/Téléphone, Mot de passe
- **Pays** (obligatoire)
- **Ville** (obligatoire)

### Étape 2 : Géolocalisation (optionnel)
- Cliquer sur "📍 Utiliser ma position actuelle"
- Le navigateur demande l'autorisation
- Si accepté : Position enregistrée avec coordonnées affichées
- Si refusé : Inscription reste possible sans GPS

### Étape 3 : Choisir le rôle
- Client ou Professionnel
- Si professionnel : Sélectionner le métier

---

## 🔍 Utilisation des Coordonnées GPS

### Recherche de proximité (Premium) :
1. **Calcul de distance** : Formule Haversine
2. **Tri par proximité** : Professionnels les plus proches en premier
3. **Filtre géographique** : Rayon de recherche personnalisable

### Exemple de calcul :
```python
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Rayon de la Terre en km
    
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    return R * c  # Distance en km
```

---

## 🛡️ Sécurité & Confidentialité

### Permissions navigateur :
- L'utilisateur **doit autoriser** l'accès à sa position
- Aucune géolocalisation forcée
- Permission demandée à chaque utilisation

### Stockage :
- Coordonnées stockées uniquement si fournies
- `NULL` par défaut si refusé
- Pas de tracking en temps réel

### RGPD :
- Consentement explicite requis
- Données utilisées uniquement pour la recherche de proximité
- Possibilité de continuer sans GPS

---

## 📱 Compatibilité

### Navigateurs supportés :
- ✅ Chrome/Edge (Desktop & Mobile)
- ✅ Firefox (Desktop & Mobile)
- ✅ Safari (Desktop & Mobile)
- ✅ Opera

### Prérequis :
- **HTTPS obligatoire** en production (l'API Geolocation nécessite une connexion sécurisée)
- GPS activé sur mobile
- Autorisation de localisation accordée

---

## 🚀 Déploiement

### Fichiers modifiés :
1. ✅ `templates/register.html` (formulaire + JavaScript)
2. ✅ `app.py` (route d'inscription)

### Hash MD5 :
```bash
md5sum templates/register.html app.py
```

### Sur PythonAnywhere :
```bash
cd /home/gkconsulting/prochenous2

# Supprimer les anciens
rm templates/register.html app.py

# Uploader les nouveaux via l'interface Files

# Reload le site
# Web → Reload www.pro-chez-nous.com
```

---

## ✅ Tests Validés

### Test 1 : Inscription avec GPS
```
✅ Coordonnées enregistrées : 6.1319, 1.2228
✅ Ville : Lomé
✅ Pays : Togo
```

### Test 2 : Inscription sans GPS
```
✅ Inscription réussie
✅ Latitude : NULL
✅ Longitude : NULL
```

### Test 3 : Validation formulaire
```
✅ Ville obligatoire
✅ Pays obligatoire
✅ Géolocalisation optionnelle
```

---

## 🎯 Impact sur la Plateforme

### Avantages :
1. **Recherche plus précise** : Tri par proximité réelle
2. **Meilleure UX** : Professionnels à proximité en premier
3. **Data enrichie** : Base de données géolocalisée
4. **Différenciation** : Fonctionnalité unique sur le marché africain

### Cas d'usage :
- Client cherche plombier → Voit les plus proches en premier
- Professionnel cherche clients → Visibilité locale renforcée
- Statistiques → Cartographie des professionnels par zone

---

**🎉 Géolocalisation opérationnelle pour tous les utilisateurs !**
