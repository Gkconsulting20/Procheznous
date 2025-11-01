# 🚀 DÉPLOIEMENT SIMPLE - PythonAnywhere

## ⏱️ Durée totale : 10 minutes

---

## 📋 ÉTAPE 1 : Ouvrir PythonAnywhere (1 min)

1. Ouvrez votre navigateur
2. Allez sur : **www.pythonanywhere.com**
3. Connectez-vous avec votre compte (gkconsulting)
4. Vous arrivez sur le **Dashboard**

✅ **Vous êtes prêt pour l'étape 2**

---

## 📁 ÉTAPE 2 : Copier le script de migration (2 min)

### **2.1 - Ouvrir l'onglet Files**
- En haut de la page, cliquez sur **"Files"**

### **2.2 - Naviguer vers votre projet**
- Dans la barre de navigation, cliquez sur :
  ```
  /home/gkconsulting/prochenous2/
  ```

### **2.3 - Créer le fichier de migration**
1. Cliquez sur **"New file"**
2. Dans le champ "Enter new file name", tapez :
   ```
   MIGRATION_COMPLETE_PYTHONANYWHERE.sh
   ```
3. Cliquez sur **"Create"**

### **2.4 - Copier le contenu du script**
1. **Sur Replit** : 
   - Ouvrez le fichier `MIGRATION_COMPLETE_PYTHONANYWHERE.sh`
   - Sélectionnez TOUT le contenu (Ctrl+A)
   - Copiez (Ctrl+C)

2. **Sur PythonAnywhere** :
   - Dans le fichier que vous venez de créer
   - Collez le contenu (Ctrl+V)
   - Cliquez sur **"Save"** (en haut à droite)

✅ **Script de migration copié !**

---

## 💾 ÉTAPE 3 : Copier app.py (2 min)

### **3.1 - Ouvrir app.py sur PythonAnywhere**
- Dans Files, cliquez sur le fichier existant :
  ```
  app.py
  ```

### **3.2 - Remplacer le contenu**
1. **Sur Replit** :
   - Ouvrez `app.py`
   - Sélectionnez TOUT (Ctrl+A)
   - Copiez (Ctrl+C)

2. **Sur PythonAnywhere** :
   - Dans le fichier app.py ouvert
   - Sélectionnez TOUT (Ctrl+A)
   - Collez le nouveau contenu (Ctrl+V)
   - Cliquez sur **"Save"**

✅ **app.py mis à jour !**

---

## 🎨 ÉTAPE 4 : Copier les templates (2 min)

### **4.1 - Copier base.html**

1. **Sur PythonAnywhere**, allez dans :
   ```
   /home/gkconsulting/prochenous2/templates/
   ```

2. Ouvrez le fichier `base.html`

3. **Sur Replit**, ouvrez `templates/base.html`
   - Copiez TOUT le contenu (Ctrl+A puis Ctrl+C)

4. **Sur PythonAnywhere**, dans base.html
   - Remplacez tout (Ctrl+A puis Ctrl+V)
   - Cliquez sur **"Save"**

### **4.2 - Créer admin_categories.html**

1. **Sur PythonAnywhere**, toujours dans `/templates/`
   - Cliquez sur **"New file"**
   - Nom : `admin_categories.html`
   - Cliquez **"Create"**

2. **Sur Replit**, ouvrez `templates/admin_categories.html`
   - Copiez tout (Ctrl+A puis Ctrl+C)

3. **Sur PythonAnywhere**, dans le fichier créé
   - Collez (Ctrl+V)
   - Cliquez **"Save"**

### **4.3 - Créer admin_category_form.html**

1. **Sur PythonAnywhere**, toujours dans `/templates/`
   - Cliquez sur **"New file"**
   - Nom : `admin_category_form.html`
   - Cliquez **"Create"**

2. **Sur Replit**, ouvrez `templates/admin_category_form.html`
   - Copiez tout (Ctrl+A puis Ctrl+C)

3. **Sur PythonAnywhere**, dans le fichier créé
   - Collez (Ctrl+V)
   - Cliquez **"Save"**

✅ **Tous les fichiers copiés !**

---

## 🔧 ÉTAPE 5 : Exécuter la migration (2 min)

### **5.1 - Ouvrir la console**
- En haut de la page, cliquez sur **"Consoles"**
- Cliquez sur **"Bash"** (console nouvelle)

### **5.2 - Aller dans le dossier du projet**
Tapez cette commande et appuyez sur **Entrée** :
```bash
cd /home/gkconsulting/prochenous2
```

### **5.3 - Exécuter le script de migration**
Tapez cette commande et appuyez sur **Entrée** :
```bash
bash MIGRATION_COMPLETE_PYTHONANYWHERE.sh
```

### **5.4 - Vérifier le résultat**
Vous devriez voir s'afficher :
```
✅ MIGRATION TERMINÉE AVEC SUCCÈS!
✅ Table categories: 75 catégories
✅ Table users: toutes les colonnes présentes
```

✅ **Migration réussie !**

---

## 🔄 ÉTAPE 6 : Recharger l'application (1 min)

### **6.1 - Ouvrir l'onglet Web**
- En haut de la page, cliquez sur **"Web"**

### **6.2 - Recharger l'app**
- Trouvez le gros bouton vert :
  ```
  Reload gkconsulting.pythonanywhere.com
  ```
- Cliquez dessus
- Attendez **15 secondes**

✅ **Application rechargée !**

---

## 🧪 ÉTAPE 7 : Tester (2 min)

### **7.1 - Vider le cache de votre téléphone/navigateur**

**Sur Chrome mobile** :
1. Menu (⋮) → Historique
2. Effacer les données de navigation
3. Cochez "Images et fichiers en cache"
4. Cliquez "Effacer les données"

**Sur Safari mobile** :
1. Réglages → Safari
2. Effacer historique et données de sites

### **7.2 - Tester le site**
Ouvrez dans votre navigateur :
```
www.pro-chez-nous.com
```

**Testez ces pages** :
- ✅ Page d'accueil → S'affiche ?
- ✅ Professionnels → Liste vide (normal)
- ✅ Inscription → Dropdown de catégories s'affiche ?

### **7.3 - Tester le compte admin**

1. Cliquez sur **"Connexion"**
2. Connectez-vous :
   - Email : `admin@test.com`
   - Mot de passe : `Admin123`
3. Vous devriez voir le **menu Admin** en haut
4. Cliquez sur **Admin → Catégories**
5. Vous devriez voir **75 catégories** !

✅ **Tout fonctionne !**

---

## ⚠️ SÉCURITÉ IMPORTANTE

### **Changez immédiatement le mot de passe admin** :

**Sur PythonAnywhere, dans la console Bash** :

```bash
cd /home/gkconsulting/prochenous2
python3 << 'EOF'
import sqlite3
import bcrypt

# Votre nouveau mot de passe (changez-le !)
nouveau_mot_de_passe = "VotreNouveauMotDePasseSecurise123!"

# Hash du mot de passe
hashed = bcrypt.hashpw(nouveau_mot_de_passe.encode('utf-8'), bcrypt.gensalt())

# Mise à jour dans la base
conn = sqlite3.connect('database.db')
conn.execute("UPDATE users SET password = ? WHERE email = 'admin@test.com'", (hashed,))
conn.commit()
print("✅ Mot de passe admin changé avec succès!")
conn.close()
EOF
```

**Remplacez** `VotreNouveauMotDePasseSecurise123!` par votre vrai mot de passe.

---

## 🎉 FÉLICITATIONS !

Votre plateforme **PRO CHEZ NOUS** est maintenant déployée avec succès sur :

### **www.pro-chez-nous.com** ✨

**Ce qui fonctionne** :
- ✅ 75 catégories professionnelles
- ✅ Menu Admin → Catégories
- ✅ Menu Admin → Vérifications
- ✅ Inscription avec dropdown de catégories
- ✅ Protection des fonctionnalités premium
- ✅ Paiements FedaPay bloqués (en attente de configuration)

**Vos utilisateurs actuels** :
- ✅ Tous conservés
- ✅ Toutes leurs données intactes

---

## 📞 EN CAS DE PROBLÈME

### **Erreur "Internal Server Error"**

1. Allez dans **Web** → En bas de page
2. Cliquez sur **"Error log"**
3. Regardez la dernière ligne d'erreur
4. Cherchez le message qui commence par `ERROR`

### **La migration affiche "Column already exists"**

C'est normal ! Le script gère automatiquement les doublons. 
Tant que vous voyez "✅ MIGRATION TERMINÉE", tout va bien.

### **Les catégories ne s'affichent pas**

1. Vérifiez que la migration s'est bien exécutée (75 catégories)
2. Rechargez l'app : Web → Reload
3. Videz le cache de votre navigateur
4. Réessayez

---

## ✅ CHECKLIST FINALE

Cochez au fur et à mesure :

- [ ] Script de migration copié sur PythonAnywhere
- [ ] app.py mis à jour
- [ ] base.html mis à jour
- [ ] admin_categories.html créé
- [ ] admin_category_form.html créé
- [ ] Migration exécutée (message "✅ MIGRATION TERMINÉE")
- [ ] App rechargée (Web → Reload)
- [ ] Cache vidé
- [ ] Site testé : www.pro-chez-nous.com fonctionne
- [ ] Login admin testé : admin@test.com fonctionne
- [ ] Menu Admin → Catégories affiché
- [ ] Mot de passe admin changé pour un mot de passe sécurisé

---

**Vous avez terminé ! Votre plateforme est en ligne ! 🚀**
