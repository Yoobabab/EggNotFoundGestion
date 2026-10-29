# Egg Not Found — console de gestion du studio

Site réservé à Greg et Yvan (studio Egg Not Found, 50/50) : chiffres de toutes leurs applis, offres, Or offert, parrainage, avances de frais avec justificatif. Toujours répondre en français, simplement : les porteurs ne codent pas.

## Où sont les choses

- `index.html` : toute la console (une seule page, sans outil de construction ; supabase-js 2.45.4 depuis jsDelivr). Copie de travail aussi dans le dépôt Tikette (`AppliDates/pages/console/index.html`), servie en attendant sur https://tikette.fr/console/.
- Serveur : pour l'instant dans le **projet Supabase de Tikette** (option A, gratuite) : `AppliDates/supabase/studio.sql` (admins, est_admin, offres, parrainage) et `console.sql` (chiffres, avances, bucket privé `justificatifs`), fonction `lire-justificatif` (IA qui lit les factures, < 1 centime chacune).
- Accès : table `admins` (admin@eggnotfound.fr, contact@eggnotfound.fr), vérifié côté serveur par `est_admin()`. Aucune clé secrète dans ce dépôt (la clé « publishable » est publique par nature).

## Décision à appliquer plus tard (Greg, 29 oct. 2026)

**Créer un projet Supabase à part pour la gestion du studio et toutes les autres applis dès qu'on pourra payer un abonnement** (Supabase Pro ≈ 25 $/mois ; l'offre gratuite est limitée à 2 projets actifs, déjà pris par Tikette et Shivr). Ce jour-là : déplacer `admins`, `offres`, `avances`, le bucket `justificatifs` et la console vers ce projet ; chaque appli y fera remonter ses chiffres.

## Règle du studio

Chaque appli a son espace admin (admin@ / contact@eggnotfound.fr) et apparaît dans cette console. Applis à brancher : Shivr, Panier Fantôme, robi.
