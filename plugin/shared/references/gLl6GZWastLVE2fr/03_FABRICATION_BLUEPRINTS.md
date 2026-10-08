# 03. Blueprints de Fabrication & Recettes de Code

Ce document fournit aux développeurs et agents de fabrication (Remotion, React, Three.js, Canvas 2D, SVG) les algorithmes exacts, équations mathématiques et composants TypeScript typés pour reproduire fidèlement les cinq systèmes cinématiques majeurs de la vidéo.

---

## 1. Moteur 1 : Grille Rythmique Déterministe & HUD Télémétrique (Remotion / React)

Rôle : Piloter la pulsation à 128 BPM, afficher les repères viewfinder `[ ]`, le métronome `BEAT ■□□□`, le numéro de mesure `BAR X/8`, et le compteur de frame `FRAME XXXX / 0900` sans dérive d'horloge.

### Principe Mathématique
- Un tempo de 128.0 BPM à 60.0 fps équivaut à `framesPerBeat = 60 * 60 / 128 = 28.125` frames.
- Une mesure (4 temps) compte `framesPerBar = 28.125 * 4 = 112.5` frames.
- La mesure courante est `barIndex = Math.min(8, Math.floor(frame / 112.5) + 1)`.
- Le beat courant dans la mesure est `beatIndex = Math.floor((frame % 112.5) / 28.125)`.
- L'impulsion élastique de beat s'exprime par une décroissance exponentielle : `scale = 1 + 0.12 * Math.exp(-progress * 4)`.

### Implémentation TypeScript (Remotion)

```tsx
import React from 'react';
import { useCurrentFrame } from 'remotion';

export interface HudOverlayProps {
  bpm?: number;
  fps?: number;
  totalFrames?: number;
  theme?: 'dark' | 'light';
}

export const HudOverlay: React.FC<HudOverlayProps> = ({
  bpm = 128,
  fps = 60,
  totalFrames = 900,
  theme = 'dark',
}) => {
  const frame = useCurrentFrame();

  const framesPerBeat = (fps * 60) / bpm; // 28.125
  const framesPerBar = framesPerBeat * 4;  // 112.5

  const currentBar = Math.min(8, Math.floor(frame / framesPerBar) + 1);
  const currentBeatInBar = Math.floor((frame % framesPerBar) / framesPerBeat); // 0, 1, 2, 3

  const beatProgress = ((frame % framesPerBeat) / framesPerBeat);
  const pulseScale = 1 + 0.15 * Math.exp(-beatProgress * 5);

  const isDark = theme === 'dark';
  const textColor = isDark ? '#FFFFFF' : '#0F0F11';
  const mutedColor = isDark ? 'rgba(255, 255, 255, 0.45)' : 'rgba(15, 15, 17, 0.45)';
  const cornerColor = isDark ? 'rgba(255, 255, 255, 0.35)' : 'rgba(15, 15, 17, 0.35)';

  const beatSymbols = ['□', '□', '□', '□'];
  beatSymbols[currentBeatInBar] = '■';

  const formattedFrame = String(frame).padStart(4, '0');
  const formattedTotal = String(totalFrames).padStart(4, '0');

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        pointerEvents: 'none',
        fontFamily: 'JetBrains Mono, monospace',
        color: textColor,
        boxSizing: 'border-box',
      }}
    >
      {/* Coins Viewfinder [ ] à 36px du bord */}
      <svg
        style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }}
        viewBox="0 0 1920 1080"
      >
        <path
          d="
            M 36 54 L 36 36 L 54 36
            M 1866 36 L 1884 36 L 1884 54
            M 36 1026 L 36 1044 L 54 1044
            M 1866 1044 L 1884 1044 L 1884 1026
          "
          fill="none"
          stroke={cornerColor}
          strokeWidth="1.5"
        />
      </svg>

      {/* Header gauche : Titre de projet */}
      <div
        style={{
          position: 'absolute',
          top: 48,
          left: 48,
          fontSize: 13,
          letterSpacing: '0.08em',
          color: mutedColor,
          textTransform: 'uppercase',
        }}
      >
        CLAUDE MOTION REEL 2026
      </div>

      {/* Header droite : Mesure et BPM */}
      <div
        style={{
          position: 'absolute',
          top: 48,
          right: 48,
          fontSize: 13,
          letterSpacing: '0.08em',
          fontWeight: 700,
          color: textColor,
        }}
      >
        BAR {currentBar}/8 &nbsp;&nbsp; {bpm} BPM
      </div>

      {/* Footer gauche : Métronome Beat interactif */}
      <div
        style={{
          position: 'absolute',
          bottom: 48,
          left: 48,
          fontSize: 13,
          letterSpacing: '0.12em',
          color: textColor,
          display: 'flex',
          alignItems: 'center',
          gap: 6,
          transform: `scale(${pulseScale})`,
          transformOrigin: 'left center',
        }}
      >
        <span style={{ color: mutedColor }}>BEAT</span>
        <span>{beatSymbols.join(' ')}</span>
      </div>

      {/* Footer droite : Compteur de frame absolu */}
      <div
        style={{
          position: 'absolute',
          bottom: 48,
          right: 48,
          fontSize: 13,
          letterSpacing: '0.08em',
          fontVariantNumeric: 'tabular-nums',
          color: mutedColor,
        }}
      >
        FRAME <span style={{ color: textColor, fontWeight: 700 }}>{formattedFrame}</span> / {formattedTotal}
      </div>
    </div>
  );
};
```

---

## 2. Moteur 2 : Morphing Géométrique Poly-Forme & Traînée de Ghosting (Canvas 2D)

Rôle : Rendre la séquence de la Bar 3 (disque rouge -> carré bleu arrondi -> fleur jaune), avec boîte englobante orientée et rémanence temporelle multi-passes.

### Principe Mathématique
- Une forme polygonale à $N$ côtés peut être paramétrée en coordonnées polaires régulières.
- Le morphing entre un cercle ($r(\theta) = R$), un carré arrondi ($r(\theta) = R / \max(|\cos \theta|, |\sin \theta|)$ avec coin lissé) et une fleur à 4 lobes ($r(\theta) = R (1 + 0.35 \cos(4\theta))$) est une interpolation linéaire vectorielle de rayon polaire :
  $$r(\theta, t) = (1 - t) \cdot r_A(\theta) + t \cdot r_B(\theta)$$
- Le ghosting est calculé par une pile FIFO de poses passées : pour chaque pas $k \in \{1..4\}$, rendu de la géométrie passée avec opacité décroissante $\alpha_k = \alpha_0 \cdot 0.3^k$.

### Implémentation TypeScript (Canvas 2D)

```typescript
export type ShapeKind = 'CIRCLE' | 'SQUARE' | 'FLOWER';

export interface GhostPose {
  x: number;
  y: number;
  rotation: number;
  radius: number;
  shape: ShapeKind;
  color: string;
}

export class GeometricMorphEngine {
  private history: GhostPose[] = [];
  private readonly maxGhosts = 4;

  // Calcul du rayon polaire selon la forme
  private getRadius(angle: number, baseRadius: number, shape: ShapeKind): number {
    if (shape === 'CIRCLE') {
      return baseRadius;
    }
    if (shape === 'SQUARE') {
      const cosA = Math.cos(angle);
      const sinA = Math.sin(angle);
      // Approximation lissée de p-norme pour carré aux coins adoucis
      const p = 4;
      const d = Math.pow(Math.abs(cosA), p) + Math.pow(Math.abs(sinA), p);
      return baseRadius * Math.pow(d, -1 / p);
    }
    if (shape === 'FLOWER') {
      // 4 lobes sinusoïdaux
      return baseRadius * (0.8 + 0.28 * Math.cos(4 * angle));
    }
    return baseRadius;
  }

  // Tracé sur Canvas
  private drawShape(
    ctx: CanvasRenderingContext2D,
    pose: GhostPose,
    opacity: number
  ) {
    const { x, y, rotation, radius, shape, color } = pose;
    const samples = 120;

    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rotation);
    ctx.globalAlpha = opacity;
    ctx.fillStyle = color;

    ctx.beginPath();
    for (let i = 0; i < samples; i++) {
      const theta = (i / samples) * Math.PI * 2;
      const r = this.getRadius(theta, radius, shape);
      const px = Math.cos(theta) * r;
      const py = Math.sin(theta) * r;
      if (i === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
    ctx.closePath();
    ctx.fill();

    ctx.restore();
  }

  // Rendu complet avec boîte englobante et traînée
  render(
    ctx: CanvasRenderingContext2D,
    currentPose: GhostPose
  ) {
    // 1. Rendu des poses passées (ghosting)
    for (let i = 0; i < this.history.length; i++) {
      const ghost = this.history[i];
      const ghostAlpha = 0.35 * Math.pow(0.4, this.history.length - i);
      this.drawShape(ctx, ghost, ghostAlpha);
    }

    // 2. Mémorisation de la pose courante dans l'historique
    this.history.push({ ...currentPose });
    if (this.history.length > this.maxGhosts) {
      this.history.shift();
    }

    // 3. Rendu de la forme active
    this.drawShape(ctx, currentPose, 1.0);

    // 4. Dessin de la boîte englobante orientée (Oriented Bounding Box)
    const { x, y, rotation, radius, shape } = currentPose;
    const boxSize = radius * 2.3;

    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rotation);

    // Cadre filaire blanc fin
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.4)';
    ctx.lineWidth = 1;
    ctx.strokeRect(-boxSize / 2, -boxSize / 2, boxSize, boxSize);

    // Coins à 90 degrés
    ctx.strokeStyle = '#FFFFFF';
    ctx.lineWidth = 2;
    const corner = 12;
    const hs = boxSize / 2;

    // Coin haut-gauche
    ctx.beginPath();
    ctx.moveTo(-hs, -hs + corner);
    ctx.lineTo(-hs, -hs);
    ctx.lineTo(-hs + corner, -hs);
    ctx.stroke();

    // Rétablir la rotation pour dessiner les labels HUD à l'horizontale
    ctx.rotate(-rotation);
    ctx.font = '11px JetBrains Mono, monospace';
    ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
    const deg = (((rotation * 180) / Math.PI) % 360).toFixed(1).padStart(5, '0');
    ctx.fillText(`ROT ${deg}°`, -hs, -hs - 8);
    ctx.fillText(`SHAPE ${shape}`, -hs, hs + 18);

    ctx.restore();
  }
}
```

---

## 3. Moteur 3 : Transition Phyllotaxie de Fibonacci vers Grille Cartésienne & Onde (Canvas 2D)

Rôle : Assurer la métamorphose de la Bar 4 entre la rosace en spirale d'or et la matrice de points orthogonale 2D balayée par l'onde rouge corail.

### Principe Mathématique
1. **Phyllotaxie de Fibonacci (Pose A)** :
   Pour chaque point $n \in [0, N-1]$ :
   $$\theta_n = n \times 137.507764^\circ, \quad r_n = c \cdot \sqrt{n}$$
   $$X_{A, n} = x_0 + r_n \cos(\theta_n), \quad Y_{A, n} = y_0 + r_n \sin(\theta_n)$$
2. **Grille Cartésienne (Pose B)** :
   Pour une grille de $C$ colonnes et $L$ lignes :
   $$col = n \pmod C, \quad row = \lfloor n / C \rfloor$$
   $$X_{B, n} = x_{\min} + col \cdot \Delta x, \quad Y_{B, n} = y_{\min} + row \cdot \Delta y$$
3. **Interpolation avec Stagger Radial** :
   Le départ de chaque particule est décalé selon son rayon $r_n$ :
   $$t_n = \text{clamp}\left(\frac{t - (r_n / r_{\max}) \cdot 0.3}{0.7}, 0, 1\right)$$
4. **Onde Colonne Transversale Rouge** :
   Une onde de position $x_{\text{wave}}(t) = x_{\min} + (x_{\max} - x_{\min}) \cdot t_{\text{wave}}$ traverse la grille. Tout point à proximité $|X_n - x_{\text{wave}}| < \sigma$ subit une élévation $\Delta y_n = -A \exp\left(-\frac{(X_n - x_{\text{wave}})^2}{2\sigma^2}\right)$ et vire au rouge corail `#EB4432`.

### Implémentation TypeScript

```typescript
export interface MatrixPoint {
  id: number;
  originX: number; // Phyllotaxie
  originY: number;
  targetX: number; // Grille
  targetY: number;
  delayFactor: number;
}

export class PhyllotaxisToGridEngine {
  private points: MatrixPoint[] = [];
  private readonly numPoints = 600;

  constructor(width = 1920, height = 1080) {
    const c = 18; // Facteur d'échelle phyllotaxie
    const phi = 137.507764 * (Math.PI / 180);
    const centerX = width / 2;
    const centerY = height / 2;

    const cols = 30;
    const rows = 20;
    const gridSpacingX = (width - 240) / (cols - 1);
    const gridSpacingY = (height - 240) / (rows - 1);
    const startX = 120;
    const startY = 120;

    let maxDist = 0;

    for (let i = 0; i < this.numPoints; i++) {
      const r = c * Math.sqrt(i);
      const theta = i * phi;
      const ox = centerX + r * Math.cos(theta);
      const oy = centerY + r * Math.sin(theta);

      const col = i % cols;
      const row = Math.floor(i / cols);
      const tx = startX + col * gridSpacingX;
      const ty = startY + row * gridSpacingY;

      const dist = Math.hypot(ox - centerX, oy - centerY);
      if (dist > maxDist) maxDist = dist;

      this.points.push({
        id: i,
        originX: ox,
        originY: oy,
        targetX: tx,
        targetY: ty,
        delayFactor: dist,
      });
    }

    // Normalisation des délais
    this.points.forEach((p) => {
      p.delayFactor = p.delayFactor / (maxDist || 1);
    });
  }

  render(
    ctx: CanvasRenderingContext2D,
    morphProgress: number, // 0 = phyllotaxie, 1 = grille cartésienne
    waveProgress: number   // 0 à 1 (balayage gauche -> droite)
  ) {
    const screenWidth = 1920;
    const waveX = 100 + waveProgress * (screenWidth - 200);
    const waveWidth = 80;

    for (const p of this.points) {
      // Calcul du morphing individuel avec stagger
      const localProgress = Math.max(
        0,
        Math.min(1, (morphProgress - p.delayFactor * 0.35) / 0.65)
      );
      // Easing expo out
      const ease = 1 - Math.pow(2, -10 * localProgress);

      let currentX = p.originX + (p.targetX - p.originX) * ease;
      let currentY = p.originY + (p.targetY - p.originY) * ease;

      // Interaction avec l'onde transversale (active quand la grille est formée)
      let color = '#0F0F11';
      let radius = 2.5;

      if (morphProgress >= 0.8 && waveProgress > 0 && waveProgress < 1) {
        const dx = currentX - waveX;
        const dist = Math.abs(dx);
        if (dist < waveWidth) {
          const factor = Math.cos((dist / waveWidth) * (Math.PI / 2));
          currentY -= factor * 18; // Déplacement vertical
          radius += factor * 2;
          color = '#EB4432'; // Rouge corail
        }
      }

      ctx.beginPath();
      ctx.arc(currentX, currentY, radius, 0, Math.PI * 2);
      ctx.fillStyle = color;
      ctx.fill();
    }
  }
}
```

---

## 4. Moteur 4 : Nuage de Points 3D & Morphing Topologique Multi-Cibles (Three.js / WebGL)

Rôle : Rendre la séquence de la Bar 5 sur fond bleu cobalt (`#2644EB`) où les points se transforment de terrain topologique ondulant en sphère de Fibonacci, puis en tore d'accrétion et enfin en cube 3D.

### Principe Mathématique
Le nuage comprend $N = 1200$ particules. Chaque sommet possède 4 positions vectorielles dans l'espace $\mathbb{R}^3$ précalculées :
1. **Terrain ondulant ($P_1$)** : Grille plane $X, Z \in [-10, 10]$, altitude $Y = 1.2 \sin(0.8 X) \cos(0.8 Z)$.
2. **Sphère de Fibonacci ($P_2$)** :
   $$Y_i = 1 - \frac{2i}{N-1}, \quad r_i = \sqrt{1 - Y_i^2}, \quad \theta_i = i \cdot \pi (3 - \sqrt{5})$$
   $$X_i = R_s \cdot r_i \cos \theta_i, \quad Z_i = R_s \cdot r_i \sin \theta_i, \quad Y_i = R_s \cdot Y_i$$
3. **Tore d'accrétion ($P_3$)** :
   $$u_i = 2\pi (i / N_{\text{ring}}), \quad v_i = 2\pi (i \pmod{N_{\text{ring}}}) / N_{\text{ring}}$$
   $$X_i = (R + r \cos v_i) \cos u_i, \quad Y_i = r \sin v_i, \quad Z_i = (R + r \cos v_i) \sin u_i$$
4. **Cube filaire ($P_4$)** : Répartition uniforme sur les 12 arêtes du cube $[-L, L]^3$.

### Implémentation TypeScript (Three.js)

```typescript
import * as THREE from 'three';

export class PointCloudMorphScene {
  public scene: THREE.Scene;
  public camera: THREE.PerspectiveCamera;
  private pointsMesh: THREE.Points;
  private numPoints = 1200;

  // Buffers de position des 4 formes cibles
  private targetTerrain: Float32Array;
  private targetSphere: Float32Array;
  private targetTorus: Float32Array;
  private targetCube: Float32Array;

  constructor() {
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color('#2644EB'); // Fond bleu cobalt

    this.camera = new THREE.PerspectiveCamera(45, 1920 / 1080, 0.1, 1000);
    this.camera.position.set(0, 15, 30);
    this.camera.lookAt(0, 0, 0);

    const N = this.numPoints;
    this.targetTerrain = new Float32Array(N * 3);
    this.targetSphere = new Float32Array(N * 3);
    this.targetTorus = new Float32Array(N * 3);
    this.targetCube = new Float32Array(N * 3);

    this.computeTargets();

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(new Float32Array(this.targetTerrain), 3));

    // Couleurs de points : 90% blanc, 10% jaune ambre
    const colors = new Float32Array(N * 3);
    const white = new THREE.Color('#FFFFFF');
    const yellow = new THREE.Color('#F5CE38');

    for (let i = 0; i < N; i++) {
      const isYellow = Math.random() < 0.12;
      const c = isYellow ? yellow : white;
      colors[i * 3] = c.r;
      colors[i * 3 + 1] = c.g;
      colors[i * 3 + 2] = c.b;
    }
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
      size: 0.35,
      vertexColors: true,
      transparent: true,
      opacity: 0.95,
    });

    this.pointsMesh = new THREE.Points(geometry, material);
    this.scene.add(this.pointsMesh);
  }

  private computeTargets() {
    const N = this.numPoints;

    // 1. Terrain
    const side = Math.floor(Math.sqrt(N));
    let idx = 0;
    for (let r = 0; r < side; r++) {
      for (let c = 0; c < side; c++) {
        const x = (c / (side - 1) - 0.5) * 20;
        const z = (r / (side - 1) - 0.5) * 20;
        const y = 1.4 * Math.sin(x * 0.6) * Math.cos(z * 0.6);
        this.targetTerrain[idx * 3] = x;
        this.targetTerrain[idx * 3 + 1] = y;
        this.targetTerrain[idx * 3 + 2] = z;
        idx++;
      }
    }

    // 2. Sphère de Fibonacci
    const phi = Math.PI * (3 - Math.sqrt(5)); // Golden angle
    const sphereRadius = 6.5;
    for (let i = 0; i < N; i++) {
      const y = 1 - (i / (N - 1)) * 2;
      const radiusAtY = Math.sqrt(1 - y * y);
      const theta = phi * i;
      this.targetSphere[i * 3] = Math.cos(theta) * radiusAtY * sphereRadius;
      this.targetSphere[i * 3 + 1] = y * sphereRadius;
      this.targetSphere[i * 3 + 2] = Math.sin(theta) * radiusAtY * sphereRadius;
    }

    // 3. Tore
    const R = 6.0; // Grand rayon
    const rTube = 2.2; // Petit rayon
    for (let i = 0; i < N; i++) {
      const u = (i / N) * Math.PI * 2 * 6; // Enroulements
      const v = (i / N) * Math.PI * 2;
      this.targetTorus[i * 3] = (R + rTube * Math.cos(v)) * Math.cos(u);
      this.targetTorus[i * 3 + 1] = rTube * Math.sin(v);
      this.targetTorus[i * 3 + 2] = (R + rTube * Math.cos(v)) * Math.sin(u);
    }

    // 4. Arêtes de Cube
    const L = 5.0;
    const edgeCount = 12;
    const pointsPerEdge = Math.floor(N / edgeCount);
    let pt = 0;
    for (let e = 0; e < edgeCount && pt < N; e++) {
      for (let k = 0; k < pointsPerEdge && pt < N; k++) {
        const t = (k / pointsPerEdge) * 2 - 1; // [-1, 1]
        let cx = 0, cy = 0, cz = 0;
        // Définition des 12 arêtes
        if (e === 0) { cx = t * L; cy = -L; cz = -L; }
        else if (e === 1) { cx = t * L; cy = L; cz = -L; }
        else if (e === 2) { cx = t * L; cy = -L; cz = L; }
        else if (e === 3) { cx = t * L; cy = L; cz = L; }
        else if (e === 4) { cx = -L; cy = t * L; cz = -L; }
        else if (e === 5) { cx = L; cy = t * L; cz = -L; }
        else if (e === 6) { cx = -L; cy = t * L; cz = L; }
        else if (e === 7) { cx = L; cy = t * L; cz = L; }
        else if (e === 8) { cx = -L; cy = -L; cz = t * L; }
        else if (e === 9) { cx = L; cy = -L; cz = t * L; }
        else if (e === 10) { cx = -L; cy = L; cz = t * L; }
        else { cx = L; cy = L; cz = t * L; }

        this.targetCube[pt * 3] = cx;
        this.targetCube[pt * 3 + 1] = cy;
        this.targetCube[pt * 3 + 2] = cz;
        pt++;
      }
    }
  }

  // Interpolation de morphing selon le temps (bar 5 progress 0 -> 4)
  update(stageProgress: number, rotationY: number) {
    const positions = this.pointsMesh.geometry.attributes.position.array as Float32Array;
    const N = this.numPoints;

    // Détermination de la source et cible selon l'étape de beat
    let from = this.targetTerrain;
    let to = this.targetSphere;
    let t = stageProgress; // [0, 1]

    if (stageProgress >= 1 && stageProgress < 2) {
      from = this.targetSphere;
      to = this.targetTorus;
      t = stageProgress - 1;
    } else if (stageProgress >= 2) {
      from = this.targetTorus;
      to = this.targetCube;
      t = Math.min(1, stageProgress - 2);
    }

    const ease = 1 - Math.pow(2, -10 * t);

    for (let i = 0; i < N * 3; i++) {
      positions[i] = from[i] + (to[i] - from[i]) * ease;
    }

    this.pointsMesh.geometry.attributes.position.needsUpdate = true;
    this.pointsMesh.rotation.y = rotationY;
  }
}
```

---

## 5. Moteur 5 : Anneaux Typographiques en Coordonnées Polaires (SVG / Remotion)

Rôle : Rendre les 4 anneaux concentriques de texte défilant de la Bar 7 en rotation orbitale alternée avec alternance plein/filaire et puces corail.

### Principe Mathématique
- 4 trajectoires circulaires concentriques SVG `<path>` de rayons $R \in [140, 220, 300, 380]$.
- Chaque texte est couplé au chemin via `<textPath href="#circle-...">`.
- L'attribut `startOffset` est incrémenté en fonction de la vitesse angulaire $\omega_k$ et de la direction $\pm 1$ :
  $$\text{offset}_k(t) = (t \cdot v_k \cdot \text{direction}_k) \pmod{2\pi R_k}$$
- Anneaux 1 et 3 : `fill="#FFFFFF"`, `stroke="none"`.
- Anneaux 2 et 4 : `fill="none"`, `stroke="#FFFFFF"`, `strokeWidth="1.5"`.

### Implémentation TypeScript (Remotion / SVG)

```tsx
import React from 'react';
import { useCurrentFrame } from 'remotion';

export interface ConcentricTextRingsProps {
  centerX?: number;
  centerY?: number;
}

export const ConcentricTextRings: React.FC<ConcentricTextRingsProps> = ({
  centerX = 960,
  centerY = 540,
}) => {
  const frame = useCurrentFrame();

  const rings = [
    {
      id: 'ring-1',
      radius: 140,
      text: 'MOTION DESIGN • ANIMATION • ART DIRECTION • ',
      speed: 2.4,
      direction: 1,
      outlined: false,
    },
    {
      id: 'ring-2',
      radius: 220,
      text: 'TYPOGRAPHY • 3D • ILLUSTRATION • CODE • ',
      speed: 1.8,
      direction: -1,
      outlined: true,
    },
    {
      id: 'ring-3',
      radius: 300,
      text: 'RHYTHM • TIMING • EASING • KINETICS • FRAME • ',
      speed: 1.4,
      direction: 1,
      outlined: false,
    },
    {
      id: 'ring-4',
      radius: 380,
      text: 'LINE • COLOR • SHAPE • COMPOSITION • FORM • ',
      speed: 1.0,
      direction: -1,
      outlined: true,
    },
  ];

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        backgroundColor: '#0F0F11',
        overflow: 'hidden',
      }}
    >
      <svg
        width="100%"
        height="100%"
        viewBox="0 0 1920 1080"
        style={{ position: 'absolute', inset: 0 }}
      >
        <defs>
          {rings.map((ring) => {
            const r = ring.radius;
            // Tracé d'un cercle fermé parfait
            const d = `
              M ${centerX} ${centerY - r}
              A ${r} ${r} 0 1 1 ${centerX} ${centerY + r}
              A ${r} ${r} 0 1 1 ${centerX} ${centerY - r}
            `;
            return <path key={ring.id} id={ring.id} d={d} fill="none" />;
          })}
        </defs>

        {/* 4 Anneaux de texte rotatifs */}
        {rings.map((ring) => {
          const circumference = 2 * Math.PI * ring.radius;
          const offset = (frame * ring.speed * ring.direction) % circumference;

          // Répétition de la chaîne pour garnir le tour complet
          const repeatedText = (ring.text + ' ').repeat(5);

          return (
            <text
              key={`text-${ring.id}`}
              style={{
                fontFamily: 'Founders Grotesk, Druk Wide, sans-serif',
                fontSize: ring.radius > 250 ? 22 : 18,
                fontWeight: 900,
                letterSpacing: '0.14em',
                textTransform: 'uppercase',
              }}
              fill={ring.outlined ? 'none' : '#FFFFFF'}
              stroke={ring.outlined ? '#FFFFFF' : 'none'}
              strokeWidth={ring.outlined ? 1.5 : 0}
            >
              <textPath
                href={`#${ring.id}`}
                startOffset={`${offset}px`}
              >
                {repeatedText}
              </textPath>
            </text>
          );
        })}

        {/* Atome rouge corail central */}
        <circle
          cx={centerX}
          cy={centerY}
          r={9}
          fill="#EB4432"
        />
      </svg>
    </div>
  );
};
```
