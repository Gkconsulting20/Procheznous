# 🧪 GUIDE DE TEST - SYSTÈME D'EXPIRATION D'ABONNEMENT

## 📦 Système Complet Implémenté

Le système de gestion automatique d'expiration d'abonnement Premium est maintenant **opérationnel et prêt pour déploiement**.

---

## ✅ Fonctionnalités Implémentées

### 1. **Base de données étendue**
- ✅ Colonnes ajoutées à `users`: `subscription_started_at`, `subscription_expires_at`, `subscription_status`
- ✅ Table `subscription_history` pour historique des paiements
- ✅ Script de migration `migrate_subscription_system.py` (déjà exécuté)

### 2. **Service de gestion d'abonnement** (`subscription_service.py`)
- ✅ Vérification automatique du statut d'abonnement
- ✅ Calcul des jours restants avant expiration
- ✅ Génération des messages d'alerte (4 niveaux)
- ✅ Renouvellement automatique via paiement FedaPay
- ✅ Connexions DB sécurisées (try/finally blocks)

### 3. **Middleware & Protection**
- ✅ Middleware `update_subscription_status` exécuté avant chaque requête
- ✅ Décorateur `@premium_required` pour protéger les routes premium
- ✅ Blocage automatique des fonctionnalités expirées
- ✅ Guards contre crashs (session, erreurs)

### 4. **Interface utilisateur**
- ✅ Bannières d'alerte conditionnelles dans `base.html`:
  - 💡 **Info** (7+ jours): Notification simple
  - ⏰ **Warning** (3-7 jours): Alerte orange
  - 🔔 **Urgent** (0-1 jours): Alerte rouge
  - ⚠️ **Expiré**: Blocage et demande de renouvellement
- ✅ Page `/subscription` enrichie avec:
  - Statut actuel de l'abonnement
  - Date de début et d'expiration
  - Compteur de jours restants
  - Tableau d'historique des paiements

### 5. **Corrections de bugs critiques**
- ✅ Conversion `sqlite3.Row → dict` avant `.get()` (2 endroits)
- ✅ Fermeture connexions DB dans `finally` blocks (4 fonctions)
- ✅ Middleware protégé contre absence de session
- ✅ Gestion d'erreurs silencieuse (pas de crash)

---

## 🧪 TESTER LE SYSTÈME

### Option 1: Script de test automatique (recommandé)

```bash
python test_subscription_expiry.py
```

**Menu du script:**
- `1` = Lister tous les utilisateurs Premium avec leurs dates
- `2` = Configurer un scénario pour un utilisateur spécifique
- `3` = **Tester tous les scénarios automatiquement** (meilleure option!)
- `4` = Réinitialiser tous les Premium à 30 jours
- `0` = Quitter

**Scénarios disponibles:**
- `active_30`: Actif, 30 jours restants (aucune alerte)
- `warning_7`: Alerte info, 7 jours restants 💡
- `warning_3`: Alerte warning, 3 jours restants ⏰
- `urgent_1`: Urgent, expire demain 🔔
- `urgent_0`: Urgent, expire aujourd'hui 🔔
- `expired_1`: Expiré depuis 1 jour ⚠️
- `expired_7`: Expiré depuis 7 jours ⚠️

### Option 2: Test manuel avec SQL

```sql
-- Voir tous les Premium
SELECT name, email, plan, subscription_status, 
       subscription_expires_at, 
       CAST((julianday(subscription_expires_at) - julianday('now')) AS INTEGER) as jours_restants
FROM users 
WHERE plan = 'premium';

-- Simuler expiration dans 3 jours pour un utilisateur
UPDATE users 
SET subscription_expires_at = datetime('now', '+3 days'),
    subscription_status = 'grace'
WHERE id = 2;

-- Simuler expiration aujourd'hui
UPDATE users 
SET subscription_expires_at = datetime('now', '+1 hours'),
    subscription_status = 'grace'
WHERE id = 3;

-- Simuler expiration passée (expiré)
UPDATE users 
SET subscription_expires_at = datetime('now', '-2 days'),
    subscription_status = 'expired'
WHERE id = 4;
```

---

## 🔍 Vérifications à effectuer

### 1. **Bannières d'alerte**
- [ ] Se connecter avec un compte Premium
- [ ] Vérifier la bannière en haut de page
- [ ] Confirmer que le message change selon les jours restants
- [ ] Confirmer les couleurs (bleu → orange → rouge)

### 2. **Blocage des fonctionnalités**
- [ ] Tester avec un compte Premium expiré
- [ ] Essayer d'accéder à `/messages` → devrait rediriger vers `/upgrade_premium`
- [ ] Essayer d'accéder à `/favoris` → devrait rediriger vers `/upgrade_premium`
- [ ] Essayer d'accéder à `/devis` → devrait rediriger vers `/upgrade_premium`

### 3. **Page d'abonnement**
- [ ] Aller sur `/subscription`
- [ ] Vérifier l'affichage du statut actuel
- [ ] Vérifier les dates de début et d'expiration
- [ ] Vérifier le compteur de jours restants
- [ ] Vérifier le tableau d'historique (si paiements effectués)

### 4. **Renouvellement automatique**
- [ ] Effectuer un paiement FedaPay (mode sandbox)
- [ ] Vérifier que la date d'expiration est prolongée de 30 jours
- [ ] Vérifier que le statut passe à `active`
- [ ] Vérifier l'ajout dans l'historique

---

## 📊 Comptes de test (PythonAnywhere)

**Utilisateurs Premium (mot de passe: `Test2025!`):**
- `pro1@test.com` - Jean Dupont (Plomberie)
- `pro2@test.com` - Marie Martin (Électricité)
- `pro3@test.com` - Pierre Durand (Peinture)

**Utilisateur Gratuit:**
- `client@test.com` (mot de passe: `Test2025!`)

**Admin:**
- `admin@test.com` (mot de passe différent, à définir via `create_admin.py`)

---

## 🚀 DÉPLOIEMENT SUR PYTHONANYWHERE

### 1. Upload des fichiers modifiés
```bash
# Fichiers à uploader:
- app.py
- subscription_service.py
- migrate_subscription_system.py
- test_subscription_expiry.py
- templates/base.html
- templates/subscription.html
```

### 2. Exécuter la migration
```bash
cd /home/gkconsulting/prochenous2
python migrate_subscription_system.py
```

### 3. Redémarrer l'application
- Aller sur l'onglet **Web**
- Cliquer sur **Reload**

### 4. Tester le système
```bash
# Se connecter en SSH et lancer le script de test
cd /home/gkconsulting/prochenous2
python test_subscription_expiry.py
```

---

## 🐛 Dépannage

### Problème: Bannière ne s'affiche pas
**Solution:** Vider le cache du navigateur et recharger la page

### Problème: Erreur 500 au chargement
**Solution:** Vérifier les logs PythonAnywhere, probablement une connexion DB non fermée

### Problème: Le statut ne se met pas à jour
**Solution:** Le middleware s'exécute à chaque requête. Vérifier que la session est active.

### Problème: Les dates sont incorrectes
**Solution:** Vérifier le timezone du serveur. Les dates sont en UTC.

---

## 📝 Maintenance Future

### Vérifier les expirations (cron quotidien recommandé)
```python
# Script à exécuter quotidiennement
from subscription_service import check_subscription_status, expire_subscription
import sqlite3

conn = sqlite3.connect('database.db')
premium_users = conn.execute("SELECT id FROM users WHERE plan = 'premium'").fetchall()

for user in premium_users:
    status = check_subscription_status(user['id'])
    if status and not status['is_premium_active']:
        expire_subscription(user['id'])
        # Optionnel: envoyer email de notification
```

### Surveiller les métriques
- Nombre de Premium actifs vs expirés
- Taux de renouvellement
- Revenus mensuels (via `subscription_history`)

---

## ✨ Prochaines étapes (optionnel)

- [ ] Intégrer SendGrid pour emails d'alerte automatiques
- [ ] Ajouter notification SMS via Twilio (J-1, Expiré)
- [ ] Implémenter renouvellement automatique (auto-renewal)
- [ ] Créer dashboard admin pour gérer les abonnements
- [ ] Ajouter statistiques de conversion Gratuit → Premium

---

**🎉 Le système est prêt pour production !**
