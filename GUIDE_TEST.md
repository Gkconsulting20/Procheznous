# 🧪 GUIDE DE TEST - PRO CHEZ NOUS

## 📋 Tests à Effectuer

### ✅ TEST 1 : Compte GRATUIT (utilisateur normal)

**Connexion :**
- Email: `gratuit@test.com`
- Mot de passe: `Test123!`

**Ce que vous DEVEZ voir :**
- ✅ Tableau de bord
- ✅ Professionnels
- ✅ Abonnement
- ✅ Déconnexion

**Ce que vous NE DEVEZ PAS voir :**
- ❌ Messages
- ❌ Favoris
- ❌ Admin

**Test du bouton "Passer au Premium" :**
1. Cliquez sur "Abonnement"
2. Cliquez sur "Passer au Premium"
3. ✅ Vous devez voir : "⚠️ Paiements temporairement désactivés"
4. ✅ Le bouton doit être grisé et non cliquable

---

### ✅ TEST 2 : Compte PREMIUM (utilisateur payant)

**Connexion :**
- Email: `premium@test.com`
- Mot de passe: `Test123!`

**Ce que vous DEVEZ voir :**
- ✅ Tableau de bord
- ✅ Professionnels
- ✅ Messages (nouveau !)
- ✅ Favoris (nouveau !)
- ✅ Abonnement
- ✅ Déconnexion

**Ce que vous NE DEVEZ PAS voir :**
- ❌ Admin

**Test des fonctionnalités premium :**
1. Cliquez sur "Messages" → ✅ Doit fonctionner
2. Cliquez sur "Favoris" → ✅ Doit fonctionner
3. Allez sur "Abonnement" → ✅ Doit afficher "Vous êtes Premium"

---

### ✅ TEST 3 : Compte ADMIN (administrateur)

**Connexion :**
- Email: `admin@test.com`
- Mot de passe: `Admin123!`

**Ce que vous DEVEZ voir :**
- ✅ Tableau de bord
- ✅ Messages
- ✅ Favoris
- ✅ Abonnement
- ✅ Admin (nouveau !)
- ✅ Déconnexion

**Test de l'accès admin :**
1. Cliquez sur "Admin" → ✅ Doit afficher la page de vérification des documents
2. ✅ Doit pouvoir valider/rejeter les documents

---

## 🔐 TEST DE SÉCURITÉ

### Test 1 : Accès direct aux routes protégées

**En étant connecté comme compte GRATUIT :**
1. Tapez manuellement dans l'URL : `/messages`
   - ✅ Doit rediriger vers `/subscription` avec message d'erreur
2. Tapez manuellement dans l'URL : `/favoris`
   - ✅ Doit rediriger vers `/subscription` avec message d'erreur
3. Tapez manuellement dans l'URL : `/admin_verification`
   - ✅ Doit rediriger vers `/dashboard` avec message "Accès refusé"

---

## 📊 RÉSUMÉ DES RÉSULTATS ATTENDUS

| Fonctionnalité | Gratuit | Premium | Admin |
|----------------|---------|---------|-------|
| Tableau de bord | ✅ | ✅ | ✅ |
| Professionnels | ✅ | ✅ | ✅ |
| Messages | ❌ | ✅ | ✅ |
| Favoris | ❌ | ✅ | ✅ |
| Abonnement | ✅ | ✅ | ✅ |
| Admin | ❌ | ❌ | ✅ |
| Paiement | 🚫 Bloqué | N/A | N/A |

---

## 🚀 COMMENT TESTER

1. **Ouvrez l'application** dans votre navigateur
2. **Connectez-vous** avec chaque compte (gratuit, premium, admin)
3. **Vérifiez les onglets** affichés dans la barre de navigation
4. **Testez les accès** en cliquant sur chaque onglet
5. **Notez les résultats** : ✅ si correct, ❌ si problème

---

## ❌ SI UN TEST ÉCHOUE

**Déconnectez-vous complètement, puis :**
1. Videz le cache du navigateur (Ctrl + Shift + Delete)
2. Fermez TOUS les onglets du site
3. Rouvrez le site dans un nouvel onglet
4. Reconnectez-vous
5. Testez à nouveau
