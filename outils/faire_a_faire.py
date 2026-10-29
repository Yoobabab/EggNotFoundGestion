"""Construit donnees/a-faire.json pour la console Egg Not Found :
- « demandes » : ce que Claude a demandé de faire (tenu à la main dans DEMANDES ci-dessous) ;
- « recette » : les tests à faire, lus dans les CLAUDE.md de Tikette et Shivr.
Chaque élément a une clé stable : la console garde les cases cochées par clé (table studio_coches)."""
import json, re, hashlib, sys

def cle(*parts):
    return ':'.join(parts[:-1]) + ':' + hashlib.sha1(parts[-1].encode()).hexdigest()[:10]

# Ce que Claude a demandé et qui n'est pas encore confirmé fait (mettre à jour à chaque séance).
DEMANDES = [
    ('tikette', 'Greg', 'Brevo : ajouter le domaine eggnotfound.fr et l’expéditeur « Egg Not Found » <contact@eggnotfound.fr>'),
    ('tikette', 'Greg', 'Supabase : créer la fonction envoyer-email (Verify JWT désactivé)'),
    ('tikette', 'Greg', 'Supabase : Authentication › Hooks › Send Email hook vers envoyer-email + secret SEND_EMAIL_HOOK_SECRET'),
    ('tikette', 'Greg', 'Supabase : lancer supabase/console2.sql (console : applis, à faire, coûts)'),
    ('tikette', 'Tous', 'Connexion par SMS : crédits SMS Brevo, fonction envoyer-sms, fournisseur Phone activé, Send SMS hook + SEND_SMS_HOOK_SECRET'),
    ('tikette', 'Tous', 'OVH : redirection de contact@tikette.fr vers contact@eggnotfound.fr'),
    ('tikette', 'Tous', 'Comptes développeur au nom du studio : Apple (99 €/an) et Google (25 $ une fois), avant la sortie'),
    ('tikette', 'Greg', 'GetYourGuide : coordonnées bancaires et SIRET une fois la micro-entreprise créée'),
    ('studio', 'Greg', 'GitHub › EggNotFoundGestion › Pages : cocher « Enforce HTTPS » dès que possible'),
    ('shivr', 'Greg', 'Supabase de Shivr : coller le nouveau modèle d’e-mail (Magic Link et Confirm signup)'),
    ('shivr', 'Tous', 'Supabase de Shivr : vérifier que les scripts tournois, messages, contact-id, support, ouvertures, ouvertures-controles et echanges-preuves sont lancés'),
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
json.dump(sortie, open(sys.argv[3], 'w'), ensure_ascii=False, indent=1)
print(len(sortie['elements']), 'éléments')
