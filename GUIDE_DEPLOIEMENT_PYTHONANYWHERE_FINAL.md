# 🚀 GUIDE COMPLET DE DÉPLOIEMENT PYTHONANYWHERE
## Système Commercial - PRO CHEZ NOUS

---

## 📋 LISTE DES FICHIERS À TRANSFÉRER

### 📝 Fichiers MODIFIÉS (Remplacer sur PythonAnywhere)
```
✓ app.py                          (Fichier principal)
✓ templates/base.html             (Menu avec rôle commercial)
✓ templates/register.html         (Capture code parrainage)
✓ replit.md                       (Documentation)
```

### ✨ Fichiers NOUVEAUX (Créer sur PythonAnywhere)
```
✓ create_commercial.py                    (Script création commercial)
✓ templates/dashboard_commercial.html     (Dashboard commercial)
✓ templates/admin_commerciaux.html        (Panel admin commerciaux)
```

---

## 🎯 DÉPLOIEMENT EN 10 MINUTES

### ⏱️ ÉTAPE 1 : Connexion PythonAnywhere (1 min)

1. Ouvrez votre navigateur
2. Allez sur : **https://www.pythonanywhere.com**
3. Connectez-vous avec vos identifiants
4. Vous arrivez sur le **Dashboard**

---

### 📂 ÉTAPE 2 : Accéder aux Fichiers (30 sec)

1. Cliquez sur l'onglet **"Files"** (en haut)
2. Naviguez vers : `/home/gkconsulting/prochenous2/`
3. Vous voyez la liste de vos fichiers

---

### 🔄 ÉTAPE 3 : Remplacer app.py (2 min)

**Sur Replit :**
1. Ouvrez `app.py`
2. Sélectionnez tout (Ctrl+A)
3. Copiez (Ctrl+C)

**Sur PythonAnywhere :**
1. Cliquez sur `app.py` dans la liste
2. Sélectionnez tout le contenu (Ctrl+A)
3. Collez le nouveau contenu (Ctrl+V)
4. Cliquez sur **"Save"** (en haut à droite)

---

### 🔄 ÉTAPE 4 : Remplacer templates/base.html (1 min)

**Sur Replit :**
1. Ouvrez `templates/base.html`
2. Copiez tout le contenu

**Sur PythonAnywhere :**
1. Naviguez vers le dossier `templates/`
2. Cliquez sur `base.html`
3. Remplacez tout le contenu
4. **Save**

---

### 🔄 ÉTAPE 5 : Remplacer templates/register.html (1 min)

**Sur Replit :**
1. Ouvrez `templates/register.html`
2. Copiez tout le contenu

**Sur PythonAnywhere :**
1. Dans `templates/`, cliquez sur `register.html`
2. Remplacez tout le contenu
3. **Save**

---

### ➕ ÉTAPE 6 : Créer create_commercial.py (2 min)

**Sur Replit :**
1. Ouvrez `create_commercial.py`
2. Copiez tout le contenu

**Sur PythonAnywhere :**
1. Retournez dans `/home/gkconsulting/prochenous2/`
2. Cliquez sur **"New file"**
3. Nom du fichier : `create_commercial.py`
4. Collez le contenu
5. **Save**

---

### ➕ ÉTAPE 7 : Créer dashboard_commercial.html (2 min)

**Sur Replit :**
1. Ouvrez `templates/dashboard_commercial.html`
2. Copiez tout le contenu

**Sur PythonAnywhere :**
1. Naviguez dans le dossier `templates/`
2. Cliquez sur **"New file"**
3. Nom : `dashboard_commercial.html`
4. Collez le contenu
5. **Save**

---

### ➕ ÉTAPE 8 : Créer admin_commerciaux.html (2 min)

**Sur Replit :**
1. Ouvrez `templates/admin_commerciaux.html`
2. Copiez tout le contenu

**Sur PythonAnywhere :**
1. Dans `templates/`, cliquez sur **"New file"**
2. Nom : `admin_commerciaux.html`
3. Collez le contenu
4. **Save**

---

### 💾 ÉTAPE 9 : Migration Base de Données (1 min)

**Sur PythonAnywhere :**

1. Cliquez sur l'onglet **"Consoles"**
2. Cliquez sur **"Bash"** → **"New console"**
3. Dans la console, tapez :

```bash
cd prochenous2
```

4. Appuyez sur Entrée

5. Tapez :

```bash
python3 -c "from app import init_db; init_db()"
```

6. Appuyez sur Entrée

**✅ Résultat attendu :** Aucune erreur (migration réussie)

---

### 🔄 ÉTAPE 10 : Redémarrer l'Application (30 sec)

**Sur PythonAnywhere :**

1. Cliquez sur l'onglet **"Web"**
2. Trouvez : **www.pro-chez-nous.com**
3. Cliquez sur le **gros bouton vert "Reload"**
4. Attendez 10-15 secondes

**✅ Application redémarrée !**

---

## 🎉 DÉPLOIEMENT TERMINÉ !

Maintenant testez :

### ✅ Test 1 : Vérifier que le site fonctionne

1. Allez sur : **www.pro-chez-nous.com**
2. La page d'accueil doit s'afficher normalement

---

### ✅ Test 2 : Créer un Commercial de Test

**Dans la Console Bash PythonAnywhere :**

```bash
cd prochenous2
python3 create_commercial.py
```

**Saisissez :**
- Nom : `Marie KOUASSI`
- Email : `commercial@pro-chez-nous.com`
- Téléphone : `+22890123456`
- Password : `Commercial2024!`

**📝 NOTEZ LE CODE GÉNÉRÉ** (ex: ABC12345)

---

### ✅ Test 3 : Connexion Commercial

1. Allez sur : **www.pro-chez-nous.com/login**
2. Email : `commercial@pro-chez-nous.com`
3. Password : `Commercial2024!`
4. Cliquez sur **"Se connecter"**

**✅ Vous devriez voir :**
- Dashboard commercial
- Menu simplifié (3 onglets seulement)
- Vos statistiques (0 inscrits au début)
- Votre lien de parrainage

---

### ✅ Test 4 : Tester le Lien de Parrainage

1. Copiez votre lien : `www.pro-chez-nous.com/register?ref=ABC12345`
2. Ouvrez une **navigation privée**
3. Collez le lien et ouvrez-le
4. Inscrivez un utilisateur test (client ou pro)
5. Fermez la navigation privée
6. Reconnectez-vous au dashboard commercial
7. **✅ Vous devriez voir : +1 inscrit**

---

### ✅ Test 5 : Panel Admin Commerciaux

1. Connectez-vous comme **admin**
2. Menu : **Admin → Commerciaux**
3. **✅ Vous devriez voir :**
   - Liste de tous les commerciaux
   - Leurs statistiques
   - Performance globale

---

## 🎊 FÉLICITATIONS !

Le système commercial est maintenant **100% opérationnel** sur PythonAnywhere !

### Ce qui fonctionne maintenant :

✅ **Comptes commerciaux** avec codes uniques  
✅ **Liens de parrainage** automatiques  
✅ **Menu simplifié** pour commerciaux (3 onglets)  
✅ **Dashboard commercial** avec stats temps réel  
✅ **Panel admin** pour gérer tous les commerciaux  
✅ **Tracking automatique** des inscriptions  
✅ **Calcul des conversions** et revenus  

---

## 🆘 DÉPANNAGE

### Erreur 500 ?
→ Onglet Web → "Error log" → Vérifiez les erreurs

### Database error ?
→ Relancez dans la console :
```bash
python3 -c "from app import init_db; init_db()"
```

### Page blanche ?
→ Vérifiez que tous les templates sont uploadés

### Menu commercial ne s'affiche pas ?
→ Vérifiez que `templates/base.html` a bien été remplacé

### Code de parrainage non reconnu ?
→ Relancez la migration DB

---

## 📞 SUPPORT

Si problème persistant :

1. **Error logs** : Web → Error log
2. **Vérifier colonnes DB** :
```bash
python3 -c "import sqlite3; conn = sqlite3.connect('database.db'); print([c[1] for c in conn.execute('PRAGMA table_info(users)')])"
```
3. **Fichiers manquants** : Vérifiez que les 7 fichiers sont bien sur le serveur

---

## 🎯 RÉCAPITULATIF

**Temps total :** ~10 minutes  
**Fichiers modifiés :** 4  
**Fichiers créés :** 3  
**Commandes exécutées :** 2  

**Résultat :** Système commercial 100% fonctionnel ! 🚀

---

**Prochaines étapes :**

1. Créez vos vrais comptes commerciaux
2. Partagez les liens de parrainage
3. Suivez les statistiques dans le dashboard
4. Gérez vos commerciaux depuis le panel admin

**Bonne chance ! 🎉**
