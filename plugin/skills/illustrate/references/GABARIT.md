# Gabarit : carte de plugin au fusain

Style visuel validé par Romain le 25/08/2026 sur un lot de dix cartes projet, repris
ici pour les plugins Claude Code eRom, puis refondu le 29/08/2026 : le gabarit à
trous d'origine dictait la mise en page mot pour mot, et toutes les cartes sortaient
identiques (voir règle 13).

Origine : Romain a testé sur NotebookLM le prompt « croquis d'un design automobile
au fusain » sur le projet erom-devil. Le modèle a rendu une voiture, ce qui n'était
pas voulu, mais l'ambiance était juste. Ce gabarit garde l'ambiance.

Ce qui a été refusé avant d'arriver là : une version au DS institut eRom (papier
crème, encre, bleu Souverain, filets). Verdict de Romain, « j'aime pas du tout, ni
le DS qui ne marche pas dans ce cas, ni en général ». Le DS institut est fait pour
des pages qu'on lit, pas pour une vignette qui doit accrocher l'œil dans une liste.

**Ce qui est figé et ce qui est libre.** Trois blocs sont validés mot pour mot et
se recopient tels quels : le STYLE, le TITRE avec son sous-titre, les CONTRAINTES.
Tout ce qui est entre les deux, la scène, s'écrit pour chaque plugin, à partir de
ce qu'il résout. Aucune mise en page n'est imposée : ni colonne, ni tableau, ni
rangée de chiffres, ni écorché obligatoire. Le style ne se rediscute pas, la
composition se réinvente à chaque carte.

---

## Réglages du tool

Serveur MCP `erom-image` (plugin), voir la skill `erom-image:gpt`.

| Paramètre | Valeur |
|---|---|
| tool | `mcp__plugin_erom-image_gpt__gpt_image_generate` |
| `size` | `1536x1024` (preset 3:2 paysage) |
| `quality` | `low` pour le brouillon de composition (environ 0,01 $), `high` pour le tirage (environ 0,30 $) |
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

Elle donne l'inventaire réel : skills, agents, hooks, serveurs MCP, serveurs LSP.
Rien de ce qui apparaît sur la carte ne s'invente : un composant qui n'est pas
dans cette sortie n'est pas chargé, donc n'existe pas pour qui installe le plugin,
donc n'a rien à faire sur la carte. Et tout ce qui y est va sur la carte, sous son
vrai nom. Le coût token projeté, lui, n'y va plus : il ne dit rien de ce que le
plugin résout.

Compléter par la lecture des `SKILL.md` et des fichiers d'agents pour savoir ce que
chaque composant fait faire, et du manifeste pour la description et la version.

---

## Le gabarit

Trois blocs figés, recopiés tels quels. Un seul emplacement libre, `{{SCÈNE}}`,
écrit pour le plugin. `{{TITRE}}` et `{{SOUS_TITRE}}` se remplissent comme dit
plus bas.

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

{{SCÈNE}}

CONTRAINTES :
- rendu monochrome, uniquement des noirs, gris et blancs de fusain et de graphite, aucune couleur.
- Tout le texte est net, parfaitement lisible, horizontal, et orthographié exactement comme indiqué, accents français compris.
- Mise en page dense mais organisée et aérée, comme une double page de magazine de design.
- Pas de publicité déguisée, aucun nom de marque.
- Aucun véhicule, aucune voiture dans le cadre.
```

---

## `{{TITRE}}` et `{{SOUS_TITRE}}`

Le titre est le nom du plugin tel qu'il est dans le manifeste, en bas de casse :
`erom-devil`, pas « eRom Devil ». C'est le nom que les gens taperont pour
l'installer, il doit se lire tel quel.

Le sous-titre fait deux lignes courtes et dit ce que le plugin fait gagner, pas ce
qu'il contient. La liste des composants est dans la scène.

---

## `{{SCÈNE}}`, ce qui fait la carte

### 1. La note de composition, avant le prompt

Quatre lignes, écrites dans la réponse avant d'ouvrir le fichier de prompt, pour que
Romain voie d'où vient la scène :

- **Résout :** une phrase. Ce que le plugin rend possible, ou ce qu'on arrête de
  faire à la main. Dérivée de l'inventaire et des `SKILL.md`, pas recopiée du
  manifeste.
- **Geste :** ce que fait l'utilisateur. Les commandes, dans leur ordre s'il y en
  a un.
- **Registre et objet :** lequel des registres ci-dessous, quel objet ou quelle
  scène, et en une demi-ligne pourquoi ça découle de « Résout ».
- **À ne pas répéter :** la composition des cartes déjà livrées (table ci-dessous)
  et, s'il existe déjà une carte de ce plugin dans `assets/`, la sienne.

C'est cette note qui décide de la planche. Un prompt écrit sans elle retombe sur
la machine posée sur un établi, comme les deux premières cartes.

### 2. Choisir le registre

La question à se poser : **quel dessin un artisan ferait-il pour montrer ce que ce
plugin résout ?** Un plugin de release ouvre un établi de tirage, un plugin
d'orchestration ouvre un standard téléphonique, un plugin de recherche ouvre une
table d'archiviste. Sept registres, qui sont sept grammaires de dessin d'atelier :

| Registre | Ce qu'il raconte | Convient quand |
|---|---|---|
| La séquence | Un même objet à plusieurs stades, de gauche à droite, sur une même ligne de sol | Le plugin est un cycle ou un enchaînement de gestes |
| L'écorché | Un objet ouvert, ses organes nommés par des lignes de rappel | Le plugin est un mécanisme qui travaille une pièce |
| La vue éclatée | Un objet démonté, ses pièces flottant alignées, chacune nommée | Le plugin est un assemblage de parties indépendantes |
| Le plan | Une pièce ou un atelier vus d'en haut, les postes nommés | Le plugin organise des acteurs autour d'un travail |
| La coupe | Un bâtiment ou un vaisseau ouvert niveau par niveau | Le plugin empile des couches autour de l'agent |
| Le mur d'outils | Des outils accrochés, chacun à sa silhouette et à son nom | Le plugin est une boîte à outils sans ordre imposé |
| L'avant-après | Deux états d'un même sujet, côte à côte | Le plugin transforme un état en un autre |

Le registre découle de « Résout », jamais de l'ordre de cette table. Deux plugins
dans le même registre, c'est acceptable si les objets diffèrent ; le même objet deux
fois, non.

**Cartes déjà livrées, à ne pas répéter.** Ajouter une ligne après chaque tirage
livré.

| Plugin | Registre | Objet | Date |
|---|---|---|---|
| `erom-devil` 0.9 | écorché | machine d'épreuve, cinq bras robotisés sur une pièce, cadran de verdict | 08/2026 |
| `erom-dev-plugin` 0.1 | écorché | presse à imprimer à manivelle | 28/08/2026 |
| `erom-dev-plugin` 0.1.4 | séquence | une caisse en bois à trois stades, ossature, fermée, cerclée vers l'étagère | 29/08/2026 |
| `erom-memory` | séquence | six stations en enfilade, une pièce qui avance | 25/08/2026 |
| `trinity` | écorché | bloc moteur, capot ouvert, six tubulures en éventail | 25/08/2026 |
| `harnais-erom` | coupe | bâtiment à trois niveaux | 25/08/2026 |
| `erom-seo` 0.1 | plan | atelier de cartographie en plongée, quatre postes en boucle autour d'une carte, lunette à l'écart | 30/08/2026 |
| `erom-vision` 0.1 | plan | poste de contrôle qualité en plongée, marbre, épreuves étiquetées par état, calibres passe / ne passe pas, tampon PASS FAIL | 05/09/2026 |

Le mauvais réflexe : dessiner un ordinateur, un écran, un terminal. Ça ne montre
rien et ça ressemble à toutes les autres cartes.

### 3. Placer tous les composants

Tous les composants de l'inventaire vont sur la carte, par leur nom réel, tel qu'on
le retrouve dans le dépôt : `release`, pas « publication ». Ils se groupent par
famille, skills, agents, hooks, serveurs MCP, et la famille se nomme en petites
capitales quand ça aide la lecture (un plugin qui n'a que des skills n'a pas besoin
de l'écrire).

Quand une famille est nombreuse, une seule zone de texte porte tous ses noms :
« gemini, glm, deepseek, opus, kimi » dans un cartouche a bien rendu sur la carte
`erom-devil` ; treize étiquettes éparpillées ne rendraient pas. Compter au plus une
dizaine de zones de texte en plus du titre.

Pour chaque zone, écrire sa position ET ce qu'elle désigne, dans l'ordre de lecture
du dessin (règle 8). Une skill peut porter sous son nom un petit texte gris qui dit
ce qu'elle fait faire, du point de vue de qui l'utilise ; deux lignes, pas un
paragraphe.

### 4. Ce que la scène ne contient pas

- **L'ancien squelette** : colonne de gauche à trois blocs, rangée de grands
  chiffres, tableau à en-têtes, mentions « SCHÉMA D'ARCHITECTURE », « PORTÉE DU
  SYSTÈME », « STACK TECHNIQUE ». Deux cartes sont sorties identiques à cause de
  lui.
- **Un nombre à côté de quelque chose qui se compte** (règle 10). Rien ne se
  compte sur la carte : ni « 3 skills », ni coût token. Les positions se disent
  à gauche, au centre, à droite, pas « trois ».
- **Un ordinateur, un écran, un terminal, un logo.**
- **Un élément non nommé.** La scène se termine par la phrase qui ferme la porte :
  « seuls les textes entre guillemets ci-dessus apparaissent sur la planche, et
  rien d'autre n'est dessiné », précédée de la liste des surfaces qui restent
  vierges (règle 12).
- Un personnage ou une main ne sont pas interdits, mais rarement utiles : c'est une
  planche d'atelier, pas une bande dessinée.

### 5. Exemple : la scène de `erom-dev-plugin`, 29/08/2026

Note de composition :

- Résout : monter, illustrer et publier un plugin Claude Code sans refaire les
  gestes à la main, du dépôt vide à la marketplace.
- Geste : trois commandes, dans l'ordre du cycle : scaffold, illustrate, release.
- Registre et objet : la séquence, une même caisse de bois à trois stades de
  fabrication. Le plugin est un cycle, la planche montre un cycle.
- À ne pas répéter : la presse à imprimer de la carte 0.1 (écorché).

Scène envoyée :

```
LE RESTE DE LA PLANCHE, sous le titre et sur toute la largeur : une même caisse
en bois dessinée trois fois de gauche à droite, à trois stades de fabrication,
comme sur une planche de suivi de prototype. Les trois dessins ont la même
taille, posés sur une même ligne de sol tracée au fusain, espacés régulièrement.
À GAUCHE, premier stade : la caisse n'est encore qu'une ossature, des montants
et des traverses assemblés à tenons, une équerre de menuisier appuyée contre,
un maillet posé au sol. Sous ce dessin, l'étiquette manuscrite "scaffold", puis
en petit texte gris : "monte la structure du dépôt, sans rien écraser".
AU CENTRE, deuxième stade : la caisse est fermée de planches ; sur sa face
avant est épinglée une feuille de croquis à peine esquissée ; un bâton de fusain
et une loupe sont posés devant. Sous ce dessin, l'étiquette manuscrite
"illustrate", puis en petit texte gris : "dessine la carte du plugin depuis son
inventaire réel".
À DROITE, troisième stade : la caisse est cerclée de feuillard, un cachet de
cire rond sur le couvercle, et elle glisse sur une courte rampe vers une étagère
de boutique. Sous ce dessin, l'étiquette manuscrite "release", puis en petit
texte gris : "publie la version, le plugin d'abord, la marketplace ensuite".
Une longue flèche fine au fusain court sous les trois dessins, de gauche à
droite ; à son départ, à gauche, le petit texte "dépôt vide" ; à son arrivée, à
droite, le petit texte "marketplace".
Les planches, le couvercle, le cachet et l'étagère restent vierges de toute
inscription ; seuls les textes entre guillemets ci-dessus apparaissent sur la
planche, et rien d'autre n'est dessiné.
```

Brouillon en `low` conforme du premier coup : trois caisses sur une ligne de sol,
trois étiquettes, la flèche de « dépôt vide » à « marketplace », aucun texte
inventé.

### 6. Second exemple, note seule : `erom-devil`, brouillon du 29/08/2026

Même journée, même doctrine, pour prouver que deux plugins donnent deux planches :

- Résout : faire critiquer un travail (brainstorming, spec, code, merge) par cinq
  modèles externes qui jugent et n'écrivent jamais dans le dépôt.
- Geste : soumettre la pièce à un devil au choix, ou à tous d'un coup (`-swarm`).
- Registre et objet : le plan, une table de délibération ronde vue en plongée,
  cinq fauteuils vides avec un chevalet nominatif chacun (les agents), un casier
  de tri à deux rangées de quatre cases (les huit skills), un tampon « GO / NO-GO ».
  Le plugin organise des juges autour d'une pièce, la planche montre une salle
  de délibération.
- À ne pas répéter : la machine d'épreuve à cinq bras de la carte 0.9 (écorché).

Sorti conforme en `low` : cinq fauteuils, cinq noms dans l'ordre horaire demandé,
huit cases nommées, les deux familles en petites capitales.

---

## Règles dures, apprises à la dure

1. **Écrire tous les accents dans le prompt.** Le premier jet a été dé-accenté par
   prudence : le modèle a rendu `arterielle`, `sante`, `Zero`, `SCHEMA`, et surtout
   `Le relève papier` au lieu de `Le relevé papier`, une vraie faute de sens. Le
   modèle recopie ce qu'on lui donne, il ne corrige pas.

2. **Tout ce qui est dessiné est nommé dans le prompt.** Sans la phrase de clôture
   (« rien d'autre n'est dessiné »), le modèle peuple la planche d'objets de son
   cru. Dire l'état positif voulu plutôt qu'une négation seule.

3. **`Aucun véhicule, aucune voiture dans le cadre`** dès que le mot « moteur »
   apparaît dans le prompt. Le style vient du croquis automobile, la pente est
   naturelle. La ligne est dans les CONTRAINTES figées.

4. **Vérifier le texte au crop avant de livrer**, en particulier les noms de
   composants et les zones denses :
   `sips -c <h> <l> --cropOffset <y> <x> carte.png --out crop.png`

5. **Timeout : ne jamais relancer sans regarder le dossier.** Le tool répond
   `timed out after 60s` alors que le PNG est écrit ; un agent qui relance paie
   l'image deux fois. Toujours mettre cette consigne dans le prompt du sous-agent.

6. **Le fichier sort sans extension** quand `filename` est fourni nu. Le renommer en
   `.png` après coup.

7. **Le prompt est plafonné à 5000 caractères.** Les blocs figés en consomment
   environ 1300 ; la scène dispose du reste. Ajouter des placements d'étiquettes
   détaillés fait vite sauter la limite (`Prompt must not exceed 5000 characters`,
   rencontré le 25/08 à 5267 caractères). Compter avant d'envoyer :
   `wc -m < prompt.txt`. Pour gagner de la place, tailler dans les descriptions
   d'objets, jamais dans les textes entre guillemets ni dans les placements.

8. **Une flèche mal pointée se règle au placement, pas à l'édition.** Quand une
   étiquette désigne le mauvais élément, écrire dans le prompt, pour chaque
   étiquette, sa position ET sa cible, dans l'ordre de lecture du dessin, plus la
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
    moindre chiffre »). Corollaire dur : ne jamais afficher un nombre à côté d'un
    objet dont on peut compter les éléments.

11. **Un composant absent de `claude plugin details` n'est pas chargé.** Une carte
    qui l'affiche ment à qui installe le plugin. C'est la seule faute de cette carte
    qui ne se voit pas à l'œil et qui se paie en confiance.

12. **Le modèle grave du texte non demandé sur les surfaces planes.** Même
    mécanisme que la règle 10, appliqué aux lettres au lieu des chiffres : une
    plaque, une forme, un cartouche, un flanc de machine appellent une inscription,
    et le modèle l'invente. Constaté le 28/08/2026 sur la carte `erom-dev-plugin` :
    la plaque du croquis `illustrate` portait « PLUG-IN INVENTAIRE » et la forme de
    la presse « SKILL MANIFESTE », deux chaînes de franglais bancal que personne
    n'avait demandées. Correctif : la scène nomme ses surfaces inscriptibles et dit
    qu'elles restent vierges. Formulation qui marche : « les planches, le couvercle
    et l'étagère restent vierges de toute inscription ; seuls les textes entre
    guillemets ci-dessus apparaissent ». Une chaîne inventée sur du décor est un
    défaut mineur : ne pas régénérer une planche par ailleurs juste pour ça, mais
    mettre la phrase dès le premier tirage puisqu'elle est gratuite.

13. **Le gabarit à trous produit la même planche à chaque fois.** Constaté le
    29/08/2026 sur `erom-devil` et `erom-dev-plugin`, deux plugins sans rapport :
    même colonne de gauche à trois blocs, même machine au centre, même rangée de
    chiffres et même tableau en bas, parce que le prompt les dictait mot pour mot.
    Le modèle obéit, il ne varie pas. La composition se dérive de ce que le plugin
    résout, elle ne se recopie pas d'un gabarit. Corollaires : la note de
    composition s'écrit avant le prompt, la table des cartes livrées se consulte,
    et le brouillon en `low` sert à vérifier que le prompt ne retombe pas dans le
    squelette avant de payer le tirage.

---

## Procédure

1. Lire l'inventaire réel avec `claude --plugin-dir plugin plugin details <nom>`,
   puis les `SKILL.md` et les fichiers d'agents.
2. Écrire la note de composition dans la réponse : Résout, Geste, Registre et
   objet, À ne pas répéter.
3. Écrire le prompt complet, blocs figés recopiés, scène écrite pour ce plugin, tous
   accents en place, dans un fichier. Compter les caractères.
4. Brouillon en `low` par un sous-agent `general-purpose` (obligatoire, la skill
   `erom-image:gpt` interdit l'appel direct du tool). Regarder la composition
   seulement : conforme à la note, hors du squelette, toutes les zones de noms
   présentes. Sinon corriger le prompt et refaire un brouillon. Ni le texte ni le
   trait ne se jugent à ce stade.
5. Tirage en `high`, même sous-agent, même prompt, avec le garde-fou timeout.
6. Renommer le fichier produit en `.png`.
7. Relire l'image, vérifier chaque chaîne de texte, cropper les zones denses, et
   compter ce qui est dénombrable.
8. Corriger une faute isolée avec `gpt_image_edit` plutôt que régénérer : une seule
   modification par appel, `size` explicite, et lister tout ce qui doit rester
   identique.
9. Ajouter la carte à la table des cartes livrées.

---

## Références

- Skill du moteur : `erom-image:gpt`
- Gabarit d'origine et ses dix cartes : `~/dev/EROM-HQ/emploi/projets/visuels/`
