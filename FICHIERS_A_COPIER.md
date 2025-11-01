# 📁 Fichiers à Copier - Déploiement Catégories

## 🔄 Fichiers MODIFIÉS (à remplacer)

### 1️⃣ **app.py**
- **Chemin Replit** : `/app.py` (racine du projet)
- **Chemin PythonAnywhere** : `/home/gkconsulting/prochenous2/app.py`
- **Modifications** :
  - Ajout de la fonction `get_categories()` (lignes 32-36)
  - Routes admin pour catégories (lignes 792-905)
  - Initialisation table `categories` dans `init_db()`

### 2️⃣ **templates/base.html**
- **Chemin Replit** : `/templates/base.html`
- **Chemin PythonAnywhere** : `/home/gkconsulting/prochenous2/templates/base.html`
- **Modifications** :
  - Menu Admin avec dropdown (lignes 43-51)
  - Lien vers "Catégories" ajouté

---

## ➕ Fichiers NOUVEAUX (à créer)

### 3️⃣ **templates/admin_categories.html**
- **Chemin Replit** : `/templates/admin_categories.html`
- **Chemin PythonAnywhere** : `/home/gkconsulting/prochenous2/templates/admin_categories.html`
- **Description** : Page de liste des catégories avec actions CRUD

### 4️⃣ **templates/admin_category_form.html**
- **Chemin Replit** : `/templates/admin_category_form.html`
- **Chemin PythonAnywhere** : `/home/gkconsulting/prochenous2/templates/admin_category_form.html`
- **Description** : Formulaire pour créer/modifier une catégorie

---

## 📋 Instructions de Copie

### **Sur Replit** :

1. Ouvrez le fichier dans l'éditeur
2. Sélectionnez TOUT le contenu (Ctrl+A ou Cmd+A)
3. Copiez (Ctrl+C ou Cmd+C)

### **Sur PythonAnywhere** :

1. Allez dans "Files"
2. Naviguez vers le fichier
3. Ouvrez-le
4. Sélectionnez tout (Ctrl+A)
5. Collez (Ctrl+V)
6. Cliquez "Save"

---

## ✅ Vérification Avant Déploiement

Avant de copier, vérifiez que les fichiers Replit contiennent :

**app.py** :
```python
def get_categories():
    """Récupère toutes les catégories actives"""
```

**base.html** :
```html
<a class="dropdown-item" href="{{ url_for('admin_categories') }}">🏷️ Catégories</a>
```

**admin_categories.html** :
```html
<h1>Gestion des Catégories</h1>
```

**admin_category_form.html** :
```html
<h2>{% if category %}Modifier{% else %}Nouvelle{% endif %} Catégorie</h2>
```

---

## 🔢 Nombre de Lignes par Fichier

- `app.py` : ~1200 lignes
- `templates/base.html` : ~120 lignes
- `templates/admin_categories.html` : ~80 lignes
- `templates/admin_category_form.html` : ~60 lignes

Si le nombre de lignes est très différent, vérifiez que vous copiez le bon fichier !

---

## ⚠️ Points de Vigilance

1. **Copier TOUT le fichier** (pas seulement les modifications)
2. **Ne pas mélanger** les lignes (copier d'un bloc)
3. **Vérifier l'indentation** (Python est sensible)
4. **Sauvegarder** avant de remplacer
5. **Recharger l'app** après chaque modification

---

## 🎯 Ordre Recommandé

1. ✅ Sauvegarde de database.db
2. ✅ Sauvegarde de app.py
3. ✅ Sauvegarde de templates/base.html
4. ✅ Copier app.py
5. ✅ Copier templates/base.html
6. ✅ Créer templates/admin_categories.html
7. ✅ Créer templates/admin_category_form.html
8. ✅ Recharger l'application
9. ✅ Tester

---

Bon déploiement ! 🚀
