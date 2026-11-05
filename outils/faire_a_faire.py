"""Construit donnees/a-faire.json pour la console Egg Not Found :
- « demandes » : ce que Claude a demandé de faire (tenu à la main dans DEMANDES ci-dessous) ;
- « recette » : les tests à faire, lus dans les CLAUDE.md de Tikette, Shivr et AppliNature (5e argument, facultatif).
Chaque élément a une clé stable : la console garde les cases cochées par clé (table studio_coches)."""
import json, re, hashlib, sys

def cle(*parts):
    return ':'.join(parts[:-1]) + ':' + hashlib.sha1(parts[-1].encode()).hexdigest()[:10]

# Ce que Claude a demandé et qui n'est pas encore confirmé fait (mettre à jour à chaque séance).
DEMANDES = [
    ('guinche', 'Greg', 'Guinche : lancer le script SQL version 6 (jeux, Crush, sécurité), puis tester la recette v0.4'),
    ('guinche', 'Greg', 'Guinche, Le Dîner de chefs : relancer supabase/diner.sql (version du 4 nov. après-midi : liens perso protégés), puis tester la recette v0.5'),
    ('guinche', 'Greg', 'Guinche, sécurité : lancer supabase/securite.sql (après diner.sql), recopier les fonctions connexion-pseudo et diner-resume, puis les réglages Auth (mot de passe 10 avec lettres et chiffres, e-mail sécurisé, anonymes off) et supprimer les fonctions Stripe inutilisées'),
    ('guinche', 'Tous', 'Avant la sortie de Guinche : retirer crush_achat_test (« Voir qui » gratuit) et brancher l’achat intégré à 1,99 € ; notifications push pour la révélation du Crush à 11 h'),
    ('guinche', 'Tous', 'Guinche : lire régulièrement la table signalements (Crush) dans Supabase'),
    ('guinche', 'Greg', 'Guinche : brancher la connexion Google puis Apple'),
    ('guinche', 'Greg', 'Guinche : faire les tests de la recette v0.3 (cagnotte par lien perso) — script SQL v4 lancé le 1er nov.'),
    ('guinche', 'Tous', 'Guinche, revenus en plus de Fête+ (retenus le 1er nov.) : lieux réservés via les partenaires de Tikette, liens affiliés costumes et déco, thèmes de saison à 0,99 €'),
    ('guinche', 'Tous', 'Avant la sortie de Guinche : retirer « Activer (gratuit pendant les tests) » de Fête+ (fonction fete_plus_test) et brancher les vrais achats (RevenueCat, compte Apple développeur)'),
    ('guinche', 'Yvan', 'Connexion Facebook de Guinche : avec ton Facebook, créer l’appli « Guinche » sur developers.facebook.com (cas d’usage Facebook Login, e-mail de contact admin@eggnotfound.fr, portefeuille business « Egg Not Found » si possible), ajouter Greg en admin, puis prévenir Claude pour la suite (adresse de retour, fournisseur dans Supabase)'),
    ('studio', 'Greg', 'Clés SMTP Brevo à renouveler (elles expirent au bout d’un an, sinon les e-mails de connexion ne partent plus) : « supabase » le 9 oct. 2027, « applibd » le 11 oct. 2027, « Applidates » (Tikette) le 12 oct. 2027, « guinche » vers le 1er nov. 2027 → Brevo › SMTP & API › SMTP › nouvelle clé, puis la recoller dans Supabase › Authentication › Emails › SMTP du bon projet'),
    ('guinche', 'Greg', 'Supabase de Guinche : finir les réglages (modèles d’e-mail « Confirm signup » et « Magic Link » avec le code, fonction connexion-pseudo avec « Verify JWT » décoché, adresses de retour exp://** et guinche://**, connexion anonyme désactivée), puis créer son compte dans l’appli'),
    ('studio', 'Tous', "Toutes les applis du studio : mêmes choix de connexion que Tikette (numéro, Apple, Google, Facebook, e-mail) ; projets Google Cloud et Meta au nom d'admin@eggnotfound.fr, une appli par projet"),
    ('tikette', 'Greg', "Tikette : avant la fin de l'essai gratuit de 7 jours (date de fin choisie dans App Store Connect, vers fin 2027), créer une nouvelle offre de lancement sur les abonnements Or mensuel et annuel, sinon plus d'essai pour les nouveaux"),
    ('tikette', 'Greg', "Tikette Or : lancer supabase/revenuecat.sql, créer la fonction « revenuecat » (Verify JWT désactivé), le secret REVENUECAT_WEBHOOK_SECRET et le webhook dans RevenueCat (Integrations › Webhooks)"),
    ('tikette', 'Greg', "Avec le compte Apple développeur : déclarer contact@tikette.fr dans « Sign in with Apple for Email Communication », sinon nos e-mails n'arrivent pas aux adresses relais Apple"),
    ('tikette', 'Yvan', "Connexion Facebook (le compte Facebook de Greg est bloqué « appareil inhabituel ») : avec ton Facebook, créer l'appli « Tikette » sur developers.facebook.com (cas d'usage Facebook Login, e-mail de contact admin@eggnotfound.fr, portefeuille business « Egg Not Found » si possible), ajouter Greg en admin, puis prévenir Claude pour la suite (permission email, adresse de retour, mise en ligne, fournisseur dans Supabase) ; bouton Facebook caché dans Tikette en attendant"),
    ('tikette', 'Greg', 'Vraie version : dans Supabase › Apple, ajouter l’identifiant de l’appli Tikette à côté de host.exp.Exponent (une fois le compte Apple développeur pris)'),
    ('tikette', 'Greg', "Tikette : tester le vrai SMS de connexion (expéditeur « Tikette » vérifié chez Brevo le 5 nov.) avec un numéro qui n'est pas un numéro de test"),
    ('tikette', 'Tous', 'Avant la sortie : retirer les numéros de test de Supabase (Sign In / Providers › Phone › Test Phone Numbers), sauf celui donné aux testeurs d’Apple et Google'),
    ('studio', 'Tous', 'Décider ensemble la proposition d’Yvan : contact@eggnotfound.fr comme adresse de contact unique de toutes les applis (Tikette l’utilise déjà ; Shivr encore sur contact@shivr.fr)'),
    ('tikette', 'Yvan', 'Adhérer au médiateur de la consommation CM2C (cm2c.net, ≈ 48 € pour 3 ans) dès l’immatriculation de la micro-entreprise, avant la vente de Tikette Or ; garder l’attestation (PDF) et donner à Claude le nom et l’adresse du médiateur pour les CGV'),
    ('tikette', 'Tous', 'Comptes développeur au nom du studio : Apple (99 €/an, ouvre TestFlight pour tester sur iPhone) et Google (25 $ une fois), vers la sortie'),
    ('tikette', 'Greg', 'GetYourGuide : coordonnées bancaires et SIRET une fois la micro-entreprise créée'),
    ('shivr', 'Greg', 'Supabase de Shivr : coller le nouveau modèle d’e-mail (Magic Link et Confirm signup)'),
    ('applinature', 'Yvan', 'Tester AppliNature v0.10 sur l’iPhone (bouton « Partir », balade du jour, nouvelle police) et dire à Claude ce qui gêne'),
    ('applinature', 'Yvan', 'Prendre une série de photos en gros plan (feuilles, fleurs, champignons) pour mesurer l’IA sur le terrain'),
    ('applinature', 'Yvan', 'GitHub : activer la page publique des défis (dépôt AppliNature-ia › Settings › Pages › branche main, dossier /docs)'),
    ('applinature', 'Tous', 'Choisir le nom définitif d’AppliNature'),
    ('applinature', 'Tous', 'Décider où mettre les comptes et les signalements d’AppliNature (offre Supabase gratuite limitée à 2 projets, déjà pris par Tikette et Shivr)'),
    ('applinature', 'Tous', 'Avant de vendre l’appli : remplacer la météo Open-Meteo (gratuite seulement sans usage commercial) par Météo-France'),
    ('hearthaven', 'Yvan', 'Relancer Hearthaven (dossier « Hearthaven » du bureau) et faire la recette de la version 0.1 ; envoyer une capture à Claude si quelque chose cloche'),
    ('hearthaven', 'Yvan', 'Choisir la prochaine grande étape d’Hearthaven : autres personnages, carte et boussole, ou biomes et animaux'),
    ('hearthaven', 'Tous', 'Décider si on sauvegarde la version Godot d’Hearthaven sur GitHub (dépôt Hearthhaven, pas à jour depuis le 27 oct.)'),
    ('hearthaven', 'Tous', 'Générique de fin d’Hearthaven : créditer Fish_233 (godotshaders.com) et Rune Skovbo Johansen (filtre d’érosion, licence MPL 2.0)'),
    ('shivr', 'Tous', 'Supabase de Shivr : vérifier que les scripts tournois, messages, contact-id, support, ouvertures, ouvertures-controles et echanges-preuves sont lancés'),
]

# Recette d'Hearthaven (pas de CLAUDE.md dans un dépôt : le projet Godot vit sur le PC d'Yvan). Mettre à jour à chaque version.
RECETTE_GUINCHE = [
    ('v0.5.1', 'Créer un compte avec un mot de passe trop simple (azerty123…) : refusé avec une phrase claire'),
    ('v0.5.1', 'Après la mise à jour, on reste connecté (la session est maintenant chiffrée sur le téléphone)'),
    ('v0.5.1', 'Avec un compte qui n’est pas admin@ ou contact@ : l’achat test Fête+ / Crush affiche « réservé à l’équipe »'),
    ('v0.2', 'Créer un compte par e-mail : le code arrive (e-mail aux couleurs de Guinche) et il marche'),
    ('v0.2', 'Se déconnecter puis se reconnecter avec son pseudo et son mot de passe : les soirées sont toujours là'),
    ('v0.2', 'Mot de passe oublié : le code arrive, le nouveau mot de passe est enregistré'),
    ('v0.2', 'Profil : photo, prénom, nom, pseudo, ville ; une date de naissance de moins de 15 ans est refusée'),
    ('v0.2', 'Ambiance de l’appli : changer de couleur, toute l’appli suit'),
    ('v0.2', 'Nouvelle soirée : choisir un thème de soirée (ex. Années 80), la carte change en direct avec le bon décor et la bonne police'),
    ('v0.2', 'Choisir une date dans 2 mois en quelques appuis (flèches du calendrier) ; heure du soir, puis « Autre heure »'),
    ('v0.2', 'Lieu : les suggestions d’adresse apparaissent pendant qu’on tape ; « Un lieu public » trouve un bar connu'),
    ('v0.2', 'Qui ramène quoi : les 6 choix et l’ajout à la main'),
    ('v0.2', 'Clavier : le bouton OK au-dessus le ferme ; glisser la page le ferme aussi'),
    ('v0.2', 'Mes invités : ajout depuis les contacts (autorisation demandée) et à la main'),
    ('v0.2', 'Lien personnel ouvert : « Salut [prénom] 👋 », prénom déjà rempli ; la réponse se range sur la bonne ligne'),
    ('v0.2', '« Envoyer » / « Relancer » ouvre WhatsApp avec le message déjà écrit'),
    ('v0.2', '« Rappeler le groupe sur WhatsApp » ouvre WhatsApp avec le rappel déjà écrit'),
    ('v0.2', 'Après avoir répondu : « Ajouter à mon agenda » crée l’événement dans l’agenda du téléphone'),
    ('v0.3', 'Fête+ : choisir un thème payant ouvre l’écran Fête+ ; « Activer (test) » puis le thème s’applique'),
    ('v0.3', 'Créer une soirée avec cagnotte : choisir Revolut, coller son lien revolut.me/… → « Lien Revolut reconnu »'),
    ('v0.3', 'Invité : « Participer 20 € avec Revolut » ouvre Revolut ; puis « J’ai participé » → le montant apparaît chez l’organisateur'),
    ('v0.3', 'Invité : « Cacher mon montant » puis « Je me suis trompé, annuler »'),
    ('v0.3', 'Organisateur : retirer une ligne avec ✕, « Changer de lien », clôturer puis rouvrir la cagnotte'),
    ('v0.3', 'Lien PayPal.me : le montant choisi est déjà rempli dans PayPal'),
    ('v0.4', 'Killer : 3 invités « Je viens » (dont toi depuis ton invitation) → Jeux de la soirée › Killer › Lancer'),
    ('v0.4', 'Killer : un joueur ouvre l’invitation › « Jouer au Killer » → voit sa cible et sa mission (touche = cacher)'),
    ('v0.4', 'Killer : « Mission réussie » → la cible voit « X dit t’avoir eu » → « C’est vrai » ; le tueur récupère la cible suivante'),
    ('v0.4', 'Killer : l’organisateur retire un joueur (✕), puis « Terminer la partie » → journal à partager'),
    ('v0.4', 'Le tel tourne : Passe le tel (compte à rebours 5 s), Tu préfères, Je n’ai jamais'),
    ('v0.4', 'Crush : répondre « Je viens » connecté → Crush de soirée → cocher les 3 cases → Participer (refusé si moins de 18 ans)'),
    ('v0.4', 'Crush : choisir une personne ; le lendemain 11 h, si c’est réciproque → « C’est un match » et discussion'),
    ('v0.4', 'Crush : « Voir qui · 1,99 € » (gratuit pendant les tests), bloquer, signaler, quitter le Crush'),
    ('v0.4', 'Modifier une soirée déjà passée (ajouter une cagnotte) : ça s’enregistre ; une cagnotte clôturée reste clôturée'),
    ('v0.4', 'Profil : la date de naissance ne se modifie plus'),
    ('v0.5', 'Accueil › « Créer un événement » : la carte « Le Dîner de chefs » est en tête, les tuiles Anniversaire / Soirée / Crémaillère / Autre ouvrent la création de soirée'),
    ('v0.5', 'Lancer une saison avec 3 chefs ou plus (deux prénoms identiques refusés) ; choisir des dates'),
    ('v0.5', 'Envoyer son lien à un chef par WhatsApp : sa page s’ouvre dans le navigateur sans compte, il peut choisir sa date et son lieu'),
    ('v0.5', 'Après la date d’un dîner : « Note le dîner de … » apparaît sur l’accueil et sur la page du chef ; on ne peut pas noter son propre dîner ni un dîner pas encore passé'),
    ('v0.5', 'L’organisateur ne voit que le nombre de notes reçues, jamais les notes ; une fois qu’un chef a ouvert son lien, l’organisateur voit « ✓ a ouvert son lien » et l’ancien lien ne marche plus ailleurs'),
    ('v0.5', 'Fluidité : revenir sur un écran déjà vu (accueil, soirée, invitation, saison) l’affiche tout de suite, sans roue de chargement ; relancer l’appli affiche l’accueil sans attendre'),
    ('v0.5', 'Finale : classement révélé à tous, récap voix off écrit par l’IA, « Écouter » le lit à voix haute, « Partager le classement »'),
]

RECETTE_HEARTHAVEN = [
    ('v0.1', 'Plus de carrés sur le sol, près de la plage comme sur la roche'),
    ('v0.1', 'Plus de carrés ni de cassures dans la mer, au bord comme au large'),
    ('v0.1', 'Gros rochers et souches sur une pente : le pied se fond dans le sol, sans bande sombre'),
    ('v0.1', 'Esprit : yeux visibles qui clignent, bouche visible, miel bien doré sur le haut de la tête'),
    ('v0.1', 'Esprit assez opaque (on ne voit plus le décor à travers son corps)'),
    ('v0.1', 'On ne traverse plus les rochers, souches, troncs couchés ni les troncs d’arbres ; on passe toujours dans les buissons, fleurs et herbes'),
    ('v0.1', 'Nuages lents, ombres en petites taches sur le sol'),
    ('v0.1', 'Objets à ramasser : brillance sans halo au sol, posés à plat'),
    ('v0.1', 'Plus de ligne nette entre les textures de la montagne'),
    ('v0.1', 'Plus de ligne droite au sol où une ombre s’arrête net (ombres de palmiers continues)'),
    ('v0.1', 'Les empreintes de pas s’assombrissent à l’ombre, sous les nuages et la nuit'),
    ('v0.1', 'Ceinture à droite : le rabat ouvre la sacoche, la nappe est dans la première poche, les outils dans les suivantes'),
    ('v0.1', 'Nappe : elle se déroule au sol, on y pose des objets, « Assembler » fait tourbillonner les objets et l’outil apparaît'),
    ('v0.1', 'Carnet : il s’ouvre comme un vrai livre (la couverture se rabat), seule la feuille de papier tourne, sans trous'),
]

def recette_tikette(texte):
    sec = texte.split('## Recette', 1)[1].split('\n## ', 1)[0]
    items = []
    version = None
    for l in sec.splitlines():
        m = re.match(r'\*\*(v[0-9.]+)[^*]*\*\*', l.strip())
        if m:
            version = m.group(1)
            reste = l.split('**', 2)[2].strip(' :')
            if version == 'v0.29' and reste:
                items.append((version, reste))
            continue
        if l.strip().startswith('**Vraie version') or l.startswith('Ancienne'):
            version = None
        m = re.match(r'\s*\d+\.\s+(.*)', l)
        if m and version:
            items.append((version, m.group(1)))
    return items

def recette_shivr(texte):
    sec = texte.split('## À tester par le porteur', 1)[1].split('\n## ', 1)[0]
    items = []
    for l in sec.splitlines():
        m = re.match(r'- (0\.\d+) : (.*)', l)
        if m:
            items.append(('v' + m.group(1), m.group(2)))
    items.sort(key=lambda x: -float(x[0][1:].split('.')[1]))
    return items

def recette_applinature(texte):
    if '## À tester par le porteur' not in texte:
        return []
    sec = texte.split('## À tester par le porteur', 1)[1].split('\n## ', 1)[0]
    return [(m.group(1), m.group(2)) for m in (re.match(r'- (v[0-9.]+) : (.*)', l) for l in sec.splitlines()) if m]

def propre(t):
    return re.sub(r'`([^`]*)`', r'\1', re.sub(r'\*\*', '', t)).strip()

tik = open(sys.argv[1]).read()
shi = open(sys.argv[2]).read()
sortie = {'maj': sys.argv[4], 'elements': []}
for appli, qui, t in DEMANDES:
    sortie['elements'].append({'cle': cle('demande', appli, t), 'groupe': 'demande', 'appli': appli, 'qui': qui, 'titre': t})
for v, t in recette_tikette(tik):
    sortie['elements'].append({'cle': cle('recette', 'tikette', v, t), 'groupe': 'recette', 'appli': 'tikette', 'qui': 'Tous', 'version': v, 'titre': propre(t)})
for v, t in recette_shivr(shi):
    sortie['elements'].append({'cle': cle('recette', 'shivr', v, t), 'groupe': 'recette', 'appli': 'shivr', 'qui': 'Tous', 'version': v, 'titre': propre(t)})
if len(sys.argv) > 5:
    for v, t in recette_applinature(open(sys.argv[5]).read()):
        sortie['elements'].append({'cle': cle('recette', 'applinature', v, t), 'groupe': 'recette', 'appli': 'applinature', 'qui': 'Tous', 'version': v, 'titre': propre(t)})
for v, t in RECETTE_GUINCHE:
    sortie['elements'].append({'cle': cle('recette', 'guinche', v, t), 'groupe': 'recette', 'appli': 'guinche', 'qui': 'Tous', 'version': v, 'titre': t})
for v, t in RECETTE_HEARTHAVEN:
    sortie['elements'].append({'cle': cle('recette', 'hearthaven', v, t), 'groupe': 'recette', 'appli': 'hearthaven', 'qui': 'Yvan', 'version': v, 'titre': t})
json.dump(sortie, open(sys.argv[3], 'w'), ensure_ascii=False, indent=1)
print(len(sortie['elements']), 'éléments')
