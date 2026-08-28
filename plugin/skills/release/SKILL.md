---
name: release
description: "Publie une nouvelle version d'un plugin Claude Code eRom : bump du manifeste et du README du plugin, commit et push de son repo, puis mise à jour de erom-marketplace (entrée du plugin, metadata, tableau du README), commit, push et vérification de la CI. Commande explicite, lancée au slash : /erom-dev-plugin:release."
user-invocable: true
disable-model-invocation: true
---

# Plugin release

Deux repos, deux commits, toujours dans cet ordre : **le plugin d'abord, la marketplace
ensuite**. L'entrée marketplace pointe `ref: main` sur le repo du plugin ; annoncer une
version dont le code n'est pas encore poussé ferait installer autre chose que ce qui est
déclaré, à toute personne qui lance `/plugin update` dans cette fenêtre.

La skill s'exécute **depuis le repo du plugin**, celui où le chantier vient d'être fait.
Le nom du plugin se lit dans son manifeste, jamais dans le nom du dossier : les dossiers
locaux s'appellent `erom-agence-image`, `erom-agence-marketing`, `caserne-net`, pour des
plugins nommés `erom-image`, `erom-marketing`, `erom-caserne`.

---

## 0. La racine du plugin

`PREFLIGHT` = `${CLAUDE_PLUGIN_ROOT}/skills/release/scripts/preflight.py`. C'est un chemin
absolu : recopie-le littéralement dans les deux commandes qui l'appellent, ne le reconstruis
pas depuis le répertoire courant, qui est celui du plugin en cours de release et pas celui
de cette skill. Si `${CLAUDE_PLUGIN_ROOT}` te parvient non expansé, résous-le : deux niveaux
au-dessus du « Base directory for this skill » injecté ci-dessus.

---

## 1. Se situer

```bash
MANIFEST="plugin/.claude-plugin/plugin.json"        # les 6 plugins eRom partagent ce chemin
[ -f "$MANIFEST" ] || MANIFEST=".claude-plugin/plugin.json"   # repli : manifeste à la racine
MARKET="$HOME/dev/erom-marketplace"

uv run --no-project --quiet python "${CLAUDE_PLUGIN_ROOT}/skills/release/scripts/preflight.py" \
  "$MANIFEST" "$MARKET/.claude-plugin/marketplace.json"
git status --short
```

Le préflight dit le nom du plugin, sa version des deux côtés, et s'il est absent de la
marketplace. Trois situations méritent un arrêt et une question à Romain plutôt qu'une
initiative :

- **Le plugin n'est pas dans la marketplace.** C'est une première publication, pas un
  bump : l'entrée à créer demande une description, une source et un choix de `strict`.
- **Les versions divergeaient déjà avant ton passage.** Quelqu'un a poussé un des deux
  côtés sans l'autre. Comprendre avant de superposer un bump.
- **`git status` montre des fichiers modifiés étrangers au chantier.** Ne les embarque
  pas dans le commit de release : un `.gitignore` ou un fichier de config qui traînait
  brouille le diff et complique un futur `revert`. Stage les fichiers du chantier
  nommément, signale les autres dans le récapitulatif, et laisse Romain trancher.

---

## 2. Choisir le numéro de version

SemVer, appliqué à ce que le diff fait réellement :

| Le plugin | Bump |
|---|---|
| gagne une skill, un serveur MCP, un tool, une capacité | mineur |
| corrige un bug, précise une doc, ajuste un défaut | patch |
| change un nom d'outil, une clé MCP, un contrat d'appel | majeur |

Annonce le niveau retenu et sa raison en une ligne, puis avance. Romain corrigera si son
intention était autre, et une question de plus sur un cas évident lui coûte plus cher
qu'une correction.

---

## 3. Le repo du plugin

**Le manifeste** (`plugin/.claude-plugin/plugin.json`) : `version`, et `description` plus
`keywords` si le plugin gagne un composant. Une description qui liste trois skills sur
quatre est ce que voient les gens dans `/plugin marketplace browse`.

**Le README du plugin** (`plugin/README.md`) : la section du nouveau composant, mais
aussi tout ce qui l'énumère ailleurs. Les endroits qui se périment en silence sont
l'intro, la liste des prérequis, la ligne des coûts et la phrase de conclusion sur qui
prend le relais de qui. Relis le fichier entier, pas seulement l'endroit où tu ajoutes.

**Le README racine**, s'il existe : c'est le repo de développement, pas l'artefact
distribué, et son intro énumère souvent les composants elle aussi.

**Le commit**, dans la convention du repo. Lis `git log -3 --format='%B'` avant de le
rédiger : ces repos ont un style dense et documenté qui vaut d'être tenu.

```
<type>(<portée>): <résumé> (<nouvelle version>)

Pourquoi ce changement existe, et ce qu'il change pour qui l'utilise.

Les faits qui ont été vérifiés : ce qui a été testé, mesuré, reproduit. Un
commit qui dit « corrigé » sans dire comment on le sait ne vaut rien six mois
plus tard.

Co-Authored-By: Claude <modèle> <noreply@anthropic.com>
Claude-Session: <url de la session>
```

Rédige le corps depuis le diff réel (`git diff --cached`), pas depuis le souvenir de la
conversation : sur une session longue, la mémoire de ce qui a été fait dérive de ce qui a
été committé. Chaque affirmation du corps doit être traçable à une ligne, une fonction ou
un fichier précis de ce diff ; une affirmation que le diff ne porte pas se corrige ou se
supprime, elle ne se publie pas. La règle vaut pour tout texte de version : corps de
commit, description du manifeste, tableau de la marketplace.

Puis `git push origin main`.

---

## 4. La marketplace

Dans `~/dev/erom-marketplace` :

**`.claude-plugin/marketplace.json`**, deux endroits :
- l'entrée du plugin : `version`, et `description` si le plugin a gagné un composant ;
- `metadata.version`, **au même niveau de bump que le plugin**. La convention se lit dans
  l'historique : `erom-image 0.3.1 → metadata 0.11.4` (patch pour patch),
  `erom-image 0.3.0 → metadata 0.10.0` (mineur pour mineur). Vérifie sur
  `git log --oneline -8` plutôt que de te fier à cette phrase, la convention peut avoir
  bougé depuis.

**`.agents/plugins/marketplace.json`** (manifeste Codex) : il ne liste qu'une partie des
plugins. Ne l'ouvre pas pour rien, mais vérifie si le plugin y figure ; s'il y est, sa
version s'y bump aussi, et le corps du commit doit le dire.

**`README.md`** : le tableau « Plugins disponibles » porte une colonne des skills et une
colonne de description. Les deux se périment.

**Valider avant de pousser**, avec les mêmes assertions que la CI :

```bash
# Les variables de l'étape 1 ne survivent pas d'un appel shell au suivant : redéfinis-les.
MANIFEST="<le chemin retenu à l'étape 1>"
uv run --no-project --quiet python "${CLAUDE_PLUGIN_ROOT}/skills/release/scripts/preflight.py" \
  "$MANIFEST" "$HOME/dev/erom-marketplace/.claude-plugin/marketplace.json"
```

Il refuse de valider si les deux versions divergent encore : c'est précisément l'erreur
que cette étape existe pour attraper.

**Le commit**, dans la convention observée :

```
chore(marketplace): <plugin> <version> (<ce qui change>), metadata <version>

Ce que le plugin gagne, en deux à quatre lignes, du point de vue de qui l'installe.

Description et README mis à jour en conséquence. Le manifeste Codex
(.agents/plugins/) ne liste que caserne et n'est pas concerné.

Co-Authored-By: Claude <modèle> <noreply@anthropic.com>
Claude-Session: <url de la session>
```

Puis `git push origin main`.

---

## 5. Vérifier, puis récapituler

```bash
gh run list --limit 2 --json status,conclusion,headSha,displayTitle \
  --jq '.[] | "\(.status) \(.conclusion // "-") \(.headSha[0:7]) \(.displayTitle)"'
```

La CI `validate.yml` de la marketplace ne se déclenche que sur les manifestes. Attends sa
conclusion avant de dire que c'est publié : `completed success` sur le SHA que tu viens de
pousser, et rien d'autre. Si elle échoue, dis-le avec la sortie, ne conclus pas.

Le récapitulatif donne les deux SHA, les deux versions, l'état de la CI, et rappelle que
la skill n'arrive dans les sessions qu'après `/plugin update <plugin>@erom-marketplace`.

Piège vérifié (2026-08-15, release erom-research 0.5.0) : les installations sont
enregistrées par scope ET par répertoire dans `~/.claude/plugins/installed_plugins.json`.
`claude plugin update` sans flag ne touche que le scope user et répond « already at
latest » même quand des enregistrements locaux restent sur l'ancienne version - une
session lancée dans ces répertoires charge alors l'ancien cache. Contrôle :
`grep -A3 '"<plugin>@erom-marketplace"' ~/.claude/plugins/installed_plugins.json` ;
alignement : `claude plugin update <plugin>@erom-marketplace --scope local` depuis
chaque répertoire listé.

---

## Garde-fous

- **Le push est autorisé par l'invocation.** Demander « je pousse ? » après que Romain a
  lancé une skill nommée `release` est du zèle. En revanche, tout ce qui sort du bump
  (fichier étranger, entrée à créer, versions divergentes) se signale avant.
- **Un tiret cadratin dans une prose que tu écris est bloqué par un hook.** Tiret simple,
  deux-points ou virgule à la place. Le hook ne bloque que ton nouveau texte : ne pars pas
  réécrire les cadratins préexistants du fichier au passage.
- **Ne bump que ce que le diff justifie.** Une version qui monte sans changement distribué
  fait réinstaller du vide à tout le monde.
- **Les deux pushs sont irréversibles côté public.** Si le second échoue, dis-le tout de
  suite : la marketplace annonce alors une version antérieure au code, ce qui est le sens
  le moins dangereux de la divergence, mais il ne faut pas le laisser dormir.
