# ✅ CHECKLIST DE TESTS - Replit (AVANT déploiement PythonAnywhere)

## 🎯 OBJECTIF
Tester TOUTES les fonctionnalités sur Replit AVANT de copier sur PythonAnywhere.
Si tout fonctionne ici, ça fonctionnera sur PythonAnywhere.

---

## ✅ ÉTAT ACTUEL (Vérifié automatiquement)

- ✅ **Base de données initialisée**
- ✅ **75 catégories présentes** (🔧 Plomberie, ⚡ Électricité, etc.)
- ✅ **Compte admin créé** : admin@test.com / Admin123
- ✅ **Tous les fichiers présents** :
  - ✅ app.py (44 KB)
  - ✅ database.db (68 KB)
  - ✅ templates/base.html
  - ✅ templates/admin_categories.html
  - ✅ templates/admin_category_form.html

---

## 📋 TESTS À FAIRE MANUELLEMENT

### **TEST 1 : Pages publiques (Non connecté)** ⏱️ 2 min

| # | Page | URL | À vérifier | Statut |
|---|------|-----|------------|--------|
| 1 | Accueil | `/` | Affichage correct, boutons "Commencer" et "Voir professionnels" | ⬜ |
| 2 | Inscription | `/register` | Formulaire + **DROPDOWN CATÉGORIES** visible | ⬜ |
| 3 | Connexion | `/login` | Formulaire email/téléphone + mot de passe | ⬜ |
| 4 | Professionnels | `/professionals` | Liste de pros + filtres (dont **dropdown catégories**) | ⬜ |

**✅ Test 1 RÉUSSI si** : Toutes les pages s'affichent sans erreur "Internal Server Error"

---

### **TEST 2 : Dropdown des catégories** ⏱️ 1 min

**Sur la page `/register` :**

1. Scrollez jusqu'au champ **"Catégorie"**
2. Cliquez sur le dropdown
3. **Vérifiez** que vous voyez les catégories :
   - 🔧 Plomberie
   - ⚡ Électricité
   - 🎨 Peinture
   - 🪚 Menuiserie
   - ... (75 au total)

**Sur la page `/professionals` :**

1. Dans la barre de recherche, cliquez sur **"Tous les métiers"**
2. **Vérifiez** que le dropdown affiche les catégories

**✅ Test 2 RÉUSSI si** : Les 75 catégories apparaissent dans les dropdowns

---

### **TEST 3 : Connexion Admin** ⏱️ 1 min

1. Allez sur `/login`
2. Connectez-vous avec :
   - **Email** : `admin@test.com`
   - **Mot de passe** : `Admin123`
3. Cliquez **Connexion**

**✅ Test 3 RÉUSSI si** : 
- Vous êtes redirigé vers le dashboard
- Le menu affiche **"Admin"** (en haut à droite ou dans le menu)

---

### **TEST 4 : Menu Admin** ⏱️ 30 sec

**Après connexion admin** :

1. Dans le menu principal, cherchez **"Admin"**
2. Cliquez dessus
3. **Vérifiez** que vous voyez un dropdown avec :
   - **Vérifications**
   - **Catégories** ← IMPORTANT !

**✅ Test 4 RÉUSSI si** : Le menu Admin apparaît avec l'option "Catégories"

---

### **TEST 5 : Page Admin → Catégories** ⏱️ 2 min

1. Cliquez **Admin** → **Catégories**
2. **Vérifiez** que la page affiche :
   - Un tableau avec les 75 catégories
   - Colonnes : Icône, Nom, Statut (Actif/Inactif), Professionnels, Actions
   - Bouton **"+ Nouvelle catégorie"**
3. **Vérifiez** les actions pour chaque catégorie :
   - ✏️ Modifier
   - ❌ Désactiver (ou ✅ Activer)
   - 🗑️ Supprimer

**✅ Test 5 RÉUSSI si** : Le tableau des catégories s'affiche correctement

---

### **TEST 6 : Ajouter une catégorie** ⏱️ 2 min

1. Sur `/admin/categories`, cliquez **"+ Nouvelle catégorie"**
2. Remplissez le formulaire :
   - **Nom** : `🧪 Test Catégorie`
   - **Icône** : `🧪`
   - **Ordre** : `999`
   - **Statut** : Actif
3. Cliquez **"Enregistrer"**
4. **Vérifiez** que vous êtes redirigé vers `/admin/categories`
5. **Vérifiez** que la nouvelle catégorie apparaît dans le tableau

**✅ Test 6 RÉUSSI si** : La catégorie "🧪 Test Catégorie" est créée et visible

---

### **TEST 7 : Modifier une catégorie** ⏱️ 1 min

1. Sur `/admin/categories`, trouvez **"🧪 Test Catégorie"**
2. Cliquez sur **✏️ Modifier**
3. Changez le nom en : `🔬 Test Modifié`
4. Cliquez **"Enregistrer"**
5. **Vérifiez** que le nom a changé dans le tableau

**✅ Test 7 RÉUSSI si** : La catégorie est renommée avec succès

---

### **TEST 8 : Désactiver une catégorie** ⏱️ 1 min

1. Sur `/admin/categories`, trouvez **"🔬 Test Modifié"**
2. Cliquez sur **❌ Désactiver**
3. **Vérifiez** que le statut passe à **"Inactif"**
4. **Ouvrez** `/register` dans un nouvel onglet
5. **Vérifiez** que "🔬 Test Modifié" **N'APPARAÎT PAS** dans le dropdown

**✅ Test 8 RÉUSSI si** : La catégorie désactivée n'apparaît plus dans les formulaires publics

---

### **TEST 9 : Supprimer une catégorie** ⏱️ 1 min

1. Sur `/admin/categories`, trouvez **"🔬 Test Modifié"**
2. Cliquez sur **🗑️ Supprimer**
3. Confirmez la suppression
4. **Vérifiez** que la catégorie a disparu du tableau

**✅ Test 9 RÉUSSI si** : La catégorie est supprimée (76 → 75 catégories)

---

### **TEST 10 : Inscription d'un professionnel** ⏱️ 2 min

1. Déconnectez-vous (si connecté)
2. Allez sur `/register`
3. Remplissez le formulaire en tant que **Professionnel** :
   - **Nom** : `Test Pro`
   - **Email** : `testpro@test.com`
   - **Mot de passe** : `Test123`
   - **Type** : Professionnel
   - **Catégorie** : Sélectionnez `🔧 Plomberie`
   - **Ville** : `Lomé`
4. Cliquez **"S'inscrire"**

**✅ Test 10 RÉUSSI si** : 
- L'inscription réussit
- Vous êtes redirigé vers le dashboard pro
- La catégorie "Plomberie" est enregistrée

---

### **TEST 11 : Vérifier que le pro apparaît** ⏱️ 1 min

1. Allez sur `/professionals`
2. Dans le filtre **"Tous les métiers"**, sélectionnez **"🔧 Plomberie"**
3. Cliquez **"Filtrer"**
4. **Vérifiez** que "Test Pro" apparaît dans les résultats

**✅ Test 11 RÉUSSI si** : Le pro nouvellement inscrit est visible et filtrable

---

## 📊 RÉSUMÉ DES TESTS

| Test | Description | Statut |
|------|-------------|--------|
| 1 | Pages publiques | ⬜ |
| 2 | Dropdown catégories | ⬜ |
| 3 | Connexion admin | ⬜ |
| 4 | Menu admin | ⬜ |
| 5 | Page admin catégories | ⬜ |
| 6 | Ajouter catégorie | ⬜ |
| 7 | Modifier catégorie | ⬜ |
| 8 | Désactiver catégorie | ⬜ |
| 9 | Supprimer catégorie | ⬜ |
| 10 | Inscription pro | ⬜ |
| 11 | Filtrage par catégorie | ⬜ |

---

## 🎯 CRITÈRES DE VALIDATION

✅ **PRÊT POUR PYTHONANYWHERE** si :
- ✅ Tous les tests passent (11/11)
- ✅ Aucune erreur "Internal Server Error"
- ✅ Les catégories s'affichent correctement partout
- ✅ Le menu Admin fonctionne
- ✅ L'ajout/modification/suppression de catégories fonctionne

❌ **NE PAS DÉPLOYER** si :
- ❌ Un seul test échoue
- ❌ Une page affiche une erreur
- ❌ Les catégories ne s'affichent pas

---

## 📝 COMMENT TESTER

### **Option 1 : Test manuel (recommandé)**
1. Ouvrez Replit dans votre navigateur
2. Suivez les tests 1 à 11 dans l'ordre
3. Cochez ✅ au fur et à mesure
4. Si TOUT passe → déployez sur PythonAnywhere

### **Option 2 : Test rapide (5 min)**
1. Test 1 : Ouvrez `/`, `/register`, `/login`, `/professionals`
2. Test 3-5 : Connectez-vous admin et allez sur Admin → Catégories
3. Test 10 : Inscrivez un pro avec une catégorie
4. Si ça fonctionne → déployez

---

## 🐛 EN CAS D'ERREUR

### Si une page affiche "Internal Server Error" :

1. Ouvrez la console Replit
2. Regardez les logs (en bas)
3. Cherchez la ligne avec `ERROR` ou `Traceback`
4. **Envoyez-moi l'erreur complète**

### Si les catégories n'apparaissent pas :

Vérifiez dans la console Replit :
```bash
python3 -c "import sqlite3; conn=sqlite3.connect('database.db'); print(conn.execute('SELECT COUNT(*) FROM categories').fetchone()[0], 'catégories')"
```

Devrait afficher : `75 catégories`

---

## ✨ APRÈS LES TESTS

Si **TOUT fonctionne** :
1. ✅ Vous êtes prêt à déployer sur PythonAnywhere
2. ✅ Suivez le guide `COPIER_COLLER_FACILE.md`
3. ✅ Copiez les 5 fichiers
4. ✅ Exécutez le script de migration
5. ✅ Rechargez l'application

**Durée totale des tests** : 10-15 minutes  
**Résultat** : Confiance à 100% que PythonAnywhere fonctionnera !

---

## 🔐 IDENTIFIANTS DE TEST

**Compte Admin** :
- Email : `admin@test.com`
- Mot de passe : `Admin123`

**Compte Pro (à créer dans Test 10)** :
- Email : `testpro@test.com`
- Mot de passe : `Test123`

---

**Bonne chance ! 🚀**
