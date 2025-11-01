# 🚨 DÉPLOIEMENT URGENT - PRO CHEZ NOUS
## Récupération complète de l'application

---

## ⚠️ PROBLÈME ACTUEL
- Erreur 500 sur www.pro-chez-nous.com
- Il manque des fichiers templates
- La base de données n'a pas les nouvelles tables

---

## ✅ SOLUTION EN 3 FICHIERS

Vous devez copier **3 FICHIERS** depuis Replit vers PythonAnywhere :

### 📋 LISTE DES FICHIERS

1. ✅ **templates/base.html** (modifié - menu admin)
2. ✅ **templates/admin_categories.html** (nouveau)
3. ✅ **templates/admin_category_form.html** (nouveau)

**NOTE** : app.py est DÉJÀ copié, il reste juste les 3 templates

---

## 📝 ÉTAPES DÉTAILLÉES

### **ÉTAPE 1 : Aller dans Files sur PythonAnywhere**
1. Connexion → www.pythonanywhere.com
2. Cliquez sur **"Files"**
3. Naviguez vers `/home/gkconsulting/prochenous2/templates/`

---

### **ÉTAPE 2 : Modifier base.html**

1. Ouvrez le fichier `base.html`
2. Cherchez la ligne avec "Admin"
3. Remplacez TOUTE la section Admin par ce code :

```html
{% if session.role == 'admin' %}
<li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" href="#" id="adminDropdown" role="button" data-bs-toggle="dropdown">
        🔐 Admin
    </a>
    <ul class="dropdown-menu">
        <li><a class="dropdown-item" href="{{ url_for('admin_verifications') }}">📋 Vérifications</a></li>
        <li><a class="dropdown-item" href="{{ url_for('admin_categories') }}">🏷️ Catégories</a></li>
    </ul>
</li>
{% endif %}
```

4. Cliquez **"Save"**

---

### **ÉTAPE 3 : Créer admin_categories.html**

1. Dans le dossier `/home/gkconsulting/prochenous2/templates/`
2. Cliquez **"New file"**
3. Nom du fichier : `admin_categories.html`
4. Copiez le contenu depuis Replit (fichier disponible)
5. Cliquez **"Save"**

---

### **ÉTAPE 4 : Créer admin_category_form.html**

1. Toujours dans `/home/gkconsulting/prochenous2/templates/`
2. Cliquez **"New file"**
3. Nom du fichier : `admin_category_form.html`
4. Copiez le contenu depuis Replit (fichier disponible)
5. Cliquez **"Save"**

---

### **ÉTAPE 5 : Initialiser la base de données**

Dans la console Bash de PythonAnywhere :

```bash
cd /home/gkconsulting/prochenous2
python3 -c "from app import init_db; init_db(); print('✅ Base de données initialisée')"
```

---

### **ÉTAPE 6 : Recharger l'application**

1. Allez dans **"Web"**
2. Cliquez sur **"Reload gkconsulting.pythonanywhere.com"**
3. Attendez 10 secondes

---

### **ÉTAPE 7 : Vérifier**

1. Ouvrez www.pro-chez-nous.com
2. Videz le cache (Ctrl+Shift+Suppr)
3. Connectez-vous avec un compte admin
4. Vérifiez le menu "Admin" → "Catégories"

---

## 🆘 SI ÇA NE MARCHE TOUJOURS PAS

Vérifiez les logs d'erreur :

```bash
tail -n 50 /var/log/gkconsulting.pythonanywhere.com.error.log
```

Erreurs communes :
- **"TemplateNotFound"** → Fichiers mal copiés ou mal nommés
- **"no such table: categories"** → Base de données pas initialisée
- **"syntax error"** → Erreur de copie du code

---

## ⏱️ Durée totale : 10-15 minutes

---

**IMPORTANT** : Ne copiez PAS app.py à nouveau, il est déjà copié !
Copiez SEULEMENT les 3 fichiers templates !
