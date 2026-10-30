"""Construit donnees/a-faire.json pour la console Egg Not Found :
- « demandes » : ce que Claude a demandé de faire (tenu à la main dans DEMANDES ci-dessous) ;
- « recette » : les tests à faire, lus dans les CLAUDE.md de Tikette, Shivr et AppliNature (5e argument, facultatif).
Chaque élément a une clé stable : la console garde les cases cochées par clé (table studio_coches)."""
import json, re, hashlib, sys

def cle(*parts):
    return ':'.join(parts[:-1]) + ':' + hashlib.sha1(parts[-1].encode()).hexdigest()[:10]

# Ce que Claude a demandé et qui n'est pas encore confirmé fait (mettre à jour à chaque séance).
DEMANDES = [
    ('tikette', 'Greg', 'SMS : suivre la validation de l’expéditeur « Tikette » chez Brevo (Paramètres › SMS Sender ID), puis faire le test du vrai SMS de connexion (remis à plus tard le 30 oct.)'),
    ('tikette', 'Tous', 'Avant la sortie : retirer les numéros de test de Supabase (Sign In / Providers › Phone › Test Phone Numbers), sauf celui donné aux testeurs d’Apple et Google'),
    ('tikette', 'Tous', 'OVH : redirection de contact@tikette.fr vers contact@eggnotfound.fr'),
    ('studio', 'Tous', 'Décider ensemble la proposition d’Yvan : contact@eggnotfound.fr comme adresse de contact unique de toutes les applis (Tikette l’utilise déjà ; Shivr encore sur contact@shivr.fr)'),
    ('tikette', 'Greg', 'Pages légales : donner à Claude nom, adresse et SIRET de la micro-entreprise dès l’immatriculation (bandeau « version provisoire » jusque-là)'),
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
for v, t in RECETTE_HEARTHAVEN:
    sortie['elements'].append({'cle': cle('recette', 'hearthaven', v, t), 'groupe': 'recette', 'appli': 'hearthaven', 'qui': 'Yvan', 'version': v, 'titre': t})
json.dump(sortie, open(sys.argv[3], 'w'), ensure_ascii=False, indent=1)
print(len(sortie['elements']), 'éléments')
