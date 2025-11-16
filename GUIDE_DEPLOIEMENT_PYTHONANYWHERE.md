# 🚀 GUIDE COMPLET : DÉPLOYER SUR PYTHONANYWHERE

## 📋 VUE D'ENSEMBLE

Ce guide vous montre **étape par étape** comment déployer vos modifications sur PythonAnywhere.

**Durée estimée :** 10 minutes  
**Niveau de difficulté :** Facile ⭐  
**Fichiers à déployer :** 2 fichiers HTML

---

## 📦 PRÉPARATION : TÉLÉCHARGER LES FICHIERS DEPUIS REPLIT

### **Étape 1.1 : Ouvrir Replit**

1. Allez sur https://replit.com
2. Connectez-vous à votre compte
3. Ouvrez votre projet **PRO CHEZ NOUS**

---

### **Étape 1.2 : Télécharger les fichiers modifiés**

Dans l'explorateur de fichiers Replit (à gauche) :

```
📁 votre-projet/
├── 📁 templates/
│   ├── 📄 register.html      ← À télécharger
│   ├── 📄 parametres.html    ← À télécharger
│   └── ...
├── app.py
└── ...
```

#### **Télécharger register.html**

1. Cliquez sur le dossier `templates/` pour l'ouvrir
2. **Clic droit** sur `register.html`
3. Sélectionnez **"Download"** dans le menu
4. Le fichier se télécharge dans votre dossier `Téléchargements`

```
┌─────────────────────────────────────┐
│  📄 register.html                   │
│                                     │
│  Clic droit ─┐                      │
│              │                      │
│              ├─ Open               │
│              ├─ Rename             │
│              ├─ Delete             │
│              └─ Download  ← CLIC   │
└─────────────────────────────────────┘
```

#### **Télécharger parametres.html**

Répétez la même opération :

1. **Clic droit** sur `parametres.html`
2. Sélectionnez **"Download"**
3. Le fichier se télécharge

---

### **Étape 1.3 : Vérifier les téléchargements**

Ouvrez votre dossier **Téléchargements** (ou Downloads) :

```
📁 Téléchargements/
├── 📄 register.html         ✅
├── 📄 parametres.html       ✅
```

✅ **Vous êtes prêt pour le déploiement !**

---

## 🌐 DÉPLOIEMENT SUR PYTHONANYWHERE

### **Étape 2.1 : Se connecter à PythonAnywhere**

1. Ouvrez votre navigateur
2. Allez sur **https://www.pythonanywhere.com**
3. Cliquez sur **"Log in"** (en haut à droite)

```
┌──────────────────────────────────────────────────────┐
│  PYTHONANYWHERE                                      │
│                                         [Sign up]    │
│  [🏠 Home] [Dashboard] [Consoles] [Files] [Log in]  │
│                                            ↑         │
│                                         CLIQUEZ ICI  │
└──────────────────────────────────────────────────────┘
```

4. Entrez vos identifiants :
   - **Username :** `gkconsulting` (votre nom d'utilisateur)
   - **Password :** (votre mot de passe)
5. Cliquez sur **"Log in"**

---

### **Étape 2.2 : Accéder à l'interface Files**

Une fois connecté, vous verrez votre **Dashboard** :

```
┌────────────────────────────────────────────────────────────┐
│  Dashboard                                                 │
│                                                            │
│  ┌─────────┬─────────┬─────────┬─────────┬─────────┐     │
│  │ Consoles│  Files  │   Web   │ Schedule│  Databases│     │
│  └─────────┴─────────┴─────────┴─────────┴─────────┘     │
│              ↑                                             │
│           CLIQUEZ ICI                                      │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

1. Cliquez sur l'onglet **"Files"** (en haut)

---

### **Étape 2.3 : Naviguer vers le dossier templates**

Vous êtes maintenant dans l'interface de gestion des fichiers :

```
┌────────────────────────────────────────────────────────┐
│  Files                                                 │
│  ┌──────────────────────────────────────────────────┐ │
│  │ Directories                                      │ │
│  │ /home/gkconsulting/                             │ │
│  │                                                  │ │
│  │  📁 prochenous2/      ← CLIQUEZ ICI             │ │
│  │  📁 .local/                                      │ │
│  │  📁 .cache/                                      │ │
│  └──────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘
```

**Navigation :**

1. Cliquez sur le dossier **`prochenous2/`**

```
┌────────────────────────────────────────────────────────┐
│  /home/gkconsulting/prochenous2/                       │
│  ┌──────────────────────────────────────────────────┐ │
│  │  📁 templates/        ← CLIQUEZ ICI              │ │
│  │  📁 static/                                      │ │
│  │  📄 app.py                                       │ │
│  │  📄 database.db                                  │ │
│  └──────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘
```

2. Cliquez sur le dossier **`templates/`**

Vous êtes maintenant dans :
```
/home/gkconsulting/prochenous2/templates/
```

---

### **Étape 2.4 : Supprimer les anciens fichiers**

⚠️ **IMPORTANT :** Supprimez les anciens fichiers avant d'uploader les nouveaux pour éviter les conflits.

Vous voyez la liste des fichiers :

```
┌────────────────────────────────────────────────────────────┐
│  /home/gkconsulting/prochenous2/templates/                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  📄 base.html                                     ❌ │  │
│  │  📄 register.html                                 ❌ │  │ ← À SUPPRIMER
│  │  📄 parametres.html                               ❌ │  │ ← À SUPPRIMER
│  │  📄 dashboard.html                                ❌ │  │
│  │  📄 professionals.html                            ❌ │  │
│  │  ...                                                 │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

**Pour chaque fichier à supprimer :**

#### **Supprimer register.html**

1. Trouvez la ligne **`register.html`**
2. Cliquez sur l'icône **❌ (poubelle/corbeille)** à droite
3. Une confirmation apparaît : **"Are you sure you want to delete register.html?"**
4. Cliquez sur **"Yes, delete it"**

```
┌──────────────────────────────────────────┐
│  ⚠️  Confirm deletion                    │
│                                          │
│  Are you sure you want to delete         │
│  register.html?                          │
│                                          │
│  [Cancel]  [Yes, delete it]              │
│                        ↑                 │
│                     CLIQUEZ              │
└──────────────────────────────────────────┘
```

#### **Supprimer parametres.html**

Répétez la même opération :

1. Cliquez sur **❌** à côté de `parametres.html`
2. Confirmez avec **"Yes, delete it"**

✅ **Les anciens fichiers sont supprimés**

---

### **Étape 2.5 : Uploader les nouveaux fichiers**

Vous êtes toujours dans :
```
/home/gkconsulting/prochenous2/templates/
```

En haut de la page, vous voyez :

```
┌────────────────────────────────────────────────────────┐
│  /home/gkconsulting/prochenous2/templates/             │
│                                                        │
│  [📤 Upload a file]  [📁 New directory]               │
│         ↑                                              │
│      CLIQUEZ ICI                                       │
└────────────────────────────────────────────────────────┘
```

#### **Uploader register.html**

1. Cliquez sur le bouton **"📤 Upload a file"**
2. Une fenêtre de sélection de fichiers s'ouvre

```
┌──────────────────────────────────────────┐
│  Sélectionner un fichier                 │
│                                          │
│  📁 Téléchargements                      │
│    📄 register.html     ← SÉLECTIONNER   │
│    📄 parametres.html                    │
│    📄 autre-fichier.pdf                  │
│                                          │
│  [Annuler]  [Ouvrir]                     │
│                  ↑                       │
│               CLIQUEZ                    │
└──────────────────────────────────────────┘
```

3. Naviguez vers votre dossier **Téléchargements**
4. Sélectionnez **`register.html`**
5. Cliquez sur **"Ouvrir"** (ou "Open")

**Barre de progression :**

```
┌────────────────────────────────────────────┐
│  Uploading register.html...                │
│  ████████████████████ 100%                 │
│  ✅ Upload complete!                       │
└────────────────────────────────────────────┘
```

6. Attendez que l'upload se termine (quelques secondes)

#### **Uploader parametres.html**

Répétez la même opération :

1. Cliquez sur **"📤 Upload a file"**
2. Sélectionnez **`parametres.html`**
3. Cliquez sur **"Ouvrir"**
4. Attendez la fin de l'upload

✅ **Les deux fichiers sont maintenant uploadés !**

---

### **Étape 2.6 : Vérifier les fichiers uploadés**

Vous devriez maintenant voir :

```
┌────────────────────────────────────────────────────────────┐
│  /home/gkconsulting/prochenous2/templates/                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  📄 base.html                           2024-11-15   │  │
│  │  📄 register.html          ✅ NOUVEAU   2024-11-16   │  │
│  │  📄 parametres.html        ✅ NOUVEAU   2024-11-16   │  │
│  │  📄 dashboard.html                      2024-11-15   │  │
│  │  ...                                                 │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

✅ **Fichiers bien uploadés avec la date d'aujourd'hui**

---

### **Étape 2.7 : OPTIONNEL - Vérifier les hash MD5**

Pour être sûr que les fichiers sont corrects, vous pouvez vérifier leur signature MD5.

1. Cliquez sur l'onglet **"Consoles"** (en haut)
2. Cliquez sur **"Bash"**

```
┌────────────────────────────────────────────────────────┐
│  Start a new console:                                  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Bash         ← CLIQUEZ ICI                      │  │
│  │  Python 3.10                                     │  │
│  │  IPython                                         │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

3. Une console Bash s'ouvre

```
┌────────────────────────────────────────────────────────┐
│  Bash console                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │ $ _                                              │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

4. Tapez les commandes suivantes :

```bash
cd /home/gkconsulting/prochenous2/templates

md5sum register.html parametres.html
```

5. Appuyez sur **Entrée**

**Résultat attendu :**

```
2f308ead47a2a267c2d1ced8f7a69ffc  register.html
8be0ef5970fae151cdb7eaec8ce4a892  parametres.html
```

✅ **Si les hash correspondent, les fichiers sont corrects !**

---

## 🔄 RECHARGER L'APPLICATION WEB

### **Étape 3.1 : Accéder à l'onglet Web**

```
┌────────────────────────────────────────────────────────────┐
│  Dashboard                                                 │
│                                                            │
│  ┌─────────┬─────────┬─────────┬─────────┬─────────┐     │
│  │ Consoles│  Files  │   Web   │ Schedule│  Databases│     │
│  └─────────┴─────────┴─────────┴─────────┴─────────┘     │
│                         ↑                                  │
│                      CLIQUEZ ICI                           │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

1. Cliquez sur l'onglet **"Web"** (en haut)

---

### **Étape 3.2 : Trouver votre application**

Vous voyez la liste de vos applications web :

```
┌────────────────────────────────────────────────────────────┐
│  Web apps                                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Configuration for www.pro-chez-nous.com             │  │
│  │                                                      │  │
│  │  Source code:  /home/gkconsulting/prochenous2/      │  │
│  │  Python version: 3.10                                │  │
│  │  WSGI file: /var/www/gkconsulting_wsgi.py           │  │
│  │                                                      │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

---

### **Étape 3.3 : Recharger l'application**

Descendez un peu dans la page jusqu'à voir :

```
┌────────────────────────────────────────────────────────────┐
│  Reload www.pro-chez-nous.com                              │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                                                      │  │
│  │        🔄 RELOAD WWW.PRO-CHEZ-NOUS.COM               │  │
│  │                                                      │  │
│  │              (gros bouton vert)                      │  │
│  │                     ↑                                │  │
│  │                  CLIQUEZ ICI                         │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

1. Cliquez sur le **gros bouton vert** : **"Reload www.pro-chez-nous.com"**

**Animation de rechargement :**

```
┌────────────────────────────────────────┐
│  Reloading...                          │
│  ⏳ Please wait...                     │
└────────────────────────────────────────┘
```

2. Attendez 5-10 secondes

**Confirmation :**

```
┌────────────────────────────────────────┐
│  ✅ Website reloaded successfully!     │
│                                        │
│  Your changes are now live at:         │
│  https://www.pro-chez-nous.com         │
└────────────────────────────────────────┘
```

✅ **Votre application est rechargée !**

---

## ✅ TESTER LE DÉPLOIEMENT

### **Étape 4.1 : Tester la page d'inscription**

1. Ouvrez un **nouvel onglet** dans votre navigateur
2. Allez sur : **https://www.pro-chez-nous.com/register**

```
┌────────────────────────────────────────────────────────────┐
│  🌐 https://www.pro-chez-nous.com/register                 │
└────────────────────────────────────────────────────────────┘

         ╔═════════════════════════════════════╗
         ║     PRO CHEZ NOUS                   ║
         ║                                     ║
         ║     📝 INSCRIPTION                  ║
         ║                                     ║
         ║  Nom / Pseudo *                     ║
         ║  [________________]                 ║
         ║                                     ║
         ║  Email / Téléphone                  ║
         ║  ◉ Email  ○ Téléphone               ║
         ║                                     ║
         ║  Pays *                             ║
         ║  [🇹🇬 Togo           ▼]             ║
         ║         ↑                           ║
         ║      CLIQUEZ ICI                    ║
         ╚═════════════════════════════════════╝
```

3. Cliquez sur le menu déroulant **"Pays"**

**Vous devriez voir :**

```
┌─────────────────────────────────────────┐
│  🌍 Afrique de l'Ouest                  │
│     🇹🇬 Togo                            │
│     🇧🇯 Bénin                           │
│     🇧🇫 Burkina Faso                    │
│     🇨🇮 Côte d'Ivoire                   │
│     🇬🇭 Ghana                           │
│     🇬🇳 Guinée                          │
│     🇲🇱 Mali                            │
│     🇳🇪 Niger                           │
│     🇳🇬 Nigeria                         │
│     🇸🇳 Sénégal                         │
│                                         │
│  🌎 Tous les pays                       │
│     🇦🇫 Afghanistan                     │
│     🇿🇦 Afrique du Sud                  │
│     🇩🇿 Algérie                         │
│     🇩🇪 Allemagne                       │
│     ... (100+ autres pays)              │
│     🇫🇷 France                          │
│     🇺🇸 États-Unis                      │
│     🇨🇳 Chine                           │
│     🇯🇵 Japon                           │
│     ...                                 │
└─────────────────────────────────────────┘
```

✅ **Test réussi si vous voyez 120+ pays !**

---

### **Étape 4.2 : Tester la page Paramètres**

1. Connectez-vous avec un compte existant
2. Allez sur : **https://www.pro-chez-nous.com/parametres**

```
┌────────────────────────────────────────────────────────────┐
│  🌐 https://www.pro-chez-nous.com/parametres               │
└────────────────────────────────────────────────────────────┘

         ╔═════════════════════════════════════╗
         ║     ⚙️ MES PARAMÈTRES               ║
         ║                                     ║
         ║  Nom / Pseudo *                     ║
         ║  [________________]                 ║
         ║                                     ║
         ║  Pays *                             ║
         ║  [🇹🇬 Togo           ▼]             ║
         ║         ↑                           ║
         ║      CLIQUEZ ICI                    ║
         ║                                     ║
         ║  Ville *                            ║
         ║  [________________]                 ║
         ╚═════════════════════════════════════╝
```

3. Cliquez sur le menu déroulant **"Pays"**

**Vous devriez voir :**

```
┌─────────────────────────────────────────┐
│  🌍 Afrique de l'Ouest                  │
│     🇹🇬 Togo                            │
│     🇧🇯 Bénin                           │
│     ... (10 pays)                       │
│                                         │
│  🌎 Autres pays                         │
│     🇿🇦 Afrique du Sud                  │
│     🇩🇿 Algérie                         │
│     🇩🇪 Allemagne                       │
│     🇧🇪 Belgique                        │
│     🇫🇷 France                          │
│     🇨🇦 Canada                          │
│     ... (~25 pays courants)             │
└─────────────────────────────────────────┘
```

✅ **Test réussi si vous voyez ~35 pays !**

---

## 🎉 FÉLICITATIONS !

Votre déploiement est **terminé** et **réussi** ! 🎊

### ✅ Checklist finale

- [x] Fichiers téléchargés depuis Replit
- [x] Anciens fichiers supprimés sur PythonAnywhere
- [x] Nouveaux fichiers uploadés
- [x] Application rechargée
- [x] Tests effectués avec succès

---

## 🔧 DÉPANNAGE (si problème)

### ❌ Problème : Je ne vois pas les nouveaux pays

**Solution :**

1. **Vider le cache du navigateur**
   - Appuyez sur `Ctrl + Shift + Delete` (Windows/Linux)
   - Ou `Cmd + Shift + Delete` (Mac)
   - Cochez "Images et fichiers en cache"
   - Cliquez sur "Effacer les données"

2. **Recharger la page en mode forcé**
   - Appuyez sur `Ctrl + F5` (Windows/Linux)
   - Ou `Cmd + Shift + R` (Mac)

---

### ❌ Problème : Erreur 500 lors du chargement

**Solution :**

1. Vérifiez les logs d'erreur :
   - Allez dans l'onglet **"Web"** sur PythonAnywhere
   - Cliquez sur le lien **"Error log"**
   - Consultez les dernières erreurs

2. Rechargez l'application :
   - Cliquez sur le bouton **"Reload"** une nouvelle fois

---

### ❌ Problème : Les fichiers ne s'affichent pas après upload

**Solution :**

1. Vérifiez le chemin :
   ```
   /home/gkconsulting/prochenous2/templates/
   ```

2. Vérifiez les permissions :
   ```bash
   cd /home/gkconsulting/prochenous2/templates
   ls -la register.html parametres.html
   ```

3. Les fichiers doivent avoir les permissions `-rw-r--r--`

---

## 📞 BESOIN D'AIDE ?

Si vous rencontrez un problème qui n'est pas résolu par ce guide :

1. Prenez une capture d'écran du problème
2. Notez le message d'erreur exact
3. Demandez de l'aide avec ces informations

---

## 📚 RESSOURCES SUPPLÉMENTAIRES

- **Documentation PythonAnywhere :** https://help.pythonanywhere.com/
- **Guide Replit :** Voir `DEPLOIEMENT_COMPLET.md`
- **Liste des pays :** Voir `DEPLOIEMENT_PAYS_MONDE.md`

---

**Date de création :** 16 novembre 2025  
**Version :** 1.0  
**Auteur :** Guide de déploiement PRO CHEZ NOUS
