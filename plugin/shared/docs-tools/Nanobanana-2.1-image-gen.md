# Manuel Opérationnel : Motion Design par Génération d'Images
## Orchestration de Démo Reels Haute Fidélité avec Nano Banana 2.1 et Python

Ce manuel définit la méthode de fabrication de démo reels (produits, logiciels, storytelling cinématique, teasers à fort impact) pour un agent autonome exploitant le modèle **Nano Banana 2.1** (`gemini-nano-banana-2.1`) piloté par **Python**.

---

## 1. Philosophie : Pourquoi le Motion Design par l'Image ?

Les modèles vidéo génératifs de bout en bout (text-to-video) souffrent de trois tares rédhibitoires pour les démo reels professionnels :
1. **Dégénérescence des détails et de la typographie** : Les interfaces logicielles (UI), les logos et les polices de caractères bavent ou subissent des hallucinations temporelles.
2. **Manque de contrôle temporel frame-accurate** : Impossible de caler un impact graphique sur le coup de caisse claire d'un morceau musical au 24e ou au 60e de seconde près.
3. **Physique molle et absence de plans de coupe nets** : Les transitions sont souvent des morphings flous au lieu de coupes franches et percutantes.

### Le paradigme Image + Code

La méthode repose sur une dissociation nette :
- **Nano Banana 2.1 génère des photogrammes maîtres (Keyframes)** d'une netteté absolue (jusqu'en 4K), avec un rendu parfait de la typographie, des reflets de matériaux et des cadrages cinématiques.
- **Python prend en charge la cinématique mathématique** : cadencement audio/BPM, interpolation, trajectoires de caméra (Ken Burns haute précision, parallax 2.5D), découpage en calques et assemblage final avec FFmpeg.

Le résultat combine la créativité visuelle d'un studio 3D haut de gamme et la rigueur temporelle d'un codeur Remotion ou Motion Designer After Effects.

---

## 2. Spécifications Techniques : Nano Banana 2.1

Nano Banana 2.1 est opéré avec l'identifiant `gemini-nano-banana-2.1` via l'API Interactions du SDK officiel `google-genai` (https://ai.google.dev/gemini-api/docs/image-generation?hl=fr).

### 2.1 Modèle et Caractéristiques

| Modèle | Identifiant API (`model`) | Points Forts | Cas d'Usage Idéal |
|---|---|---|---|
| **Nano Banana 2.1** | `gemini-nano-banana-2.1` | Rendu 4K, fidélité texte absolue, cohérence multi-références, rapide | Keyframes principales, plans cinématiques, UI, storytelling |

### 2.2 Formats d'Aspect et Résolutions Supportés

Nano Banana 2.1 supporte nativement les résolutions et ratios de projection suivants sous l'objet `response_format` :

| Ratio | Résolution 1K | Résolution 2K | Résolution 4K | Utilisation Cible |
|---|---|---|---|---|
| **16:9** | 1376x768 | 2752x1536 | 5504x3072 | YouTube, Landing pages, Présentations |
| **9:16** | 768x1376 | 1536x2752 | 3072x5504 | TikTok, Instagram Reels, Shorts |
| **21:9** | 1584x672 | 3168x1344 | 6336x2688 | Teasers cinématiques, plans larges anamorphiques |
| **1:1** | 1024x1024 | 2048x2048 | 4096x4096 | Posts carrés, avatars, cartes produits isolées |

> **Règle d'or de résolution** : Toujours générer les keyframes en **2K ou 4K**. Cela permet à Python d'effectuer des zooms numériques (push-in / dolly-in) de 120% à 200% dans la frame sans perte de netteté sur une timeline de sortie en 1080p ou 4K.

---

## 3. Les 6 Piliers du Motion Design par l'Image

### Pilier 1 : La Matrice Tri-Anchor pour la Cohérence Visuelle

Le piège majeur de la génération d'images séquentielles est la dérive stylistique (drift) : le produit ou le personnage change d'aspect entre deux plans. Nano Banana 2.1 gère plusieurs images d'entrée en simultané. Il faut impérativement conditionner chaque requête avec trois ancres :

```
[Ancre 1 : Asset Master] + [Ancre 2 : DA / Texture Guide] + [Ancre 3 : Frame N-1] + Prompt Directionnel
```

1. **Ancre 1 (Identity Anchor)** : L'asset original du produit (capture d'écran Figma de l'UI, photo packshot du boîtier hardware, logo vectoriel).
2. **Ancre 2 (Style & Palette Anchor)** : Une image de référence de la charte graphique définissant l'éclairage studio (ex. fond obsidienne, reflets bleutés, rim light ambrée).
3. **Ancre 3 (Temporal Continuity Anchor)** : Le photogramme précédemment généré (Frame N-1) ou l'interaction parente (`previous_interaction_id`) pour assurer une transition fluide.

### Pilier 2 : Grammaire Cinématographique et Cadrages

Pour dynamiser un reel, chaque plan doit avoir une fonction spatiale précise. Alterner systématiquement les valeurs de plan :

1. **Extreme Wide Shot (Establishing)** : Situe l'environnement global (ex. un data-center futuriste, un bureau de designer baigné de lumière rasante).
2. **Medium Shot (Action / Contexte)** : Montre le produit dans son écosystème (ex. un ordinateur portable ouvert affichant le logiciel sur un bureau en chêne massif).
3. **Macro / Extreme Close-up (Tactilité et Matière)** : Focalise sur un détail microscopique (ex. le chanfrein en aluminium brossé, le grain du verre dépoli, la courbure d'un bouton UI en neumorphisme).
4. **Isometric / Technical Orthographic** : Vue éclatée à 45° mettant en valeur la structure interne ou l'architecture modulaire d'une solution logicielle.

### Pilier 3 : Typographie et Interfaces (UI) Zéro Déchet

Nano Banana 2.1 dispose d'une capacité remarquable à dessiner du texte net à l'intérieur de l'image. Pour garantir un rendu irréprochable :
- Toujours mettre le texte textuellement entre guillemets doubles dans le prompt : `the words "ANALYTICS ENGINE" in bold sans-serif font`.
- Spécifier l'alignement et la hiérarchie : `centered at the top, followed by a secondary label "v2.4 READY" in smaller monospace type`.
- Indiquer le contraste : `crisp white typography on dark charcoal background, high contrast, clean kerning`.
- Ne pas surcharger l'image de texte : laisser les paragraphes au code d'habillage vidéo (overlays SVG/CSS/Remotion) et réserver à Nano Banana les titres majeurs, jauges clés et logotypes.

### Pilier 4 : Découpage en Calques (Scene Graph 2.5D)

Pour créer des effets de profondeur réalistes en Python, décomposer les scènes complexes en calques générés séparément :
- **Calque Fond (Z0)** : Environnement lointain flouté (bokeh / shallow depth of field).
- **Calque Midground (Z1)** : Le produit ou l'écran principal.
- **Calque Foreground (Z2)** : Particules en suspension, halos lumineux ou éléments flottants passant devant la caméra pour créer de la parallaxe.

### Pilier 5 : Synchronisation Rythmique et Grille Audio (BPM Lock)

Un banger reel tire sa puissance de la collision synchrone entre l'image et la musique.

#### Formules de conversion Temporelle
À une cadence de **60 FPS** (standard de fluidité recommandé) :
- Durée d'un temps (beat) en frames : `Frames_Per_Beat = (60 * FPS) / BPM`
  - Exemple à 120 BPM : `(60 * 60) / 120 = 30 frames` (0.50 s)
- Durée d'une mesure (bar 4/4) en frames : `4 * Frames_Per_Beat = 120 frames` (2.00 s)

#### Rôles Temporels des Plans
1. **Smash Cut (Impact)** : 4 à 8 frames (0.06 à 0.13 s). Utilisé sur les drops et les transitions ultra-rapides.
2. **Rhythm Cut** : 15 à 30 frames (0.25 à 0.50 s). Synchronisé sur chaque battement de caisse claire ou kick.
3. **Power Hold (Plan Héros)** : 60 à 120 frames (1.0 à 2.0 s). Toujours accompagné en Python d'un mouvement lent continu (slow zoom ou slow pan) pour éviter l'effet d'image morte.

### Pilier 6 : Trajectoires de Caméra et Cinétique Numérique

Une image fixe ne doit jamais rester statique à l'écran. Python applique des matrices de transformation par-dessus la frame haute résolution :
- **Dolly-in / Push-in progressif** : Zoom doux de 1.00 vers 1.15 avec un profil d'amortissement ease-out.
- **Whip Pan (Fouetté)** : Translation horizontale ultra-rapide sur 6 frames avec flou de mouvement directionnel simulé.
- **Rack Focus (Basculement de point)** : Défloutage progressif d'un premier plan pendant que l'arrière-plan devient net.

---

## 4. Pipeline d'Exécution Python

Voici l'architecture logicielle complète que l'agent doit employer pour générer, animer et compiler un reel.

### 4.1 Client de Génération Déterministe (`nano_engine.py`)

Ce module encapsule l'API `google-genai` avec support du mode multi-image et gestion du format de sortie 16:9 4K.

```python
"""Module d'interaction direct avec Nano Banana 2.1 (gemini-nano-banana-2.1)."""

import base64
import os
from pathlib import Path
from typing import Optional, List
from google import genai
from PIL import Image
import io

class NanoBananaEngine:
    def __init__(self, api_key: Optional[str] = None):
        api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY manquante.")
        self.client = genai.Client(api_key=api_key)
        self.default_model = "gemini-nano-banana-2.1"

    def _encode_image(self, image_path: Path) -> dict:
        """Encode une image locale en bloc d'entrée base64 pour l'API."""
        with open(image_path, "rb") as f:
            raw_bytes = f.read()
        
        mime_type = "image/png"
        if image_path.suffix.lower() in [".jpg", ".jpeg"]:
            mime_type = "image/jpeg"
        elif image_path.suffix.lower() == ".webp":
            mime_type = "image/webp"

        return {
            "type": "image",
            "data": base64.b64encode(raw_bytes).decode("utf-8"),
            "mime_type": mime_type
        }

    def generate_keyframe(
        self,
        prompt: str,
        output_path: Path,
        reference_images: Optional[List[Path]] = None,
        previous_interaction_id: Optional[str] = None,
        aspect_ratio: str = "16:9",
        image_size: str = "2K"
    ) -> str:
        """
        Génère un photogramme en haute définition et retourne l'ID d'interaction
        pour permettre l'enchaînement d'état.
        """
        input_payload = []

        # 1. Injection des références (Ancres Produit / Style / Temporalité)
        if reference_images:
            for ref_path in reference_images:
                if ref_path.exists():
                    input_payload.append(self._encode_image(ref_path))

        # 2. Injection du prompt de direction artistique
        input_payload.append({"type": "text", "text": prompt})

        # 3. Requête auprès de l'API Interactions
        interaction_kwargs = {
            "model": self.default_model,
            "input": input_payload,
            "response_format": {
                "type": "image",
                "aspect_ratio": aspect_ratio,
                "image_size": image_size
            }
        }

        if previous_interaction_id:
            interaction_kwargs["previous_interaction_id"] = previous_interaction_id

        interaction = self.client.interactions.create(**interaction_kwargs)

        # 4. Décodage et écriture sécurisée sur disque
        if interaction.output_image and interaction.output_image.data:
            image_bytes = base64.b64decode(interaction.output_image.data)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(image_bytes)
        else:
            raise RuntimeError(f"Aucune image retournée par le modèle pour le prompt : {prompt[:60]}...")

        return interaction.id
```

### 4.2 Moteur Cinématique de Caméra (`camera_animator.py`)

Ce script transforme une image fixe 2K/4K en une séquence fluide de photogrammes animés avec easing non-linéaire (dolly-in cinématique, slow drift et shake subtil).

```python
"""Module d'animation cinématique par recadrage dynamique (Ken Burns 2.0)."""

import numpy as np
from PIL import Image, ImageFilter
from pathlib import Path

def ease_out_cubic(t: float) -> float:
    """Courbe d'amortissement cubique pour une entrée vive et un arrêt doux."""
    return 1.0 - pow(1.0 - t, 3)

def ease_in_out_quad(t: float) -> float:
    """Accélération progressive suivie d'une décélération."""
    if t < 0.5:
        return 2.0 * t * t
    return 1.0 - pow(-2.0 * t + 2.0, 2) / 2.0

def render_camera_motion(
    source_image_path: Path,
    output_dir: Path,
    total_frames: int,
    start_scale: float = 1.0,
    end_scale: float = 1.15,
    pan_x_ratio: float = 0.05,
    pan_y_ratio: float = 0.0,
    target_width: int = 1920,
    target_height: int = 1080
):
    """
    Génère une série de frames interpolées appliquant un zoom et un panoramique doux.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    master_img = Image.open(source_image_path).convert("RGB")
    orig_w, orig_h = master_img.size

    for frame_idx in range(total_frames):
        progress = frame_idx / max(1, total_frames - 1)
        curved_t = ease_out_cubic(progress)

        # Évolution de l'échelle (Scale)
        current_scale = start_scale + (end_scale - start_scale) * curved_t

        # Calcul de la fenêtre de découpe (Crop Box)
        crop_w = int(orig_w / current_scale)
        crop_h = int(orig_h / current_scale)

        # Calcul du décentrage (Pan X / Y)
        offset_x = int((orig_w - crop_w) * 0.5 + (orig_w * pan_x_ratio * curved_t))
        offset_y = int((orig_h - crop_h) * 0.5 + (orig_h * pan_y_ratio * curved_t))

        # Borner les coordonnées à l'image source
        offset_x = max(0, min(orig_x_limit := orig_w - crop_w, offset_x))
        offset_y = max(0, min(orig_y_limit := orig_h - crop_h, offset_y))

        cropped = master_img.crop((offset_x, offset_y, offset_x + crop_w, offset_y + crop_h))
        frame_resized = cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)

        frame_file = output_dir / f"frame_{frame_idx:05d}.png"
        frame_resized.save(frame_file, quality=95)
```

### 4.3 Compilateur et Synchroniseur Audio (`timeline_compiler.py`)

Ce module compile la timeline complète en vidéo MP4 60 FPS avec FFmpeg, en asservissant les cuts sur les temps musicaux.

```python
"""Compilation de la timeline finale et calage sur l'audio via FFmpeg."""

import subprocess
from pathlib import Path

def compile_video_with_audio(
    frames_dir: Path,
    audio_path: Path,
    output_video_path: Path,
    fps: int = 60
):
    """
    Assemble les frames ordonnées et la bande sonore en un MP4 H.264 prêt pour diffusion.
    """
    cmd = [
        "ffmpeg",
        "-y",
        "-framerate", str(fps),
        "-i", str(frames_dir / "frame_%05d.png"),
        "-i", str(audio_path),
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "320k",
        "-shortest",
        str(output_video_path)
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Erreur d'encodage FFmpeg :\n{result.stderr}")
```

---

## 5. Guide de Prompt Engineering pour Demo Reels

### 5.1 Anatomie d'un Prompt Keyframe Idéal

Pour obtenir une image prête au motion design, le prompt doit comporter 5 sections strictes :
1. **Sujet Principal** : Identité exacte de l'objet, du composant logiciel ou de la scène.
2. **Cadrage et Focale** : Optique simulée (`35mm anamorphic`, `85mm macro`, `orthographic 45°`).
3. **Éclairage et Ambiance** : Disposition des sources lumineuses (`key light softbox`, `neon edge rim light`, `dark obsidian reflective ground`).
4. **Matériaux et Textures** : Précision physique (`matte anodized space grey aluminum`, `frosted glass with chromatic dispersion`, `organic 35mm film grain`).
5. **Typographie et Micro-Détails** : Emplacement des libellés et textes sans ambiguïté.

### 5.2 Recettes de Démo Reels par Cas d'Usage

#### Recette A : Software UI Cinematic Reveal (Produit SaaS)
```text
A cinematic high-angle 3/4 perspective shot of a dark-mode SaaS dashboard interface floating in a sleek obsidian studio. The screen displays an analytics graph with luminous emerald green and cyan curves. In the top-center header, crisp typography reads "ORBITAL OS" in a clean grotesque sans-serif font. The dashboard glass panel features subtle frosted blur and soft bevel reflections. Dark moody atmospheric background with faint volumetric light rays. Extreme clarity, 4K resolution, minimalist luxury aesthetic, shot on 50mm cinema lens.
```

#### Recette B : Hardware / Physical Device Hero Shot
```text
Extreme macro close-up of a precision-engineered smart device edge. Matte dark titanium finish with diamond-cut chamfered borders catching a sharp amber rim light. A tactile rotary knob engraved with radial knurling is in the foreground. In the background, smooth photographic bokeh. Raytraced realistic reflections, crisp industrial design, Octane render quality, ultra-sharp detail, cinematic lighting.
```

#### Recette C : Storytelling & Emotional Transition
```text
Wide cinematic establishing shot of a futuristic urban creator studio at twilight. Floor-to-ceiling windows showing a blurred skyline with warm neon signs. A minimalist desk with a single illuminated workstation casting a cool glow across architectural drawings. Cinematic 2.39:1 widescreen framing, moody teal and orange color grading, soft atmospheric haze, 35mm film aesthetic.
```

---

## 6. Anti-Patterns et Erreurs Fatales à Bannir

| Pratique Interdite (Anti-Pattern) | Conséquence Visuelle | Correction Immédiate |
|---|---|---|
| **Laisser l'image statique sans mouvement de caméra** | Sensation d'un diaporama PowerPoint figé et ennuyeux | Toujours appliquer un slow zoom (1.00 à 1.12) ou un pan programmé en Python |
| **Générer chaque plan sans image de référence** | Rupture totale de style d'un plan à l'autre (drift visuel) | Toujours alimenter l'API avec l'asset original et le photogramme précédent (Ancres 1 et 3) |
| **Générer des paragraphes entiers de texte dans l'image** | Texte qui bave ou hallucinations de lettres illisibles | Ne générer que les titres majeurs (1 à 3 mots). Les sous-titres et données denses se posent en calque via code |
| **Coupes aléatoires hors tempo musical** | Rythme mou, absence d'énergie | Aligner rigoureusement chaque coupure sur un multiple ou diviseur de temps (ex. 15, 30 ou 60 frames) |
| **Interpolation linéaire pure (`t`)** | Mouvement robotique et artificiel | Utiliser des courbes d'easing non-linéaires (`ease_out_cubic`, courbes de Bézier) |

---

## 7. Grille d'Auto-Évaluation pour l'Agent

Avant de considérer une production comme terminée, l'agent doit valider les points suivants :
- [ ] **Fidélité Produit** : L'interface ou le matériel présenté est-il immédiatement reconnaissable et fidèle à la marque ?
- [ ] **Absence de bavure textuelle** : Tous les mots visibles générés dans les images sont-ils orthographiés sans la moindre lettre déformée ?
- [ ] **Métrique de Résolution** : Les photogrammes sources sont-ils en 2K ou 4K pour supporter le crop cinématique sans pixellisation ?
- [ ] **Cadence Temporelle** : La vidéo finale est-elle encodée à 60 FPS avec calage strict sur la grille BPM audio ?
- [ ] **Dynamique des Plans** : La séquence alterne-t-elle judicieusement entre plans larges d'ambiance, vues produit à 45° et macros hyper-détaillées ?
