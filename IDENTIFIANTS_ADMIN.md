# 🔐 IDENTIFIANTS ADMINISTRATEUR

## ✅ Compte Admin Conservé

Votre compte administrateur est présent dans la base de données et sera disponible sur **www.pro-chez-nous.com** après le déploiement.

---

## 👤 VOS IDENTIFIANTS

### **Email** :
```
admin@test.com
```

### **Mot de passe** :
```
Admin123
```

### **Rôle** :
```
admin
```

---

## 🎯 ACCÈS ADMIN

Après connexion, vous aurez accès à :

### **Menu Admin** (visible uniquement pour vous) :

1. **Admin → Vérifications**  
   - Gérer les documents de vérification des professionnels
   - Valider ou refuser les documents
   - Marquer les professionnels comme "✓ Vérifié"

2. **Admin → Catégories**  
   - Voir les 75 catégories professionnelles
   - Ajouter de nouvelles catégories
   - Modifier les catégories existantes
   - Activer/Désactiver des catégories
   - Supprimer des catégories (si non utilisées)
   - Voir les statistiques d'utilisation

---

## 🔒 SÉCURITÉ

**⚠️ IMPORTANT** : Ce compte a tous les privilèges administrateur !

### **Après le déploiement sur PythonAnywhere** :

**CHANGEZ IMMÉDIATEMENT LE MOT DE PASSE** :

1. Connectez-vous avec `admin@test.com` / `Admin123`
2. Allez dans **Profil** ou **Paramètres**
3. Changez le mot de passe pour un mot de passe **fort et sécurisé**

### **Recommandations pour un mot de passe sécurisé** :

✅ **Minimum 12 caractères**  
✅ **Majuscules + minuscules + chiffres + caractères spéciaux**  
✅ **Unique** (ne pas réutiliser ailleurs)  
✅ **Pas de mots du dictionnaire**

**Exemple de mot de passe fort** :  
`ProCN@2025!Secure#Admin`

---

## 📧 CHANGER L'EMAIL ADMIN (Optionnel)

Si vous voulez utiliser **votre propre email** :

1. Connectez-vous sur PythonAnywhere
2. Ouvrez la console Bash
3. Exécutez :

```bash
cd /home/gkconsulting/prochenous2
python3 << 'EOF'
import sqlite3
conn = sqlite3.connect('database.db')
conn.execute("UPDATE users SET email = 'votre.email@exemple.com' WHERE role = 'admin'")
conn.commit()
print("✅ Email admin mis à jour!")
conn.close()
EOF
```

Remplacez `votre.email@exemple.com` par votre vrai email.

---

## 🚨 NE JAMAIS PARTAGER

**Ces identifiants donnent un contrôle TOTAL sur la plateforme** :

❌ Ne les partagez JAMAIS  
❌ Ne les écrivez pas en clair dans le code  
❌ Ne les envoyez pas par email non chiffré  

---

## ✅ APRÈS LE DÉPLOIEMENT

**Checklist de sécurité** :

- [ ] Se connecter avec admin@test.com / Admin123
- [ ] Tester l'accès au menu Admin
- [ ] Tester Admin → Catégories
- [ ] Tester Admin → Vérifications
- [ ] **CHANGER LE MOT DE PASSE** immédiatement
- [ ] (Optionnel) Changer l'email vers votre vraie adresse
- [ ] Supprimer ce fichier `IDENTIFIANTS_ADMIN.md` de Replit

---

## 📝 NOTES

- Le compte admin a été créé avec le script `create_admin.py`
- Il est le **seul utilisateur** dans la base nettoyée de Replit
- Sur PythonAnywhere, il sera ajouté à vos utilisateurs existants après migration
- Plan actuel : `gratuit` (vous pouvez le passer en `premium` si besoin via la base de données)

---

## 🎉 VOUS ÊTES PRÊT !

**Prochaine étape** : Déployez sur PythonAnywhere en suivant :  
`DEPLOIEMENT_FINAL_PYTHONANYWHERE.md`

Une fois déployé, connectez-vous et changez le mot de passe ! 🔒
