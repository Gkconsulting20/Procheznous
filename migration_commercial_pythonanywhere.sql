-- ============================================================
-- MIGRATION BASE DE DONNÉES - SYSTÈME COMMERCIAL
-- PRO CHEZ NOUS - PythonAnywhere
-- ============================================================

-- Ajouter la colonne commercial_id (ID du commercial qui a parrainé)
ALTER TABLE users ADD COLUMN commercial_id INTEGER;

-- Ajouter la colonne code_commercial (code de parrainage unique)
ALTER TABLE users ADD COLUMN code_commercial TEXT;

-- Créer un index unique sur code_commercial (seulement si non NULL)
CREATE UNIQUE INDEX IF NOT EXISTS idx_code_commercial 
ON users(code_commercial) 
WHERE code_commercial IS NOT NULL;

-- ============================================================
-- VÉRIFICATION
-- ============================================================
-- Exécutez ceci pour vérifier que les colonnes ont été ajoutées:
-- PRAGMA table_info(users);
-- 
-- Vous devriez voir:
-- - commercial_id | INTEGER
-- - code_commercial | TEXT
-- ============================================================
