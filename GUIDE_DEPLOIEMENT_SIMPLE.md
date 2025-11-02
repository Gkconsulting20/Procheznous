# 🚀 GUIDE DE DÉPLOIEMENT SIMPLE - PYTHONANYWHERE

## ⚠️ IMPORTANT : VOS DONNÉES SONT PROTÉGÉES
- ✅ Backup automatique avant toute modification
- ✅ Seulement **ajout** de nouvelles colonnes (pas de suppression)
- ✅ Toutes vos données actuelles restent intactes

---

## 📋 ÉTAPE 1 : BACKUP DE SÉCURITÉ (3 minutes)

1. Aller sur **www.pythonanywhere.com** et se connecter
2. Cliquer sur **"Consoles"** en haut
3. Cliquer sur **"Bash"** (console avec fond noir)
4. Copier-coller ces commandes **une par une** :

```bash
cd ~
cp pro_chez_nous.db pro_chez_nous.db.backup_02nov2025
ls -lh pro_chez_nous.db*
```

✅ **Vérifier** : Vous devez voir 2 fichiers :
```
pro_chez_nous.db
pro_chez_nous.db.backup_02nov2025
```

---

## 📋 ÉTAPE 2 : REMPLACER LES FICHIERS (10 minutes)

### **A) Fichier principal : app.py**

1. Sur **PythonAnywhere** :
   - Cliquer sur **"Files"** en haut
   - Cliquer sur le fichier **`app.py`**
   - L'éditeur s'ouvre

2. Sur **Replit** (cet onglet) :
   - Ouvrir le fichier `app.py` dans l'explorateur de fichiers à gauche
   - Cliquer sur **"Tout sélectionner"** (Ctrl+A ou Cmd+A)
   - Copier (Ctrl+C ou Cmd+C)

3. Retour sur **PythonAnywhere** :
   - Sélectionner tout le contenu (Ctrl+A)
   - Coller le nouveau contenu (Ctrl+V)
   - Cliquer sur **"Save"** (bouton vert en haut)

---

### **B) Fichier navigation : templates/base.html**

1. Sur **PythonAnywhere** :
   - Cliquer sur **"Files"**
   - Naviguer dans `templates/`
   - Cliquer sur **`base.html`**

2. Sur **Replit** :
   - Ouvrir `templates/base.html`
   - Sélectionner tout (Ctrl+A)
   - Copier (Ctrl+C)

3. Sur **PythonAnywhere** :
   - Sélectionner tout (Ctrl+A)
   - Coller (Ctrl+V)
   - Cliquer sur **"Save"**

---

### **C) Mettre à jour templates/profil.html**

1. Sur **PythonAnywhere** :
   - Ouvrir `templates/profil.html`

2. Sur **Replit** :
   - Ouvrir `templates/profil.html`
   - Copier tout le contenu

3. Sur **PythonAnywhere** :
   - Remplacer tout
   - **Save**

---

### **D) Mettre à jour templates/admin_users.html**

1. Sur **PythonAnywhere** :
   - Ouvrir `templates/admin_users.html`

2. Sur **Replit** :
   - Ouvrir `templates/admin_users.html`
   - Copier tout le contenu

3. Sur **PythonAnywhere** :
   - Remplacer tout
   - **Save**

---

### **E) CRÉER 5 nouveaux fichiers de templates**

Pour chaque fichier ci-dessous, suivre cette procédure :

1. Sur **PythonAnywhere** :
   - Aller dans `templates/`
   - Cliquer sur **"New file"** (en haut à droite)
   - Nommer le fichier exactement comme indiqué
   - Cliquer sur **"Create"**

2. Sur **Replit** :
   - Ouvrir le fichier correspondant
   - Copier tout le contenu

3. Sur **PythonAnywhere** :
   - Coller dans le nouveau fichier
   - Cliquer sur **"Save"**

**Liste des 5 fichiers à créer :**

1. ✨ `demander_devis.html`
2. ✨ `repondre_devis.html`
3. ✨ `creer_devis.html`
4. ✨ `devis_client.html`
5. ✨ `devis_pro.html`

---

## 📋 ÉTAPE 3 : MISE À JOUR DE LA BASE DE DONNÉES (2 minutes)

1. Sur **PythonAnywhere**, dans la console **Bash** (celle de l'ÉTAPE 1) :

```bash
cd ~
python3
```

2. Vous êtes maintenant dans la console Python (vous voyez `>>>`). Copier-coller ces commandes **UNE PAR UNE** :

```python
import sqlite3
conn = sqlite3.connect('pro_chez_nous.db')

# Ajouter colonne statut_compte si manquante
try:
    conn.execute('ALTER TABLE users ADD COLUMN statut_compte TEXT DEFAULT "actif"')
    print("✅ Colonne statut_compte ajoutée")
except:
    print("ℹ️ Colonne statut_compte existe déjà")

# Créer table devis si manquante
try:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS devis (
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
    print("✅ Table devis créée/vérifiée")
except Exception as e:
    print(f"❌ Erreur table devis: {e}")

# Ajouter colonne type_devis si manquante
try:
    conn.execute('ALTER TABLE devis ADD COLUMN type_devis TEXT DEFAULT "demande_client"')
    print("✅ Colonne type_devis ajoutée")
except:
    print("ℹ️ Colonne type_devis existe déjà")

conn.commit()
print("✅ Base de données mise à jour avec succès!")
conn.close()
exit()
```

3. Quitter la console Python :

```python
exit()
```

---

## 📋 ÉTAPE 4 : REDÉMARRER L'APPLICATION (1 minute)

1. Sur **PythonAnywhere** :
   - Cliquer sur l'onglet **"Web"** en haut
   - Trouver votre site **www.pro-chez-nous.com**
   - Cliquer sur le gros bouton vert **"Reload www.pro-chez-nous.com"**
   - Attendre 10-15 secondes

---

## 📋 ÉTAPE 5 : VÉRIFIER QUE TOUT FONCTIONNE (2 minutes)

### **Test 1 : Page d'accueil**
1. Ouvrir **www.pro-chez-nous.com** dans votre navigateur
2. ✅ Vérifier que la page d'accueil s'affiche

### **Test 2 : Connexion**
1. Cliquer sur **"Connexion"**
2. Se connecter avec votre compte admin : `admin@test.com` / `Admin123`
3. ✅ Vérifier que vous êtes connecté

### **Test 3 : Menu Admin**
1. Une fois connecté, vérifier que vous voyez le menu **"🔒 Admin"**
2. Cliquer dessus
3. ✅ Vérifier que vous voyez :
   - "Vérifications"
   - "Catégories"
   - **"Utilisateurs"** (nouveau !)

### **Test 4 : Blocage utilisateur**
1. Aller dans **Admin → Utilisateurs**
2. ✅ Vérifier que vous voyez la liste des utilisateurs avec boutons **Bloquer/Débloquer**

### **Test 5 : Menus dynamiques**
1. Se déconnecter
2. Créer un nouveau compte **gratuit** (client)
3. Se connecter avec ce compte
4. ✅ Vérifier que vous **NE VOYEZ PAS** les menus "Messages" et "Devis"

---

## 🆘 EN CAS DE PROBLÈME

### **Si l'application ne démarre pas :**

1. Aller dans **Web** → **Error log** (lien rouge)
2. Regarder les dernières lignes d'erreur
3. Si vous voyez une erreur de colonne manquante :
   - Retourner dans la console Bash
   - Relancer les commandes de l'ÉTAPE 3

### **Si vous voulez tout annuler :**

```bash
cd ~
rm pro_chez_nous.db
cp pro_chez_nous.db.backup_02nov2025 pro_chez_nous.db
```

Puis recharger l'application dans l'onglet **Web**.

---

## ✅ RÉCAPITULATIF

**Temps total estimé** : 15-20 minutes  
**Niveau de difficulté** : Facile (copier-coller)  
**Risque** : Très faible (backup fait au début)

### **Ce qui a été ajouté :**

1. ✅ **Blocage utilisateurs** (admin peut bloquer/débloquer)
2. ✅ **Messagerie hybride Premium** (au moins 1 Premium pour envoyer)
3. ✅ **Système de devis complet** (demander + créer proactivement)
4. ✅ **Menus dynamiques** (Messages/Devis visibles si Premium OU si contenu existant)

### **Vos données :**

- ✅ **0 donnée supprimée**
- ✅ **Tous les utilisateurs conservés**
- ✅ **Tous les rendez-vous conservés**
- ✅ **Toutes les catégories conservées**

---

## 📞 BESOIN D'AIDE ?

Si vous rencontrez un problème à une étape :
1. Notez le **numéro de l'étape**
2. Notez le **message d'erreur exact** (si affiché)
3. Faites une capture d'écran
4. Demandez de l'aide en précisant ces informations

---

**Bonne chance ! 🚀**
