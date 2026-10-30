#!/usr/bin/env python3
"""Ajoute (ou remplace) le logo d'une appli ou d'un jeu dans la console Egg Not Found.

Usage :
    python3 outils/logo.py <id> <image> [--fond "#1A1426"]

- <id>    : l'identifiant de l'appli dans donnees/applis.json (ex. braise, robi, guinche)
- <image> : le logo choisi (PNG, JPG, WEBP ou SVG converti en PNG), de préférence carré

Le script :
1. met l'image au carré (sur un fond de la couleur --fond si elle n'est pas carrée),
2. l'enregistre en 256 × 256 dans logos/<id>.png,
3. renseigne "logo": "logos/<id>.png" dans donnees/applis.json,
4. recopie le logo et applis.json dans ../applidates-pages/console/ si ce dossier existe
   (tant que la console est servie sur tikette.fr/console/).

Ensuite : committer et pousser les deux dépôts (EggNotFoundGestion et applidates-pages).
"""
import json
import shutil
import sys
from pathlib import Path

from PIL import Image

RACINE = Path(__file__).resolve().parent.parent
TAILLE = 256


def carre(image: Image.Image, fond: str) -> Image.Image:
    image = image.convert("RGBA")
    l, h = image.size
    if l == h:
        return image.resize((TAILLE, TAILLE), Image.LANCZOS)
    cote = max(l, h)
    toile = Image.new("RGBA", (cote, cote), fond)
    toile.alpha_composite(image, ((cote - l) // 2, (cote - h) // 2))
    return toile.resize((TAILLE, TAILLE), Image.LANCZOS)


def main() -> None:
    args = sys.argv[1:]
    if len(args) < 2:
        sys.exit(__doc__)
    ident, chemin = args[0], Path(args[1])
    fond = args[args.index("--fond") + 1] if "--fond" in args else "#0A0A0A"

    fichier = RACINE / "donnees" / "applis.json"
    donnees = json.loads(fichier.read_text(encoding="utf-8"))
    appli = next((a for a in donnees["applis"] if a["id"] == ident), None)
    if appli is None:
        sys.exit(f"Aucune appli « {ident} » dans donnees/applis.json : ajoutez-la d'abord.")

    sortie = RACINE / "logos" / f"{ident}.png"
    carre(Image.open(chemin), fond).save(sortie, optimize=True)
    appli["logo"] = f"logos/{ident}.png"
    fichier.write_text(json.dumps(donnees, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Logo enregistré : {sortie.relative_to(RACINE)}")

    copie = RACINE.parent / "applidates-pages" / "console"
    if copie.is_dir():
        shutil.copy(sortie, copie / "logos" / sortie.name)
        shutil.copy(fichier, copie / "donnees" / "applis.json")
        print("Recopié dans applidates-pages/console/")


if __name__ == "__main__":
    main()
