# Gabarit : carte de plugin au fusain

Style visuel validé par Romain le 25/08/2026 sur un lot de dix cartes projet, puis
repris ici pour les plugins Claude Code eRom.

Origine : Romain a testé sur NotebookLM le prompt « croquis d'un design automobile
au fusain » sur le projet erom-devil. Le modèle a rendu une voiture, ce qui n'était
pas voulu, mais l'ambiance était juste. Ce gabarit garde l'ambiance et remplace la
voiture par l'objet propre au plugin.

Ce qui a été refusé avant d'arriver là : une version au DS institut eRom (papier
crème, encre, bleu Souverain, filets). Verdict de Romain, « j'aime pas du tout, ni
le DS qui ne marche pas dans ce cas, ni en général ». Le DS institut est fait pour
des pages qu'on lit, pas pour une vignette qui doit accrocher l'œil dans une liste.

**Ce qui change par rapport au gabarit d'origine** (`EROM-HQ/emploi/projets/visuels/GABARIT.md`,
qui sert les cartes de candidature France Travail) : là-bas la carte plaide pour
Romain et la colonne de gauche raconte le problème métier. Ici la carte présente un
plugin sur GitHub, et tout son contenu vient de l'inventaire réel du plugin :
skills, agents, hooks, serveurs MCP. Le style et les règles dures sont communs, la
doctrine de contenu ne l'est pas.

---

## Réglages du tool

Serveur MCP `erom-image` (plugin), voir la skill `erom-image:gpt`.

| Paramètre | Valeur |
|---|---|
| tool | `mcp__plugin_erom-image_gpt__gpt_image_generate` |
| `size` | `1536x1024` (preset 3:2 paysage) |
| `quality` | `high` |
| `output_format` | `png` |
| `output_dir` | `<dépôt>/assets`, chemin absolu, toujours |

**Moteur : GPT Image, pas nanobanana.** Les deux ont été mis en concurrence sur le
même prompt le 25/08. Nanobanana rend une mise en page plus nette et un titre plus
massif, mais GPT Image dessine avec plus de matière, et le dessin est ce qui se
remplace le moins facilement. La mise en page, elle, se rattrape au prompt.

---

## D'où vient le contenu

Une seule source, la même que celle qui sert de preuve de chargement au dépôt :

```bash
claude --plugin-dir plugin plugin details <nom-plugin>
```

Elle donne l'inventaire réel (skills, agents, hooks, serveurs MCP, serveurs LSP) et
le coût token projeté. Rien de ce qui apparaît sur la carte ne s'invente : un
composant qui n'est pas dans cette sortie n'est pas chargé, donc n'existe pas pour
qui installe le plugin, donc n'a rien à faire sur la carte.

Compléter par la lecture des `SKILL.md` pour savoir ce que chaque skill fait, et du
manifeste pour la description et la version.

---

## Le gabarit

Emplacements à remplir, notés `{{...}}`. Tout le reste se recopie tel quel.

```
Planche d'infographie dessinée entièrement au fusain et au graphite sur papier
blanc légèrement grisé, dans le style d'une planche d'atelier de design
industriel : traits vifs et nerveux, hachures énergiques, traits de construction
laissés apparents, ombres estompées au doigt, quelques rehauts de gomme. Un
cadre au trait de fusain entoure toute la planche. Format paysage.

TOUS les textes ci-dessous doivent être rendus en français avec leurs accents
exacts, tels qu'ils sont écrits ici.

EN HAUT À GAUCHE, le titre "{{TITRE}}" en grosse typographie sans empattement
noire et grasse. Juste dessous, sur deux lignes en petit texte gris :
"{{SOUS_TITRE}}"

COLONNE DE GAUCHE, un tiers de la largeur, trois blocs empilés séparés par de
fins traits horizontaux. Chaque bloc associe un petit croquis technique au
fusain à gauche et un texte à droite.
Bloc 1, croquis {{CROQUIS_1}} : titre en gras "{{TITRE_1}}", puis en petit texte
"{{TEXTE_1}}"
Bloc 2, croquis {{CROQUIS_2}} : titre en gras "{{TITRE_2}}", puis en petit texte
"{{TEXTE_2}}"
Bloc 3, croquis {{CROQUIS_3}} : titre en gras "{{TITRE_3}}", puis en petit texte
"{{TEXTE_3}}"

PARTIE CENTRALE ET DROITE, le sujet principal, très grand : {{ECORCHE}}.
{{N}} étiquettes manuscrites reliées par de fines lignes de rappel avec petites
flèches pointent vers ces modules :
"{{LABEL_1}}" ; "{{LABEL_2}}" ; "{{LABEL_3}}" ; "{{LABEL_4}}" ; "{{LABEL_5}}".
Au-dessus de ce dessin, en petites capitales grasses : "SCHÉMA D'ARCHITECTURE".

EN BAS AU CENTRE, sous un titre en petites capitales grasses "{{TITRE_CHIFFRES}}",
trois chiffres très grands en noir, alignés horizontalement, séparés par de fins
filets verticaux, chacun suivi d'une courte légende : "{{N1}}" puis "{{LEG1}}" ;
"{{N2}}" puis "{{LEG2}}" ; "{{N3}}" puis "{{LEG3}}".

EN BAS À DROITE, sous un titre en petites capitales grasses "STACK TECHNIQUE",
un petit tableau à trois colonnes et quatre lignes, aux filets fins, ligne
d'en-tête sur fond gris foncé avec texte blanc. En-têtes : "Couche",
"Technologie", "Rôle". Ligne 1 : "{{C1}}", "{{T1}}", "{{R1}}". Ligne 2 :
"{{C2}}", "{{T2}}", "{{R2}}". Ligne 3 : "{{C3}}", "{{T3}}", "{{R3}}".

CONTRAINTES : rendu monochrome, uniquement des noirs, gris et blancs de fusain
et de graphite, aucune couleur. Tout le texte est net, parfaitement lisible,
horizontal, et orthographié exactement comme indiqué, accents français compris.
Mise en page dense mais organisée et aérée, comme une double page de magazine de
design. Les seuls objets représentés sont {{OBJET_UNIQUE}} et les trois petits
croquis techniques décrits ci-dessus. Aucune inscription, aucun mot gravé, aucun
numéro de série sur les plaques, formes, cartouches et flancs de machine : ces
surfaces restent vierges, seuls les textes donnés entre guillemets ci-dessus
apparaissent sur la planche. Aucun véhicule, aucune voiture dans le cadre.
```

---

## Comment remplir les emplacements

### `{{TITRE}}` et `{{SOUS_TITRE}}`

Le titre est le nom du plugin tel qu'il est dans le manifeste, en bas de casse :
`erom-devil`, pas « eRom Devil ». C'est le nom que les gens taperont pour
l'installer, il doit se lire tel quel.

Le sous-titre fait deux lignes courtes et dit ce que le plugin fait gagner, pas ce
qu'il contient. La liste des composants est ailleurs sur la carte, trois fois.

### `{{ECORCHE}}`, le choix qui fait ou casse la carte

Ce n'est jamais un diagramme de boîtes : c'est un objet physique, ouvert, dont les
organes internes portent les noms des composants du plugin. Quatre familles qui ont
marché, la dernière étant propre aux plugins :

| Famille | Quand | Exemple livré |
|---|---|---|
| L'atelier de machines | Le plugin fait travailler N moteurs sur un même objet | `erom-devil` : machine d'épreuve, cinq bras robotisés convergeant sur une pièce, un cadran de verdict |
| La chaîne de traitement | Le plugin est un pipeline à étapes | `erom-memory` : six stations en enfilade, une pièce qui avance |
| Le bloc moteur à tubulures | Le plugin est un hub avec N entrées | `trinity` : capot ouvert, six tubulures en éventail, un embout par canal |
| La coupe de bâtiment | Le plugin est une pile d'outillage autour de l'agent | `harnais-erom` : trois niveaux en coupe |

Pour un plugin, la question à se poser est : **quel objet un artisan ouvrirait pour
montrer comment ça marche ?** Un plugin de release ouvre un établi de tirage. Un
plugin d'orchestration ouvre un standard téléphonique. Un plugin de recherche ouvre
une table d'archiviste. Le mauvais réflexe est de dessiner un ordinateur ou un
écran : ça ne montre rien et ça ressemble à toutes les autres cartes.

### `{{LABEL_1}}` à `{{LABEL_5}}`, les composants réels

Une étiquette par composant de l'inventaire, dans l'ordre de lecture du dessin. Les
skills d'abord, puis les agents, puis les serveurs MCP. Le libellé est le nom réel
du composant, pas une paraphrase : quelqu'un doit pouvoir retrouver `release` dans
le dépôt après avoir vu la carte.

Cinq étiquettes est le maximum tenable. Au-delà, le modèle emmêle les lignes de
rappel et la carte devient illisible. Si le plugin a plus de cinq composants,
étiqueter les cinq qui décident de l'installation et laisser les autres au tableau
de la stack.

### Les trois blocs de gauche

Ils portent les trois capacités qui décident de l'installation, une par bloc. Titre
en gras : le nom de la skill. Texte : ce qu'elle fait faire, en deux ou trois lignes,
du point de vue de qui l'utilise et pas du point de vue du code.

Les `{{CROQUIS_n}}` sont des métaphores mécaniques de l'idée, jamais des captures
d'écran : un mécanisme à cliquet pour un automate qui interdit les raccourcis, un
cadenas en coupe pour du local-only, un jeu de poinçons pour un scaffold, une presse
à épreuve pour une porte de merge.

### Les trois chiffres

Ils viennent de l'inventaire et du coût token projeté. `{{TITRE_CHIFFRES}}` est
« PORTÉE DU SYSTÈME » par défaut, ou tout titre en deux mots qui dit ce que les
chiffres mesurent.

**Choisir des chiffres qui ne se comptent pas dans le dessin.** Un « 5 » en gros à
côté d'un objet à cinq bras invite le modèle à se tromper (voir règle 10). Le coût
token, un nombre de commandes, un nombre de dépôts servis, un zéro de dépendance :
tous sont sûrs parce qu'ils ne correspondent à rien de dénombrable sur la planche.

### La stack technique

Trois lignes, trois couches réelles. Pour un plugin, elles se lisent presque
toujours ainsi : ce qui distribue, ce qui exécute, ce qui sort. Exemple pour un
plugin de skills pures : `Distribution` / `Marketplace git-subdir` / `Installation
en une commande` ; `Composants` / `Skills Markdown` / `Aucune étape de build` ;
`Vérification` / `claude plugin details` / `Inventaire réel chargé`.

---

## Règles dures, apprises à la dure

1. **Écrire tous les accents dans le prompt.** Le premier jet a été dé-accenté par
   prudence : le modèle a rendu `arterielle`, `sante`, `Zero`, `SCHEMA`, et surtout
   `Le relève papier` au lieu de `Le relevé papier`, une vraie faute de sens. Le
   modèle recopie ce qu'on lui donne, il ne corrige pas.

2. **Un seul objet dessiné.** Nommer explicitement l'objet unique dans les
   contraintes, sinon le modèle peuple la planche.

3. **`Aucun véhicule, aucune voiture dans le cadre`** dès que le mot « moteur »
   apparaît dans le prompt. Le style vient du croquis automobile, la pente est
   naturelle.

4. **Vérifier le texte au crop avant de livrer**, en particulier les noms de
   composants et les en-têtes de tableau :
   `sips -c <h> <l> --cropOffset <y> <x> carte.png --out crop.png`

5. **Timeout : ne jamais relancer sans regarder le dossier.** Le tool répond
   `timed out after 60s` alors que le PNG est écrit ; un agent qui relance paie
   l'image deux fois. Toujours mettre cette consigne dans le prompt du sous-agent.

6. **Le fichier sort sans extension** quand `filename` est fourni nu. Le renommer en
   `.png` après coup.

7. **Le prompt est plafonné à 5000 caractères.** Le gabarit complet en consomme déjà
   3500 à 4500 ; ajouter des placements d'étiquettes détaillés fait sauter la limite
   (`Prompt must not exceed 5000 characters`, rencontré le 25/08 à 5267 caractères).
   Compter avant d'envoyer : `wc -m < prompt.txt`. Pour gagner de la place, tailler
   dans la description du style et dans les CONTRAINTES, jamais dans les textes
   entre guillemets ni dans les placements.

8. **Une flèche mal pointée se règle au placement, pas à l'édition.** Quand une
   étiquette désigne le mauvais élément, écrire dans le prompt, pour chaque
   étiquette, sa position ET sa cible, dans l'ordre vertical du dessin, plus la
   consigne qu'aucune ligne de rappel ne croise une autre. Retirer aussi du décor
   l'élément qui attirait la mauvaise flèche.

9. **Une lettre fautive ne se corrige pas par édition, elle se régénère.**
   `gpt_image_edit` préserve trop bien : il redessine fidèlement ce qui est là,
   artefact compris, et la consigne « garde tout identique » protège justement la
   faute. Mesuré le 25/08 sur `erom-memory` : le mot `SQLïte` a survécu à deux
   passes d'édition ciblées, dont une nommant explicitement le tréma. Une édition
   marche pour **remplacer un mot entier** ou **ajouter un élément** ; elle ne
   marche pas pour retoucher un glyphe. Dans ce cas, régénérer la planche complète
   en épelant le mot dans les CONTRAINTES. Le style est assez stable d'un tirage à
   l'autre pour que ce soit sans risque.

10. **Le modèle écrit juste et compte faux.** Lot du 28/08/2026, quatre planches en
    `1536x1024` `high` : les quatre ont rendu tous les textes français sans une
    seule faute d'accent, et deux sur quatre ont raté une quantité. Sept feuillets
    demandés, huit et plus dessinés ; un cadran gradué avec deux fois « 20 » et pas
    de « 10 ». Ne pas insister en redemandant le bon nombre : **supprimer le
    comptage**. Espacer les objets en une rangée unique dénombrable d'un coup d'œil
    plutôt qu'en éventail serré ; rendre muette toute surface graduée (« la couronne
    ne montre que de fins traits de graduation, la surface reste vierge, sans le
    moindre chiffre »). Corollaire dur : ne jamais afficher un nombre en gros à côté
    d'un objet dont on peut compter les éléments sans avoir vérifié ce compte au
    crop.

11. **Un composant absent de `claude plugin details` n'est pas chargé.** Une carte
    qui l'affiche ment à qui installe le plugin. C'est la seule faute de cette carte
    qui ne se voit pas à l'œil et qui se paie en confiance.

12. **Le modèle grave du texte non demandé sur les surfaces planes.** Même
    mécanisme que la règle 10, appliqué aux lettres au lieu des chiffres : une
    plaque, une forme, un cartouche, un flanc de machine appellent une inscription,
    et le modèle l'invente. Constaté le 28/08/2026 sur la carte `erom-dev-plugin` :
    la plaque du croquis `illustrate` porte « PLUG-IN INVENTAIRE » et la forme de la
    presse « SKILL MANIFESTE », deux chaînes de franglais bancal que personne n'a
    demandées. Aucun texte commandé n'était fautif sur ce même tirage. Correctif :
    ajouter aux CONTRAINTES que les surfaces inscriptibles du dessin restent
    muettes, sauf celles dont le texte est donné entre guillemets. Formulation qui
    marche : « aucune inscription, aucun mot gravé, aucun numéro de série sur les
    plaques, formes, cartouches et flancs de machine ; ces surfaces restent
    vierges ». Une chaîne inventée sur du décor est un défaut mineur : ne pas
    régénérer une planche par ailleurs juste pour ça, mais mettre la contrainte dès
    le premier tirage puisqu'elle est gratuite.

---

## Procédure

1. Lire l'inventaire réel avec `claude --plugin-dir plugin plugin details <nom>`.
2. Écrire le prompt complet depuis le gabarit, tous accents en place, dans un
   fichier. Compter les caractères.
3. Déléguer à un sous-agent `general-purpose` (obligatoire, la skill `erom-image:gpt`
   interdit l'appel direct du tool) avec le garde-fou timeout.
4. Renommer le fichier produit en `.png`.
5. Relire l'image, vérifier chaque chaîne de texte, cropper les zones denses, et
   compter ce qui est dénombrable.
6. Corriger une faute isolée avec `gpt_image_edit` plutôt que régénérer : une seule
   modification par appel, `size` explicite, et lister tout ce qui doit rester
   identique.

---

## Références

- Skill du moteur : `erom-image:gpt`
- Gabarit d'origine et ses dix cartes : `~/dev/EROM-HQ/emploi/projets/visuels/`
