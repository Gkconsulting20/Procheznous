-- Migration: Ajout du système de gestion d'expiration d'abonnement
-- Date: 2025-11-02
-- Description: Ajoute les colonnes pour gérer l'expiration des abonnements Premium

-- 1. Ajouter les colonnes de gestion d'abonnement à la table users
ALTER TABLE users ADD COLUMN subscription_started_at TEXT;
ALTER TABLE users ADD COLUMN subscription_expires_at TEXT;
ALTER TABLE users ADD COLUMN subscription_status TEXT DEFAULT 'active';

-- 2. Créer la table d'historique des abonnements
CREATE TABLE IF NOT EXISTS subscription_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    plan TEXT NOT NULL,
    period_start TEXT NOT NULL,
    period_end TEXT NOT NULL,
    amount REAL,
    payment_reference TEXT,
    status TEXT DEFAULT 'completed',
    created_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 3. Créer la table des notifications (optionnelle mais recommandée)
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    message TEXT NOT NULL,
    sent_at TEXT NOT NULL,
    read_at TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 4. Initialiser les dates pour les utilisateurs Premium existants
-- Donner 30 jours d'abonnement à partir d'aujourd'hui
UPDATE users 
SET 
    subscription_started_at = datetime('now'),
    subscription_expires_at = datetime('now', '+30 days'),
    subscription_status = 'active'
WHERE plan = 'premium';

-- 5. Initialiser les statuts pour les utilisateurs gratuits
UPDATE users 
SET subscription_status = 'inactive'
WHERE plan = 'gratuit' OR plan IS NULL;
