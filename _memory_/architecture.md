# Architecture

Dernière mise à jour : 2026-08-28

## Ce que c'est

Dépôt de développement du plugin Claude Code `erom-dev-plugin`, publié dans
`erom-marketplace`. Le plugin outille le cycle de vie des autres plugins eRom :
monter un dépôt, dessiner sa carte de présentation, publier une version.

Version publiée à ce jour : **0.1.2**.

## Stack

Markdown pur, aucune étape de build. Deux scripts seulement :

- `preflight.py` (Python, lancé par `uv run --no-project`, zéro dépendance hors
  stdlib)
- `scaffold.sh` (bash, `set -euo pipefail`)

## Arborescence

```
README.md                        vitrine GitHub, image de tête
assets/erom-dev-plugin.png       carte au fusain 1536x1024, produite par illustrate
_memory_/                        ces notes, non distribuées
plugin/                          SEUL dossier distribué (git-subdir)
  .claude-plugin/plugin.json     manifeste
  README.md                      même contenu que la racine, sans image
  LICENSE
  skills/scaffold/               SKILL.md + scripts/scaffold.sh + references/
  skills/illustrate/             SKILL.md + references/GABARIT.md
  skills/release/                SKILL.md + scripts/preflight.py
```

## Distribution

L'entrée marketplace est une source `git-subdir` : `url` du dépôt, `path: plugin`,
`ref: main`, `strict: true`. **Conséquence structurante : le paquet installé ne
contient que le contenu de `plugin/`.** Tout chemin relatif qui sort de ce dossier
casse à l'installation. Vérifié sur le cache : il ne porte que `.claude-plugin/`,
`README.md`, `LICENSE` et `skills/`.

## Dépendances externes

| Skill | Dépend de |
|---|---|
| `illustrate` | Plugin `erom-image` actif (MCP GPT Image), `OPENAI_API_KEY` |
| `release` | `uv`, `gh`, copie locale de `~/dev/erom-marketplace` |
| `scaffold` | Aucune. `caserne onboard` en amont est optionnel |

## Flux d'une release

`preflight.py` compare la version du manifeste à celle de l'entrée marketplace et
rejoue les assertions de la CI. Puis commit et push du plugin, **puis** de la
marketplace. L'ordre est structurel : l'entrée pointe `ref: main` sur le dépôt du
plugin, annoncer une version non poussée ferait installer autre chose que ce qui
est déclaré.
