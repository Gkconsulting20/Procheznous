# 🔗 Guide : Configurer le Callback FedaPay

**Objectif :** Permettre à FedaPay de notifier automatiquement PRO CHEZ NOUS quand un paiement est complété.

**Durée :** 5 minutes ⏱️

---

## 🎯 Pourquoi c'est Important ?

Sans le callback configuré :
- ❌ Les paiements sont effectués MAIS votre application n'est pas notifiée
- ❌ Le compte utilisateur ne passe PAS en Premium automatiquement
- ❌ L'utilisateur doit contacter le support manuellement

Avec le callback configuré :
- ✅ FedaPay notifie automatiquement votre application
- ✅ Le compte passe en Premium instantanément
- ✅ Tout est automatique et transparent

---

## 📋 Étapes de Configuration

### Étape 1 : Connexion au Dashboard FedaPay

1. **Ouvrez votre navigateur**
2. **Allez sur** : https://fedapay.com
3. **Cliquez sur** "Connexion" (ou "Se connecter")
4. **Entrez vos identifiants** :
   - Email : votre_email@exemple.com
   - Mot de passe : ••••••••••
5. **Cliquez sur** "Se connecter"

```
┌─────────────────────────────────────┐
│  🌐 FedaPay                         │
│                                     │
│  📧 Email : _________________       │
│  🔒 Mot de passe : _________        │
│                                     │
│        [ Se connecter ]             │
└─────────────────────────────────────┘
```

---

### Étape 2 : Accéder aux Paramètres

Une fois connecté, vous verrez le **tableau de bord FedaPay** :

1. **Dans le menu de gauche**, cherchez **"Paramètres"** ou **"Settings"**
2. **Cliquez dessus**

```
┌─────────────────────────────────────────┐
│  FedaPay Dashboard                      │
├─────────────────────────────────────────┤
│  📊 Tableau de bord                     │
│  💰 Transactions                        │
│  💳 Paiements                           │
│  📈 Statistiques                        │
│  ⚙️  Paramètres  ◄── CLIQUEZ ICI       │
│  🔑 Clés API                            │
│  📞 Support                             │
└─────────────────────────────────────────┘
```

---

### Étape 3 : Trouver la Section Webhooks/Notifications

Dans les **Paramètres**, cherchez une de ces sections :
- **"Webhooks"** (le plus courant)
- **"Notifications"**
- **"API Callbacks"**
- **"URL de notification"**

```
┌──────────────────────────────────────────┐
│  ⚙️  Paramètres                          │
├──────────────────────────────────────────┤
│  👤 Profil                               │
│  🏢 Entreprise                           │
│  🔐 Sécurité                             │
│  🔑 Clés API                             │
│  🔔 Webhooks  ◄── CLIQUEZ ICI            │
│  📧 Emails                               │
└──────────────────────────────────────────┘
```

**Cliquez** sur cette section.

---

### Étape 4 : Ajouter une Nouvelle URL de Webhook

Dans la page **Webhooks**, vous verrez :

1. **Un bouton** "Ajouter" ou "Nouveau webhook" ou "+ Ajouter URL"
2. **Cliquez dessus**

```
┌─────────────────────────────────────────────┐
│  🔔 Webhooks                                │
├─────────────────────────────────────────────┤
│  Configurez les URLs où FedaPay enverra    │
│  les notifications de paiement             │
│                                            │
│  [ + Ajouter un webhook ]  ◄── CLIQUEZ     │
│                                            │
│  Liste des webhooks :                      │
│  (aucun pour le moment)                    │
└─────────────────────────────────────────────┘
```

---

### Étape 5 : Entrer l'URL de Callback

Un **formulaire** va s'ouvrir. Remplissez-le comme suit :

#### 🌐 URL de Callback

**IMPORTANT** : Utilisez l'URL correspondant à votre environnement :

**Option A - Production (PythonAnywhere) :**
```
https://www.pro-chez-nous.com/fedapay/callback
```

**Option B - Test (Replit) :**
```
https://[votre-repl-url].repl.co/fedapay/callback
```

#### 📝 Description (optionnel)
```
Callback PRO CHEZ NOUS - Activation Premium
```

#### 🔔 Événements à Sélectionner

**Cochez ces événements** (IMPORTANT) :

- ✅ **`transaction.approved`** (Transaction approuvée)
- ✅ **`transaction.canceled`** (Transaction annulée)
- ✅ **`transaction.declined`** (Transaction refusée) - optionnel

```
┌──────────────────────────────────────────────┐
│  Ajouter un Webhook                         │
├──────────────────────────────────────────────┤
│  URL *                                       │
│  https://www.pro-chez-nous.com/fedapay/callback │
│                                              │
│  Description                                 │
│  Callback PRO CHEZ NOUS                      │
│                                              │
│  Événements :                                │
│  ☑️ transaction.approved                     │
│  ☑️ transaction.canceled                     │
│  ☐ transaction.declined                      │
│  ☐ transaction.pending                       │
│                                              │
│        [ Annuler ]    [ Enregistrer ]        │
└──────────────────────────────────────────────┘
```

---

### Étape 6 : Sauvegarder

1. **Vérifiez** que l'URL est correcte (pas d'espaces, pas de fautes)
2. **Vérifiez** que les événements sont cochés
3. **Cliquez sur** "Enregistrer" ou "Sauvegarder" ou "Save"

```
✅ Webhook enregistré avec succès !
```

---

### Étape 7 : Vérification

Après enregistrement, vous devriez voir votre webhook dans la liste :

```
┌─────────────────────────────────────────────────┐
│  🔔 Webhooks Actifs                            │
├─────────────────────────────────────────────────┤
│  ✅ https://www.pro-chez-nous.com/fedapay/callback  │
│     Événements : transaction.approved,          │
│                  transaction.canceled           │
│     Statut : Actif                              │
│     [ Modifier ] [ Tester ] [ Supprimer ]       │
└─────────────────────────────────────────────────┘
```

---

## 🧪 Tester le Callback (Optionnel)

Certains dashboards FedaPay permettent de **tester** le webhook :

1. **Cliquez sur** "Tester" à côté de votre webhook
2. FedaPay enverra une **notification de test** à votre URL
3. **Vérifiez** que votre application reçoit bien la notification

---

## ✅ Comment Vérifier que Ça Marche ?

### Test Complet (Recommandé)

1. **Connectez-vous** sur www.pro-chez-nous.com
2. **Créez** un compte utilisateur de test (ou utilisez un compte existant)
3. **Allez dans** "Abonnement" → "Passer au Premium"
4. **Cliquez sur** "Payer 1000 FCFA"
5. **Effectuez** un paiement de test (vous pouvez payer 100 FCFA pour tester)
6. **Après paiement**, retournez sur PRO CHEZ NOUS
7. **Vérifiez** que votre compte est passé en **Premium** automatiquement

### Si ça fonctionne :
- ✅ Votre badge "Premium" est visible
- ✅ Vous avez accès aux fonctionnalités Premium
- ✅ La date d'expiration est affichée (30 jours)

### Si ça ne fonctionne pas :
- ❌ Le compte reste en "Gratuit"
- ❌ Pas d'accès aux fonctionnalités Premium

➡️ **Vérifiez** l'URL du callback dans FedaPay (pas d'erreur de frappe)

---

## 🔧 Résolution de Problèmes

### Problème 1 : "URL invalide"

**Cause** : L'URL contient une erreur ou n'est pas accessible

**Solutions** :
- ✅ Vérifiez qu'il n'y a pas d'espaces avant/après l'URL
- ✅ Vérifiez que l'URL commence par `https://` (pas `http://`)
- ✅ Testez l'URL dans votre navigateur (elle doit exister)

### Problème 2 : "Webhook non déclenché"

**Cause** : Les événements ne sont pas sélectionnés

**Solutions** :
- ✅ Retournez dans FedaPay → Webhooks
- ✅ Modifiez le webhook
- ✅ Cochez bien `transaction.approved` et `transaction.canceled`
- ✅ Sauvegardez à nouveau

### Problème 3 : "Le compte ne passe pas en Premium"

**Cause** : Votre application ne reçoit pas les notifications

**Solutions** :
- ✅ Vérifiez les logs dans PythonAnywhere (Web → Error log)
- ✅ Vérifiez que la route `/fedapay/callback` existe dans `app.py`
- ✅ Testez manuellement l'URL : https://www.pro-chez-nous.com/fedapay/callback

---

## 📸 Captures d'Écran Typiques

### 🖼️ Dashboard FedaPay (Vue Générale)

```
┌────────────────────────────────────────────────────────┐
│  FedaPay                                    [👤 Menu]  │
├────────────────────────────────────────────────────────┤
│  Sidebar                │  Contenu Principal           │
│  ├─ 📊 Dashboard        │                              │
│  ├─ 💰 Transactions     │  🎯 Bienvenue sur FedaPay   │
│  ├─ 📊 Statistiques     │                              │
│  ├─ ⚙️  Paramètres      │  Aujourd'hui :              │
│  │   ├─ Profil         │  💵 Revenus : 0 FCFA        │
│  │   ├─ Entreprise     │  📈 Transactions : 0        │
│  │   ├─ Clés API       │                              │
│  │   └─ 🔔 Webhooks    │                              │
│  └─ 📞 Support          │                              │
└────────────────────────────────────────────────────────┘
```

### 🖼️ Page de Configuration Webhook

```
┌──────────────────────────────────────────────────────┐
│  🔔 Configuration des Webhooks                       │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Les webhooks permettent à FedaPay de notifier      │
│  votre application en temps réel quand un           │
│  événement se produit.                              │
│                                                      │
│  [ + Ajouter un webhook ]                           │
│                                                      │
│  ┌───────────────────────────────────────────────┐  │
│  │ URL du webhook                                │  │
│  │ https://www.pro-chez-nous.com/fedapay/callback   │  │
│  │                                               │  │
│  │ Événements :                                  │  │
│  │ ☑️ transaction.approved                       │  │
│  │ ☑️ transaction.canceled                       │  │
│  │ ☐ transaction.declined                        │  │
│  │                                               │  │
│  │        [ Annuler ]    [ Enregistrer ]         │  │
│  └───────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

---

## 🎯 Checklist Finale

Avant de quitter le dashboard FedaPay, vérifiez :

- [ ] L'URL du webhook est **exactement** : `https://www.pro-chez-nous.com/fedapay/callback`
- [ ] L'événement **`transaction.approved`** est coché
- [ ] L'événement **`transaction.canceled`** est coché
- [ ] Le webhook est marqué comme **"Actif"**
- [ ] Vous avez cliqué sur **"Enregistrer"**

---

## 📞 Besoin d'Aide ?

Si vous ne trouvez pas la section Webhooks dans votre dashboard FedaPay :

1. **Contactez le support FedaPay** :
   - 📧 Email : [email protected]
   - 💬 Chat en ligne : Sur le dashboard FedaPay (coin bas droit)

2. **Demandez** : "Comment configurer une URL de notification/webhook pour recevoir les callbacks de paiement ?"

3. **Donnez-leur** votre URL : `https://www.pro-chez-nous.com/fedapay/callback`

---

## ✨ C'est Terminé !

Une fois le callback configuré :

- ✅ Tous les paiements seront notifiés automatiquement
- ✅ Les comptes passeront en Premium instantanément
- ✅ Aucune intervention manuelle nécessaire
- ✅ Système 100% automatisé

**Félicitations ! Votre intégration FedaPay est complète ! 🎉**
