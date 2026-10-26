---
name: suno-song
description: Créer le style et/ou les paroles d'un morceau Suno puis remplir le formulaire via fill.py. À utiliser dès que l'utilisateur veut créer une musique, un style musical ou des paroles (lyrics) pour Suno. Commence TOUJOURS par un questionnaire exhaustif pour cerner le morceau.
---

# Création d'un morceau Suno

Projet : `/home/pintok/Agents/claude/create_suno`. Le navigateur est piloté via CDP
(`launch.py` l'ouvre, `fill.py <json>` remplit le formulaire). L'utilisateur clique lui-même
sur **Create** — ne jamais cliquer dessus.

## Étape 1 — Questionnaire exhaustif (obligatoire)

Avant d'écrire quoi que ce soit, interroger l'utilisateur avec l'outil `AskUserQuestion`,
en plusieurs tours (4 questions max par appel, 2 à 4 options concrètes chacune, l'utilisateur
peut toujours répondre librement via « Other »). Utiliser `multiSelect: true` quand plusieurs
réponses ont du sens (instruments, ambiances…).

Règles :
- Ne pas reposer une question dont la réponse est déjà connue (message initial, réponses
  précédentes, mémoire des préférences).
- Adapter les options aux réponses précédentes (ex. après « synthwave », proposer des
  instruments synthwave, pas un banjo).
- Si on ne crée que le style, sauter le bloc Paroles ; si on ne crée que les paroles, poser
  quand même genre / ambiance / tempo (ils conditionnent la métrique du texte).
- Si l'utilisateur répond « peu importe » / « surprends-moi » à un bloc, choisir soi-même et le
  signaler dans le récapitulatif.

### Blocs de questions (dans cet ordre)

**A. Intention**
- Usage du morceau (écoute perso, vidéo/contenu, cadeau/dédicace, jeu de rôle / ambiance, pub…)
- Artistes, morceaux ou bandes-son de référence
- Ce qui doit absolument ressortir (une émotion, une phrase, un son…)

**B. Genre**
- Genre principal et sous-genre
- Fusion éventuelle avec un 2ᵉ genre
- Époque / décennie de référence
- Couleur géographique ou culturelle (french touch, latino, k-pop, celtique…)

**C. Ambiance & énergie**
- Émotions dominantes (mélancolique, euphorique, sombre, nostalgique, rageur, apaisant…)
- Niveau d'énergie (très calme → explosif)
- Évolution de l'énergie (constante, montée progressive, calme→drop, alternance…)
- Cadre / image mentale (nuit en voiture, plage, taverne, bataille, club…)

**D. Rythme**
- Tempo (lent < 80 BPM, moyen 80–110, rapide 110–140, très rapide > 140, ou BPM précis)
- Groove / feel (straight, swing, shuffle, half-time, syncopé, four-on-the-floor…)
- Batterie (acoustique, électronique, boîte à rythmes 808/909, percussions ethniques, aucune)

**E. Instrumentation**
- Instruments principaux / leads
- Section rythmique (basse : slap, synthé, contrebasse, sub…)
- Textures (pads, cordes, cuivres, chœurs, field recordings…)
- Acoustique vs électronique vs hybride
- Instruments à exclure

**F. Voix**
- Chant ou instrumental
- Genre vocal (homme, femme, duo, chœur)
- Timbre (grave, aigu, rauque, soufflé, puissant, doux, nasillard…)
- Mode (chanté, rappé, parlé, scandé, mélange)
- Effets (autotune, vocoder, reverb, voix doublées, harmonies)
- Langue du chant

**G. Production**
- Son global (lo-fi, polished/radio, live/brut, vintage/analogique, cinématique)
- Espace (sec et proche, large et réverbéré, stéréo immersive)
- Qualité recherchée (démo crue vs production finie)

**H. Structure & durée**
- Durée visée (courte < 2 min, standard 2–4 min, longue > 4 min)
- Structure (classique couplet/refrain, avec pont, avec drop, intro longue, sans refrain…)
- Début et fin (intro instrumentale ? fin en fade-out, cut sec, outro a cappella ?)

**I. Paroles** (si chant)
- Thème / sujet
- Histoire ou narration (oui/non, résumé)
- Point de vue (je, tu, il/elle, nous)
- **Style d'écriture** — question dédiée, `multiSelect: true` (on peut combiner, ex.
  littéraire + mélancolique). Comme `AskUserQuestion` limite à 4 options, la poser en deux
  questions dans le même appel :
  - *Approche* : Élaboré / littéraire (images, métaphores, vocabulaire riche) ·
    Simple / direct (accessible, efficace, refrain fédérateur) ·
    Narratif / storytelling (une histoire avec début-milieu-fin) ·
    Abstrait / onirique (images impressionnistes, sens ouvert)
  - *Ton* : Drôle / décalé (jeux de mots, absurde, chute comique) ·
    Ironique / satirique · Engagé / revendicatif · Épique / lyrique (grandiose, héroïque)
  Autres styles à suggérer selon le genre ou en relance : poétique classique (alexandrins,
  rimes riches), rap technique (multisyllabiques, punchlines, double sens), chanson
  française à texte, parodie, comptine / naïf, sombre / gothique, sensuel, introspectif /
  confessionnel, conte / légende (pour le JDR), slogan / hymne.
- **Échantillons de style (SYSTÉMATIQUE)** : pour chaque morceau avec paroles, une fois le
  thème et le style d'écriture choisis, écrire 2 ou 3 courts extraits (4 lignes, même thème)
  qui déclinent le style demandé de façons différentes (ou les styles combinés dans des
  dosages différents), puis demander lequel garder (ou quel mélange) avant d'écrire le texte
  complet. Ne jamais sauter cette étape, sauf si l'utilisateur a explicitement demandé de
  désactiver les extraits.
  **Prévisualisation obligatoire** : chaque fois qu'on propose des textes au choix (extraits,
  titres, refrains, directions de style…), les poser via `AskUserQuestion` en mettant le
  texte complet de chaque option dans le champ `preview` (avec le compte de syllabes), et
  dans une question à choix unique (le `preview` ne marche pas en `multiSelect`). Poser les
  autres questions (multiSelect) dans un appel séparé.
- Registre de langue (soutenu, courant, familier, argot)
- Rimes (riches, simples, libres) et densité (phrases courtes vs denses type rap)
- Mots, noms, références ou phrase-clé à inclure
- Sujets ou mots à éviter, contenu explicite autorisé ou non
- Titre (imposé, à proposer)

**I bis. Exclusions (champ `exclude`)**
Ne pas demander à froid « que veux-tu exclure ? » : à partir du brief, proposer les dérives
probables de Suno pour ce genre et laisser l'utilisateur cocher (`multiSelect: true`) puis
compléter librement. Catégories à couvrir :
- Genres voisins vers lesquels Suno glisse (ex. synthpop → EDM, big room ; folk → country ;
  rock → metal ; lo-fi → trap). Constaté : rap français + voix chantée-rappée → glisse vers
  l'afro (afrotrap, afropop) ; si le brief n'est pas afro, proposer d'exclure
  `afro, afrobeat, afrotrap, afropop, amapiano, dancehall`.
- Instruments ou sons indésirables (guitare électrique saturée, cuivres, 808, piano…)
- Traitements vocaux (autotune, vocoder, voix robotique, chœurs, cris/growl)
- Éléments de production (drop, basses trop lourdes, son trop propre/trop radio, applause…)
- Côté voix : genre vocal opposé si l'utilisateur en veut un précis, rap si chant pur, chant
  si instrumental
Rester court dans le champ : mots-clés séparés par des virgules, uniquement ce qui risque
réellement d'apparaître.

**J. Réglages Suno**
- **Modèle** — NE PAS poser de question : le choisir soi-même d'après le brief et
  l'annoncer (avec une demi-phrase de justification) dans le récapitulatif de l'étape 2 :
  - `v6-wild` (par défaut, préférence de l'utilisateur) : expérimental, à utiliser pour tous
    les morceaux sauf exception ci-dessous
  - `v6` : seulement si l'utilisateur le demande, ou s'il signale que `v6-wild` dérive trop
    du genre demandé (rendu plus sage et plus propre)
  - `v6-mini` : uniquement si l'utilisateur parle de brouillon / test / économiser des crédits
  - Comparaison A/B seulement si l'utilisateur la demande : remplir en `v6-wild`, il clique
    Create, puis relancer `fill.py` avec uniquement `{"model": "v6"}` pour un 2ᵉ Create.
- **Curseurs et options** — même règle que le modèle : pas de question, les régler soi-même
  d'après le brief et les annoncer dans le récapitulatif (l'utilisateur peut ajuster).
  Paliers affichés par Suno (relevés sur l'interface) et usage :
  - **Weirdness** (0–100, défaut 50) — degré de surprise/créativité
    - 0–~35 « Safe zone » : genre très codifié, morceau fonctionnel (ambiance JDR, jingle,
      hymne), quand Suno part trop dans tous les sens
    - ~35–65 « Expected results » : défaut ; 40–55 pour la plupart des morceaux
    - 66–79 « Experimental results » : fusions, direction « audacieuse », structures
      inhabituelles (souvent avec `v6-wild`)
    - 80–100 « Chaos mode » : seulement sur demande explicite
  - **Style Influence** (0–100, défaut 50) — fidélité au prompt de style
    - 0–~35 « Loose » : prompt vague ou volonté de laisser Suno interpréter
    - ~35–66 « Moderate » : défaut
    - 67–100 « Strong » : prompt précis à respecter, ou Suno dérive du genre demandé ;
      65–80 est un bon réglage pour un style très défini. Éviter le très haut si le prompt
      mélange des tags contradictoires.
  - **Variety** (0–4, défaut 1) — écart de style entre les 2 clips générés
    - 0 « Exact style » : les 2 clips collent au même style (style très précis)
    - 1 « Balanced variety » : légère variation (défaut)
    - 2 « Distinct styles » : 2 interprétations différentes, utile pour explorer
    - 3 « Bold exploration », 4 « Unreasonably varied » : seulement pour explorer largement
  - **Max Mode** : « plus de calcul pour maximiser la cohérence sur tout le morceau », coûte
    2× les crédits → **On par défaut** (préférence de l'utilisateur) ; Off seulement si
    l'utilisateur parle de brouillon / test / économiser des crédits, ou avec `v6-mini`.
  - **Personalize / My Taste** : oriente la Variety selon les goûts de l'utilisateur → Off
    par défaut (pour que le résultat reflète le prompt), On si l'utilisateur le souhaite.
  - **Vocal Gender** : male/female selon le brief ; `null` pour un duo, un chœur ou un
    instrumental.

## Étape 2 — Récapitulatif

Résumer le brief en quelques lignes (genre, ambiance, tempo, instruments, voix, thème, réglages)
et le faire valider avant d'écrire.

## Étape 3 — Écriture

### Propositions de style (SYSTÉMATIQUE, avant le prompt)
Après le questionnaire, avant d'écrire le prompt Suno, décrire 2 ou 3 directions musicales
différentes, chacune en 1 ou 2 phrases en langage naturel (comment ça sonne, ce qu'on entend,
l'image que ça évoque — pas de liste de mots-clés). Les directions doivent respecter le brief
mais se distinguer clairement (ex. une fidèle/classique, une plus riche ou cinématique, une
plus audacieuse). Demander à l'utilisateur laquelle garder (ou quel mélange), puis seulement
écrire le prompt Suno correspondant à ce choix. Ne jamais sauter cette étape, sauf si
l'utilisateur demande explicitement de la désactiver.

### Prompt de style (champ `styles`, max 1000 caractères)
- Mots-clés courts séparés par des virgules, du plus important au moins important :
  genre/sous-genre → ambiance → tempo/BPM → instruments clés → voix → production/époque.
- Concret et sonore (« gated reverb drums, warm analog bass ») plutôt qu'abstrait.
- Pas de noms d'artistes (Suno les refuse) : décrire leur son à la place.
- Mettre ce qu'on ne veut pas dans `exclude`, pas dans `styles`.

### Paroles (champ `lyrics`, max 5000 caractères)
- Balises de section entre crochets sur leur propre ligne : `[Intro]`, `[Verse 1]`,
  `[Pre-Chorus]`, `[Chorus]`, `[Bridge]`, `[Drop]`, `[Break]`, `[Outro]`, `[Instrumental]`,
  `[Guitar Solo]`, `[Fade Out]`, `[End]`.
- Indications d'interprétation possibles dans la balise : `[Verse 1: whispered]`,
  `[Chorus: female & male duet]`.
- Chœurs / échos / ad-libs entre parenthèses : `(oh-oh)`, `(encore)`.
- Ligne vide entre les sections. Lignes de longueur régulière, adaptées au tempo et au mode
  (rap = plus dense, ballade = plus court).
- **Compter les syllabes** (avec élisions parlées) et viser, pour ~1 ligne = 1 mesure :
  - ~100–115 BPM chanté-rappé : 10–14 syllabes ; style minimaliste/aéré : 8–11
  - rap dense : 14–16 max ; au-delà Suno accélère et mâche les mots
  - chant / ballade : 6–10 ; refrain : plus court que les couplets (6–9)
  À tempo lent en double temps, on peut aller plus haut ; à tempo rapide, plus bas.
  **Préférence de l'utilisateur : lignes courtes.** 13–17 syllabes lui a paru trop long,
  même en rap dense à 75 BPM → plafonner à ~12 syllabes par ligne en couplet, même si le
  brief dit « flow dense » (la densité vient alors des rimes, pas de la longueur).
  Indiquer le compte des syllabes quand on montre les extraits.
- Refrain répété en entier à chaque occurrence (ne pas écrire « x2 »).
- Instrumental : `"lyrics": ""`.
- **Prononciation (relecture obligatoire avant envoi)** : Suno ne comprend pas le sens, il
  devine la prononciation. Constaté : « On travaille plus » chanté « plu » au lieu de
  « pluss », ce qui inverse le sens. Relire les mots français à prononciation ambiguë et les
  écrire phonétiquement dans `lyrics` : `pluss` (davantage), `toutt` (« tous » pronom),
  `fiss` (le fils), etc. Forcer élisions et liaisons avec apostrophes/tirets (`j'traverse`,
  `les-z-amis`). Si le phonétique ne passe pas, changer de mot. Signaler ces graphies à
  l'utilisateur quand on montre les paroles.

## Étape 4 — Remplissage

**Enchaîner directement, sans demander de validation** : dès que le style et les paroles
sont écrits, envoyer dans Suno dans le même tour (l'utilisateur ajustera après coup s'il
veut). Ne pas terminer par « Je remplis le formulaire ? ».

1. Montrer à l'utilisateur le titre, le style et les paroles.
2. Écrire `songs/<slug>.json` (format documenté en tête de `fill.py`).
3. Vérifier que le navigateur tourne (`curl -s http://127.0.0.1:9222/json/version`), sinon
   lancer `.venv/bin/python launch.py` et demander à l'utilisateur de se connecter.
4. `.venv/bin/python fill.py songs/<slug>.json`, contrôler le rapport affiché.
5. Dire à l'utilisateur que c'est prêt et qu'il peut cliquer sur **Create**.

## Après

Si l'utilisateur donne un retour sur le résultat (ce qui a marché ou non), proposer de
l'ajouter dans la mémoire des préférences pour les prochains morceaux.

**Retouches du style ou des paroles : ne pas toucher aux curseurs.** Quand l'utilisateur
demande seulement de modifier le style (voix, instruments, ambiance…) ou les paroles, ne
changer QUE `styles` / `exclude` / `lyrics` (et `title` si besoin) : laisser `weirdness`,
`style_influence` et `variety` à leurs valeurs actuelles. Ne les modifier que si
l'utilisateur le demande explicitement ; on peut au plus suggérer un réglage dans la
réponse, sans l'appliquer.
