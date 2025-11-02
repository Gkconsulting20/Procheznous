#!/bin/bash
# Tests de vérification pour PythonAnywhere
# Copiez-collez ces commandes dans le bash console de PythonAnywhere

echo "========================================================================"
echo "VÉRIFICATION DES FICHIERS - PRO CHEZ NOUS"
echo "========================================================================"

# 1. Vérifier qu'on est dans le bon dossier
echo ""
echo "1️⃣ DOSSIER ACTUEL:"
pwd
echo ""

# 2. Aller dans le dossier du projet
cd /home/gkconsulting/prochenous2

# 3. Vérifier la ligne critique dans app.py (ligne 428)
echo "2️⃣ VÉRIFICATION app.py - Ligne 428 (ajout créneau):"
sed -n '428p' app.py
echo ""
echo "✅ ATTENDU: conn.execute('INSERT INTO slots (user_id, date, heure, disponible)"
echo "❌ MAUVAIS: Si vous voyez 'pro_id' au lieu de 'user_id'"
echo ""

# 4. Vérifier la ligne pour suppression utilisateur (ligne 1397)
echo "3️⃣ VÉRIFICATION app.py - Ligne 1397 (suppression):"
sed -n '1397p' app.py
echo ""
echo "✅ ATTENDU: conn.execute('DELETE FROM rendezvous WHERE client_id = ?', (id,))"
echo "❌ MAUVAIS: Si vous voyez 'pro_id'"
echo ""

# 5. Vérifier la fonction dashboard (lignes 238-277)
echo "4️⃣ VÉRIFICATION app.py - Dashboard professionnel:"
echo "   Doit charger: rdvs, my_slots, other_pros"
sed -n '241,277p' app.py | grep -E "rdvs =|my_slots =|other_pros ="
echo ""
echo "✅ ATTENDU: Vous devez voir 3 lignes avec rdvs, my_slots, other_pros"
echo ""

# 6. Vérifier dashboard_pro.html
echo "5️⃣ VÉRIFICATION templates/dashboard_pro.html:"
if grep -q "Mes créneaux" templates/dashboard_pro.html; then
    echo "   ✅ Section 'Mes créneaux' trouvée"
else
    echo "   ❌ Section 'Mes créneaux' MANQUANTE"
fi

if grep -q "Autres professionnels" templates/dashboard_pro.html; then
    echo "   ✅ Section 'Autres professionnels' trouvée"
else
    echo "   ❌ Section 'Autres professionnels' MANQUANTE"
fi

if grep -q "my_slots" templates/dashboard_pro.html; then
    echo "   ✅ Variable 'my_slots' utilisée"
else
    echo "   ❌ Variable 'my_slots' MANQUANTE"
fi

if grep -q "other_pros" templates/dashboard_pro.html; then
    echo "   ✅ Variable 'other_pros' utilisée"
else
    echo "   ❌ Variable 'other_pros' MANQUANTE"
fi
echo ""

# 7. Compter les lignes des fichiers
echo "6️⃣ NOMBRE DE LIGNES (pour comparaison):"
echo "   app.py: $(wc -l < app.py) lignes"
echo "   templates/dashboard_pro.html: $(wc -l < templates/dashboard_pro.html) lignes"
echo ""
echo "   ✅ ATTENDU app.py: environ 1630 lignes"
echo "   ✅ ATTENDU dashboard_pro.html: environ 129 lignes"
echo ""

# 8. Vérifier la date de modification
echo "7️⃣ DATE DE DERNIÈRE MODIFICATION:"
ls -lh app.py templates/dashboard_pro.html
echo ""
echo "   ⚠️  Si la date est ancienne (avant aujourd'hui), les fichiers ne sont PAS à jour!"
echo ""

echo "========================================================================"
echo "FIN DE LA VÉRIFICATION"
echo "========================================================================"
