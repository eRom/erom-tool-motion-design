# 03. Blueprints de Fabrication & Recettes de Code

Ce guide fournit aux agents développeurs (Remotion, WebGL/Three.js, Canvas 2D, SVG) les équations physiques, algorithmes et architectures logicielles nécessaires pour reproduire fidèlement les sept briques visuelles maîtresses de la vidéo `minchoi-check-out.mp4`.

---

## 1. Moteur 1 : Projection & Rotation 4D d'Hypercube (Tesseract Wireframe)

Utilisé pour : La matérialisation technologique à `00:08` (Séquence 03) et le manifeste humain à `00:50` (Séquence 14).

### 1.1. Principe Mathématique
Un tesseract (hypercube à 4 dimensions) est défini par 16 sommets dans $\mathbb{R}^4$ :
$$V_i = (\pm 1, \pm 1, \pm 1, \pm 1), \quad i \in \{0, \dots, 15\}$$
Deux sommets sont reliés par une arête si et seulement si ils ne diffèrent que d'une seule coordonnée (soit 32 arêtes au total).

Pour l'animer, on applique une double rotation appartenant au groupe de Lie $\text{SO}(4)$ dans les plans $XW$ et $YZ$ :
$$R_{XW}(\theta) = \begin{pmatrix} \cos\theta & 0 & 0 & -\sin\theta \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ \sin\theta & 0 & 0 & \cos\theta \end{pmatrix}, \quad R_{YZ}(\phi) = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & \cos\phi & -\sin\phi & 0 \\ 0 & \sin\phi & \cos\phi & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}$$

On projette ensuite le point $P_4 = (x, y, z, w)$ de la 4D vers la 3D via une projection stéréographique ou perspective avec une distance focale $d_w > 1$ :
$$P_3 = \left( \frac{x}{d_w - w}, \frac{y}{d_w - w}, \frac{z}{d_w - w} \right)$$
Puis on projette $P_3$ sur le plan 2D de la caméra Three.js / Canvas.

### 1.2. Implémentation de Référence (TypeScript / Three.js & Remotion)

```typescript
import * as THREE from 'three';

export class Tesseract4DEngine {
  private vertices4D: number[][] = [];
  private edges: [number, number][] = [];
  public linesMesh: THREE.LineSegments;
  public nodesMesh: THREE.InstancedMesh;

  constructor(private dw: number = 2.4, private scale: number = 180) {
    // 1. Génération des 16 sommets 4D
    for (let i = 0; i < 16; i++) {
      this.vertices4D.push([
        (i & 1 ? 1 : -1),
        (i & 2 ? 1 : -1),
        (i & 4 ? 1 : -1),
        (i & 8 ? 1 : -1),
      ]);
    }

    // 2. Génération des 32 arêtes
    for (let i = 0; i < 16; i++) {
      for (let j = i + 1; j < 16; j++) {
        let diff = 0;
        for (let k = 0; k < 4; k++) {
          if (this.vertices4D[i][k] !== this.vertices4D[j][k]) diff++;
        }
        if (diff === 1) this.edges.push([i, j]);
      }
    }

    // 3. Maillages Three.js
    const lineGeo = new THREE.BufferGeometry();
    const positions = new Float32Array(this.edges.length * 2 * 3);
    lineGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));

    const lineMat = new THREE.LineBasicMaterial({
      color: 0x5DFF26,
      transparent: true,
      opacity: 0.95,
      blending: THREE.AdditiveBlending,
    });
    this.linesMesh = new THREE.LineSegments(lineGeo, lineMat);

    const sphereGeo = new THREE.SphereGeometry(3.5, 8, 8);
    const sphereMat = new THREE.MeshBasicMaterial({
      color: 0xC4FF93,
      blending: THREE.AdditiveBlending,
    });
    this.nodesMesh = new THREE.InstancedMesh(sphereGeo, sphereMat, 16);
  }

  public update(thetaXW: number, phiYZ: number) {
    const projected3D: THREE.Vector3[] = [];
    const dummy = new THREE.Object3D();

    for (let i = 0; i < 16; i++) {
      let [x, y, z, w] = this.vertices4D[i];

      // Rotation dans le plan XW
      const rx = x * Math.cos(thetaXW) - w * Math.sin(thetaXW);
      const rw = x * Math.sin(thetaXW) + w * Math.cos(thetaXW);
      x = rx;
      w = rw;

      // Rotation dans le plan YZ
      const ry = y * Math.cos(phiYZ) - z * Math.sin(phiYZ);
      const rz = y * Math.sin(phiYZ) + z * Math.cos(phiYZ);
      y = ry;
      z = rz;

      // Projection perspective 4D -> 3D
      const distance = this.dw - w;
      const factor = this.scale / Math.max(distance, 0.1);
      const p3 = new THREE.Vector3(x * factor, y * factor, z * factor);
      projected3D.push(p3);

      // Mise à jour des sommets sphériques incandescents
      dummy.position.copy(p3);
      dummy.updateMatrix();
      this.nodesMesh.setMatrixAt(i, dummy.matrix);
    }
    this.nodesMesh.instanceMatrix.needsUpdate = true;

    // Mise à jour des positions des segments
    const posAttr = this.linesMesh.geometry.attributes.position as THREE.BufferAttribute;
    const array = posAttr.array as Float32Array;
    let ptr = 0;
    for (const [idxA, idxB] of this.edges) {
      const vA = projected3D[idxA];
      const vB = projected3D[idxB];
      array[ptr++] = vA.x; array[ptr++] = vA.y; array[ptr++] = vA.z;
      array[ptr++] = vB.x; array[ptr++] = vB.y; array[ptr++] = vB.z;
    }
    posAttr.needsUpdate = true;
  }
}
```

---

## 2. Moteur 2 : Vortex Gravitationnel & Trou Noir de Cartes Tâches (N-Body Ingestion)

Utilisé pour : L'ingestion des micro-tâches répétitives à `00:16 - 00:20` (Séquence 05).

### 2.1. Principe Physique
Les cartes de tâches sont modélisées comme des corps soumis à un champ gravitationnel central couplé à une force d'entraînement azimutale (vortex de type tornade ou trou noir de Kerr) :
1. **Accélération radiale** : $a_r = -\frac{G \cdot M}{r^2} - k_{\text{drag}} \cdot v_r$.
2. **Vitesse tangentielle** : $v_\theta = \frac{\omega_0}{r^{0.5}}$ (conservation approchée du moment cinétique).
3. **Réduction d'échelle et vaporisation** : $Scale(r) = \min(1.0, \frac{r}{r_{\text{threshold}}})$, avec émission de poussières de particules vertes lorsque $r < r_{\text{threshold}}$.

### 2.2. Algorithme Frame-par-Frame (Canvas 2D / Remotion)

```typescript
export interface WorkCard {
  id: string;
  label: string;
  r: number;        // Rayon orbital par rapport au centre
  angle: number;    // Angle azimutal
  zDepth: number;   // Altitude Z
  tilt: number;     // Inclinaison de rotation 3D
  opacity: number;
}

export class TaskVortexEngine {
  private cards: WorkCard[] = [];

  constructor(count = 32) {
    const tasks = ['COPY TO CRM', 'RE-KEY INPUT', 'FIND INVOICE', 'SEND APPROVAL', 'EXTRACT PDF'];
    for (let i = 0; i < count; i++) {
      this.cards.push({
        id: `card-${i}`,
        label: tasks[i % tasks.length],
        r: 380 + Math.random() * 260,
        angle: Math.random() * Math.PI * 2,
        zDepth: (Math.random() - 0.5) * 140,
        tilt: (Math.random() - 0.5) * 0.8,
        opacity: 0.95,
      });
    }
  }

  public update(speedMultiplier = 1.0) {
    const G = 1200 * speedMultiplier;
    for (const card of this.cards) {
      // Vitesse angulaire proportionnelle à la proximité du centre
      const omega = (1.8 / Math.sqrt(Math.max(card.r, 40))) * speedMultiplier;
      card.angle += omega;

      // Aspiration radiale vers le centre
      card.r -= (G / Math.max(card.r, 50)) * 0.12;
      card.tilt += 0.02;

      // Disparition au centre
      if (card.r < 30) {
        card.opacity = Math.max(0, card.r / 30);
      }
    }
  }

  public render(ctx: CanvasRenderingContext2D, centerX: number, centerY: number) {
    // Rendu des arêtes filaires du graphe reliant les cartes proches
    ctx.strokeStyle = 'rgba(93, 255, 38, 0.15)';
    ctx.lineWidth = 1;
    for (let i = 0; i < this.cards.length; i++) {
      for (let j = i + 1; j < this.cards.length; j++) {
        const cA = this.cards[i];
        const cB = this.cards[j];
        const xA = centerX + Math.cos(cA.angle) * cA.r;
        const yA = centerY + Math.sin(cA.angle) * cA.r * 0.55; // Projection elliptique
        const xB = centerX + Math.cos(cB.angle) * cB.r;
        const yB = centerY + Math.sin(cB.angle) * cB.r * 0.55;
        const dist = Math.hypot(xA - xB, yA - yB);
        if (dist < 110) {
          ctx.beginPath();
          ctx.moveTo(xA, yA);
          ctx.lineTo(xB, yB);
          ctx.stroke();
        }
      }
    }

    // Rendu des cartes rectangulaires
    for (const card of this.cards) {
      if (card.opacity <= 0) continue;
      const x = centerX + Math.cos(card.angle) * card.r;
      const y = centerY + Math.sin(card.angle) * card.r * 0.55;
      const scale = Math.max(0.2, Math.min(1.0, card.r / 180));

      ctx.save();
      ctx.translate(x, y);
      ctx.rotate(card.angle + card.tilt);
      ctx.scale(scale, scale);
      ctx.globalAlpha = card.opacity;

      // Fond de la carte
      ctx.fillStyle = '#FFFFFF';
      ctx.beginPath();
      ctx.roundRect(-45, -28, 90, 56, 6);
      ctx.fill();

      // Texte de la tâche
      ctx.fillStyle = '#0F172A';
      ctx.font = '600 9px monospace';
      ctx.textAlign = 'center';
      ctx.fillText(card.label, 0, 4);

      ctx.restore();
    }
  }
}
```

---

## 3. Moteur 3 : Balayage Laser Holographique (UI Scanline Materializer)

Utilisé pour : La matérialisation verticale des interfaces logicielles à `00:24 - 00:28` (Séquence 07).

### 3.1. Principe Géométrique
Un plan d'interface 2D/3D est partitionné en deux zones par une ligne horizontale mobile d'ordonnée $Y_{\text{scan}}(t) \in [0, H]$ :
- **Zone supérieure ($y < Y_{\text{scan}}$)** : Interface résolue avec données pleines, typographies contrastées, graphes et cartes texturées.
- **Zone de la ligne ($y \approx Y_{\text{scan}}$)** : Faisceau laser additif ultra-lumineux d'épaisseur 6px avec dégradé d'atténuation gaussien et glow néon (`#C4FF93`).
- **Zone inférieure ($y > Y_{\text{scan}}$)** : Squelette filaire vert néon sombre (`stroke: 1.5px solid #2E5E24`), arrière-plan transparent laissant transparaître la grille de sol.

### 3.2. Fragment Shader GLSL (Reveal Shader)

```glsl
uniform sampler2D u_fullTexture;     // Texture résolue (UI pleine)
uniform sampler2D u_wireTexture;     // Texture filaire (Wireframe vert)
uniform float u_scanProgress;        // Progression de 0.0 à 1.0
uniform float u_beamHeight;          // Épaisseur de la ligne (ex: 0.035)
varying vec2 v_uv;

void main() {
    float currentY = 1.0 - v_uv.y; // Balayage du haut vers le bas
    vec4 resolvedColor = texture2D(u_fullTexture, v_uv);
    vec4 wireColor = texture2D(u_wireTexture, v_uv);

    float diff = currentY - u_scanProgress;

    if (diff < -u_beamHeight * 0.5) {
        // Au-dessus du faisceau : UI résolue
        gl_FragColor = resolvedColor;
    } else if (diff > u_beamHeight * 0.5) {
        // En-dessous du faisceau : UI filaire
        gl_FragColor = wireColor;
    } else {
        // Dans le faisceau laser de balayage : éclat néon additif
        float normDist = abs(diff) / (u_beamHeight * 0.5);
        float intensity = 1.0 - smoothstep(0.0, 1.0, normDist);
        vec4 laserColor = vec4(0.76, 1.0, 0.58, 1.0) * intensity * 2.2;
        gl_FragColor = mix(resolvedColor, laserColor, intensity);
    }
}
```

---

## 4. Moteur 4 : Pipeline Laser Ascendant & Cartes Validées (Pinned Value Cards)

Utilisé pour : L'alignement des briques à haute valeur ajoutée à `00:20 - 00:24` (Séquence 06).

### 4.1. Principe Géométrique
Un vecteur directeur orienté $\vec{u} = (\cos\alpha, \sin\alpha)$ définit la droite du faisceau laser avec $\alpha = 22^\circ$.
Chaque carte d'état $k \in \{0, 1, 2\}$ est ancrée à une abscisse curviligne $s_k$ le long de cette droite :
$$P_k = P_{\text{origin}} + s_k \cdot \vec{u}$$
L'entrée de chaque carte est asservie à un ressort physique avec retard échelonné (stagger de 12 frames) :
$$Progress_k(t) = \text{spring}\left(\text{frame} - \text{delay}_k, \text{config} = \{ \text{stiffness}: 200, \text{damping}: 20 \}\right)$$

### 4.2. Composant Remotion Typé (React / SVG)

```tsx
import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

interface PinnedCardProps {
  label: string;
  sub: string;
  anchorX: number;
  anchorY: number;
  delayFrame: number;
}

export const PinnedValueCard: React.FC<PinnedCardProps> = ({
  label,
  sub,
  anchorX,
  anchorY,
  delayFrame,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame: frame - delayFrame,
    fps,
    config: { stiffness: 190, damping: 21, mass: 0.9 },
  });

  const scale = interpolate(entrance, [0, 1], [0.65, 1.0]);
  const opacity = interpolate(entrance, [0, 1], [0, 1]);
  const translateY = interpolate(entrance, [0, 1], [30, 0]);

  return (
    <g
      transform={`translate(${anchorX}, ${anchorY})`}
      style={{ opacity, transform: `scale(${scale}) translateY(${translateY}px)` }}
    >
      {/* Point de connexion sur le faisceau laser */}
      <circle r="4" fill="#C4FF93" filter="drop-shadow(0 0 6px #5DFF26)" />
      <line x1="0" y1="0" x2="0" y2="-28" stroke="#5DFF26" strokeWidth="1.5" />

      {/* Boîtier de la carte */}
      <g transform="translate(-110, -96)">
        <rect
          width="220"
          height="64"
          rx="10"
          fill="rgba(10, 20, 12, 0.92)"
          stroke="#5DFF26"
          strokeWidth="1.5"
          filter="drop-shadow(0 4px 16px rgba(93, 255, 38, 0.2))"
        />
        {/* Pastille checkmark */}
        <circle cx="24" cy="24" r="10" fill="#5DFF26" />
        <path
          d="M 19 24 L 22 27 L 29 20"
          fill="none"
          stroke="#000000"
          strokeWidth="2.2"
          strokeLinecap="round"
        />
        {/* Typographies */}
        <text x="44" y="27" fill="#FFFFFF" fontSize="14" fontWeight="600" fontFamily="Inter, sans-serif">
          {label}
        </text>
        <text x="44" y="46" fill="#8E929B" fontSize="10" fontFamily="Inter, sans-serif">
          {sub}
        </text>
      </g>
    </g>
  );
};
```

---

## 5. Moteur 5 : Vol Hyperspace à Vitesse Relativiste (Relativistic Star Streaks)

Utilisé pour : La propulsion cinématique à `00:36 - 00:40` (Séquence 10).

### 5.1. Principe Mathématique
Les étoiles sont modélisées par des coordonnées cylindriques $(r_i, \theta_i, z_i)$.
À l'accélération $a(t)$, la vitesse de caméra $V_z$ augmente exponentiellement.
Sous l'effet de la vitesse et de la persistance rétinienne (motion blur), chaque point devient un segment 3D entre sa position actuelle $z$ et sa position à $t - \Delta t$ :
$$L_{\text{streak}} = V_z(t) \cdot \Delta t$$
En projection 2D, les étoiles proches du centre fuient radialement vers les bords de l'écran avec un ratio d'aspect allongé.

### 5.2. Snippet Three.js (Instanced Star Streaks)

```typescript
import * as THREE from 'three';

export class WarpSpeedField {
  public mesh: THREE.LineSegments;
  private starCount = 600;
  private velocities: Float32Array;

  constructor() {
    const geo = new THREE.BufferGeometry();
    const positions = new Float32Array(this.starCount * 2 * 3);
    this.velocities = new Float32Array(this.starCount);

    for (let i = 0; i < this.starCount; i++) {
      const x = (Math.random() - 0.5) * 1600;
      const y = (Math.random() - 0.5) * 900;
      const z = Math.random() * -2000;
      this.velocities[i] = 15 + Math.random() * 25;

      const idx = i * 6;
      positions[idx] = x;     positions[idx + 1] = y;     positions[idx + 2] = z;
      positions[idx + 3] = x; positions[idx + 4] = y; positions[idx + 5] = z;
    }

    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const mat = new THREE.LineBasicMaterial({
      color: 0x83FF6B,
      transparent: true,
      opacity: 0.85,
      blending: THREE.AdditiveBlending,
    });
    this.mesh = new THREE.LineSegments(geo, mat);
  }

  public update(warpFactor: number) {
    const pos = this.mesh.geometry.attributes.position.array as Float32Array;
    for (let i = 0; i < this.starCount; i++) {
      const idx = i * 6;
      const speed = this.velocities[i] * warpFactor;

      pos[idx + 2] += speed; // Tête de l'étoile
      // Queue de l'étoile décalée selon la vitesse
      pos[idx + 5] = pos[idx + 2] - speed * 1.8;

      // Recyclage en fond de champ quand l'étoile dépasse la caméra
      if (pos[idx + 2] > 200) {
        pos[idx + 2] = -2000;
        pos[idx + 5] = -2000;
      }
    }
    this.mesh.geometry.attributes.position.needsUpdate = true;
  }
}
```

---

## 6. Moteur 6 : Cylindre Radial de Code Source (Radial Code Vortex)

Utilisé pour : L'antithèse architecturale à `00:44` (Séquence 12).

### 6.1. Principe Géométrique
Un ensemble de $N = 36$ colonnes verticales de code TypeScript sont disposées sur la surface d'un cylindre ou d'un entonnoir 3D orienté vers la caméra :
$$X_k(\theta, y) = R(y) \cdot \sin(\theta_k), \quad Z_k(\theta, y) = R(y) \cdot \cos(\theta_k)$$
avec $R(y) = R_0 + k_{\text{cone}} \cdot y$ pour créer un effet d'entonnoir gravitationnel.
La caméra est placée à l'intérieur du cône et regarde vers le centre d'extinction sombre.

### 6.2. Implémentation CSS 3D / Remotion

```tsx
export const RadialCodeColumn: React.FC<{
  index: number;
  totalColumns: number;
  radius: number;
  codeSnippets: string[];
}> = ({ index, totalColumns, radius, codeSnippets }) => {
  const angle = (index / totalColumns) * 360;

  return (
    <div
      style={{
        position: 'absolute',
        top: '50%',
        left: '50%',
        transformStyle: 'preserve-3d',
        transform: `rotateZ(${angle}deg) translateY(-${radius}px) rotateX(75deg)`,
        transformOrigin: '0 0',
      }}
    >
      <pre
        style={{
          color: '#8E929B',
          fontSize: '11px',
          fontFamily: 'Geist Mono, monospace',
          lineHeight: '1.4',
          margin: 0,
          maskImage: 'linear-gradient(to bottom, white, transparent)',
        }}
      >
        {codeSnippets.join('\n')}
      </pre>
    </div>
  );
};
```

---

## 7. Moteur 7 : Dissolution Alvéolaire Procédurale (Hexagonal Cellular Wipe)

Utilisé pour : La transition de sortie du Climax Vert à `00:58 - 01:00` (Séquence 16).

### 7.1. Principe Mathématique
L'écran est pavé d'un réseau hexagonal à coordonnées axiales $(q, r)$.
Le rayon circonscrit d'une cellule est $R_{\text{cell}} = 32\text{px}$.
Chaque cellule possède une coordonnée spatiale normalisée en $X \in [0, 1]$.
L'extinction d'une cellule est déterminée par une fonction de seuil combinant la position horizontale et un bruit pseudorandom à haute fréquence spatiale :
$$\text{Threshold}(q, r) = \frac{x(q, r)}{W} + \kappa \cdot \text{noise}(q \cdot 0.3, r \cdot 0.3)$$
La cellule s'éteint si $\text{Threshold}(q, r) < \text{Progress}(t)$.

### 7.2. Shader GLSL / Canvas 2D (Cellular Hex Wipe)

```typescript
export class HexWipeTransition {
  private hexRadius = 26;

  public render(
    ctx: CanvasRenderingContext2D,
    width: number,
    height: number,
    progress: number // De 0.0 (plein vert) à 1.0 (fond noir sidéral)
  ) {
    const dx = this.hexRadius * 1.5;
    const dy = this.hexRadius * Math.sqrt(3);
    const cols = Math.ceil(width / dx) + 2;
    const rows = Math.ceil(height / dy) + 2;

    for (let q = 0; q < cols; q++) {
      for (let r = 0; r < rows; r++) {
        const cx = q * dx;
        const cy = r * dy + (q % 2 ? dy * 0.5 : 0);

        // Bruit pseudo-aléatoire déterministe par cellule
        const pseudoNoise = (Math.sin(q * 12.9898 + r * 78.233) * 43758.5453) % 1;
        const cellThreshold = (cx / width) * 0.75 + pseudoNoise * 0.25;

        if (cellThreshold > progress) {
          // La cellule est encore verte (non balayée)
          ctx.save();
          ctx.translate(cx, cy);
          this.drawHexagon(ctx, this.hexRadius - 1);
          ctx.fillStyle = '#6AFF3C';
          ctx.fill();
          ctx.strokeStyle = '#55E820';
          ctx.lineWidth = 1;
          ctx.stroke();
          ctx.restore();
        }
      }
    }
  }

  private drawHexagon(ctx: CanvasRenderingContext2D, r: number) {
    ctx.beginPath();
    for (let i = 0; i < 6; i++) {
      const a = (i * Math.PI) / 3;
      const px = r * Math.cos(a);
      const py = r * Math.sin(a);
      if (i === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
    ctx.closePath();
  }
}
```
