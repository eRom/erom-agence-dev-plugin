---
name: illustrate
description: "Dessine la carte de présentation d'un plugin Claude Code eRom : une planche au fusain en 1536x1024, générée par GPT Image, dont tout le contenu vient de l'inventaire réel du plugin (skills, agents, hooks, serveurs MCP). Sort dans assets/, destinée au README GitHub. Commande explicite, lancée au slash : /erom-dev-plugin:illustrate."
user-invocable: true
disable-model-invocation: true
---

# illustrate

Une carte de plugin au fusain, format paysage, pour le README GitHub du dépôt.
Le style est figé et validé, il ne se rediscute pas : c'est le contenu qui se
travaille, et il vient entièrement de ce que le plugin charge vraiment.

Cible : le plugin du dépôt courant, ou celui nommé en argument.

```
$ARGUMENTS
```

## 0. La racine du plugin

`GABARIT` = `${CLAUDE_PLUGIN_ROOT}/skills/illustrate/references/GABARIT.md`. C'est un
chemin absolu : recopie-le littéralement, ne le reconstruis pas depuis le répertoire
courant, qui est le dépôt à illustrer et pas celui de cette skill. Si
`${CLAUDE_PLUGIN_ROOT}` te parvient non expansé, résous-le : deux niveaux au-dessus
du « Base directory for this skill » injecté ci-dessus.

## 1. Lire l'inventaire réel

```bash
MANIFEST="plugin/.claude-plugin/plugin.json"
[ -f "$MANIFEST" ] || MANIFEST=".claude-plugin/plugin.json"
NOM="$(jq -r .name "$MANIFEST")"

claude --plugin-dir "$(dirname "$(dirname "$MANIFEST")")" plugin details "$NOM"
jq -r '.description, .version' "$MANIFEST"
```

C'est la seule source de la carte. Un composant absent de cette sortie n'est pas
chargé : il ne va pas sur la planche, même s'il existe sur le disque. Cette sortie
donne aussi le coût token projeté, qui fournit un des trois chiffres.

Puis lire les `SKILL.md` des skills listées pour savoir ce que chacune fait faire.
Sans ça, les trois blocs de gauche sortent génériques, et une carte générique ne
vaut pas son prix.

## 2. Écrire le prompt

Lire `GABARIT` en entier avant d'écrire une ligne : il porte le gabarit exact à
recopier, la façon de choisir l'écorché, et onze règles dures qui sont chacune une
image ratée qu'on ne repaiera pas.

Écrire le prompt rempli dans un fichier, puis compter :

```bash
wc -m < /tmp/prompt-carte.txt     # doit rester sous 5000
```

Trois pièges qui coûtent une image entière, détaillés dans le gabarit :

- **Tous les accents en place.** Le modèle recopie, il ne corrige pas.
- **Aucun gros chiffre dénombrable dans le dessin.** Un « 3 » à côté de trois
  modules dessinés se rate une fois sur deux.
- **Un seul objet.** Nommer l'objet unique dans les CONTRAINTES, sinon la planche
  se peuple toute seule.
- **Aucune surface inscriptible laissée libre.** Plaques, formes et cartouches
  appellent une inscription et le modèle l'invente, en franglais bancal.

Relire le prompt écrit avant de l'envoyer, en particulier les chaînes entre
guillemets. Une image coûte environ 0,30 $ en `high` à cette taille, et une faute
de frappe dans une étiquette se repaie en planche entière : l'édition ne sait pas
corriger une lettre.

## 3. Générer

**Préflight, avant de payer un sous-agent.** Le plugin `erom-image` doit être actif
dans la session, sinon ses tools MCP n'existent pour personne, sous-agent compris :

```bash
jq -r '.enabledPlugins | keys[]' .claude/settings.local.json | grep erom-image
claude mcp list | grep 'erom-image:gpt'      # doit dire ✔ Connected
```

Si l'entrée manque dans `settings.local.json`, l'ajouter. Si elle y est mais que le
tool reste introuvable, la session a été lancée avant : `/reload-plugins`. Vérifié le
28/08/2026 sur ce dépôt : `erom-image@erom-marketplace` était bien activé et les deux
serveurs répondaient `✔ Connected` au CLI, mais le sous-agent ne voyait aucun tool
`mcp__plugin_erom-image_*`. Il a brûlé 92 k tokens à chercher avant d'abandonner, et
`/reload-plugins` a suffi. Ne jamais laisser un sous-agent diagnostiquer ça.

Appel obligatoirement délégué : la skill `erom-image:gpt` interdit d'appeler ses
tools MCP depuis le contexte principal.

Déléguer à un sous-agent `general-purpose`, en lui donnant le chemin du fichier de
prompt plutôt que le prompt recopié, et ces paramètres :

| Paramètre | Valeur |
|---|---|
| tool | `mcp__plugin_erom-image_gpt__gpt_image_generate` |
| `size` | `1536x1024` |
| `quality` | `high` |
| `output_format` | `png` |
| `output_dir` | `<dépôt>/assets`, en absolu |
| `filename` | le nom du plugin |

Consigne à mettre mot pour mot dans le prompt du sous-agent :

> Si le tool répond `timed out after 60s`, ne relance pas. Liste le dossier de
> sortie : le fichier est presque toujours écrit malgré le timeout. Un relancement
> paie l'image deux fois.

Le sous-agent ne remonte que le chemin du fichier, jamais le bloc de réponse entier.

## 4. Vérifier avant de montrer

```bash
mv assets/<nom> assets/<nom>.png        # le fichier sort sans extension
sips -g pixelWidth -g pixelHeight assets/<nom>.png
```

Puis regarder l'image, et vérifier dans cet ordre :

1. **Chaque chaîne de texte**, caractère par caractère, accents compris. Cropper les
   zones denses : le tableau de la stack et les étiquettes de l'écorché.
   `sips -c <h> <l> --cropOffset <y> <x> assets/<nom>.png --out /tmp/crop.png`
2. **Les noms de composants** correspondent à l'inventaire de l'étape 1.
3. **Ce qui est dénombrable** : compter les modules dessinés et les comparer aux
   chiffres affichés.

Une faute isolée se corrige par `gpt_image_edit` si c'est un mot entier à remplacer
ou un élément à ajouter. Une lettre fautive dans un mot se régénère : l'édition
préserve l'artefact au lieu de le corriger, vérifié le 25/08 sur `SQLïte` qui a
survécu à deux passes ciblées.

## 5. Livrer

Annoncer le chemin, les dimensions, et ce qui a été vérifié au crop. Si un défaut
subsiste et qu'il ne vaut pas une régénération, le dire plutôt que le laisser
découvrir.

La ligne à ajouter au README du dépôt :

```markdown
![<nom du plugin>](assets/<nom>.png)
```

## Garde-fous

- **Le style ne se rediscute pas.** Il a été choisi contre une version au DS
  institut, explicitement rejetée. Ne propose pas de variante de style, propose des
  variantes d'écorché.
- **Rien ne s'invente sur la carte.** Chaque nom, chaque chiffre se retrace à la
  sortie de `claude plugin details` ou à un `SKILL.md`. Une carte qui affiche un
  composant non chargé ment à qui installe le plugin, et c'est la seule faute qui ne
  se voit pas à l'œil.
- **Une génération par validation.** Ne pas enchaîner deux tirages pour comparer
  sans que Romain l'ait demandé : à ce format et en `high`, chaque essai se paie.
