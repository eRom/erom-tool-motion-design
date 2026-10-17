# Contrat du dépôt

Dépôt de développement du plugin Claude Code `erom-motion-design` : boîte à outils
de motion design (références décortiquées de vidéos marquantes, guides des
générateurs d'images et de musique, banque de bruitages Sonniss).

**Pourquoi ce plugin existe.** Enlever les limites de `hyperframes` constatées sur
`/Users/recarnot/dev/erom-agence-demo-reel/`. Toute skill ajoutée ici doit pouvoir
se rattacher à une limite observée sur ce chantier (ou un suivant), pas à une
envie générique.

**HyperFrames est acquis.** Le motion (composition, animation, rendu) est fait
par le plugin `hyperframes`. Ce plugin ne le remplace pas et n'a pas de moteur
à lui : il guide Claude pour brancher des outils externes (images, musique,
bruitages, références) dans une composition HyperFrames. Une ancienne idée de
CLI maison (`motion render`, `motion ears`…) a été abandonnée le 2026-10-08 :
ne pas la réintroduire.

Ce fichier dit comment travailler ici. Il décrit un contrat, pas un état atteint :
la section « État actuel » dit ce qui n'y est pas encore conforme.

## Structure

```
plugin/                          seul dossier distribué (source marketplace git-subdir)
  .claude-plugin/plugin.json     manifeste
  skills/<nom>/SKILL.md          une skill par dossier
  skills/<nom>/references/       matière longue, lue seulement quand la skill tourne
  skills/<nom>/scripts/          scripts appelés par la skill (bun, bash)
  shared/references/<id>/        vidéos de référence décortiquées, 4 fichiers chacune
  shared/docs-tools/             guides des outils externes (Seedream, Nanobanana, Lyria, Pixabay)
  agents/<nom>.md                subagents, découverts automatiquement
  assets/erom-motion-design.png  image de tête du README racine
docs/                            specs, plans, recherches, revues
_memory_/                        connaissance de session persistée, indexée par le vault RAG
.claude/                         notes et settings locaux, jamais distribués
```

Pas d'étape de build : les skills sont du Markdown pur, écrit à la main
directement dans `plugin/`.

## Invariants

1. **Seul `plugin/` est distribué.** Tout ce qui est hors de ce dossier reste
   local ou sert le développement : notes, matière de travail, mémoire.
2. **Chemins via `${CLAUDE_PLUGIN_ROOT}`.** Une fois installé, le plugin vit dans
   le cache de Claude Code, pas dans le projet de l'utilisateur. Tout chemin vers
   un fichier du plugin (référence, doc, script) s'écrit
   `${CLAUDE_PLUGIN_ROOT}/...`, jamais `.claude/skills/...` ni un chemin absolu
   de ce Mac.
3. **Français.** Le plugin sert des projets français. Skills, exemples et
   sorties en français, y compris les descriptions de `SKILL.md`. Le code des
   scripts reste en anglais (identifiants, flags, messages techniques).
4. **Aucune capacité dupliquée.** Avant d'ajouter une skill, vérifier qu'aucun
   autre plugin ne la porte déjà : les plugins eRom
   (`~/dev/erom-marketplace/.claude-plugin/marketplace.json`), mais aussi
   `hyperframes` et `remotion`, dont ce plugin est le complément. Image :
   `erom-image` couvre déjà Nano Banana et GPT Image.
5. **Les références sont des exemples, pas des gabarits.** Les dossiers de
   `shared/references/` nourrissent l'œil. Une skill ne doit jamais ancrer une
   création sur une seule référence.
6. **La règle vient de ce qui a déjà tourné.** Chaque consigne d'une skill doit
   pouvoir se rattacher à un artefact réel : une sortie observée, un test qui
   passe, un incident daté. Le générique ne décrit aucun usage et ne sert de
   source à rien.
7. **Pas de secret dans le dépôt.** Les clés (`GEMINI_API_KEY`,
   `PIXABAY_API_KEY`, OpenRouter) se lisent depuis l'environnement.
8. **Le manifeste ne déclare pas ses agents.** La clé `agents` absente vaut
   découverte automatique de `plugin/agents/`. Une liste explicite fige les
   chemins et fait mentir `claude plugin details`, qui affiche alors « Agents (0) ».

## Vérifier

```bash
claude --plugin-dir plugin plugin details erom-motion-design
```

Affiche l'inventaire réel des composants chargés et le coût token projeté.
C'est la seule preuve que le manifeste charge ce qu'on croit : un dossier
`skills/` ou `agents/` peuplé mais invisible ici n'est pas chargé.

## Publication

Publié depuis le 2026-10-17 (0.1.0) sur `eRom/erom-tool-motion-design`, entrée
`git-subdir` (`path: plugin`, `ref: main`, `strict: true`) dans la marketplace. La
publication ne se fait pas à la main : la skill `release`
du plugin `erom-dev-plugin` la porte de bout en bout, depuis ce dépôt.

```
/erom-dev-plugin:release
```

Elle lit le nom et la version dans le manifeste, choisit le bump SemVer, commite
et pousse ce dépôt, puis met à jour `~/dev/erom-marketplace` (entrée du plugin,
metadata, README), et vérifie la CI. Toujours dans cet ordre : le plugin d'abord,
la marketplace ensuite, parce que l'entrée pointe `ref: main` sur ce dépôt.

Les releases suivantes sont de simples bumps : plugin, puis entrée et
`metadata.version` de la marketplace au même niveau.

## État actuel - 2026-10-17

Quatre skills écrites, publié en 0.1.0.

| Élément | État |
|---|---|
| `skills/motion-context` | écrite : vérifie `hyperframes` et `remotion`, passe la main à `/hyperframes:hyperframes`, liste références et outils externes |
| `skills/sonniss-catalog-audio-fx` | écrite, scripts `search.ts` et `fetch.sh`. Pose les bruitages en pistes `<audio>` HyperFrames. Dépend de `rclone` et du remote `gdrive:`. Pose `<audio>` pas encore éprouvée sur un vrai rendu |
| `skills/gemini-vocal-generator` | écrite, 3 scripts Python (`uv`). Voice design, TTS single et dialogue, pose `<audio>` HyperFrames. 6 evals passées le 2026-10-08 sur l'API réelle ; pose dans une composition pas encore éprouvée |
| `skills/reverse-animation` | écrite le 2026-10-17, scripts `glimpse.ts` (Glimpse via OpenRouter, ralenti x8 par défaut) et `contact-sheet.sh`. Recette sur une vidéo témoin à vérité connue : Glimpse juste sur la géométrie, faux sur durée et easing, d'où la mesure du timing par planche-contact. Pas encore éprouvée de bout en bout sur une vraie capture |
| Génération vidéo | Seedance 2.5 et MiniMax H3 via les MCP `fal` et `fal-docs` (`plugin/.mcp.json`), section dans `motion-context` |
| `shared/references/` | 14 vidéos décortiquées, indexées dans `INDEX.md` (famille, durée, tempo, signature) |
| `shared/docs-tools/` | 4 guides : Seedream 5.0 Pro, Nanobanana 2.1, Lyria, Pixabay |
| `assets/erom-motion-design.png` | carte au fusain livrée le 2026-10-08 (`/erom-dev-plugin:illustrate`) |
| Onboarding caserne (`_memory_/ONBOARD.md`) | fait : Linear (team EAT), Slack `#motion-design-tools` |
| Publication marketplace | faite le 2026-10-17 : plugin 0.1.0 (`952bba7`), marketplace metadata 0.30.0 (`3227af9`), CI verte |
