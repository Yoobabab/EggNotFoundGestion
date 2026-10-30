# Egg Not Found — console de gestion du studio

Site réservé à Greg et Yvan (studio Egg Not Found, 50/50) : chiffres de toutes leurs applis, offres, Or offert, parrainage, avances de frais avec justificatif. Toujours répondre en français, simplement : les porteurs ne codent pas.

## Où sont les choses

- `index.html` : toute la console (une seule page, sans outil de construction ; supabase-js 2.45.4 depuis jsDelivr). Copie de travail aussi dans le dépôt Tikette (`AppliDates/pages/console/index.html`), servie en attendant sur https://tikette.fr/console/.
- Serveur : pour l'instant dans le **projet Supabase de Tikette** (option A, gratuite) : `AppliDates/supabase/studio.sql` (admins, est_admin, offres, parrainage) et `console.sql` (chiffres, avances, bucket privé `justificatifs`), fonction `lire-justificatif` (IA qui lit les factures, < 1 centime chacune).
- Accès : table `admins` (admin@eggnotfound.fr, contact@eggnotfound.fr), vérifié côté serveur par `est_admin()`. Aucune clé secrète dans ce dépôt (la clé « publishable » est publique par nature).

## Décision à appliquer plus tard (Greg, 29 oct. 2026)

**Créer un projet Supabase à part pour la gestion du studio et toutes les autres applis dès qu'on pourra payer un abonnement** (Supabase Pro ≈ 25 $/mois ; l'offre gratuite est limitée à 2 projets actifs, déjà pris par Tikette et Shivr). Ce jour-là : déplacer `admins`, `offres`, `avances`, le bucket `justificatifs` et la console vers ce projet ; chaque appli y fera remonter ses chiffres.

## Contenu du site (v2, 29 oct. 2026, validé par Greg)

- Thème Egg Not Found : noir #0A0A0A, rouge œuf #E8344E, crème #EDE7DC, Space Mono (titres, chiffres) + Space Grotesk ; logo « 404 | EGG NOT FOUND » dessiné en HTML/SVG (fonction `marque`).
- `donnees/applis.json` : applis et jeux (logo dans `logos/`, couleur, version, dépôt). **Chaque fois qu'on lance une nouvelle appli ou un nouveau jeu avec Claude : l'ajouter ici avec `"statut": "proposee"`** → elle apparaît dans « À CONFIRMER » en transparence avec un œuf qui se craquelle au survol ; un clic la confirme (table `studio_applis`). Mettre à jour `version` à chaque publication.
- `donnees/a-faire.json` : généré par `python3 outils/faire_a_faire.py <AppliDates/CLAUDE.md> <AppliCard/CLAUDE.md> donnees/a-faire.json <date> <AppliNature/CLAUDE.md>` — demandes de Claude (liste `DEMANDES` du script, à tenir à jour à chaque séance : retirer ce qui est fait) + recette (tests) lue dans les CLAUDE.md. Cases cochées gardées dans `studio_coches` par clé ; tâches ajoutées à la main dans `studio_taches`.
- `donnees/partenaires.json` : état des affiliations (à tenir à jour).
- Moteurs : champs `moteur` (court, ex. « Godot 4.7 », « Expo · React Native », suffixe « (à confirmer) » ou « (prévu) » si pas tranché) et `technique` (détails) dans `applis.json` ; affichés sur les cartes, la page de l'appli et le panneau « Nos moteurs » de la vue d'ensemble (regroupés sans le numéro de version). **À renseigner pour chaque nouvelle appli ou jeu, et à corriger si le moteur change.**
- `donnees/avancement.json` : grandes étapes par appli (`fait` / `en cours` / `à faire`), affichées dans le panneau « Avancement » de la page de l'appli et en barre sur sa carte (« en cours » compte pour moitié). **À tenir à jour à chaque séance de travail sur un projet** (date `maj`). Hearthaven y est depuis le 30 oct. 2026 ; sa recette (`RECETTE_HEARTHAVEN`) et ses demandes sont dans `outils/faire_a_faire.py` (pas de CLAUDE.md : le projet Godot vit sur le PC d'Yvan).
- Coûts et échéances : table `studio_couts` (modifiable dans la console), alerte à J-15.
- Robots : API GitHub publique (applidates-pages, AppliCard-donnees, AppliNature-ia).
- SQL : `AppliDates/supabase/console2.sql` (après console.sql), puis `console3.sql` (offres par appli : colonne `appli`, `offres_actives()` = Tikette, `offres_actives_de('shivr')` pour les autres).
- v3 (29 oct. 2026, demandes de Greg) : bouton « Liens rapides » (fenêtre avec logos des sites) ; vue d'ensemble = 4 chiffres (revenus, coûts, abonnés payants, avances) + « À faire maintenant » + « À surveiller » + cartes des applis avec leur étape (`etape` dans applis.json : idée, en cours, en test, en ligne, en pause) ; mot « abonnement / abonnés » partout (« Or » seulement pour Tikette) ; comptes du studio jamais comptés dans les abonnés ; À faire en 2 onglets (À faire par personne Greg / Yvan / Greg et Yvan, Recette par appli et version) ; Offres pour toutes les applis ; montants acceptés avec « € » ou « $ » (`lireMontant`). Contrôle : `rendre3.mjs` (dossier de travail de Claude) rend les 9 pages en ordinateur et téléphone et signale erreurs, « [object », « undefined », « NaN » et débordements.
- Applis du studio uniquement : Callikoe (projet IRT NETWORK) n'y figure pas.
- **Toute modification du site doit aussi être recopiée dans `applidates-pages/console/`** (index.html, donnees/, logos/) tant que tikette.fr/console/ existe.
- E-mails : logos servis par https://tikette.fr/mail/ (dépôt applidates-pages) ; Tikette et Egg Not Found par la fonction `envoyer-email` (Send Email hook de Supabase Tikette), Shivr par le modèle `AppliCard/supabase/email-code.html`.

## Page Objectifs (30 oct. 2026, demande de Greg)

- `objectifs.html` : départs prévus (Greg septembre 2029, Yvan avril 2030 ; 24 000 € nets chacun la 1re année puis 3 000 €/mois dès 2031), courbe des encaissements sur 12 mois, dividendes et « qui fait les revenus » au choix pessimiste / réaliste / optimiste, priorités des 9 projets, temps de maintenance. Affichée dans la console (onglet rouge « Objectifs » sous « Vue d'ensemble », page `#objectifs`, `objectifs.html?console=1` cache le logo). Chiffres repris du document « Priorités et plans de revenus » (https://claude.ai/artifact/N6tbNcaKPr27u7CyhjN6CR) : **à mettre à jour ensemble** (tableau `PROJETS` du fichier). Copie publiée aussi en artefact : https://claude.ai/artifact/DUdL22Z4nYo3VVAqyCicbC
- Le fichier est public comme le reste du site (pas de données Supabase) : quelqu'un qui connaît l'adresse exacte peut le lire.

## Règle du studio

Chaque appli a son espace admin (admin@ / contact@eggnotfound.fr) et apparaît dans cette console. Applis à brancher : Shivr, Panier Fantôme, robi. AppliNature : demandes, recette et robot IA dans la console (30 oct. 2026) ; chiffres pas encore reliés (pas de serveur).
