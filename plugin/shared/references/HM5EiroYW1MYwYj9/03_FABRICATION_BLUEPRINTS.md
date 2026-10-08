# 03_FABRICATION_BLUEPRINTS.md
## Blueprints Techniques de Fabrication - Remotion, Canvas 2D, WebGL & SVG
**Référence vidéo** : `HM5EiroYW1MYwYj9.mp4` (1920x1080 @ 30fps, 143.55 BPM)  
**Direction Artistique** : Pop Riso Rétro-Futuriste / Manga Synthwave / Papercraft

---

### Table des Matières
1. [Blueprint 1 : Shader d'Impression Risographe Halftone & Décalage Cyan/Magenta (Misregistration)](#1-blueprint-1--shader-dimpression-risographe-halftone--décalage-cyanmagenta-misregistration)
2. [Blueprint 2 : Composant Washi Tape Procédural & Décollement Élastique](#2-blueprint-2--composant-washi-tape-procédural--décollement-élastique)
3. [Blueprint 3 : Moteur d'Essaim de Trombones Exponentiels (Paperclips Swarm Engine)](#3-blueprint-3--moteur-dessaim-de-trombones-exponentiels-paperclips-swarm-engine)
4. [Blueprint 4 : Tracé de Spline de Perte d'Entraînement & Suiveur de Tangente (Loss Follower)](#4-blueprint-4--tracé-de-spline-de-perte-dentraînement--suiveur-de-tangente-loss-follower)
5. [Blueprint 5 : Odomètre Électromécanique Décimal à Tambours Rotatifs (1E30 FLOP/s)](#5-blueprint-5--odomètre-électromécanique-décimal-à-tambours-rotatifs-1e30-flops)
6. [Blueprint 6 : Dislocation Particulaire en Demi-Teinte Riso (Atomic Rearrangement)](#6-blueprint-6--dislocation-particulaire-en-demi-teinte-riso-atomic-rearrangement)

---

### 1. Blueprint 1 : Shader d'Impression Risographe Halftone & Décalage Cyan/Magenta (Misregistration)

#### 1.1. Modèle Mathématique & Physique
L'impression risographe repose sur des passages d'encres successifs sur un tambour rotatif micro-perforé. Deux artefacts physiques définissent le rendu :
1. **La trame de demi-teinte (Halftone Screening)** : La luminance continue d'un canal est échantillonnée par une grille de coordonnées orientée d'un angle $\theta$ (traditionnellement 45° pour la couche sombre, 15° et 75° pour les couleurs primaires). À chaque point de coordonnée tournée $(u, v) = R(\theta) \cdot (x, y)$, on calcule la distance au centre de la cellule de pas $P$ :
   $$d = \left\| \text{mod}(u, P) - \frac{P}{2}, \text{mod}(v, P) - \frac{P}{2} \right\|$$
   Le rayon du point d'encre est directement proportionnel à l'absorption d'encre $1 - L$, où $L$ est la luminance locale. Le point est imprimé si $d \le r(L)$.
2. **Le micro-décalage mécanique (Misregistration Bleed)** : Les rouleaux de papier introduisent un décalage sub-millimétrique entre le passage d'encre Marine foncé ($C_1$), le Magenta fluorescent ($C_2$) et le Jaune chaud ($C_3$). Les coordonnées de lecture de texture sont perturbées :
   $$UV_M = UV + \Delta_M, \quad UV_C = UV + \Delta_C, \quad UV_Y = UV + \Delta_Y$$
3. **Le grain de papier buvard (Porous Absorption)** : Bruit de Perlin haute fréquence simulant la capillarité de la fibre de cellulose non couchée.

#### 1.2. Implémentation WebGL Fragment Shader (Compatible Remotion Three.js / Canvas Post-Process)

```typescript
// RisoShaderMaterial.ts
import * as THREE from "three";

export const RisoHalftoneShader = {
  uniforms: {
    tDiffuse: { value: null as THREE.Texture | null },
    uResolution: { value: new THREE.Vector2(1920, 1080) },
    uGridSize: { value: 6.0 }, // Diamètre maximal de cellule en pixels
    uAngle: { value: Math.PI / 4.0 }, // 45 degrés
    uBleedMarine: { value: new THREE.Vector2(1.2, -0.6) }, // Décalage en pixels
    uBleedPink: { value: new THREE.Vector2(-1.5, 1.0) },
    uBleedYellow: { value: new THREE.Vector2(0.5, 1.8) },
    uPaperColor: { value: new THREE.Color("#F4EAD4") }, // Papier crème vergé
    uInkMarine: { value: new THREE.Color("#1B2A4A") }, // Encre bleu nuit
    uInkPink: { value: new THREE.Color("#FF3366") }, // Rose néon riso
    uInkYellow: { value: new THREE.Color("#FFCC00") }, // Jaune cadmium riso
    uGrainIntensity: { value: 0.12 },
    uTime: { value: 0.0 },
  },

  vertexShader: /* glsl */ `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,

  fragmentShader: /* glsl */ `
    uniform sampler2D tDiffuse;
    uniform vec2 uResolution;
    uniform float uGridSize;
    uniform float uAngle;
    uniform vec2 uBleedMarine;
    uniform vec2 uBleedPink;
    uniform vec2 uBleedYellow;
    uniform vec3 uPaperColor;
    uniform vec3 uInkMarine;
    uniform vec3 uInkPink;
    uniform vec3 uInkYellow;
    uniform float uGrainIntensity;
    uniform float uTime;

    varying vec2 vUv;

    // Générateur pseudo-aléatoire pour grain de papier
    float hash21(vec2 p) {
      p = fract(p * vec2(234.34, 435.345));
      p += dot(p, p + 34.23);
      return fract(p.x * p.y);
    }

    // Calcul de point de trame tourné
    float halftonePoint(vec2 st, float angle, float gridSize, float density) {
      float s = sin(angle);
      float c = cos(angle);
      mat2 rot = mat2(c, -s, s, c);
      vec2 rotSt = rot * st;
      vec2 grid = fract(rotSt / gridSize) - 0.5;
      float dist = length(grid) * 2.0; // Normalisé 0 à 1 dans le cercle
      float maxRadius = sqrt(clamp(density, 0.0, 1.0));
      // Antialiasing doux au bord du point
      return 1.0 - smoothstep(maxRadius - 0.15, maxRadius + 0.15, dist);
    }

    void main() {
      vec2 fragCoord = vUv * uResolution;
      vec2 px = 1.0 / uResolution;

      // Échantillonnage trichromique avec décalages mécaniques
      vec4 colMarine = texture2D(tDiffuse, vUv + uBleedMarine * px);
      vec4 colPink   = texture2D(tDiffuse, vUv + uBleedPink * px);
      vec4 colYellow = texture2D(tDiffuse, vUv + uBleedYellow * px);

      // Séparation des densités par canal complémentaire
      float lumM = dot(colMarine.rgb, vec3(0.299, 0.587, 0.114));
      float densityMarine = 1.0 - lumM;

      float densityPink = (1.0 - colPink.g) * colPink.r;
      float densityYellow = (1.0 - colYellow.b) * colYellow.r;

      // Calcul des points de trame pour chaque tambour avec angles distincts
      float dotM = halftonePoint(fragCoord, uAngle, uGridSize, densityMarine);
      float dotP = halftonePoint(fragCoord, uAngle + 0.5236, uGridSize * 1.1, densityPink); // +30 deg
      float dotY = halftonePoint(fragCoord, uAngle - 0.5236, uGridSize * 0.9, densityYellow); // -30 deg

      // Bruit de texture papier buvard
      float grain = hash21(fragCoord + sin(uTime * 10.0)) * uGrainIntensity;

      // Composition soustractive réaliste de l'encre sur papier
      vec3 finalColor = uPaperColor - vec3(grain);

      // Multiplication soustractive des encres
      finalColor = mix(finalColor, finalColor * (1.0 - (1.0 - uInkYellow) * dotY), dotY * 0.85);
      finalColor = mix(finalColor, finalColor * (1.0 - (1.0 - uInkPink) * dotP), dotP * 0.90);
      finalColor = mix(finalColor, finalColor * (1.0 - (1.0 - uInkMarine) * dotM), dotM * 0.95);

      gl_FragColor = vec4(finalColor, 1.0);
    }
  `
};
```

---

### 2. Blueprint 2 : Composant Washi Tape Procédural & Décollement Élastique

#### 2.1. Modèle Mathématique & Physique
Le ruban adhésif japonais Washi présente :
1. **Des bords dentelés de découpe fibreuse** : Générés via une somme de fonctions sinusoïdales à fréquences harmoniques non entières (synthèse additive de Fourier discrète) pour éviter la répétition visible.
2. **Une translucidité avec réfraction diffuse** : Rendu en `mix-blend-mode: multiply` avec un fond semi-transparent (opacité 0.88), couplé à une texture fibreuse discrète.
3. **Une cinématique de pose par ressort amorti (Spring Dynamics)** : L'angle de rotation d'impact $\theta(t)$ et le déploiement de largeur $w(t)$ suivent l'équation différentielle de ressort :
   $$\ddot{x} + 2\zeta\omega_0\dot{x} + \omega_0^2(x - x_{\text{target}}) = 0$$
   avec un facteur d'amortissement sous-critique $\zeta = 0.65$ créant un léger rebond avant immobilisation.

#### 2.2. Composant React / Remotion

```tsx
// WashiTape.tsx
import React, { useMemo } from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export interface WashiTapeProps {
  text: string;
  enterFrame: number;
  width?: number;
  height?: number;
  baseColor?: string;
  textColor?: string;
  rotation?: number; // Degrés cibles
  seed?: number;
}

export const WashiTape: React.FC<WashiTapeProps> = ({
  text,
  enterFrame,
  width = 320,
  height = 54,
  baseColor = "#FF6B8B",
  textColor = "#FFFFFF",
  rotation = 4.5,
  seed = 42,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Animation d'entrée au ressort (Spring)
  const springProgress = spring({
    frame: frame - enterFrame,
    fps,
    config: {
      damping: 12,
      mass: 0.8,
      stiffness: 180,
    },
  });

  // Déploiement élastique de l'échelle et de la rotation
  const scale = interpolate(springProgress, [0, 1], [0.4, 1.0]);
  const currentRotation = interpolate(springProgress, [0, 1], [rotation - 15, rotation]);
  const opacity = interpolate(springProgress, [0, 0.4], [0, 0.92], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Génération procédurale du polygone de découpe dentelée
  const clipPathSvg = useMemo(() => {
    const steps = 16;
    let leftEdge = "";
    let rightEdge = "";

    // Bord gauche dentelé
    for (let i = 0; i <= steps; i++) {
      const y = (i / steps) * 100;
      const noise = Math.sin(i * 1.7 + seed) * 3 + Math.cos(i * 3.3 + seed * 2) * 1.5;
      const x = Math.max(0, noise + 4);
      leftEdge += `${x}% ${y}%, `;
    }

    // Bord droit dentelé
    for (let i = steps; i >= 0; i--) {
      const y = (i / steps) * 100;
      const noise = Math.cos(i * 1.9 + seed * 3) * 3 + Math.sin(i * 2.7 + seed) * 1.5;
      const x = Math.min(100, 96 + noise);
      rightEdge += `${x}% ${y}%, `;
    }

    const fullPolygon = `polygon(${leftEdge} ${rightEdge.slice(0, -2)})`;
    return fullPolygon;
  }, [seed]);

  if (frame < enterFrame) return null;

  return (
    <div
      style={{
        transform: `rotate(${currentRotation}deg) scale(${scale})`,
        transformOrigin: "center center",
        opacity,
        filter: "drop-shadow(2px 6px 4px rgba(27, 42, 74, 0.28))",
        display: "inline-block",
      }}
    >
      <div
        style={{
          width,
          height,
          backgroundColor: baseColor,
          clipPath: clipPathSvg,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          mixBlendMode: "multiply",
          position: "relative",
          overflow: "hidden",
        }}
      >
        {/* Lignes de trame fibreuse interne */}
        <div
          style={{
            position: "absolute",
            inset: 0,
            background:
              "repeating-linear-gradient(45deg, rgba(255,255,255,0.08) 0px, rgba(255,255,255,0.08) 2px, transparent 2px, transparent 6px)",
            pointerEvents: "none",
          }}
        />
        <span
          style={{
            fontFamily: "'Space Mono', monospace",
            fontWeight: 700,
            fontSize: "19px",
            color: textColor,
            letterSpacing: "0.12em",
            textTransform: "uppercase",
            zIndex: 1,
            userSelect: "none",
          }}
        >
          {text}
        </span>
      </div>
    </div>
  );
};
```

---

### 3. Blueprint 3 : Moteur d'Essaim de Trombones Exponentiels (Paperclips Swarm Engine)

#### 3.1. Modèle Mathématique & Physique
Dans le plan 21 (frame 2854-3004), la métaphore de l'IA maximisatrice de trombones de Nick Bostrom est visualisée par une inondation exponentielle :
1. **Courbe de population exponentielle** :
   $$N(t) = N_0 \cdot 2^{\frac{t - t_0}{\tau}}$$
   où $\tau \approx 18\text{ frames}$ (doublement toutes les 0.6 secondes).
2. **Balistique particulaire 2D avec frottement de l'air** :
   Chaque trombone possède une position $\vec{p}$, une vitesse $\vec{v}$, une vitesse angulaire $\omega$ et un angle $\theta$ :
   $$\vec{v}_{t+1} = \vec{v}_t + \vec{g}\Delta t - \gamma \vec{v}_t \Delta t$$
   $$\theta_{t+1} = \theta_t + \omega_t \Delta t$$
   où $\vec{g} = (0, 980\text{ px/s}^2)$ et $\gamma = 0.08$ est le coefficient de traînée aérodynamique.
3. **Optimisation d'instanciation Canvas 2D** : Pré-rendu d'un sprite SVG de trombone haute définition dans un canevas hors-écran (`OffscreenCanvas`), puis multiplication via `ctx.drawImage` avec matrice de transformation affine unitaire.

#### 3.2. Implémentation Canvas 2D / Remotion

```typescript
// PaperclipSwarmEngine.ts
export interface PaperclipParticle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  angle: number;
  angularVelocity: number;
  scale: number;
  colorIdx: number; // Index palette riso
}

export class PaperclipSwarmEngine {
  private particles: PaperclipParticle[] = [];
  private spriteCanvas: HTMLCanvasElement;
  private colors = ["#1B2A4A", "#FF3366", "#2D9CDB", "#F4C430"];
  private rngSeed = 1337;

  constructor() {
    this.spriteCanvas = document.createElement("canvas");
    this.spriteCanvas.width = 64;
    this.spriteCanvas.height = 128;
    this.renderSprite();
  }

  private pseudoRandom(): number {
    this.rngSeed = (this.rngSeed * 9301 + 49297) % 233280;
    return this.rngSeed / 233280;
  }

  // Pré-génération vectorielle du trombone en mémoire
  private renderSprite() {
    const ctx = this.spriteCanvas.getContext("2d")!;
    ctx.clearRect(0, 0, 64, 128);
    ctx.lineWidth = 5;
    ctx.strokeStyle = "#1B2A4A";
    ctx.lineCap = "round";
    ctx.lineJoin = "round";

    // Tracé de trombone standard en boucle fermée
    ctx.beginPath();
    ctx.moveTo(22, 110);
    ctx.lineTo(22, 35);
    ctx.arc(32, 35, 10, Math.PI, 0, false);
    ctx.lineTo(42, 95);
    ctx.arc(32, 95, 10, 0, Math.PI, false);
    ctx.lineTo(22, 60);
    ctx.arc(27, 60, 5, Math.PI, 0, false);
    ctx.lineTo(32, 85);
    ctx.stroke();
  }

  // Émission exponentielle asservie à la frame Remotion
  public updateAndRender(
    ctx: CanvasRenderingContext2D,
    frame: number,
    startFrame: number,
    width = 1920,
    height = 1080
  ) {
    const elapsed = Math.max(0, frame - startFrame);
    if (elapsed === 0) return;

    // Calcul de l'accroissement exponentiel d'émission
    const spawnRate = Math.min(180, Math.floor(Math.pow(1.11, elapsed)));

    for (let i = 0; i < spawnRate; i++) {
      this.particles.push({
        x: this.pseudoRandom() * width,
        y: -40 - this.pseudoRandom() * 120,
        vx: (this.pseudoRandom() - 0.5) * 14,
        vy: 4 + this.pseudoRandom() * 18,
        angle: this.pseudoRandom() * Math.PI * 2,
        angularVelocity: (this.pseudoRandom() - 0.5) * 0.22,
        scale: 0.45 + this.pseudoRandom() * 0.55,
        colorIdx: Math.floor(this.pseudoRandom() * this.colors.length),
      });
    }

    const dt = 1.0;
    const gravity = 0.85;
    const airResistance = 0.985;

    // Mise à jour de l'état physique et affichage
    for (let i = 0; i < this.particles.length; i++) {
      const p = this.particles[i];
      p.vy = (p.vy + gravity) * airResistance;
      p.vx *= airResistance;
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      p.angle += p.angularVelocity;

      // Dessin avec translation et rotation instanciée
      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate(p.angle);
      ctx.scale(p.scale, p.scale);

      ctx.drawImage(this.spriteCanvas, -32, -64);
      ctx.restore();
    }

    // Purge des particules sorties du champ bas (+300px)
    if (this.particles.length > 5000) {
      this.particles = this.particles.filter((p) => p.y < height + 300);
    }
  }
}
```

---

### 4. Blueprint 4 : Tracé de Spline de Perte d'Entraînement & Suiveur de Tangente (Loss Follower)

#### 4.1. Modèle Mathématique & Physique
Dans le plan 13 (frame 1752-1902), une courbe de décroissance d'entropie croisée $\mathcal{L}(t)$ est tracée avec une mascotte qui glisse sur la tangente :
1. **Modèle de courbe de perte avec bruit d'échantillonnage de gradient** :
   $$\mathcal{L}(x) = L_{\text{min}} + (L_0 - L_{\text{min}}) \cdot e^{-\lambda x} + A_{\text{noise}} \sum_{k=1}^3 \frac{1}{k} \sin(\omega_k x)$$
   La courbe est convertie en une spline de Bézier cubique 2D continue $\mathcal{C}(u) = (x(u), y(u))$.
2. **Déploiement temporel par `strokeDashoffset`** :
   La longueur d'arc totale $S_{\text{tot}} = \int_0^1 \|\mathcal{C}'(u)\| du$ est calculée par quadrature de Gauss-Legendre ou via l'API SVG native `getTotalLength()`. Le décalage s'exprime par :
   $$\text{offset}(t) = S_{\text{tot}} \cdot (1 - \tau(t))$$
   où $\tau(t)$ est une interpolation sigmoïdale fluide.
3. **Position et orientation angulaire de la mascotte** :
   La position $\vec{P}(t) = \mathcal{C}(\tau(t))$ et la tangente unitaire $\vec{T}(t) = \frac{\mathcal{C}'(\tau(t))}{\|\mathcal{C}'(\tau(t))\|}$ donnent l'angle de tangage :
   $$\theta(t) = \text{atan2}(T_y(t), T_x(t))$$

#### 4.2. Composant SVG / Remotion

```tsx
// LossCurveFollower.tsx
import React, { useMemo, useRef, useEffect, useState } from "react";
import { interpolate, useCurrentFrame, Easing } from "remotion";

export interface LossCurveFollowerProps {
  startFrame: number;
  durationFrames: number;
  width?: number;
  height?: number;
}

export const LossCurveFollower: React.FC<LossCurveFollowerProps> = ({
  startFrame,
  durationFrames,
  width = 1200,
  height = 500,
}) => {
  const frame = useCurrentFrame();
  const pathRef = useRef<SVGPathElement>(null);
  const [totalLength, setTotalLength] = useState<number>(1800);

  // Définition géométrique de la courbe de perte exponentielle bruitée
  const pathData = useMemo(() => {
    const points: [number, number][] = [];
    const steps = 40;
    for (let i = 0; i <= steps; i++) {
      const u = i / steps;
      const x = 50 + u * (width - 100);
      // Décroissance exponentielle + micro-bruit SGD
      const decay = 380 * Math.exp(-u * 3.5);
      const noise = Math.sin(u * 28.0) * (8 * (1.0 - u * 0.7));
      const y = 80 + decay + noise;
      points.push([x, y]);
    }

    // Construction d'un tracé cubique Catmull-Rom vers Bézier
    let d = `M ${points[0][0]} ${points[0][1]}`;
    for (let i = 1; i < points.length; i++) {
      const prev = points[i - 1];
      const curr = points[i];
      const cx = (prev[0] + curr[0]) / 2;
      d += ` C ${cx} ${prev[1]}, ${cx} ${curr[1]}, ${curr[0]} ${curr[1]}`;
    }
    return d;
  }, [width]);

  // Mesure de la longueur réelle du path
  useEffect(() => {
    if (pathRef.current) {
      setTotalLength(pathRef.current.getTotalLength());
    }
  }, [pathData]);

  // Progression temporelle normalisée 0 -> 1
  const progress = interpolate(
    frame - startFrame,
    [0, durationFrames],
    [0, 1],
    {
      easing: Easing.bezier(0.16, 1, 0.3, 1),
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  // Calcul du point d'impact et de l'angle tangentiel
  const { currentX, currentY, tangentAngle } = useMemo(() => {
    if (!pathRef.current) return { currentX: 50, currentY: 460, tangentAngle: 0 };
    const dist = progress * totalLength;
    const pt = pathRef.current.getPointAtLength(dist);
    // Échantillonnage à +2px pour déterminer le vecteur directeur
    const ptAhead = pathRef.current.getPointAtLength(Math.min(totalLength, dist + 2));
    const angleRad = Math.atan2(ptAhead.y - pt.y, ptAhead.x - pt.x);
    return {
      currentX: pt.x,
      currentY: pt.y,
      tangentAngle: (angleRad * 180) / Math.PI,
    };
  }, [progress, totalLength]);

  const dashOffset = totalLength * (1 - progress);

  return (
    <div style={{ position: "relative", width, height }}>
      <svg width={width} height={height} style={{ overflow: "visible" }}>
        {/* Grille millimétrée de fond */}
        <defs>
          <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
            <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#E2D7BE" strokeWidth="1" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" opacity="0.6" />

        {/* Tracé de la courbe de perte */}
        <path
          ref={pathRef}
          d={pathData}
          fill="none"
          stroke="#FF3366"
          strokeWidth="6"
          strokeLinecap="round"
          strokeDasharray={totalLength}
          strokeDashoffset={dashOffset}
        />
      </svg>

      {/* Mascotte suiveuse le long de la spline */}
      <div
        style={{
          position: "absolute",
          left: currentX,
          top: currentY,
          transform: `translate(-50%, -85%) rotate(${tangentAngle}deg)`,
          transformOrigin: "center bottom",
          pointerEvents: "none",
        }}
      >
        {/* Sprite vectoriel mascotte fleur jaune */}
        <svg width="60" height="60" viewBox="0 0 60 60">
          <circle cx="30" cy="30" r="22" fill="#FFCC00" stroke="#1B2A4A" strokeWidth="4" />
          <circle cx="23" cy="26" r="3" fill="#1B2A4A" />
          <circle cx="37" cy="26" r="3" fill="#1B2A4A" />
          <path d="M 23 37 Q 30 43 37 37" fill="none" stroke="#1B2A4A" strokeWidth="3" strokeLinecap="round" />
        </svg>
      </div>
    </div>
  );
};
```

---

### 5. Blueprint 5 : Odomètre Électromécanique Décimal à Tambours Rotatifs (1E30 FLOP/s)

#### 5.1. Modèle Mathématique & Physique
Dans le plan 19 (frame 2553-2703), le calcul des FLOPs ($10^{30}$) est matérialisé par un rouleau mécanique vintage :
1. **Cinématique de bascule par décade** :
   Pour un chiffre à la position décimale $k$, sa rotation dépend de la partie entière et fractionnaire du ratio de division :
   $$\theta_k(t) = -36^\circ \cdot \left( \lfloor v_k(t) \rfloor + f(\text{frac}(v_k(t))) \right)$$
   où $f(x)$ est une fonction d'entraînement mécanique à engrenage croix de Malte (Geneva drive) : l'entraînement ne se produit que sur les derniers 15% de rotation de la décade précédente :
   $$f(x) = \begin{cases} 0 & \text{si } x < 0.85 \\ \frac{x - 0.85}{0.15} & \text{si } x \ge 0.85 \end{cases}$$
2. **Flou de mouvement stroboscopique (Motion Blur)** :
   Sur les rouleaux rapides ($k \in [0, 2]$), la vitesse angulaire dépasse la fréquence critique de fusion visuelle (120° par frame), introduisant une traînée verticale semi-transparente simulée en CSS `filter: blur(0px, 4px)`.

#### 5.2. Composant Remotion / CSS 3D Transforms

```tsx
// FlopsOdometer.tsx
import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

interface DigitWheelProps {
  value: number; // Valeur flottante continue
  height?: number;
}

const DigitWheel: React.FC<DigitWheelProps> = ({ value, height = 90 }) => {
  const digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0];
  const floorVal = Math.floor(value);
  const frac = value - floorVal;

  // Modèle croix de Malte : la bascule a lieu sur les 15% finals
  const mechanicalOffset = frac < 0.85 ? 0 : (frac - 0.85) / 0.15;
  const currentPos = (floorVal % 10) + mechanicalOffset;
  const translateY = -currentPos * height;

  // Calcul du flou cinétique proportionnel à la vitesse instantanée
  const isFastRolling = frac > 0.05 && frac < 0.95;

  return (
    <div
      style={{
        width: 60,
        height,
        overflow: "hidden",
        backgroundColor: "#1B2A4A",
        border: "3px solid #2D9CDB",
        borderRadius: 8,
        position: "relative",
        boxShadow: "inset 0 10px 15px rgba(0,0,0,0.6), inset 0 -10px 15px rgba(0,0,0,0.6)",
      }}
    >
      <div
        style={{
          transform: `translateY(${translateY}px)`,
          transition: "none",
          filter: isFastRolling ? "blur(0px 2.5px)" : "none",
        }}
      >
        {digits.map((d, index) => (
          <div
            key={index}
            style={{
              height,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontFamily: "'Chakra Petch', monospace",
              fontWeight: 700,
              fontSize: 64,
              color: "#FFCC00",
              textShadow: "0 0 10px rgba(255, 204, 0, 0.5)",
            }}
          >
            {d}
          </div>
        ))}
      </div>
    </div>
  );
};

export const FlopsOdometer: React.FC<{ startFrame: number }> = ({ startFrame }) => {
  const frame = useCurrentFrame();
  const elapsed = Math.max(0, frame - startFrame);

  // Accélération exponentielle du compteur
  const totalValue = interpolate(elapsed, [0, 150], [1e3, 1e12], {
    extrapolateRight: "clamp",
  });

  // Extraction des décades pour 6 tambours
  const d0 = totalValue % 10;
  const d1 = (totalValue / 10) % 10;
  const d2 = (totalValue / 100) % 10;
  const d3 = (totalValue / 1000) % 10;
  const d4 = (totalValue / 10000) % 10;
  const d5 = (totalValue / 100000) % 10;

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: 24,
        background: "#0D1B2A",
        border: "4px solid #FF3366",
        borderRadius: 16,
        boxShadow: "8px 8px 0px #1B2A4A",
      }}
    >
      <div
        style={{
          fontFamily: "'Space Mono', monospace",
          color: "#2D9CDB",
          fontSize: 18,
          marginBottom: 12,
          letterSpacing: "0.2em",
        }}
      >
        ACCUMULATED COMPUTE / FLOPs
      </div>
      <div style={{ display: "flex", gap: 8 }}>
        <DigitWheel value={d5} />
        <DigitWheel value={d4} />
        <DigitWheel value={d3} />
        <div style={{ fontSize: 60, color: "#F4EAD4", alignSelf: "center" }}>,</div>
        <DigitWheel value={d2} />
        <DigitWheel value={d1} />
        <DigitWheel value={d0} />
      </div>
      <div
        style={{
          marginTop: 14,
          fontFamily: "'Chakra Petch', sans-serif",
          color: "#FF3366",
          fontSize: 22,
          fontWeight: 700,
        }}
      >
        PEAK: 1.00e+30 OPS
      </div>
    </div>
  );
};
```

---

### 6. Blueprint 6 : Dislocation Particulaire en Demi-Teinte Riso (Atomic Rearrangement)

#### 6.1. Modèle Mathématique & Physique
Dans le plan 17 (frame 2252-2402) et la transition vers l'alignement, le corps de la chanteuse se disloque en millions de points risographes ("atoms rearranging") :
1. **Grille d'échantillonnage de luminance** :
   L'image source est projetée sur une matrice discrète de pas $S = 8\text{ px}$. Chaque cellule $(i, j)$ génère une particule si sa luminance $L_{i,j} < 0.85$. Le rayon initial de la particule vaut $r_{i,j} = \frac{S}{2} \sqrt{1 - L_{i,j}}$.
2. **Force de dérive brownienne & turbulence de Curl** :
   Chaque particule subit une force dissipative et un champ de vitesse de Perlin divergent nul $\vec{v}_{\text{curl}}(x, y) = (\frac{\partial \psi}{\partial y}, -\frac{\partial \psi}{\partial x})$ :
   $$\vec{P}_{t+1} = \vec{P}_t + \vec{v}_{\text{curl}}(\vec{P}_t) \cdot A(t) + \vec{\eta}_t$$
   où $\vec{\eta}_t \sim \mathcal{N}(0, \sigma^2)$ est un bruit gaussien blanc et $A(t)$ est une enveloppe d'amplitude en cloche :
   $$A(t) = \sin^2\left(\pi \frac{t - t_0}{T}\right)$$
3. **Restitution élastique vers la forme cible (Attractor Spring)** :
   En fin de phase ($t > t_0 + \frac{2}{3}T$), un champ d'attraction ramène chaque particule vers sa position d'ancrage $\vec{P}_{\text{orig}}$ avec amortissement critique.

#### 6.2. Implémentation Canvas 2D / TypeScript

```typescript
// AtomicDislocationEngine.ts
export interface RisoDotParticle {
  origX: number;
  origY: number;
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  color: string;
}

export class AtomicDislocationEngine {
  private particles: RisoDotParticle[] = [];
  private isInitialized = false;

  // Initialisation à partir d'un élément image ou vidéo
  public initFromImageData(
    ctx: CanvasRenderingContext2D,
    imageSource: CanvasImageSource,
    width: number,
    height: number,
    step = 7
  ) {
    const tempCanvas = document.createElement("canvas");
    tempCanvas.width = width;
    tempCanvas.height = height;
    const tempCtx = tempCanvas.getContext("2d")!;
    tempCtx.drawImage(imageSource, 0, 0, width, height);

    const imgData = tempCtx.getImageData(0, 0, width, height).data;
    this.particles = [];

    for (let y = 0; y < height; y += step) {
      for (let x = 0; x < width; x += step) {
        const idx = (y * width + x) * 4;
        const r = imgData[idx];
        const g = imgData[idx + 1];
        const b = imgData[idx + 2];
        const a = imgData[idx + 3];

        if (a > 50) {
          const lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
          if (lum < 0.9) {
            // Choix chromatique riso en fonction du ton dominant
            let color = "#1B2A4A"; // Marine
            if (r > 180 && g < 100) color = "#FF3366"; // Rose
            else if (r > 180 && g > 150 && b < 100) color = "#FFCC00"; // Jaune

            const dotRadius = (step / 2) * Math.sqrt(1 - lum);

            this.particles.push({
              origX: x,
              origY: y,
              x,
              y,
              vx: 0,
              vy: 0,
              radius: Math.max(1.2, dotRadius),
              color,
            });
          }
        }
      }
    }
    this.isInitialized = true;
  }

  // Boucle de mise à jour physique et rendu
  public render(
    ctx: CanvasRenderingContext2D,
    progress: number // De 0.0 (image intacte) à 1.0 (recomposée), pic de dispersion à 0.5
  ) {
    if (!this.isInitialized) return;

    // Enveloppe de dispersion en cloche (0 -> 1 -> 0)
    const dispersion = Math.sin(progress * Math.PI);
    const chaosForce = dispersion * 18.0;

    for (let i = 0; i < this.particles.length; i++) {
      const p = this.particles[i];

      if (progress < 0.5) {
        // Phase 1 : Explosion et répulsion brownienne
        const angle = Math.sin(p.origX * 0.05) + Math.cos(p.origY * 0.05) + i;
        p.vx += Math.cos(angle) * chaosForce * 0.15;
        p.vy += Math.sin(angle) * chaosForce * 0.15;
      } else {
        // Phase 2 : Force de rappel élastique vers la position d'origine
        const dx = p.origX - p.x;
        const dy = p.origY - p.y;
        const springK = 0.12;
        p.vx = (p.vx + dx * springK) * 0.82; // Amorti 0.82
        p.vy = (p.vy + dy * springK) * 0.82;
      }

      p.x += p.vx;
      p.y += p.vy;

      // Dessin du point riso
      ctx.fillStyle = p.color;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fill();
    }
  }
}
```

---

### Synthèse d'Intégration & Recette de Fabrication
1. **Ordre de composition des calques (Render Tree)** :
   `Fond Papier Vergé (#F4EAD4)` $\rightarrow$ `Éléments Vectoriels SVG / Canvas` $\rightarrow$ `Composants Washi Tape` $\rightarrow$ `Shader Riso Halftone Post-Process (Blueprint 1)`.
2. **Cadence d'échantillonnage temporelle** : Tous les calculs utilisent la frame absolue Remotion synchronisée sur la base temporelle $1\text{ beat} = 12.54\text{ frames}$ (143.55 BPM).
3. **Respect strict des tokens** : Aucun dégradé standard Tailwind, toutes les teintes et décalages d'encre répondent aux spécifications fixées dans `01_GLOBAL_DA_AND_SYSTEM.md`.
