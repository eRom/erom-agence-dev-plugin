# Gotchas

Dernière mise à jour : 2026-08-28

## `render()` détruit tout fichier binaire

`scaffold.sh:render()` fait `content="$(cat "$src")"` pour substituer les
`{{...}}`. La substitution de commande supprime les octets NUL. Un PNG de
21993 octets est ressorti à 18237, `file` le voyant comme `data` au lieu de
`PNG image data`, et `sips` ne lisant plus ses dimensions.

Correctif en place : fonction `copy()`, un `cp` avec la même idempotence et le
même comptage. Tout nouveau gabarit binaire passe par elle.

Re-vérifier : lancer le scaffold dans un dossier jetable, puis
`cmp references/plugin.png <cible>/assets/plugin.png`.

## `set -euo pipefail` fait mourir le scaffold en silence

Une ligne `render "$REFS/<fichier absent>"` tue le script au milieu du rendu, avec
les seuls fichiers déjà écrits en place. Constaté le 28/08/2026 : une ligne
rendait `GABARIT.md`, absent de `references/`, et le dépôt sortait avec 2 fichiers
sur 7, sans que rien n'annonce l'échec autrement qu'un `exit 1`.

Toujours vérifier le compte final, pas seulement le code de sortie.

## Un sous-agent ne voit pas les tools MCP d'un plugin non rechargé

Le 28/08/2026, un sous-agent `general-purpose` n'avait aucun tool
`mcp__plugin_erom-image_*`, alors que `erom-image@erom-marketplace` était bien
dans `.claude/settings.local.json` et que `claude mcp list` répondait
`✔ Connected` pour les deux serveurs. La session avait été lancée avant
l'activation. Le sous-agent a brûlé 92 k tokens à diagnostiquer avant d'abandonner.

`/reload-plugins` a suffi. Faire le préflight côté session principale, jamais
laisser un sous-agent chercher un tool qu'on ne lui a pas donné.

## `git-subdir` ne remonte pas ce qui est hors de `path`

Le paquet installé ne contient que le contenu de `plugin/`. Un
`![](../assets/x.png)` dans `plugin/README.md` résout sur la page GitHub et casse
dans le cache d'installation. Vérifié en listant
`~/.claude/plugins/cache/erom-marketplace/erom-dev-plugin/<version>/` : ni
`assets/`, ni quoi que ce soit hors `plugin/`.

## GPT Image grave du texte que personne n'a demandé

Sur le tirage du 28/08/2026 en `1536x1024` `high` : la plaque du croquis
`illustrate` portait « PLUG-IN INVENTAIRE » et la forme de la presse
« SKILL MANIFESTE », deux chaînes de franglais inventées. Aucun texte commandé
n'était fautif sur le même tirage.

Même mécanisme que le comptage faux, appliqué aux lettres : une surface plane
appelle une inscription. Correctif, désormais dans le bloc CONTRAINTES du
`GABARIT.md` : « aucune inscription, aucun mot gravé, aucun numéro de série sur
les plaques, formes, cartouches et flancs de machine ; ces surfaces restent
vierges ». **Non encore éprouvé sur un tirage**, le prochain le validera ou
l'infirmera.

## `claude plugin update` ment sur les installations locales

Repris de la skill `release`, incident du 15/08/2026 sur `erom-research` : les
installations sont enregistrées par scope ET par répertoire dans
`~/.claude/plugins/installed_plugins.json`. Sans flag, la commande ne touche que
le scope user et répond « already at latest » même quand des enregistrements
locaux restent en arrière.

Sur ce plugin, un seul enregistrement, scope user : le piège n'a pas encore mordu
ici.

## Le fichier de GPT Image sort sans extension

Quand `filename` est fourni nu, le PNG arrive sans `.png`. Le renommer après coup.
Et sur un `timed out after 60s`, ne jamais relancer avant d'avoir listé le dossier
de sortie : le fichier est presque toujours écrit malgré le timeout, un
relancement paie l'image deux fois.
