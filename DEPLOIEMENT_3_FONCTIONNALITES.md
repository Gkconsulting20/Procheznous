# 🚀 DÉPLOIEMENT COMPLET - 3 NOUVELLES FONCTIONNALITÉS

**Date** : 02 novembre 2025  
**Plateforme** : PythonAnywhere (www.pro-chez-nous.com)  
**Status** : ✅ Validé par l'architecte - Prêt pour production

---

## 📋 RÉSUMÉ DES FONCTIONNALITÉS

### 1️⃣ **Blocage/Déblocage des utilisateurs (Admin)**
- ✅ Nouvelle colonne `statut_compte` (actif/bloqué)
- ✅ Vérification automatique à la connexion
- ✅ Interface admin avec boutons bloquer/débloquer
- ✅ Protection contre l'auto-blocage des admins

### 2️⃣ **Messagerie Hybride Premium**
- ✅ **NOUVELLE LOGIQUE** : AU MOINS UN des deux utilisateurs doit être Premium
- ✅ Client gratuit ↔ Pro Premium = ✅ Autorisé
- ✅ Client Premium ↔ Pro gratuit = ✅ Autorisé
- ✅ Client gratuit ↔ Pro gratuit = ❌ Bloqué
- ✅ Filtrage côté serveur pour sécurité

### 3️⃣ **Système de Gestion de Devis**
- ✅ Nouvelle table `devis` (demandes et réponses)
- ✅ Routes complètes : liste, demande, réponse
- ✅ Templates pour clients ET professionnels
- ✅ Même logique Premium que la messagerie
- ✅ Intégration dans menu et profils pros

---

## 📁 FICHIERS À DÉPLOYER

### **Fichiers modifiés** (à remplacer sur PythonAnywhere)

1. **`app.py`** ⚠️ CRITIQUE
   - Table `devis` dans `init_db()`
   - Routes : `/devis`, `/demander_devis/<pro_id>`, `/repondre_devis/<devis_id>`
   - Modification logique messagerie : `/messages`, `/send_message`
   - Route admin : `/admin/toggle_user_status/<user_id>`

2. **`templates/base.html`**
   - Ajout lien "📝 Devis" dans le menu de navigation

3. **`templates/profil.html`**
   - Ajout bouton "📝 Demander un devis" sur profils professionnels

4. **`templates/admin_users.html`**
   - Ajout boutons "Bloquer" / "Débloquer" pour chaque utilisateur

### **Nouveaux fichiers** (à créer sur PythonAnywhere)

5. **`templates/devis_client.html`** ✨ NOUVEAU
   - Interface de visualisation des devis pour les clients

6. **`templates/devis_pro.html`** ✨ NOUVEAU
   - Interface de gestion des devis pour les professionnels

7. **`templates/demander_devis.html`** ✨ NOUVEAU
   - Formulaire pour demander un devis à un professionnel

8. **`templates/repondre_devis.html`** ✨ NOUVEAU
   - Formulaire pour qu'un pro réponde à une demande de devis

---

## 🔧 INSTRUCTIONS DE DÉPLOIEMENT

### **ÉTAPE 1 : Backup de sécurité** ⚠️
```bash
# Sur PythonAnywhere, dans le répertoire de votre application
cp app.py app.py.backup_20251102
cp templates/base.html templates/base.html.backup_20251102
```

### **ÉTAPE 2 : Télécharger les fichiers modifiés**

Via l'interface **Files** de PythonAnywhere :

1. Ouvrir `app.py` et remplacer tout le contenu par la nouvelle version
2. Ouvrir `templates/base.html` et remplacer le contenu
3. Ouvrir `templates/profil.html` et remplacer le contenu
4. Ouvrir `templates/admin_users.html` et remplacer le contenu

### **ÉTAPE 3 : Créer les nouveaux templates**

Dans le dossier `templates/`, créer 4 nouveaux fichiers :

1. **`devis_client.html`** - copier le contenu depuis Replit
2. **`devis_pro.html`** - copier le contenu depuis Replit
3. **`demander_devis.html`** - copier le contenu depuis Replit
4. **`repondre_devis.html`** - copier le contenu depuis Replit

### **ÉTAPE 4 : Mettre à jour la base de données** 🗄️

Ouvrir un **Bash console** sur PythonAnywhere et exécuter :

```bash
cd ~/votrenomdutilisateur  # Remplacer par votre username
python3
```

Dans la console Python :
```python
from app import init_db
init_db()
exit()
```

**Cela va :**
- ✅ Créer la colonne `statut_compte` si elle n'existe pas
- ✅ Créer la table `devis` avec toutes les colonnes nécessaires
- ✅ Ne pas toucher aux données existantes

### **ÉTAPE 5 : Redémarrer l'application** 🔄

1. Aller dans l'onglet **Web** de PythonAnywhere
2. Cliquer sur le bouton vert **"Reload votresite.pythonanywhere.com"**
3. Attendre quelques secondes

### **ÉTAPE 6 : Tests de validation** ✅

Tester ces scénarios dans l'ordre :

#### **Test 1 : Blocage admin**
1. Se connecter en tant qu'admin (admin@test.com)
2. Aller dans "Admin" → "Utilisateurs"
3. Bloquer un utilisateur test
4. Se déconnecter
5. Essayer de se connecter avec ce compte → Message "Votre compte a été bloqué"
6. Reconnecter en admin et débloquer le compte

#### **Test 2 : Messagerie hybride Premium**
1. Créer 2 comptes : Client gratuit + Pro Premium
2. Le client gratuit envoie un message au pro Premium → ✅ Doit fonctionner
3. Créer 2 comptes gratuits : Client gratuit + Pro gratuit
4. Essayer d'envoyer un message → ❌ Message d'erreur visible

#### **Test 3 : Système de devis**
1. Se connecter en tant que client (gratuit ou Premium)
2. Voir le menu "📝 Devis"
3. Aller sur un profil professionnel Premium
4. Cliquer sur "📝 Demander un devis"
5. Remplir et envoyer
6. Se connecter en tant que pro Premium
7. Voir la demande dans "📝 Devis"
8. Répondre avec montant et délai
9. Vérifier que le client voit la réponse

---

## 🎯 POINTS DE VÉRIFICATION

### ✅ Checklist post-déploiement

- [ ] Le serveur redémarre sans erreur
- [ ] La page d'accueil s'affiche normalement
- [ ] Le lien "Devis" est visible dans le menu
- [ ] Les comptes admin peuvent bloquer/débloquer des utilisateurs
- [ ] La messagerie fonctionne avec au moins un Premium
- [ ] La messagerie bloque quand les deux sont gratuits
- [ ] Les clients peuvent demander des devis
- [ ] Les pros peuvent répondre aux devis
- [ ] Le bouton "Demander un devis" apparaît sur les profils pros

---

## 🛡️ SÉCURITÉ ET BONNES PRATIQUES

### **Logique Premium cohérente**
- ✅ Messagerie : AU MOINS UN Premium
- ✅ Devis : AU MOINS UN Premium
- ✅ Filtrage côté serveur (pas de fuite de données)
- ✅ Messages flash explicites pour l'utilisateur

### **Protection admin**
- ✅ Vérification `statut_compte` à chaque connexion
- ✅ Bouton "Bloquer" désactivé pour le compte admin lui-même
- ✅ Seuls les admins accèdent à `/admin/users`

### **Permissions par rôle**
- ✅ Route `/devis` : adapte l'affichage selon rôle (user/pro)
- ✅ Route `/demander_devis` : clients seulement
- ✅ Route `/repondre_devis` : pros seulement

---

## 📊 STRUCTURE DE LA TABLE DEVIS

```sql
CREATE TABLE IF NOT EXISTS devis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    pro_id INTEGER NOT NULL,
    titre TEXT NOT NULL,
    description TEXT,
    statut TEXT DEFAULT 'en_attente',  -- 'en_attente' ou 'repondu'
    montant INTEGER,
    delai TEXT,
    notes_pro TEXT,
    date_demande TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_reponse TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES users(id),
    FOREIGN KEY (pro_id) REFERENCES users(id)
)
```

---

## 🆘 DÉPANNAGE

### **Erreur "no such column: statut_compte"**
→ Relancer `init_db()` dans la console Python

### **Erreur "no such table: devis"**
→ Relancer `init_db()` dans la console Python

### **Le menu "Devis" n'apparaît pas**
→ Vider le cache du navigateur (Ctrl + Shift + R)

### **La messagerie affiche une erreur**
→ Vérifier que les deux utilisateurs ont bien le champ `plan` dans la base

### **Les templates de devis ne s'affichent pas**
→ Vérifier que les 4 fichiers sont bien dans `templates/` avec les bons noms

---

## 📞 SUPPORT

En cas de problème :
1. Vérifier les logs d'erreur dans PythonAnywhere (onglet **Web** → **Error log**)
2. Vérifier que tous les fichiers sont uploadés
3. Vérifier que `init_db()` a bien été exécuté
4. Tester en mode incognito (pour éviter problèmes de cache)

---

## ✅ VALIDATION FINALE

**Status architecte** : ✅ PASS  
**Sécurité** : ✅ Aucun problème détecté  
**Performance** : ✅ Optimisé  
**Prêt pour production** : ✅ OUI

Toutes les fonctionnalités ont été testées et validées sur l'environnement Replit.
Le déploiement peut être effectué en toute sécurité sur PythonAnywhere.

---

**Bon déploiement ! 🚀**
