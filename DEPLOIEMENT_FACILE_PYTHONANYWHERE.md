# 🎯 GUIDE PAS À PAS - Déploiement sur PythonAnywhere

## ⏱️ Durée totale : 10 minutes

---

## 📋 PARTIE 1 : COPIER LE SCRIPT DE MIGRATION

### **Étape 1.1 : Ouvrir PythonAnywhere**
1. Allez sur **www.pythonanywhere.com**
2. Connectez-vous avec votre compte

### **Étape 1.2 : Créer le fichier script**
1. Cliquez sur **"Files"** (en haut)
2. Dans le dossier, tapez : `/home/gkconsulting/prochenous2/`
3. Cliquez sur **"New file"**
4. Nom du fichier : `MIGRATION_COMPLETE_PYTHONANYWHERE.sh`
5. Cliquez **"Create"**

### **Étape 1.3 : Copier le contenu**
1. **Sur Replit**, ouvrez le fichier `MIGRATION_COMPLETE_PYTHONANYWHERE.sh`
2. **Sélectionnez TOUT** (Ctrl+A)
3. **Copiez** (Ctrl+C)
4. **Sur PythonAnywhere**, dans l'éditeur du fichier que vous venez de créer
5. **Collez** (Ctrl+V)
6. Cliquez **"Save"** (en haut à droite)

✅ **Script copié !**

---

## 📋 PARTIE 2 : COPIER LES TEMPLATES

### **Template 1 : admin_categories.html**

1. Sur PythonAnywhere → **Files** → `/home/gkconsulting/prochenous2/templates/`
2. **New file** → `admin_categories.html`
3. Sur **Replit**, ouvrez `templates/admin_categories.html`
4. **Copiez tout** (Ctrl+A puis Ctrl+C)
5. Sur **PythonAnywhere**, **collez** dans le nouveau fichier
6. **Save**

### **Template 2 : admin_category_form.html**

1. Sur PythonAnywhere → **Files** → `/home/gkconsulting/prochenous2/templates/`
2. **New file** → `admin_category_form.html`
3. Sur **Replit**, ouvrez `templates/admin_category_form.html`
4. **Copiez tout** (Ctrl+A puis Ctrl+C)
5. Sur **PythonAnywhere**, **collez** dans le nouveau fichier
6. **Save**

✅ **Templates copiés !**

---

## 📋 PARTIE 3 : COPIER app.py ET base.html

### **Fichier 1 : app.py**

1. Sur PythonAnywhere → **Files** → `/home/gkconsulting/prochenous2/`
2. **Cliquez** sur `app.py` (il existe déjà)
3. Sur **Replit**, ouvrez `app.py`
4. **Copiez tout** (Ctrl+A puis Ctrl+C)
5. Sur **PythonAnywhere**, **supprimez tout** le contenu actuel
6. **Collez** le nouveau contenu
7. **Save**

### **Fichier 2 : base.html**

1. Sur PythonAnywhere → **Files** → `/home/gkconsulting/prochenous2/templates/`
2. **Cliquez** sur `base.html`
3. Sur **Replit**, ouvrez `templates/base.html`
4. **Copiez tout** (Ctrl+A puis Ctrl+C)
5. Sur **PythonAnywhere**, **supprimez tout** le contenu actuel
6. **Collez** le nouveau contenu
7. **Save**

✅ **Fichiers mis à jour !**

---

## 📋 PARTIE 4 : EXÉCUTER LA MIGRATION

### **Étape 4.1 : Ouvrir la console**
1. Sur PythonAnywhere, cliquez **"Consoles"**
2. Cliquez **"Bash"** (ou utilisez une console existante)

### **Étape 4.2 : Exécuter le script**

Copiez-collez cette commande dans la console :

```bash
cd /home/gkconsulting/prochenous2 && bash MIGRATION_COMPLETE_PYTHONANYWHERE.sh
```

Appuyez sur **Entrée**

### **Étape 4.3 : Vérifier le résultat**

Vous devriez voir :
```
🚀 Début de la migration complète...
📦 Étape 1/4 : Sauvegarde de la base de données...
✅ Sauvegarde créée
🔧 Étape 2/4 : Migration de la base de données...
  → Ajout des colonnes à la table users...
    ✅ Colonne 'phone' ajoutée
    ✅ Colonne 'plan' ajoutée
    ...
✅ MIGRATION TERMINÉE AVEC SUCCÈS!
```

✅ **Migration réussie !**

---

## 📋 PARTIE 5 : RECHARGER L'APPLICATION

### **Étape 5.1 : Aller dans Web**
1. Cliquez sur **"Web"** (en haut)
2. Trouvez votre application : `gkconsulting.pythonanywhere.com`

### **Étape 5.2 : Recharger**
1. Cliquez sur le gros bouton vert **"Reload gkconsulting.pythonanywhere.com"**
2. Attendez **15 secondes**

✅ **Application rechargée !**

---

## 📋 PARTIE 6 : TESTER

### **Étape 6.1 : Vider le cache**
1. Sur votre téléphone/ordinateur
2. Ouvrez **www.pro-chez-nous.com**
3. **Videz le cache** :
   - Chrome : Menu → Historique → Effacer données → Cache
   - Safari : Réglages → Safari → Effacer historique

### **Étape 6.2 : Tester les pages**

Vérifiez que ces pages fonctionnent :

- ✅ **Page d'accueil** : www.pro-chez-nous.com
- ✅ **Connexion** : www.pro-chez-nous.com/login
- ✅ **Inscription** : www.pro-chez-nous.com/register (vous devez voir les catégories)
- ✅ **Professionnels** : www.pro-chez-nous.com/professionals

### **Étape 6.3 : Tester le menu admin**
1. Connectez-vous avec un compte admin
2. Vous devriez voir **"Admin"** dans le menu
3. Cliquez → **"Catégories"**
4. Vous devriez voir les 75 catégories

---

## ⚠️ EN CAS DE PROBLÈME

### Si vous voyez "Internal Server Error" :

**Vérifiez les logs** :

```bash
tail -n 50 /var/log/gkconsulting.pythonanywhere.com.error.log
```

Envoyez-moi la dernière erreur que vous voyez.

### Si le script ne fonctionne pas :

Vérifiez que vous êtes dans le bon dossier :
```bash
pwd
```
Devrait afficher : `/home/gkconsulting/prochenous2`

### Si les catégories n'apparaissent pas :

Vérifiez dans la console Bash :
```bash
cd /home/gkconsulting/prochenous2
python3 -c "import sqlite3; conn=sqlite3.connect('database.db'); print(conn.execute('SELECT COUNT(*) FROM categories').fetchone()[0], 'catégories')"
```

---

## ✅ CHECKLIST FINALE

Cochez au fur et à mesure :

- [ ] Script `MIGRATION_COMPLETE_PYTHONANYWHERE.sh` copié
- [ ] Template `admin_categories.html` copié
- [ ] Template `admin_category_form.html` copié
- [ ] Fichier `app.py` mis à jour
- [ ] Fichier `base.html` mis à jour
- [ ] Script exécuté avec succès
- [ ] Application rechargée
- [ ] Cache vidé
- [ ] Site testé et fonctionnel

---

## 🎉 FÉLICITATIONS !

Votre application PRO CHEZ NOUS fonctionne maintenant avec :

✨ Gestion dynamique des catégories  
✨ Menu admin amélioré  
✨ 75 catégories professionnelles  
✨ Toutes les colonnes nécessaires dans la base  

**Votre plateforme est prête pour vos utilisateurs !** 🚀
