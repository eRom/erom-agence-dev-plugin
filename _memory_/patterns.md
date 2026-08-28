# Patterns

Dernière mise à jour : 2026-08-28

## Chemins dans une skill distribuée

Jamais `~/.claude/skills/...` : une skill distribuée ne peut pas dépendre du
répertoire personnel de qui l'installe. Toujours `${CLAUDE_PLUGIN_ROOT}`.

Chaque skill qui appelle un script porte une section « 0. La racine du plugin »
en tête de sa procédure, sur ce moule :

> `NOM` = `${CLAUDE_PLUGIN_ROOT}/skills/<skill>/scripts/<fichier>`. C'est un chemin
> absolu : recopie-le littéralement, ne le reconstruis pas depuis le répertoire
> courant, qui est le dépôt cible et pas celui de cette skill. Si
> `${CLAUDE_PLUGIN_ROOT}` te parvient non expansé, résous-le : deux niveaux
> au-dessus du « Base directory for this skill » injecté ci-dessus.

Convention reprise de `erom-gemini` et `erom-research`, qui la portaient déjà.

## Frontmatter des skills

Les trois skills sont des commandes explicites :

```yaml
user-invocable: true
disable-model-invocation: true
```

Description en français, se terminant par l'invocation réelle
(`/erom-dev-plugin:<skill>`), jamais par le nom d'une skill personnelle.

## Deux README

Racine avec image, `plugin/` sans. Voir `architecture.md` pour le pourquoi
structurel. Le tableau des skills est à remplir dans les deux.

## Conventions de commit

Dépôt du plugin :

```
<type>(<portée>): <résumé> (<nouvelle version>)

Pourquoi le changement existe, et ce qu'il change pour qui l'utilise.
Les faits vérifiés : ce qui a été testé, mesuré, reproduit.
```

Marketplace : `chore(marketplace): <plugin> <version> (<ce qui change>), metadata <version>`.

Chaque affirmation du corps doit être traçable au `git diff --cached`. Les deux
commits portent `Co-Authored-By` et `Claude-Session`.

## Bump de version

SemVer sur ce que le diff fait réellement. `metadata.version` de la marketplace se
bump **au même niveau que le plugin** : patch pour patch, mineur pour mineur.
Vérifié sur l'historique (`erom-devil 0.8.1` vers `metadata 0.22.1`,
`erom-insight 0.6.0` vers `metadata 0.22.0`).

## Toute règle est ancrée

Chaque consigne des skills se rattache à un artefact réel : une sortie observée,
un test qui passe, un incident daté. Les règles dures du `GABARIT.md` citent leur
date et leur mesure. Une règle sans incident derrière elle ne s'écrit pas.

## Vérification

`claude --plugin-dir plugin plugin details <nom>` est la seule preuve que le
manifeste charge ce qu'on croit. Un dossier `skills/` peuplé mais invisible ici
n'est pas chargé.

Pour un script, la preuve est de le faire tourner dans un dossier jetable créé par
`mktemp -d` sous le scratchpad, jamais un `rm -rf` de préparation.
