# Fichiers clés

Dernière mise à jour : 2026-08-28

## Manifeste et vitrine

| Fichier | Rôle |
|---|---|
| `plugin/.claude-plugin/plugin.json` | Manifeste. `skills: "./skills/"` déclaré, pas de clé `agents` (découverte auto). Description et keywords remplis. |
| `README.md` | Vitrine GitHub, seule à porter `![...](assets/erom-dev-plugin.png)`. |
| `plugin/README.md` | Même contenu, sans ligne d'image, seule différence de texte : la phrase sur la carte renvoie au dépôt GitHub. |
| `assets/erom-dev-plugin.png` | Carte au fusain 1536x1024, 3,3 Mo. Non distribuée. |

## Skill scaffold

| Fichier | Rôle |
|---|---|
| `plugin/skills/scaffold/SKILL.md` | Procédure. Section « 0. La racine du plugin » en tête, puis contexte, lancement, personnalisation, vérification, commit. |
| `plugin/skills/scaffold/scripts/scaffold.sh` | Le moteur. `render()` pour le texte avec substitution `{{...}}`, `copy()` pour les binaires, `make_dir()` pour les dossiers. Idempotent. |
| `plugin/skills/scaffold/references/` | Les sept gabarits rendus : `gitignore`, `CLAUDE.md`, `README_GITHUB.md`, `README_PLUGIN.md`, `plugin.json`, `LICENSE`, `plugin.png`. |
| `references/plugin.png` | Placeholder 1536x1024, 22 Ko, généré par Pillow. Dit lui-même `/erom-dev-plugin:illustrate`. |

Les deux gabarits de README ne diffèrent que par les deux premières lignes :
`README_GITHUB.md` porte l'image, `README_PLUGIN.md` non.

## Skill illustrate

| Fichier | Rôle |
|---|---|
| `plugin/skills/illustrate/SKILL.md` | Procédure. Préflight `erom-image` avant de payer un sous-agent, puis prompt, génération déléguée, vérification au crop. |
| `plugin/skills/illustrate/references/GABARIT.md` | Le gabarit de prompt complet, les quatre familles d'écorché, et douze règles dures ancrées sur incidents datés. |

Gabarit d'origine, pour les cartes de candidature France Travail :
`~/dev/EROM-HQ/emploi/projets/visuels/GABARIT.md`. Style commun, doctrine de
contenu différente.

## Skill release

| Fichier | Rôle |
|---|---|
| `plugin/skills/release/SKILL.md` | Procédure en cinq étapes, plus les garde-fous. |
| `plugin/skills/release/scripts/preflight.py` | Compare les deux versions et rejoue les assertions de `validate.yml`. Exit 0 aligné, 1 divergent, 2 absent de la marketplace. |

## Hors dépôt, indispensables

| Chemin | Rôle |
|---|---|
| `~/dev/erom-marketplace/.claude-plugin/marketplace.json` | L'entrée du plugin et `metadata.version`. |
| `~/dev/erom-marketplace/README.md` | Tableau « Plugins disponibles », une ligne par plugin, sans version. |
| `~/.claude/plugins/installed_plugins.json` | Ce qui est réellement installé, par scope et par répertoire. |
