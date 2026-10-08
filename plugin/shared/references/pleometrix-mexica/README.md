# Reverse-Engineering Motion Design : Pleometrix - P(doom)

Dossier d'analyse technique et de rétro-ingénierie intégrale de la vidéo de référence `pleometrix-mexica.mp4` (musique et motion design par Mexica / @pleometrix).

Ce travail sert de cas d'école de référence pour concevoir le futur skill d'analyse automatisée `.agents/skills/reverse-motion/`.

---

## Sommaire des Spécifications Disponibles

1. [01_GLOBAL_DA_AND_SYSTEM.md](file:///Users/recarnot/dev/tmp/video-motion-design/motion-code/pleometrix-mexica/01_GLOBAL_DA_AND_SYSTEM.md)
   - **Direction Artistique & Design Tokens** : Palette chromatique complète (Hex, rôles, modes de fusion), stack typographique quadruple (Grotesque, Monospace, Typewriter, Serif), système de grille et viewfinder `[ ]`, métriques temporelles audio (129.2 BPM = 27.8 frames/beat à 60 fps), courbes d'easing mathématiques et pipeline de shaders / post-processing.

2. [02_CHRONOLOGICAL_BREAKDOWN.md](file:///Users/recarnot/dev/tmp/video-motion-design/motion-code/pleometrix-mexica/02_CHRONOLOGICAL_BREAKDOWN.md)
   - **Découpage Plan-par-Plan Exhaustif** : Analyse des 28 séquences de la vidéo (9399 frames à 60 fps), avec timestamps précis, corrélation rythmique audio, transitions entrantes, vecteurs de mouvement, pile de calques (Z-Index / Scene Graph) et observations techniques orientées fabrication.

3. [03_FABRICATION_BLUEPRINTS.md](file:///Users/recarnot/dev/tmp/video-motion-design/motion-code/pleometrix-mexica/03_FABRICATION_BLUEPRINTS.md)
   - **Recettes de Code & Algorithmes de Reproduction** : Implémentations concrètes pour agents développeurs (Remotion, Three.js, Canvas 2D, SVG) :
     1. Moteur Sparkler / Traceur vectoriel incandescant.
     2. Moteur de paysage de perte 3D & trou noir d'accrétion.
     3. Moteur HUD Computer Vision avec bounding boxes et tracking.
     4. Moteur d'odomètre mécanique analogique et compteur haute vélocité.
     5. Moteur de formulaire papier bureaucratique et tampon encreur à ressort.
     6. Moteur de terminal avec dactylographie variable et barres de logits.
     7. Moteur de kinetic typography massive avec double calque fill/stroke.

4. [04_AUDIO_AND_SOUND_DESIGN.md](file:///Users/recarnot/dev/tmp/video-motion-design/motion-code/pleometrix-mexica/04_AUDIO_AND_SOUND_DESIGN.md)
   - **Cartographie Audio & Sound Design (SFX)** : Analyse du montage sonore, asservissement de l'image sur les kicks/snares/voix, typologie des bruitages (Whooshes, Risers, Impacts, Glitches/Bleeps, Foley d'étincelle/machine/papier/tampon/trombones), et gestion des silences et suspensions (hang time).

5. [04_PROMPT_EVOLUTION_FOR_SKILL.md](file:///Users/recarnot/dev/tmp/video-motion-design/motion-code/pleometrix-mexica/04_PROMPT_EVOLUTION_FOR_SKILL.md)
   - **Évolution du Prompt & Architecture du Skill** : Retour critique sur le prompt initial de Gemini.app, identification des manques majeurs pour la fabrication de code, et formalisation du méta-prompt pour `.agents/skills/reverse-motion/`.
