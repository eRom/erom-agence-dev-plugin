#!/usr/bin/env bash
#
# Scaffold d'un depot de plugin Claude Code eRom.
#
# Part d'un dossier deja cree et onboarde (caserne onboard) : git est init,
# le remote origin pointe sur GitHub, _memory_/ONBOARD.md existe.
# Le script ne cree ni le dossier, ni le repo, ni le projet Linear ou Slack.
#
# Idempotent : n'ecrase jamais un fichier existant, signale ce qu'il saute.
#
# Usage : scaffold.sh <nom-plugin> [chemin] [description]
#   nom-plugin  : le "name" du manifeste, ex. erom-seo
#   chemin      : racine du depot, defaut = repertoire courant
#   description : une phrase, defaut = placeholder a remplir

set -euo pipefail

REFS="$(cd "$(dirname "${BASH_SOURCE[0]}")/../references" && pwd)"

PLUGIN_NAME="${1:-}"
TARGET="${2:-$PWD}"
DESCRIPTION="${3:-A REMPLIR : une phrase qui dit ce que fait le plugin.}"

if [[ -z "$PLUGIN_NAME" ]]; then
  echo "usage: scaffold.sh <nom-plugin> [chemin] [description]" >&2
  exit 2
fi
if [[ ! -d "$TARGET" ]]; then
  echo "erreur: le dossier '$TARGET' n'existe pas. Cree-le et lance caserne onboard avant." >&2
  exit 2
fi
TARGET="$(cd "$TARGET" && pwd)"

# --- Contexte lu, jamais devine -------------------------------------------

REPO_SLUG=""
if git -C "$TARGET" rev-parse --git-dir >/dev/null 2>&1; then
  ORIGIN="$(git -C "$TARGET" remote get-url origin 2>/dev/null || true)"
  if [[ -n "$ORIGIN" ]]; then
    REPO_SLUG="$(basename "$ORIGIN" .git)"
  fi
fi
if [[ -z "$REPO_SLUG" ]]; then
  REPO_SLUG="$(basename "$TARGET")"
  echo "  ! pas de remote origin : repository deduit du dossier ($REPO_SLUG), a verifier"
fi

if [[ ! -f "$TARGET/_memory_/ONBOARD.md" ]]; then
  echo "  ! _memory_/ONBOARD.md absent : caserne onboard n'a pas tourne ici."
  echo "    Le plugin se scaffolde quand meme, mais le projet n'a ni Linear ni Slack."
fi

DATE="$(date +%F)"

# --- Rendu ----------------------------------------------------------------

created=0
skipped=0

render() {
  local src="$1" dest="$2" content
  if [[ -e "$dest" ]]; then
    echo "  = ${dest#$TARGET/} (existe, laisse tel quel)"
    skipped=$((skipped + 1))
    return
  fi
  mkdir -p "$(dirname "$dest")"
  content="$(cat "$src")"
  content="${content//\{\{PLUGIN_NAME\}\}/$PLUGIN_NAME}"
  content="${content//\{\{REPO_SLUG\}\}/$REPO_SLUG}"
  content="${content//\{\{DESCRIPTION\}\}/$DESCRIPTION}"
  content="${content//\{\{DATE\}\}/$DATE}"
  printf '%s\n' "$content" > "$dest"
  echo "  + ${dest#$TARGET/}"
  created=$((created + 1))
}

# Les binaires ne passent jamais par render() : la substitution via $(...) mange
# les octets NUL et corrompt le fichier. Verifie le 28/08/2026, un placeholder
# PNG de 21993 octets ressorti a 18237, `file` le voyant comme `data` et sips
# ne lisant plus ses dimensions.
copy() {
  local src="$1" dest="$2"
  if [[ -e "$dest" ]]; then
    echo "  = ${dest#$TARGET/} (existe, laisse tel quel)"
    skipped=$((skipped + 1))
    return
  fi
  mkdir -p "$(dirname "$dest")"
  cp "$src" "$dest"
  echo "  + ${dest#$TARGET/}"
  created=$((created + 1))
}

make_dir() {
  local d="$1"
  if [[ -d "$TARGET/$d" ]]; then
    echo "  = $d/ (existe)"
  else
    mkdir -p "$TARGET/$d"
    # .gitkeep pour que le dossier vide survive au commit
    : > "$TARGET/$d/.gitkeep"
    echo "  + $d/"
    created=$((created + 1))
  fi
}

echo "Scaffold $PLUGIN_NAME dans $TARGET (repo eRom/$REPO_SLUG)"
echo

make_dir "assets"
make_dir "docs"
make_dir "plugin/skills"

render "$REFS/gitignore"           "$TARGET/.gitignore"
render "$REFS/CLAUDE.md"           "$TARGET/CLAUDE.md"
render "$REFS/README_GITHUB.md"    "$TARGET/README.md"
render "$REFS/plugin.json"         "$TARGET/plugin/.claude-plugin/plugin.json"
render "$REFS/README_PLUGIN.md"    "$TARGET/plugin/README.md"
render "$REFS/LICENSE"             "$TARGET/plugin/LICENSE"
copy   "$REFS/plugin.png"          "$TARGET/assets/plugin.png"

echo
echo "$created cree(s), $skipped laisse(s) en place."
echo
echo "Reste a faire, dans l'ordre :"
echo "  1. Ecrire description et keywords dans plugin/.claude-plugin/plugin.json"
echo "  2. Ecrire au moins une skill dans plugin/skills/<nom>/SKILL.md"
echo "  3. Verifier : claude --plugin-dir plugin plugin details $PLUGIN_NAME"
echo "  4. Commiter"
