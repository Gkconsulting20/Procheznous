# 🚀 Guide de Déploiement - Système de Gestion des Catégories
## PRO CHEZ NOUS - PythonAnywhere Production

---

## 📋 **Vue d'ensemble**

Ce guide vous aide à déployer le nouveau **système de gestion dynamique des catégories** sur votre serveur de production PythonAnywhere (www.pro-chez-nous.com).

**Fichiers à transférer** :
1. `app.py` (modifié)
2. `templates/base.html` (modifié)
3. `templates/admin_categories.html` (nouveau)
4. `templates/admin_category_form.html` (nouveau)

---

## ⚠️ **IMPORTANT : Sauvegarde Obligatoire**

Avant toute modification, **sauvegardez votre base de données** :

```bash
# Sur PythonAnywhere Console
cd /home/gkconsulting/prochenous2
cp database.db database.db.backup_$(date +%Y%m%d_%H%M%S)
```

---

## 🔄 **Étapes de Déploiement**

### **Étape 1 : Connexion à PythonAnywhere**

1. Allez sur **www.pythonanywhere.com**
2. Connectez-vous à votre compte `gkconsulting`
3. Cliquez sur **"Consoles"** → **"Bash"**

---

### **Étape 2 : Sauvegarde des Fichiers Actuels**

Dans la console Bash :

```bash
cd /home/gkconsulting/prochenous2

# Créer un dossier de sauvegarde
mkdir -p backups/$(date +%Y%m%d)

# Sauvegarder les fichiers actuels
cp app.py backups/$(date +%Y%m%d)/app.py
cp templates/base.html backups/$(date +%Y%m%d)/base.html
cp database.db backups/$(date +%Y%m%d)/database.db

# Vérifier
ls -lh backups/$(date +%Y%m%d)/
```

---

### **Étape 3 : Téléchargement des Fichiers depuis Replit**

**Option A : Via l'éditeur de fichiers PythonAnywhere**

1. Cliquez sur **"Files"** dans PythonAnywhere
2. Naviguez vers `/home/gkconsulting/prochenous2/`
3. Pour chaque fichier :
   - Cliquez sur le fichier
   - Remplacez le contenu complet
   - Cliquez **"Save"**

**Fichiers à copier depuis Replit** :

📄 **app.py** → `/home/gkconsulting/prochenous2/app.py`
📄 **templates/base.html** → `/home/gkconsulting/prochenous2/templates/base.html`

**Nouveaux fichiers à créer** :

📄 **templates/admin_categories.html** (nouveau fichier)
📄 **templates/admin_category_form.html** (nouveau fichier)

---

**Option B : Via Git (si configuré)**

```bash
cd /home/gkconsulting/prochenous2
git pull origin main
```

---

### **Étape 4 : Vérification de la Base de Données**

La table `categories` sera créée automatiquement au premier lancement.

Pour vérifier :

```bash
cd /home/gkconsulting/prochenous2
python3 -c "
from app import init_db
init_db()
print('✅ Base de données initialisée avec succès')
"
```

---

### **Étape 5 : Rechargement de l'Application**

**Sur PythonAnywhere** :

1. Allez dans **"Web"**
2. Cliquez sur **"Reload gkconsulting.pythonanywhere.com"**

OU dans la console Bash :

```bash
touch /var/www/gkconsulting_pythonanywhere_com_wsgi.py
```

---

### **Étape 6 : Vérification**

1. **Ouvrez** www.pro-chez-nous.com
2. **Connectez-vous** avec votre compte admin
3. **Vérifiez** que le menu "🔐 Admin" contient :
   - ✅ 📋 Vérifications
   - ✅ 🏷️ Catégories (nouveau)
4. **Cliquez sur "🏷️ Catégories"**
5. **Vérifiez** que vous voyez la liste des 75 catégories par défaut

---

### **Étape 7 : Test Fonctionnel**

**Testez les fonctions principales** :

1. ✅ **Créer une catégorie** :
   - Nom : `Test Catégorie`
   - Icône : `🧪`
   - Ordre : `999`
   - Cliquez "Enregistrer"

2. ✅ **Modifier la catégorie** :
   - Changez le nom ou l'icône
   - Sauvegardez

3. ✅ **Désactiver/Activer** :
   - Cliquez sur "🔕 Désactiver"
   - Vérifiez qu'elle disparaît du formulaire d'inscription
   - Réactivez-la

4. ✅ **Supprimer** :
   - Supprimez la catégorie de test
   - Devrait fonctionner car aucun pro ne l'utilise

5. ✅ **Vérifier les professionnels** :
   - Allez sur le formulaire d'inscription pro
   - Vérifiez que seules les catégories **actives** apparaissent

---

## 🔧 **En Cas de Problème**

### **Problème 1 : Erreur 500**

```bash
# Vérifier les logs d'erreur
tail -n 50 /var/log/gkconsulting.pythonanywhere.com.error.log
```

### **Problème 2 : Table categories introuvable**

```bash
cd /home/gkconsulting/prochenous2
python3
>>> from app import init_db
>>> init_db()
>>> exit()
```

### **Problème 3 : Menu Admin invisible**

- Vérifiez que vous êtes connecté avec un compte admin
- Vérifiez le rôle dans la base de données :

```bash
sqlite3 database.db "SELECT nom, email, role FROM users WHERE role='admin';"
```

### **Problème 4 : Restaurer la Sauvegarde**

```bash
cd /home/gkconsulting/prochenous2
cp backups/YYYYMMDD/app.py app.py
cp backups/YYYYMMDD/base.html templates/base.html
cp backups/YYYYMMDD/database.db database.db
touch /var/www/gkconsulting_pythonanywhere_com_wsgi.py
```

---

## 📱 **Après Déploiement - Cache Mobile**

**Important** : Si vous testez depuis votre mobile, videz le cache :

**Android Chrome** :
1. Menu (⋮) → Historique
2. Effacer les données de navigation
3. Cochez "Images et fichiers en cache"
4. Effacer

**iOS Safari** :
1. Réglages → Safari
2. Effacer historique et données de sites

---

## ✅ **Checklist de Déploiement**

- [ ] Sauvegarde de database.db effectuée
- [ ] Sauvegarde de app.py effectuée
- [ ] Sauvegarde de templates/base.html effectuée
- [ ] app.py mis à jour
- [ ] templates/base.html mis à jour
- [ ] templates/admin_categories.html créé
- [ ] templates/admin_category_form.html créé
- [ ] Application rechargée (Reload)
- [ ] Connexion admin testée
- [ ] Menu "Catégories" visible
- [ ] Liste des 75 catégories affichée
- [ ] Création/modification/suppression testées
- [ ] Formulaire d'inscription pro vérifié

---

## 📞 **Support**

Si vous rencontrez des difficultés, fournissez-moi :
1. Le message d'erreur exact
2. Les dernières lignes du log d'erreur
3. L'étape où le problème survient

---

**Durée estimée** : 15-20 minutes  
**Niveau de difficulté** : Intermédiaire  
**Risque** : Faible (avec sauvegardes)

---

Bonne chance ! 🚀
