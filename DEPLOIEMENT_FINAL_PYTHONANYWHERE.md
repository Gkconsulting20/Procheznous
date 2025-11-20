# 🚀 DÉPLOIEMENT FINAL - PythonAnywhere

**Date :** 19 novembre 2025  
**Plateforme :** PRO CHEZ NOUS  
**Nouvelles fonctionnalités :** Conditions d'utilisation + FedaPay LIVE

---

## ⏱️ Temps Total : 30 minutes

```
📦 Transfert fichiers : 15 min
🔐 Configuration secrets : 5 min
🔗 Configuration FedaPay : 5 min
✅ Tests : 5 min
```

---

## 📋 ÉTAPE 1 : PRÉPARATION (2 min)

### Ce que vous allez déployer :

✅ **5 fichiers MODIFIÉS** (à remplacer)
✅ **2 fichiers NOUVEAUX** (à créer)
✅ **3 secrets** (à configurer)
✅ **1 callback** (à configurer dans FedaPay)

### Avant de commencer :

- [ ] Vous êtes connecté à PythonAnywhere
- [ ] Vous êtes connecté à FedaPay
- [ ] Vous avez vos clés FedaPay LIVE sous la main

---

## 📤 ÉTAPE 2 : TRANSFERT DES FICHIERS (15 min)

### Méthode Recommandée : Via le Dashboard "Files"

1. **Connectez-vous** à https://www.pythonanywhere.com
2. **Allez dans l'onglet** "Files"
3. **Naviguez vers** `/home/votre_nom/mysite/`

---

### 📝 A. Fichiers Python (à remplacer)

#### 1. `app.py`

```bash
Chemin : /home/votre_nom/mysite/app.py
Action : Remplacer le contenu
```

**Comment faire :**
1. Sur **Replit**, ouvrez `app.py`
2. **Sélectionnez tout** (Ctrl+A)
3. **Copiez** (Ctrl+C)
4. Sur **PythonAnywhere**, ouvrez `app.py`
5. **Sélectionnez tout** et supprimez
6. **Collez** (Ctrl+V)
7. **Sauvegardez** (Ctrl+S ou bouton "Save")

✅ Fichier 1/7 terminé

---

#### 2. `fedapay_service.py`

```bash
Chemin : /home/votre_nom/mysite/fedapay_service.py
Action : Remplacer le contenu
```

**Répétez** la même opération :
1. Ouvrez sur Replit → Copiez tout
2. Ouvrez sur PythonAnywhere → Collez
3. Sauvegardez

✅ Fichier 2/7 terminé

---

### 📄 B. Templates (à remplacer + créer)

**Naviguez vers** : `/home/votre_nom/mysite/templates/`

#### 3. `templates/base.html` (REMPLACER)

```bash
Chemin : /home/votre_nom/mysite/templates/base.html
Action : Remplacer le contenu
```

1. Copiez depuis Replit
2. Remplacez sur PythonAnywhere
3. Sauvegardez

✅ Fichier 3/7 terminé

---

#### 4. `templates/register.html` (REMPLACER)

```bash
Chemin : /home/votre_nom/mysite/templates/register.html
Action : Remplacer le contenu
```

1. Copiez depuis Replit
2. Remplacez sur PythonAnywhere
3. Sauvegardez

✅ Fichier 4/7 terminé

---

#### 5. `templates/conditions.html` (CRÉER - NOUVEAU)

```bash
Chemin : /home/votre_nom/mysite/templates/conditions.html
Action : Créer un nouveau fichier
```

**Comment créer un nouveau fichier :**
1. Dans le dossier `templates/`
2. Cliquez sur **"New file"** (ou icône "+" ou "Créer fichier")
3. Nommez-le **exactement** : `conditions.html`
4. Copiez le contenu depuis Replit
5. Collez dans le nouveau fichier
6. Sauvegardez

✅ Fichier 5/7 terminé

---

#### 6. `templates/admin_fedapay_test.html` (CRÉER - NOUVEAU)

```bash
Chemin : /home/votre_nom/mysite/templates/admin_fedapay_test.html
Action : Créer un nouveau fichier
```

1. Dans le dossier `templates/`
2. Créez un nouveau fichier : `admin_fedapay_test.html`
3. Copiez depuis Replit
4. Collez
5. Sauvegardez

✅ Fichier 6/7 terminé

---

#### 7. `replit.md` (OPTIONNEL - Documentation)

```bash
Chemin : /home/votre_nom/mysite/replit.md
Action : Remplacer le contenu (optionnel)
```

Ce fichier n'est pas critique pour le fonctionnement, mais gardez-le à jour pour la documentation.

✅ Fichier 7/7 terminé

---

## 🔐 ÉTAPE 3 : CONFIGURATION DES SECRETS (5 min)

### A. Accéder aux Variables d'Environnement

1. **Allez dans l'onglet** "Web" de PythonAnywhere
2. **Scrollez vers le bas** jusqu'à la section **"Environment variables"**
3. Vous verrez probablement déjà des variables (SECRET_KEY, etc.)

---

### B. Ajouter les 3 Secrets FedaPay

⚠️ **IMPORTANT** : Utilisez vos VRAIES clés FedaPay LIVE

#### Secret 1 : FEDAPAY_SECRET_KEY

```
Nom : FEDAPAY_SECRET_KEY
Valeur : sk_live_votre_clé_secrète_ici
```

**Comment faire :**
1. Cliquez sur **"Add new environment variable"**
2. Dans "Name" : tapez `FEDAPAY_SECRET_KEY`
3. Dans "Value" : collez votre clé (commence par `sk_live_`)
4. Cliquez sur le ✓ (coche verte) pour valider

---

#### Secret 2 : FEDAPAY_PUBLIC_KEY

```
Nom : FEDAPAY_PUBLIC_KEY
Valeur : pk_live_votre_clé_publique_ici
```

1. Ajoutez une nouvelle variable
2. Name : `FEDAPAY_PUBLIC_KEY`
3. Value : votre clé (commence par `pk_live_`)
4. Validez

---

#### Secret 3 : FEDAPAY_ENV

```
Nom : FEDAPAY_ENV
Valeur : live
```

⚠️ **ATTENTION** : Tapez exactement `live` (en minuscules, pas de guillemets)

1. Ajoutez une nouvelle variable
2. Name : `FEDAPAY_ENV`
3. Value : `live`
4. Validez

---

### C. Vérification

Vous devriez maintenant voir **3 nouvelles variables** :

```
FEDAPAY_SECRET_KEY = sk_live_•••••••••••
FEDAPAY_PUBLIC_KEY = pk_live_•••••••••••
FEDAPAY_ENV = live
```

✅ Secrets configurés !

---

## 🔄 ÉTAPE 4 : REDÉMARRER L'APPLICATION (1 min)

### C'EST L'ÉTAPE LA PLUS IMPORTANTE !

1. **Dans l'onglet "Web"** de PythonAnywhere
2. **En haut de la page**, trouvez le **gros bouton vert** marqué **"Reload www.pro-chez-nous.com"**
3. **Cliquez dessus**
4. **Attendez** 10-20 secondes

```
┌─────────────────────────────────────────┐
│  🌐 www.pro-chez-nous.com               │
│                                         │
│  [ 🔄 Reload www.pro-chez-nous.com ]   │
│         ↑                               │
│    CLIQUEZ ICI                          │
└─────────────────────────────────────────┘
```

⚠️ **Sans ce reload, les changements ne seront PAS actifs !**

---

## ✅ ÉTAPE 5 : TESTS (5 min)

### Test 1 : Page d'Accueil

```
URL : https://www.pro-chez-nous.com
Résultat attendu : La page charge correctement
```

✅ Si la page s'affiche → Bon signe !  
❌ Si erreur 500 → Consultez les logs (voir section Dépannage)

---

### Test 2 : Inscription avec Conditions

```
URL : https://www.pro-chez-nous.com/register
```

**Vérifications :**
- [ ] La checkbox "J'accepte les conditions d'utilisation" est visible
- [ ] Le lien "conditions d'utilisation" est cliquable
- [ ] Si vous essayez de vous inscrire SANS cocher → Message d'erreur
- [ ] Si vous cochez et remplissez le formulaire → Inscription réussie

---

### Test 3 : Page Conditions

```
URL : https://www.pro-chez-nous.com/conditions
```

**Vérifications :**
- [ ] La page s'affiche
- [ ] Les 9 sections sont visibles
- [ ] Le design est propre

---

### Test 4 : Connexion Admin

```
1. Connectez-vous avec votre compte admin
2. Vérifiez que le menu "Admin" est visible en haut
```

---

### Test 5 : Page FedaPay (Admin)

```
URL : https://www.pro-chez-nous.com/admin/fedapay
```

**Vérifications :**
- [ ] La page s'affiche (vous devez être connecté en admin)
- [ ] Environnement affiché : **"live"** (pas "sandbox")
- [ ] Les clés sont affichées (partiellement masquées)
- [ ] Cliquez sur "Lancer le test de connexion"
- [ ] Résultat : ✅ Connexion réussie (même si erreur email de test)

⚠️ **Si vous voyez "Erreur email invalide"** → C'est NORMAL ! Ça confirme que FedaPay est connecté mais refuse l'email de test fictif.

---

## 🔗 ÉTAPE 6 : CONFIGURER LE CALLBACK FEDAPAY (5 min)

### C'est l'Étape CRITIQUE pour les Paiements Automatiques

1. **Ouvrez un nouvel onglet** : https://fedapay.com
2. **Connectez-vous** avec vos identifiants FedaPay
3. **Dans le menu**, allez dans **"Paramètres"** → **"Webhooks"**
4. **Cliquez sur** "Ajouter un webhook" ou "+ Ajouter URL"

---

### URL à Copier-Coller :

```
https://www.pro-chez-nous.com/fedapay/callback
```

⚠️ **Copiez-collez cette URL EXACTEMENT** (pas d'espaces !)

---

### Événements à Cocher :

```
☑️ transaction.approved
☑️ transaction.canceled
```

---

### Sauvegarder

1. Cliquez sur **"Enregistrer"** ou **"Save"**
2. Vérifiez que le webhook apparaît dans la liste
3. Le statut doit être **"Actif"**

✅ Callback configuré !

**📖 Pour plus de détails**, consultez le fichier `GUIDE_CALLBACK_FEDAPAY.md`

---

## 🎉 ÉTAPE 7 : TEST DE PAIEMENT (Optionnel)

### Test Complet du Système

1. **Déconnectez-vous** de votre compte admin
2. **Créez un nouveau compte** utilisateur de test
3. **Connectez-vous** avec ce compte
4. **Allez dans** "Abonnement" (menu du haut)
5. **Cliquez sur** "Passer au Premium"
6. **Cliquez sur** "Payer 1000 FCFA"
7. **Vous serez redirigé** vers FedaPay
8. **Effectuez un paiement** (100 FCFA suffit pour tester)
9. **Après paiement**, retournez sur www.pro-chez-nous.com
10. **Vérifiez** que votre compte affiche **"Premium"** 🎯

---

### Résultat Attendu :

✅ Badge "Premium" visible dans le menu  
✅ Date d'expiration affichée (30 jours)  
✅ Accès aux fonctionnalités Premium  

❌ Si le compte reste "Gratuit" → Vérifiez la configuration du callback dans FedaPay

---

## 🐛 DÉPANNAGE

### Problème : "500 Internal Server Error"

**Solutions :**

1. **Consultez les logs** :
   - Onglet "Web" → Cliquez sur "Error log"
   - Lisez les dernières erreurs
   
2. **Vérifications** :
   - Tous les fichiers sont bien uploadés ?
   - Les secrets sont bien configurés (pas d'espaces, orthographe) ?
   - Vous avez cliqué sur "Reload" ?

---

### Problème : "Checkbox conditions non visible"

**Solutions :**

1. Videz le cache du navigateur : **Ctrl+Shift+R** (Windows) ou **Cmd+Shift+R** (Mac)
2. Vérifiez que `templates/register.html` est bien remplacé
3. Re-reload l'application PythonAnywhere

---

### Problème : "Menu Admin → FedaPay non visible"

**Solutions :**

1. Vérifiez que vous êtes connecté avec un compte **admin** (pas un compte utilisateur normal)
2. Vérifiez que `templates/base.html` est bien remplacé
3. Re-reload l'application

---

### Problème : "Page /conditions introuvable (404)"

**Solutions :**

1. Vérifiez que `templates/conditions.html` existe dans le dossier `templates/`
2. Vérifiez que `app.py` contient la route `/conditions` (ligne 285-287)
3. Re-reload l'application

---

### Problème : "Erreur d'authentification FedaPay"

**Solutions :**

1. Vérifiez que `FEDAPAY_ENV` = `live` (minuscules, pas de guillemets)
2. Vérifiez que vos clés commencent par `sk_live_` et `pk_live_`
3. Vérifiez qu'il n'y a pas d'espaces avant/après les clés
4. Re-copiez les clés depuis votre dashboard FedaPay

---

### Problème : "Le compte ne passe pas en Premium après paiement"

**Solutions :**

1. Vérifiez que le callback est bien configuré dans FedaPay
2. Vérifiez l'URL du callback : `https://www.pro-chez-nous.com/fedapay/callback`
3. Vérifiez que les événements `transaction.approved` et `transaction.canceled` sont cochés
4. Consultez les logs PythonAnywhere pour voir si le callback est reçu

---

## 📊 RÉCAPITULATIF

### Ce qui a été déployé :

✅ **Conditions d'utilisation obligatoires** à l'inscription  
✅ **Page dédiée aux conditions** (/conditions)  
✅ **Intégration FedaPay LIVE** (paiements réels)  
✅ **Interface admin FedaPay** (/admin/fedapay)  
✅ **Système de callback automatique**  

### Nouveaux moyens de paiement acceptés :

💳 T-Money (Togocel)  
💸 Flooz (Moov Africa)  
📱 MTN Mobile Money  
🍊 Orange Money  
💳 Cartes bancaires  

### Prix :

**Plan Premium** : 1000 FCFA/mois (prix de lancement)  
**Essai gratuit** : 30 jours pour tous les nouveaux inscrits  

---

## ✅ CHECKLIST FINALE

Avant de considérer le déploiement terminé, vérifiez :

### Fichiers
- [ ] `app.py` remplacé
- [ ] `fedapay_service.py` remplacé
- [ ] `templates/base.html` remplacé
- [ ] `templates/register.html` remplacé
- [ ] `templates/conditions.html` créé
- [ ] `templates/admin_fedapay_test.html` créé

### Secrets
- [ ] `FEDAPAY_SECRET_KEY` configuré
- [ ] `FEDAPAY_PUBLIC_KEY` configuré
- [ ] `FEDAPAY_ENV` = `live`

### Application
- [ ] Bouton "Reload" cliqué
- [ ] Page d'accueil fonctionne
- [ ] Page /register affiche la checkbox
- [ ] Page /conditions s'affiche
- [ ] Connexion admin possible
- [ ] Page /admin/fedapay accessible

### FedaPay
- [ ] Callback URL configuré dans FedaPay
- [ ] Événements `transaction.approved` et `transaction.canceled` cochés
- [ ] Webhook marqué comme "Actif"

### Tests (Optionnel)
- [ ] Test de paiement effectué
- [ ] Compte passé en Premium automatiquement

---

## 🎯 PROCHAINES ÉTAPES

Une fois le déploiement terminé et validé :

1. **Testez** avec quelques utilisateurs de confiance
2. **Surveillez** les logs pour détecter d'éventuels problèmes
3. **Communiquez** le lancement à vos utilisateurs
4. **Annoncez** les nouveaux moyens de paiement (T-Money, Flooz)
5. **Proposez** l'essai gratuit de 30 jours pour attirer des utilisateurs

---

## 📞 SUPPORT

### Logs PythonAnywhere
```
Web → Log files → Error log (erreurs)
Web → Log files → Server log (accès)
```

### Documentation
```
DEPLOIEMENT_PYTHONANYWHERE_NOVEMBRE_2025.md  (guide complet)
GUIDE_CALLBACK_FEDAPAY.md                     (configuration webhook)
FEDAPAY_CONFIGURATION_COMPLETE.md             (documentation technique)
LISTE_FICHIERS_A_DEPLOYER.txt                 (checklist fichiers)
```

### Support FedaPay
```
Email : [email protected]
Documentation : https://docs.fedapay.com
```

---

## ✨ FÉLICITATIONS !

Une fois toutes ces étapes terminées, **PRO CHEZ NOUS** sera :

🎯 **100% fonctionnel** avec paiements en production  
🔒 **100% conforme** avec conditions d'utilisation  
💰 **100% automatisé** avec callbacks FedaPay  
🚀 **Prêt pour le lancement** officiel !  

**Bonne chance avec votre lancement ! 🎉**

---

**Guide créé le 19 novembre 2025**  
**Version : 1.0 - Production Ready**
