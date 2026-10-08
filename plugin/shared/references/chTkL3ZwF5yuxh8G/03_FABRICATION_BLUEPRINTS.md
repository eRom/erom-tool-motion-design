# 03. Blueprints de Fabrication & Recettes de Code

Ce document fournit aux agents développeurs (Remotion, WebGL/Three.js, Canvas 2D, SVG/GSAP) l'ensemble des algorithmes, formulations mathématiques et composants logiciels typés nécessaires pour implémenter les six briques cinématiques majeures de *Crew in the Dark*.

---

## 1. Moteur 1 : Traceur Polaire & Tête d'Étincelle (Polar Spline & Sparkler Particle Engine)

Utilisé pour : L'initialisation du cercle polaire (00:00), la ligne de code en voie ferrée (00:13), la spline télémétrique (01:28) et le réticule final (01:54).

### 1.1. Formulation Mathématique
1. **Échantillonnage de trajectoire** :
   À chaque frame `t \in [0, T]`, la progression normale est calculée par :
   $$s(t) = \text{clamp}\left(\frac{t - t_{\text{start}}}{t_{\text{duration}}}, 0, 1\right)$$
   Le point courant $P(s) = (x(s), y(s))$ est extrait via `path.getPointAtLength(s \cdot L)$`.
2. **Vecteur Tangent & Angle d'Émission** :
   $$\vec{T} = P(s) - P(s - \Delta s) \implies \theta_T = \text{atan2}(T_y, T_x)$$
3. **Traverses de Voie Ferrée (Ladder Normal)** :
   Le vecteur normal unitaire $\vec{N} = (-T_y, T_x) / \|\vec{T}\|$ définit les extrémités des traverses de largeur $2w$ :
   $$P_{\text{left}} = P(s) + w \cdot \vec{N}, \quad P_{\text{right}} = P(s) - w \cdot \vec{N}$$
4. **Cinématique des Particules d'Étincelle** :
   Chaque particule $i$ est émise à $P(s)$ dans le cône arrière $(\theta_T + \pi \pm \frac{\pi}{3})$ :
   $$v_{x,i} = \cos(\theta_i) \cdot v_{\text{rand}}, \quad v_{y,i} = \sin(\theta_i) \cdot v_{\text{rand}}$$
   $$x_i(t + 1) = x_i(t) + v_{x,i}, \quad y_i(t + 1) = y_i(t) + v_{y,i} + g_{\text{gravity}}$$

### 1.2. Implémentation TypeScript / Canvas 2D (Remotion Ready)

```typescript
// SparklerEngine.ts
export interface SparkParticle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  life: number;
  maxLife: number;
  size: number;
  hue: number;
}

export class SparklerEngine {
  private particles: SparkParticle[] = [];

  public emit(x: number, y: number, tangentAngle: number, count = 12): void {
    for (let i = 0; i < count; i++) {
      const spread = (Math.random() - 0.5) * (Math.PI * 0.65);
      const angle = tangentAngle + Math.PI + spread;
      const speed = Math.random() * 5.5 + 2.0;
      const maxLife = Math.floor(Math.random() * 12) + 8;

      this.particles.push({
        x,
        y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        life: 0,
        maxLife,
        size: Math.random() * 2.5 + 1.2,
        hue: 15 + Math.random() * 15, // Teinte orange-corail (#FF5533)
      });
    }
  }

  public updateAndRender(ctx: CanvasRenderingContext2D): void {
    ctx.save();
    ctx.globalCompositeOperation = 'lighter'; // Rendu additif incandescent

    for (let i = this.particles.length - 1; i >= 0; i--) {
      const p = this.particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.vy += 0.06; // Légère gravité descendante
      p.life++;

      const progress = p.life / p.maxLife;
      const alpha = Math.max(0, 1 - progress);
      const radius = p.size * (1 - progress * 0.5);

      const grad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, radius * 2.5);
      grad.addColorStop(0, `rgba(255, 255, 255, ${alpha})`);
      grad.addColorStop(0.35, `rgba(255, 85, 51, ${alpha * 0.9})`);
      grad.addColorStop(1, `rgba(255, 30, 0, 0)`);

      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.arc(p.x, p.y, radius * 2.5, 0, Math.PI * 2);
      ctx.fill();

      if (p.life >= p.maxLife) {
        this.particles.splice(i, 1);
      }
    }
    ctx.restore();
  }
}
```

---

## 2. Moteur 2 : Nappe Infinie de Cartes 3D en Perspective (Infinite 3D Card Floor)

Utilisé pour : La satire du motion design générique à cartes "Seamless" et "SAME" (00:24, 00:28, 01:52).

### 2.1. Formulation Mathématique
1. **Grille Matricielle Isométrique** :
   Un ensemble de cartes $C_{i,j}$ est disposé sur le plan horizontal $Y = Y_{\text{floor}}$ pour $i \in [-N, N]$ et $j \in [0, M]$.
   $$X_{i,j} = i \cdot \text{step}_X, \quad Z_{i,j} = (j \cdot \text{step}_Z - \text{scroll}_Z(t)) \pmod{M \cdot \text{step}_Z}$$
2. **Projection Perspective Caméra** :
   Avec une focale $f$ et une caméra à la hauteur $H_{\text{cam}}$ :
   $$x_{\text{proj}} = x_{\text{center}} + \frac{X_{i,j} \cdot f}{Z_{i,j}}, \quad y_{\text{proj}} = y_{\text{center}} + \frac{H_{\text{cam}} \cdot f}{Z_{i,j}}$$
   $$w_{\text{proj}} = \frac{W_{\text{card}} \cdot f}{Z_{i,j}}, \quad h_{\text{proj}} = \frac{H_{\text{card}} \cdot f}{Z_{i,j}}$$
3. **Atténuation Volumétrique de Profondeur (Fog Decay)** :
   $$\alpha(Z) = \text{clamp}\left(1 - \frac{Z - Z_{\text{near}}}{Z_{\text{far}} - Z_{\text{near}}}, 0, 1\right)^2$$

### 2.2. Implémentation Three.js / InstancedMesh (Haute Performance)

```typescript
// InfiniteCardFloor.ts
import * as THREE from 'three';

export interface CardFloorOptions {
  rows: number;
  cols: number;
  cardWidth: number;
  cardHeight: number;
  spacingX: number;
  spacingZ: number;
}

export class InfiniteCardFloor {
  public mesh: THREE.InstancedMesh;
  private dummy = new THREE.Object3D();
  private totalInstances: number;

  constructor(private opts: CardFloorOptions) {
    this.totalInstances = opts.rows * opts.cols;
    
    // Géométrie d'une carte aux coins biseautés
    const geom = new THREE.PlaneGeometry(opts.cardWidth, opts.cardHeight);
    geom.rotateX(-Math.PI / 2); // Coucher à plat sur le sol XZ

    // ShaderMaterial avec dégradé générique parodié (#2E1E6B -> #5B42D6 -> #43B0FF)
    const mat = new THREE.ShaderMaterial({
      vertexShader: `
        varying vec2 vUv;
        varying float vDepth;
        void main() {
          vUv = uv;
          vec4 worldPos = instanceMatrix * vec4(position, 1.0);
          vec4 mvPosition = modelViewMatrix * worldPos;
          vDepth = -mvPosition.z;
          gl_Position = projectionMatrix * mvPosition;
        }
      `,
      fragmentShader: `
        varying vec2 vUv;
        varying float vDepth;
        void main() {
          vec3 colStart = vec3(0.18, 0.12, 0.42); // #2E1E6B
          vec3 colMid   = vec3(0.36, 0.26, 0.84); // #5B42D6
          vec3 colEnd   = vec3(0.26, 0.69, 1.00); // #43B0FF

          vec3 grad = mix(colStart, colMid, smoothstep(0.0, 0.5, vUv.x));
          grad = mix(grad, colEnd, smoothstep(0.5, 1.0, vUv.x));

          // Atténuation de brouillard de profondeur
          float fog = smoothstep(1200.0, 300.0, vDepth);
          gl_FragColor = vec4(grad * fog, fog);
        }
      `,
      transparent: true,
      side: THREE.DoubleSide,
    });

    this.mesh = new THREE.InstancedMesh(geom, mat, this.totalInstances);
    this.updatePositions(0);
  }

  public updatePositions(scrollZ: number): void {
    let idx = 0;
    const totalDepth = this.opts.rows * this.opts.spacingZ;

    for (let r = 0; r < this.opts.rows; r++) {
      for (let c = 0; c < this.opts.cols; c++) {
        const x = (c - (this.opts.cols - 1) / 2) * this.opts.spacingX;
        let z = (r * this.opts.spacingZ - scrollZ) % totalDepth;
        if (z < 0) z += totalDepth;

        this.dummy.position.set(x, -80, z + 100);
        this.dummy.scale.set(1, 1, 1);
        this.dummy.updateMatrix();

        this.mesh.setMatrixAt(idx++, this.dummy.matrix);
      }
    }
    this.mesh.instanceMatrix.needsUpdate = true;
  }
}
```

---

## 3. Moteur 3 : Trou Noir & Lentille Gravitationnelle (Gravitational Lensing & Grid Warp)

Utilisé pour : L'effondrement gravitationnel du "One Prompt" (00:40).

### 3.1. Formulation Mathématique
1. **Déviation Géodésique Radiale** :
   Soit une coordonnée écran normalisée $\vec{u} \in [-1, 1]^2$. La distance au centre du trou noir $\vec{c} = (0, 0)$ est $r = \|\vec{u}\|$.
   Le rayon critique de capture (rayon de Schwarzschild) est noté $r_s \approx 0.25$.
   La déformation géodésique de la coordonnée de texture $\vec{u}_{\text{distorted}}$ est :
   $$\vec{u}_{\text{distorted}} = \vec{c} + \frac{\vec{u} - \vec{c}}{r} \cdot \left(r - \frac{r_s^2}{r + \epsilon}\right) \quad \text{pour } r > r_s$$
   Pour $r \le r_s$, la matière est absorbée : opacité nulle ou noir absolu.
2. **Disque d'Accrétion Lumineux (Photon Ring)** :
   L'intensité lumineuse du photon ring à $r_{\text{ring}} = 1.5 \cdot r_s$ suit une lorentzienne étroite :
   $$I_{\text{ring}}(r) = \frac{A}{\left(\frac{r - r_{\text{ring}}}{\gamma}\right)^2 + 1}$$

### 3.2. Fragment Shader GLSL (Lentille Gravitationnelle)

```glsl
// blackhole_warp.frag
uniform vec2 u_resolution;
uniform float u_time;
uniform float u_rs; // Rayon de Schwarzschild (ex: 0.22)
uniform sampler2D u_grid_texture;

varying vec2 v_uv;

void main() {
  vec2 p = (gl_FragCoord.xy * 2.0 - u_resolution) / min(u_resolution.x, u_resolution.y);
  float r = length(p);

  if (r < u_rs) {
    // Intérieur de l'horizon des événements : noir absolu
    gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
    return;
  }

  // Déflexion gravitationnelle relativiste
  float deflection = (u_rs * u_rs) / (r - u_rs * 0.4);
  vec2 warped_p = p * (1.0 - deflection / r);

  // Rotation différentielle de l'espace (effet Lense-Thirring / frame dragging)
  float angle_drag = (u_rs / (r * r + 0.05)) * 1.8;
  float cosA = cos(angle_drag);
  float sinA = sin(angle_drag);
  warped_p = vec2(
    warped_p.x * cosA - warped_p.y * sinA,
    warped_p.x * sinA + warped_p.y * cosA
  );

  // Échantillonnage de la texture de grille déformée
  vec2 sample_uv = warped_p * 0.5 + 0.5;
  vec4 grid_color = texture2D(u_grid_texture, sample_uv);

  // Rendu de l'anneau de photon lumineux orange braise (#FF5533)
  float ring_dist = abs(r - u_rs * 1.35);
  float ring_intensity = 0.015 / (ring_dist * ring_dist + 0.002);
  vec3 ring_color = vec3(1.0, 0.33, 0.20) * ring_intensity;

  vec3 final_color = grid_color.rgb + ring_color;
  gl_FragColor = vec4(final_color, 1.0);
}
```

---

## 4. Moteur 4 : Odomètre Mécanique Analogique (Mechanical Barrel Drum Roller)

Utilisé pour : Le défilement effréné du compteur de likes ("SIXTEEN THOUSAND ... 17,111 HEARTS", 00:18).

### 4.1. Formulation Mathématique
1. **Décomposition Décimale** :
   La valeur cible $V = 17111$ est décomposée en 5 chiffres $d_k$ ($k \in [0, 4]$ de gauche à droite) : $[1, 7, 1, 1, 1]$.
2. **Cinématique Angulaire des Tambours** :
   Chaque tambour $k$ effectue $N_k$ révolutions complètes avant de s'arrêter sur son chiffre cible $d_k$ :
   $$\theta_k(t) = 2\pi \cdot \left(N_k \cdot f_{\text{ease}}(t) + \frac{d_k}{10}\right)$$
   Où $N_k = 4 + k \cdot 3$ (les chiffres de droite tournent plus longtemps et plus vite).
3. **Flou de Mouvement Vertical (Motion Blur Dynamique)** :
   Le flou directionnel vertical $B_y$ est proportionnel à la vitesse instantanée $\dot{\theta}_k$ :
   $$B_y(t) = \text{clamp}\left(\beta \cdot |\theta_k(t) - \theta_k(t - \Delta t)|, 0, B_{\text{max}}\right)$$

### 4.2. Implémentation React / Remotion

```tsx
// OdometerRoller.tsx
import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

interface DrumProps {
  digit: number;
  delayFrames: number;
  extraSpins: number;
}

const DrumColumn: React.FC<DrumProps> = ({ digit, delayFrames, extraSpins }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const anim = spring({
    frame: frame - delayFrames,
    fps,
    config: { mass: 0.8, damping: 13, stiffness: 180 },
  });

  const totalDigits = extraSpins * 10 + digit;
  const currentOffset = interpolate(anim, [0, 1], [0, totalDigits * 54]); // 54px par chiffre

  return (
    <div
      style={{
        width: 44,
        height: 70,
        overflow: 'hidden',
        background: 'linear-gradient(180deg, #1A1A1A 0%, #E8E8E8 48%, #FFFFFF 52%, #1A1A1A 100%)',
        borderRadius: 4,
        border: '1px solid #444',
        boxShadow: 'inset 0 4px 10px rgba(0,0,0,0.8), inset 0 -4px 10px rgba(0,0,0,0.8)',
        position: 'relative',
      }}
    >
      <div
        style={{
          transform: `translateY(-${currentOffset % (10 * 54)}px)`,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          fontFamily: '"Neue Haas Grotesk", "Inter", sans-serif',
          fontWeight: 900,
          fontSize: 42,
          color: '#111',
        }}
      >
        {Array.from({ length: 20 }).map((_, i) => (
          <div key={i} style={{ height: 54, display: 'flex', alignItems: 'center' }}>
            {i % 10}
          </div>
        ))}
      </div>
    </div>
  );
};

export const MechanicalOdometer: React.FC<{ value: number }> = ({ value }) => {
  const digits = value.toString().padStart(5, '0').split('').map(Number);

  return (
    <div
      style={{
        display: 'inline-flex',
        gap: 6,
        padding: '12px 18px',
        background: '#0D0D0E',
        borderRadius: 8,
        border: '2px solid #28282C',
        boxShadow: '0 18px 36px rgba(0,0,0,0.8)',
      }}
    >
      {digits.map((d, idx) => (
        <DrumColumn key={idx} digit={d} delayFrames={idx * 2} extraSpins={3 + idx * 2} />
      ))}
    </div>
  );
};
```

---

## 5. Moteur 5 : Réseau Constellation Multi-Agent & Checklist de Review Interactive

Utilisé pour : La chorégraphie des 4 agents (`REFERENCE-BREAKER`, `STORYBOARDER`, `BUILDER`, `FILM-REVIEWER`) et la revue animée (00:44, 01:34).

### 5.1. Formulation Mathématique
1. **Topologie du Graphe de Transmission** :
   4 nœuds $N_i = (x_i, y_i, z_i)$ reliés à un centre $C = (0, 0, 0)$ portant l'astérisque Anthropic.
   À l'instant $t_{\text{activate}}$, l'impulsion lumineuse parcourt l'arête $(N_i, C)$ selon :
   $$P_{\text{pulse}}(s) = (1 - s) \cdot N_i + s \cdot C, \quad s = \text{fract}\left(\frac{t - t_0}{T_{\text{period}}}\right)$$
2. **Rature Animée SVG (Strikethrough Shader)** :
   Une ligne horizontale traversant l'item corrigé utilise un `stroke-dashoffset` :
   $$\text{dashoffset} = \text{length} \cdot \left(1 - \text{clamp}\left(\frac{t - t_{\text{strike}}}{\Delta t}, 0, 1\right)\right)$$

### 5.2. Implémentation React / SVG / Remotion

```tsx
// ReviewerChecklist.tsx
import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';

interface ReviewItem {
  priority: 'P0' | 'P1' | 'P2';
  text: string;
  strikeFrame: number;
}

const ITEMS: ReviewItem[] = [
  { priority: 'P0', text: 'text overlaps at 0:41', strikeFrame: 20 },
  { priority: 'P1', text: 'zoom too fast in scene 3', strikeFrame: 999 },
  { priority: 'P2', text: "kerning on 'genius'", strikeFrame: 999 },
];

export const ReviewerChecklistModal: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <div
      style={{
        width: 440,
        background: 'rgba(22, 22, 24, 0.92)',
        backdropFilter: 'blur(16px)',
        border: '1px solid rgba(255, 255, 255, 0.12)',
        borderRadius: 8,
        padding: '24px 28px',
        color: '#FFFFFF',
        fontFamily: '"JetBrains Mono", monospace',
        boxShadow: '0 24px 48px rgba(0,0,0,0.6)',
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 20, fontSize: 13, color: '#888' }}>
        <span>REVIEW · P0 P1 P2</span>
        <span>PASS 03</span>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
        {ITEMS.map((item, idx) => {
          const isStruck = frame >= item.strikeFrame;
          const strikeProgress = interpolate(frame, [item.strikeFrame, item.strikeFrame + 12], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });

          return (
            <div key={idx} style={{ display: 'flex', alignItems: 'center', gap: 12, position: 'relative' }}>
              {/* Checkbox */}
              <div
                style={{
                  width: 18,
                  height: 18,
                  borderRadius: 3,
                  border: isStruck ? '1px solid #FF5533' : '1px solid #555',
                  background: isStruck ? 'rgba(255, 85, 51, 0.2)' : 'transparent',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: 12,
                  color: '#FF5533',
                }}
              >
                {isStruck ? '✓' : ''}
              </div>

              {/* Badge Priorité */}
              <span
                style={{
                  padding: '2px 6px',
                  borderRadius: 3,
                  fontSize: 11,
                  fontWeight: 700,
                  background: item.priority === 'P0' ? '#D6453D' : '#333',
                  color: '#FFF',
                }}
              >
                {item.priority}
              </span>

              {/* Texte avec rature */}
              <div style={{ position: 'relative', fontSize: 14 }}>
                <span style={{ color: isStruck ? '#777' : '#EEE' }}>{item.text}</span>
                {item.strikeFrame < 900 && (
                  <div
                    style={{
                      position: 'absolute',
                      top: '52%',
                      left: 0,
                      width: `${strikeProgress * 100}%`,
                      height: 2,
                      background: '#FF5533',
                    }}
                  />
                )}
              </div>
            </div>
          );
        })}
      </div>

      <div style={{ marginTop: 24, display: 'flex', justifyContent: 'space-between', fontSize: 12, color: '#666' }}>
        <span>{frame >= 32 ? '1 / 3 RESOLVED' : '0 / 3 RESOLVED'}</span>
        <span>REVIEWER · CLAUDE</span>
      </div>
    </div>
  );
};
```

---

## 6. Moteur 6 : Cône Volumétrique de Projecteur Scénique & Rideaux de Théâtre

Utilisé pour : La sélection du storyboard (01:09) et la révélation finale du fauteuil de réalisateur ("You're the director now", 01:46).

### 6.1. Formulation Mathématique
1. **Cône de Lumière Volumétrique (Bilinear Lighting Mask)** :
   Une source lumineuse au zénith $S = (x_{\text{light}}, y_{\text{light}})$ projette un faisceau conique de demi-angle $\alpha \approx 22^\circ$.
   L'intensité $I(x, y)$ est maximale sur l'axe central vertical et décroît selon une gaussienne latérale :
   $$I(x, y) = I_0 \cdot \exp\left(-\frac{(x - x_{\text{center}}(y))^2}{2 \sigma(y)^2}\right) \cdot \text{clamp}\left(\frac{y - y_{\text{light}}}{H_{\text{beam}}}, 0, 1\right)$$
   Où $\sigma(y) = y \cdot \tan(\alpha)$.
2. **Poussières de Scène en Suspension (Brownian Float)** :
   Particules de poussière lumineuse $p_i$ dérivant lentement :
   $$x_i(t) = x_{0,i} + A_x \cdot \sin(\omega_x t + \phi_{x,i}), \quad y_i(t) = y_{0,i} - v_{\text{up}} \cdot t$$

### 6.2. Implémentation Canvas 2D (Remotion Hook)

```typescript
// VolumetricSpotlight.ts
export class VolumetricSpotlight {
  private dustMotes: Array<{ x: number; y: number; r: number; alpha: number; speed: number }> = [];

  constructor(private width: number, private height: number, dustCount = 45) {
    for (let i = 0; i < dustCount; i++) {
      this.dustMotes.push({
        x: width * 0.5 + (Math.random() - 0.5) * 160,
        y: Math.random() * height,
        r: Math.random() * 1.5 + 0.5,
        alpha: Math.random() * 0.6 + 0.2,
        speed: Math.random() * 0.4 + 0.2,
      });
    }
  }

  public render(ctx: CanvasRenderingContext2D, lightX: number, floorY: number): void {
    ctx.save();

    // 1. Cône volumétrique
    ctx.globalCompositeOperation = 'screen';
    const coneGrad = ctx.createRadialGradient(lightX, 0, 10, lightX, floorY, floorY * 0.9);
    coneGrad.addColorStop(0, 'rgba(255, 230, 200, 0.35)');
    coneGrad.addColorStop(0.5, 'rgba(255, 180, 130, 0.12)');
    coneGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');

    ctx.fillStyle = coneGrad;
    ctx.beginPath();
    ctx.moveTo(lightX - 25, 0);
    ctx.lineTo(lightX + 25, 0);
    ctx.lineTo(lightX + 170, floorY);
    ctx.lineTo(lightX - 170, floorY);
    ctx.closePath();
    ctx.fill();

    // 2. Spot au sol (ellipse d'impact)
    const floorSpot = ctx.createRadialGradient(lightX, floorY, 0, lightX, floorY, 150);
    floorSpot.addColorStop(0, 'rgba(255, 220, 180, 0.45)');
    floorSpot.addColorStop(0.6, 'rgba(255, 120, 80, 0.15)');
    floorSpot.addColorStop(1, 'rgba(0, 0, 0, 0)');

    ctx.fillStyle = floorSpot;
    ctx.beginPath();
    ctx.ellipse(lightX, floorY, 150, 45, 0, 0, Math.PI * 2);
    ctx.fill();

    // 3. Poussières de scène scintillantes
    ctx.fillStyle = '#FFFFFF';
    for (const d of this.dustMotes) {
      d.y -= d.speed;
      if (d.y < 0) d.y = floorY;

      // Masque d'inclusion dans le faisceau
      const beamHalfWidth = (d.y / floorY) * 160 + 20;
      if (Math.abs(d.x - lightX) < beamHalfWidth) {
        ctx.globalAlpha = d.alpha * (1 - Math.abs(d.x - lightX) / beamHalfWidth);
        ctx.beginPath();
        ctx.arc(d.x, d.y, d.r, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    ctx.restore();
  }
}
```
