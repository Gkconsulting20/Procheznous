# 🚀 Guide de Déploiement PythonAnywhere - Novembre 2025

**Plateforme :** PRO CHEZ NOUS  
**Date :** 19 novembre 2025  
**Nouvelles fonctionnalités :** Conditions d'utilisation + FedaPay LIVE

---

## 📦 Fichiers à Transférer

### 1️⃣ Fichiers MODIFIÉS (à remplacer)

```bash
✓ app.py                    # Routes FedaPay + Conditions + Commercial admin
✓ fedapay_service.py        # Correction email format
✓ replit.md                 # Documentation mise à jour
✓ templates/base.html       # Menu Admin → FedaPay ajouté
✓ templates/register.html   # Checkbox conditions d'utilisation
```

### 2️⃣ Fichiers NOUVEAUX (à créer)

```bash
✓ templates/conditions.html              # Page conditions d'utilisation
✓ templates/admin_fedapay_test.html      # Page diagnostic FedaPay
✓ FEDAPAY_CONFIGURATION_COMPLETE.md     # Documentation FedaPay
```

---

## 🔐 Secrets à Configurer

### Étape 1 : Allez dans votre dashboard PythonAnywhere

1. Connectez-vous sur https://www.pythonanywhere.com
2. Allez dans l'onglet **"Web"**
3. Cherchez la section **"Environment variables"** (ou "Variables d'environnement")

### Étape 2 : Ajoutez/Modifiez ces 3 secrets

| Nom | Valeur | Description |
|-----|--------|-------------|
| **FEDAPAY_SECRET_KEY** | `sk_live_votre_clé_ici` | Votre clé secrète FedaPay LIVE |
| **FEDAPAY_PUBLIC_KEY** | `pk_live_votre_clé_ici` | Votre clé publique FedaPay LIVE |
| **FEDAPAY_ENV** | `live` | Mode production (tapez exactement "live") |

⚠️ **IMPORTANT** : Utilisez vos VRAIES clés FedaPay (commençant par `sk_live_` et `pk_live_`)

---

## 📤 Instructions de Transfert des Fichiers

### Méthode 1 : Upload via Dashboard (Recommandée)

1. **Allez dans l'onglet "Files"** de PythonAnywhere
2. **Naviguez vers le dossier** `/home/votre_nom_utilisateur/mysite/`
3. **Pour chaque fichier modifié** :
   - Cliquez sur le nom du fichier
   - Sélectionnez tout le contenu (Ctrl+A)
   - Copiez le nouveau contenu depuis Replit
   - Collez et sauvegardez

### Méthode 2 : Via Console Bash

```bash
# 1. Ouvrir une console Bash sur PythonAnywhere
# 2. Aller dans votre dossier
cd /home/votre_nom_utilisateur/mysite/

# 3. Éditer chaque fichier avec nano
nano app.py
# Coller le nouveau contenu, Ctrl+X pour sauvegarder

nano fedapay_service.py
# Coller le nouveau contenu, Ctrl+X pour sauvegarder

# 4. Créer les nouveaux fichiers
cd templates
nano conditions.html
# Coller le contenu, Ctrl+X pour sauvegarder

nano admin_fedapay_test.html
# Coller le contenu, Ctrl+X pour sauvegarder
```

---

## ✅ Checklist de Déploiement

### AVANT de commencer

- [ ] Vous avez vos clés FedaPay LIVE (`sk_live_...` et `pk_live_...`)
- [ ] Vous êtes connecté à PythonAnywhere
- [ ] Vous avez fait une sauvegarde de votre base de données (par sécurité)

### PENDANT le déploiement

**Étape 1 : Fichiers Python**
- [ ] `app.py` remplacé
- [ ] `fedapay_service.py` remplacé

**Étape 2 : Templates**
- [ ] `templates/base.html` remplacé
- [ ] `templates/register.html` remplacé
- [ ] `templates/conditions.html` créé
- [ ] `templates/admin_fedapay_test.html` créé

**Étape 3 : Documentation** (optionnel)
- [ ] `replit.md` mis à jour
- [ ] `FEDAPAY_CONFIGURATION_COMPLETE.md` créé

**Étape 4 : Secrets**
- [ ] `FEDAPAY_SECRET_KEY` configuré
- [ ] `FEDAPAY_PUBLIC_KEY` configuré
- [ ] `FEDAPAY_ENV` = `live`

**Étape 5 : Redémarrage**
- [ ] Clic sur le bouton **"Reload"** (bouton vert) dans l'onglet Web
- [ ] Attendre 10-20 secondes

### APRÈS le déploiement

- [ ] Tester la page d'accueil : https://www.pro-chez-nous.com
- [ ] Tester l'inscription avec checkbox conditions
- [ ] Tester la page conditions : https://www.pro-chez-nous.com/conditions
- [ ] Se connecter en tant qu'admin
- [ ] Tester le menu Admin → FedaPay
- [ ] Vérifier la configuration FedaPay

---

## 🧪 Tests à Effectuer

### Test 1 : Conditions d'Utilisation

```
1. Allez sur https://www.pro-chez-nous.com/register
2. Vérifiez que la checkbox "J'accepte les conditions d'utilisation" est présente
3. Essayez de vous inscrire SANS cocher → Doit afficher une erreur
4. Cochez la case → L'inscription doit fonctionner
5. Cliquez sur le lien "conditions d'utilisation" → Page doit s'ouvrir
```

### Test 2 : FedaPay Configuration

```
1. Connectez-vous en tant qu'admin
2. Allez dans Admin → FedaPay
3. Vérifiez que l'environnement affiche "live"
4. Vérifiez que les clés sont affichées (partiellement masquées)
5. Cliquez sur "Lancer le test de connexion"
6. Si erreur "email invalide" → C'EST NORMAL (email de test)
7. Si "Erreur d'authentification" → Vérifiez vos clés
```

### Test 3 : Paiement Premium

```
1. Créez un compte utilisateur (ou connectez-vous)
2. Allez dans "Abonnement" dans le menu
3. Cliquez sur "Passer au Premium"
4. Cliquez sur "Payer 1000 FCFA"
5. Vous devez être redirigé vers la page FedaPay
6. Testez un paiement (optionnel - paiement réel)
```

---

## 🔧 Configuration FedaPay (IMPORTANT)

### Étape Finale : Configurer l'URL de Callback

1. **Connectez-vous à FedaPay** : https://fedapay.com
2. **Allez dans Paramètres** → **Webhooks** (ou **Notifications**)
3. **Ajoutez cette URL de callback** :

```
https://www.pro-chez-nous.com/fedapay/callback
```

4. **Événements à sélectionner** :
   - ✅ `transaction.approved` (transaction approuvée)
   - ✅ `transaction.canceled` (transaction annulée)

5. **Sauvegardez**

⚠️ **Cette étape est CRITIQUE** - Sans callback configuré, les paiements ne seront pas validés automatiquement !

---

## 🐛 Résolution de Problèmes

### Problème : "500 Internal Server Error"

**Solution** :
1. Allez dans **Web** → **Error log**
2. Consultez les dernières erreurs
3. Vérifiez que tous les fichiers sont bien uploadés
4. Vérifiez les secrets (orthographe, espaces)

### Problème : "Checkbox conditions non visible"

**Solution** :
1. Vérifiez que `templates/register.html` est bien remplacé
2. Videz le cache du navigateur (Ctrl+Shift+R)
3. Reload l'application PythonAnywhere

### Problème : "Menu Admin → FedaPay non visible"

**Solution** :
1. Vérifiez que `templates/base.html` est bien remplacé
2. Connectez-vous avec un compte **admin** (rôle='admin')
3. Reload l'application

### Problème : "Erreur d'authentification FedaPay"

**Solutions** :
1. ✅ Vérifiez que `FEDAPAY_ENV` = `live` (pas de majuscules, pas d'espaces)
2. ✅ Vérifiez que vos clés commencent par `sk_live_` et `pk_live_`
3. ✅ Vérifiez qu'il n'y a pas d'espaces avant/après les clés
4. ✅ Re-copiez les clés depuis FedaPay

### Problème : "Page conditions non trouvée (404)"

**Solution** :
1. Vérifiez que `templates/conditions.html` existe
2. Vérifiez que `app.py` contient la route `/conditions`
3. Reload l'application

---

## 📋 Commandes PythonAnywhere Utiles

```bash
# Voir les logs d'erreur
tail -f /var/log/votre_nom_utilisateur.pythonanywhere.com.error.log

# Voir les logs d'accès
tail -f /var/log/votre_nom_utilisateur.pythonanywhere.com.access.log

# Lister les fichiers
ls -la /home/votre_nom_utilisateur/mysite/

# Vérifier les templates
ls -la /home/votre_nom_utilisateur/mysite/templates/
```

---

## 🎯 Résumé Rapide (Pour les Pressés)

```bash
# 1. Uploader 5 fichiers modifiés + 2 nouveaux templates
# 2. Configurer 3 secrets FedaPay dans Web → Environment variables
# 3. Cliquer sur "Reload" (bouton vert)
# 4. Tester l'inscription avec checkbox
# 5. Tester Admin → FedaPay
# 6. Configurer callback URL dans FedaPay.com
# 7. C'est terminé ! ✅
```

---

## 📞 Support

Si vous rencontrez des problèmes :

1. **Consultez les logs** dans PythonAnywhere (Web → Log files)
2. **Testez localement** sur Replit pour comparer
3. **Vérifiez la documentation** FedaPay : https://docs.fedapay.com
4. **Page de diagnostic** : https://www.pro-chez-nous.com/admin/fedapay

---

## ✨ Félicitations !

Une fois le déploiement terminé, votre plateforme PRO CHEZ NOUS aura :

✅ **Conditions d'utilisation obligatoires** à l'inscription  
✅ **Paiements FedaPay LIVE** (T-Money, Flooz, etc.)  
✅ **Interface admin FedaPay** pour diagnostic  
✅ **Système de commercial** complet avec tracking  

**Bonne chance avec votre lancement ! 🚀**
