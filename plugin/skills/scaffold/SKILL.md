---
name: scaffold
description: Scaffold un dépôt de plugin Claude Code eRom déjà créé et onboardé (structure plugin/, manifeste, contrat de dépôt), et prépare sa publication dans la eRom Marketplace.
user-invocable: true
disable-model-invocation: true
---

# scaffold

## Ce que produit la skill

Un dépôt de plugin prêt à recevoir sa première skill :

```
.gitignore
README.md                        vitrine GitHub, image de tête en placeholder
CLAUDE.md                        contrat du dépôt, à compléter
assets/plugin.png                placeholder 1536x1024, remplacé par illustrate
docs/
plugin/                          seul dossier distribué
  .claude-plugin/plugin.json     manifeste rempli avec le vrai repo
  skills/
  README.md                      même contenu, sans image
  LICENSE
```

**Deux README, pour deux lecteurs.** Celui de la racine est ce que GitHub affiche
en page d'accueil du dépôt : il porte l'image de tête, et son chemin
`assets/plugin.png` résout depuis là. Celui de `plugin/` part dans le paquet
distribué, où `assets/` n'existe pas puisque la source marketplace est un
`git-subdir` sur `plugin/` : il reste en Markdown pur. Les deux sont à remplir,
le tableau des skills compris.

## Point de départ attendu

La skill ne crée ni le dossier, ni le dépôt GitHub, ni le projet Linear ou
Slack. Elle suppose que ces deux gestes ont déjà eu lieu :

```bash
mkdir ~/dev/erom-agence-<nom> && cd $_
caserne onboard --as claude          # repo GitHub privé + git init + remote
                                     # + Linear + Slack + _memory_/ONBOARD.md
                                     # + enregistrement RAG dans gerber-vault
```

Si `_memory_/ONBOARD.md` manque, le script le dit et continue : le plugin sera
scaffoldé, mais le projet n'aura ni Linear ni Slack. Le proposer avant de
poursuivre plutôt que l'ignorer.

## Procédure

### 0. La racine du plugin

`SCAFFOLD` = `${CLAUDE_PLUGIN_ROOT}/skills/scaffold/scripts/scaffold.sh`. C'est un chemin
absolu : recopie-le littéralement à l'étape 2, ne le reconstruis pas depuis le répertoire
courant, qui est le dépôt à scaffolder et pas celui de cette skill. Si
`${CLAUDE_PLUGIN_ROOT}` te parvient non expansé, résous-le : deux niveaux au-dessus du
« Base directory for this skill » injecté ci-dessus.

### 1. Lire le contexte, ne rien deviner

```bash
git remote get-url origin        # -> eRom/erom-agence-<nom>, source du champ repository
cat _memory_/ONBOARD.md          # -> onboarding caserne fait ou non
```

Le nom du plugin n'est pas le nom du dépôt : le dépôt garde le préfixe
`erom-agence-`, le plugin s'appelle `erom-<nom>` (dépôt `erom-agence-seo`,
plugin `erom-seo`). Déduire le nom, l'annoncer, et laisser Romain corriger.

Demander aussi la **description en une phrase** si elle n'a pas été donnée :
elle part dans le manifeste, dans le README et dans le CLAUDE.md d'un seul
coup, et c'est elle qui décidera plus tard du déclenchement des skills.

### 2. Lancer le scaffold

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/scaffold/scripts/scaffold.sh" \
  <nom-plugin> [chemin] "<description>"
```

Le chemin vaut le répertoire courant par défaut. Le script est idempotent :
il n'écrase jamais un fichier existant, il annonce ce qu'il laisse en place.
Le relancer après coup est sans danger.

### 3. Personnaliser

Trois trous à combler, dans cet ordre d'importance :

1. `plugin/.claude-plugin/plugin.json` : `keywords` (vide au scaffold).
2. `CLAUDE.md` : les invariants du gabarit sont génériques. Ajouter ceux qui
   sont propres à ce plugin, et surtout la section « État actuel », qui est le
   seul endroit qui dit la vérité sur ce qui existe vraiment.
3. Les deux `README.md`, celui de la racine et celui de `plugin/` : le tableau des
   skills, à remplir au fur et à mesure dans les deux. L'image de tête du README
   racine est un placeholder tant que `/erom-dev-plugin:illustrate` n'a pas tourné.

### 4. Vérifier

```bash
claude --plugin-dir plugin plugin details <nom-plugin>
```

Affiche l'inventaire réel des composants chargés et le coût token projeté.
C'est la seule preuve que le manifeste charge ce qu'on croit. Un dossier
`skills/` ou `agents/` peuplé mais qui n'apparaît pas ici n'est pas chargé,
et le plugin ne fera rien une fois installé.

### 5. Commiter

```bash
git add -A && git status         # relire avant de valider
git commit -m "chore: scaffold du plugin <nom-plugin>"
```

## Publier dans la marketplace

Pas au scaffold : quand le plugin a au moins une skill qui tourne. Publier un
plugin vide met une entrée `strict: true` sur un dépôt sans composant, et le CI
de la marketplace valide alors dans le vide.

Le jour venu, ne rien éditer à la main : la skill `release` de ce plugin porte le
geste complet, lancée depuis le dépôt du plugin.

```
/erom-dev-plugin:release
```

Elle bumpe le manifeste et le README, commite et pousse le dépôt du plugin,
puis met à jour `~/dev/erom-marketplace` (entrée, metadata, README, et le
manifeste Codex `.agents/plugins/` s'il liste ce plugin) et vérifie la CI.
L'ordre plugin puis marketplace est structurel : l'entrée pointe `ref: main`
sur le dépôt du plugin.

Sur une première publication elle s'arrête et demande, parce que l'entrée à
créer réclame une description, une source `git-subdir` et un choix de `strict`.
Le CLAUDE.md scaffoldé porte déjà ce renvoi, section « Publication ».

## Pièges connus

| Piège | Ce qui se passe |
|---|---|
| `"agents": []` dans le manifeste | Zéro agent chargé, même avec `plugin/agents/` peuplé. La clé absente vaut découverte automatique. Vérifié le 27/08/2026 : `erom-devil` sans la clé charge ses 5 agents, un manifeste avec `[]` n'en charge aucun. |
| Liste explicite d'agents | Fonctionne, mais `claude plugin details` affiche « Agents (0) » alors qu'ils sont chargés (artefact d'affichage, constaté au renommage du 30/07/2026). Préférer la découverte automatique. |
| `_memory_/` entièrement gitignoré | `caserne onboard` inscrit le dépôt dans le vault RAG en indexant `README.md`, `docs/` et `_memory_/` depuis GitHub. Tout ignorer vide l'index. Seul `_memory_/ONBOARD.md` est exclu, parce qu'il porte les IDs Linear et Slack. |
| `plugin/.mcp.json` créé par réflexe | Un manifeste qui déclare un serveur MCP vers un chemin inexistant casse le plugin à l'installation. Ne créer ce fichier que quand un vrai serveur existe (`erom-marketing` a dû le supprimer le 07/08/2026 pour cette raison). |
| Nom du dépôt utilisé comme nom de plugin | `erom-agence-seo` est le dépôt, `erom-seo` est le plugin. Le manifeste porte le second, le champ `repository` porte le premier. |
