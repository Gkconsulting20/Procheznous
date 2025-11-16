# ⚙️ PARAMÈTRES UTILISATEURS & PROTECTION DES DONNÉES

## 🎯 Objectif
Permettre aux utilisateurs existants de **compléter leurs informations** (ville, pays, géolocalisation) et protéger leurs **données personnelles sensibles** (email, téléphone) dans l'affichage public.

---

## ✅ Fonctionnalités Implémentées

### 1. **Page de Paramètres** (`/parametres`)

Accessible via le menu "⚙️ Paramètres", cette page permet aux utilisateurs de :

#### Informations personnelles :
- ✅ Modifier leur nom/pseudo
- ✅ Consulter leur email/téléphone (non modifiable, contact assistance requis)
- ✅ **Changer de pays** (liste déroulante)
- ✅ **Modifier la ville** (obligatoire)
- ✅ **Ajouter ou mettre à jour leur géolocalisation** (latitude/longitude)
- ✅ Modifier leur métier (professionnels uniquement)

#### Bouton de géolocalisation :
- 📍 "Utiliser ma position actuelle"
- API HTML5 Geolocation
- Affichage des coordonnées après capture
- Messages d'erreur clairs (permission refusée, timeout, etc.)

#### Sécurité :
- 🔒 Changement de mot de passe sécurisé
- Vérification du mot de passe actuel
- Confirmation du nouveau mot de passe
- Minimum 6 caractères

---

### 2. **Protection des Données Sensibles**

Fonction `mask_sensitive_data()` pour masquer les informations personnelles :

#### Email :
```
user@example.com → u***@example.com
```

#### Téléphone :
```
+22890123456 → +2289***456
```

Cette fonction est disponible dans **tous les templates** et peut être utilisée comme suit :

```html
{{ mask_sensitive_data(user.email, 'email') }}
{{ mask_sensitive_data(user.phone, 'phone') }}
```

---

## 📦 Fichiers Créés/Modifiés

### Nouveaux fichiers :
1. ✅ `templates/parametres.html` - Interface paramètres utilisateur

### Fichiers modifiés :
1. ✅ `app.py` 
   - Routes `/parametres` (GET/POST) - lignes 886-922
   - Route `/change_password` (POST) - lignes 924-958
   - Fonction `mask_sensitive_data()` - lignes 107-136
   - Context processor mis à jour - ligne 180

2. ✅ `templates/base.html`
   - Lien menu "⚙️ Paramètres" - ligne 44

---

## 🔧 Utilisation

### Pour les utilisateurs :

1. **Compléter les informations** :
   - Se connecter
   - Cliquer sur "⚙️ Paramètres" dans le menu
   - Remplir ville, pays
   - Cliquer sur "📍 Utiliser ma position actuelle" pour la géolocalisation
   - Enregistrer

2. **Changer le mot de passe** :
   - Aller dans Paramètres
   - Scroller jusqu'à "Modifier mon mot de passe"
   - Entrer le mot de passe actuel
   - Entrer le nouveau mot de passe (2 fois)
   - Valider

---

## 🛡️ Sécurité & Confidentialité

### Données non modifiables via l'interface :
- **Email** : Protection contre le vol de compte
- **Téléphone** : Protection contre l'usurpation d'identité
- **Rôle** : Sécurité du système

Pour modifier ces données, l'utilisateur doit contacter l'assistance.

### Masquage automatique :
- Les emails/téléphones ne sont **jamais affichés en clair** dans les profils publics
- Seul l'utilisateur voit ses propres données complètes
- Protection contre le spam et le phishing

---

## 📊 Exemples de Mise à Jour

### Cas 1 : Utilisateur sans géolocalisation

**Avant :**
```
Nom: Jean Dupont
Ville: NULL
Pays: NULL
Latitude: NULL
Longitude: NULL
```

**Après :**
```
Nom: Jean Dupont
Ville: Lomé
Pays: Togo
Latitude: 6.131935
Longitude: 1.222757
```

### Cas 2 : Professionnel changement de métier

**Avant :**
```
Nom: Marie Pro
Métier: Plomberie
Ville: Cotonou
```

**Après :**
```
Nom: Marie Pro
Métier: Électricité
Ville: Cotonou
```

---

## 🎨 Interface Utilisateur

### Page Paramètres :
- **Card 1** : Informations personnelles
  - Nom (modifiable)
  - Email (lecture seule)
  - Téléphone (lecture seule)
  - Pays (dropdown)
  - Ville (input)
  - Géolocalisation (bouton + coordonnées)
  - Métier (pro uniquement)

- **Card 2** : Changer le mot de passe
  - Mot de passe actuel
  - Nouveau mot de passe
  - Confirmation

- **Bouton retour** : Vers le tableau de bord

---

## ✅ Tests Validés

### Test 1 : Accès page
```
✅ Page accessible aux utilisateurs connectés
✅ Redirection login si non connecté
✅ Données utilisateur pré-remplies
```

### Test 2 : Mise à jour informations
```
✅ Nom modifié : "Test Paramètres" → "Test Paramètres MODIFIÉ"
✅ Ville changée : "Cotonou" → "Lomé"
✅ Pays changé : "Bénin" → "Togo"
✅ Géolocalisation ajoutée : 6.131935, 1.222757
```

### Test 3 : Masquage données
```
✅ Email : "user@example.com" → "u***@example.com"
✅ Téléphone : "+22890123456" → "+2289***456"
```

### Test 4 : Changement mot de passe
```
✅ Vérification mot de passe actuel
✅ Validation nouveau mot de passe
✅ Confirmation mot de passe
✅ Hachage bcrypt
```

---

## 🚀 Déploiement

### Fichiers à uploader sur PythonAnywhere :
1. `app.py`
2. `templates/parametres.html`
3. `templates/base.html`

### Hash MD5 de vérification :
```bash
md5sum app.py templates/parametres.html templates/base.html
```

### Sur PythonAnywhere :
```bash
cd /home/gkconsulting/prochenous2

# Supprimer les anciens
rm app.py templates/parametres.html templates/base.html

# Uploader les nouveaux via l'interface Files

# Vérifier hash MD5
md5sum app.py templates/parametres.html templates/base.html

# Reload le site
# Web → Reload www.pro-chez-nous.com
```

---

## 🎯 Impact Utilisateur

### Avantages :
1. **Complétion de profil** : Les utilisateurs existants peuvent ajouter ville, pays, GPS
2. **Confidentialité** : Email/téléphone protégés dans l'affichage public
3. **Contrôle** : Modification facile des informations personnelles
4. **Sécurité** : Changement de mot de passe autonome

### Cas d'usage :
- Utilisateur inscrit sans ville → Ajoute sa localisation
- Utilisateur sans GPS → Active la géolocalisation pour la recherche de proximité
- Professionnel change de métier → Met à jour sa catégorie
- Utilisateur oublie son mot de passe → Le change dans Paramètres

---

**🎉 Système de paramètres opérationnel pour tous les utilisateurs !**
