"""Contrôle de cohérence avant et après un bump de plugin eRom.

Rejoue les assertions de la CI `validate.yml` de erom-marketplace, et compare la
version déclarée dans le manifeste du plugin à celle annoncée par la marketplace.
Cette divergence est normale entre les deux commits d'une release, et fautive
partout ailleurs : c'est l'erreur silencieuse que ce script existe pour attraper.

Usage :
    python preflight.py <plugin.json> <marketplace.json>

Codes de sortie :
    0  cohérent
    1  divergence de version, ou manifeste invalide
    2  le plugin est absent de la marketplace (première publication)
"""

import json
import sys
from pathlib import Path


def charger(chemin: Path) -> dict:
    try:
        return json.loads(chemin.read_text(encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(f"❌ introuvable : {chemin}")
    except json.JSONDecodeError as e:
        sys.exit(f"❌ JSON invalide dans {chemin} : {e}")


def valider_marketplace(market: dict, chemin: Path) -> None:
    """Les mêmes assertions que .github/workflows/validate.yml."""
    for cle in ("name", "owner", "plugins"):
        if cle not in market:
            sys.exit(f"❌ {chemin.name} : clé « {cle} » manquante")
    if not isinstance(market["plugins"], list):
        sys.exit(f"❌ {chemin.name} : « plugins » n'est pas une liste")
    for p in market["plugins"]:
        if not (p.get("name") and p.get("source")):
            sys.exit(f"❌ {chemin.name} : entrée sans name ou source : {p}")
    noms = [p["name"] for p in market["plugins"]]
    doublons = {n for n in noms if noms.count(n) > 1}
    if doublons:
        sys.exit(f"❌ {chemin.name} : noms en double : {doublons}")


def main() -> int:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    chemin_plugin, chemin_market = Path(sys.argv[1]), Path(sys.argv[2])

    plugin = charger(chemin_plugin)
    market = charger(chemin_market)
    valider_marketplace(market, chemin_market)

    nom = plugin.get("name")
    version_locale = plugin.get("version")
    if not nom or not version_locale:
        sys.exit(f"❌ {chemin_plugin} : name ou version manquant")

    print(f"plugin        {nom} {version_locale}   ({chemin_plugin})")
    print(f"marketplace   {len(market['plugins'])} plugins, "
          f"metadata {market.get('metadata', {}).get('version', '?')}")

    entree = next((p for p in market["plugins"] if p["name"] == nom), None)
    if entree is None:
        print(f"\n⚠️  « {nom} » est absent de la marketplace.")
        print("   Première publication : l'entrée est à créer (source, description,")
        print("   strict), ce n'est pas un simple bump. Demander à Romain.")
        return 2

    version_market = entree.get("version")
    print(f"entrée        {nom} {version_market}")

    # Le manifeste Codex ne liste qu'une partie des plugins.
    codex = chemin_market.parent.parent / ".agents" / "plugins" / "marketplace.json"
    if codex.exists():
        noms_codex = [p.get("name") for p in charger(codex).get("plugins", [])]
        concerne = nom in noms_codex or nom.removeprefix("erom-") in noms_codex
        print(f"manifeste Codex  {'CONCERNÉ, à bump aussi' if concerne else 'non concerné'}"
              f"  ({', '.join(noms_codex) or 'vide'})")

    if version_locale != version_market:
        print(f"\n❌ divergence : plugin {version_locale} ≠ marketplace {version_market}")
        print("   Normal entre les deux commits d'une release, fautif ailleurs.")
        return 1

    print(f"\n✅ versions alignées sur {version_locale}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
