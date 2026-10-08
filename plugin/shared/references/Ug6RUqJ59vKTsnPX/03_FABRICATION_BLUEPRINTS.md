# 03. Blueprints de Fabrication & Recettes de Code

Ce guide fournit aux agents développeurs (Remotion, Canvas 2D, SVG/GSAP, WebGL/Three.js) les algorithmes, formules mathématiques et architectures logicielles nécessaires pour ré-implémenter fidèlement les sept briques visuelles maîtresses de la vidéo `Ug6RUqJ59vKTsnPX.mp4`.

---

## 1. Blueprint 1 : Moteur de Génération & Éclosion de l'Astérisque Claude (12-Arm Sunburst)

Utilisé pour l'introduction (Scène 01, Frames 0 à 112) et la signature finale (Scène 07, Frames 788 à 904).

### 1.1. Principe Géométrique & Modélisation Polaire
L'astérisque signature Claude est composé de **12 rayons arrondis** (capsules géométriques) émanant du centre $(x_c, y_c)$, disposés tous les $30^\circ$ ($\Delta\theta = \frac{2\pi}{12}$).
Chaque rayon $i \in \{0, \dots, 11\}$ possède une longueur $L_i$, une largeur $W$ et des extrémités en demi-cercle parfait (`stroke-linecap: round`).
Dans le logo officiel Claude, les longueurs des rayons présentent de subtiles asymétries organiques qui lui confèrent sa chaleur humaine.
- Longueurs nominales des rayons :
  $$L_i = L_0 \cdot \left[1.0 + 0.18 \cdot \sin(2\theta_i) - 0.08 \cdot \cos(3\theta_i)\right]$$
  avec $L_0 = 120px$ et largeur de trait $W = 20px$.
- Éclosion radiale (Frames 28 à 55) :
  $$R_{progress}(t) = \text{spring}(t; F=2.6, \zeta=0.35)$$
  Chaque rayon s'allonge du centre vers l'extérieur selon $L_i(t) = L_i \cdot R_{progress}(t)$.

### 1.2. Implémentation Complète (TypeScript / Remotion + SVG)

```typescript
import React from 'react';
import { useCurrentFrame, spring } from 'remotion';

interface ClaudeAsteriskProps {
  x: number;
  y: number;
  color?: string;
  size?: number; // Diamètre maximal de référence
  rotationOffset?: number; // En degrés
}

export const ClaudeAsterisk: React.FC<ClaudeAsteriskProps> = ({
  x,
  y,
  color = '#F04B38',
  size = 280,
  rotationOffset = 0,
}) => {
  const frame = useCurrentFrame();
  const fps = 60;

  // Animation d'éclosion en ressort
  const growth = spring({
    frame,
    fps,
    config: {
      damping: 12,
      mass: 0.8,
      stiffness: 100,
    },
  });

  // Pulsation harmonique continue calée sur le BPM (128 BPM = 28.125 frames par beat)
  const pulse = 1 + 0.04 * Math.sin((frame / 28.125) * Math.PI * 2);

  const NUM_RAYS = 12;
  const rayLengths = [1.0, 0.92, 1.08, 0.95, 1.05, 0.90, 1.02, 0.94, 1.06, 0.91, 1.03, 0.96];
  const strokeWidth = (size * 0.08) * growth;

  return (
    <g
      transform={`translate(${x}, ${y}) rotate(${rotationOffset}) scale(${growth * pulse})`}
      style={{ willChange: 'transform' }}
    >
      {rayLengths.map((lenMultiplier, i) => {
        const angleRad = (i * (360 / NUM_RAYS) * Math.PI) / 180;
        const currentLength = (size * 0.42) * lenMultiplier;
        const x2 = Math.cos(angleRad) * currentLength;
        const y2 = Math.sin(angleRad) * currentLength;

        return (
          <line
            key={i}
            x1={0}
            y1={0}
            x2={x2}
            y2={y2}
            stroke={color}
            strokeWidth={strokeWidth}
            strokeLinecap="round"
          />
        );
      })}
    </g>
  );
};
```

---

## 2. Blueprint 2 : Kinetic Typography Variable & Asymmetric Modulation

Utilisé pour l'impact monumental de la Scène 01.2 (Frames 113 à 225).

### 2.1. Principe de Déformation Asymétrique
Le mot "CLAUDE" est affiché en grotesque condensée massive (`#090806`, corps 260px).
Au beat 2 (Frame 141), la lettre "C" subit une dilatation horizontale majeure ($scaleX = 1.85$, expansion de $85\%$), tandis que le bloc restant "LAUDE" subit une contraction compensatoire ($scaleX = 0.72$) afin que la largeur totale du mot demeure ancrée dans les marges de sécurité du viewport ($W_{total} \approx 1400px$).
Simultanément, le sous-titre `motion designer` en italique Didone émerge d'un masque d'écrêtage vertical (`overflow: hidden`) avec amortissement cubique.

### 2.2. Implémentation Complète (TypeScript / React & CSS)

```typescript
import React from 'react';
import { useCurrentFrame, interpolate, spring } from 'remotion';

export const KineticTitleClaude: React.FC = () => {
  const frame = useCurrentFrame();
  const fps = 60;

  // Frame locale dans la scène 01.2 (Frames 113 à 225)
  // Phase 1 : Snap-in d'entrée (Frames 0 à 15 locales)
  const snapScale = interpolate(frame, [0, 12], [1.18, 1.0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Phase 2 : Modulation de largeur du "C" (Déclenchée à la frame locale 28 = Beat 2)
  const stretchProgress = spring({
    frame: frame - 28,
    fps,
    config: { damping: 10, mass: 0.6, stiffness: 120 },
  });

  const scaleXC = interpolate(stretchProgress, [0, 1], [1.0, 1.85]);
  const scaleXRest = interpolate(stretchProgress, [0, 1], [1.0, 0.72]);

  // Phase 3 : Entrée du sous-titre italique (Déclenchée à la frame locale 56 = Beat 3)
  const subtitleY = interpolate(frame - 56, [0, 20], [80, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const subtitleOpacity = interpolate(frame - 56, [0, 15], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        backgroundColor: '#F04B38',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: '"Neue Haas Grotesk", "Inter Tight", sans-serif',
      }}
    >
      {/* Filet supérieur */}
      <div style={{ width: 1400, borderTop: '2px solid #090806', marginBottom: 20 }} />

      {/* Titre Principal CLAUDE avec déformation des glyphes */}
      <div
        style={{
          display: 'flex',
          alignItems: 'baseline',
          fontSize: 260,
          fontWeight: 900,
          letterSpacing: '-0.03em',
          color: '#090806',
          transform: `scale(${snapScale})`,
          lineHeight: 0.85,
        }}
      >
        <span
          style={{
            display: 'inline-block',
            transformOrigin: 'left center',
            transform: `scaleX(${scaleXC})`,
            marginRight: 8,
          }}
        >
          C
        </span>
        <span
          style={{
            display: 'inline-block',
            transformOrigin: 'left center',
            transform: `scaleX(${scaleXRest})`,
          }}
        >
          LAUDE
        </span>
      </div>

      {/* Filet inférieur & Sous-titre Italique Didone */}
      <div style={{ width: 1400, marginTop: 24, position: 'relative' }}>
        <div style={{ width: '100%', borderBottom: '2px solid #090806' }} />

        {/* Masque d'écrêtage vertical */}
        <div
          style={{
            overflow: 'hidden',
            paddingTop: 16,
            display: 'flex',
            justifyContent: 'center',
          }}
        >
          <span
            style={{
              fontFamily: '"Playfair Display", "Instrument Serif", Georgia, serif',
              fontStyle: 'italic',
              fontWeight: 400,
              fontSize: 110,
              color: '#F2EFE6',
              transform: `translateY(${subtitleY}px)`,
              opacity: subtitleOpacity,
              letterSpacing: '-0.01em',
            }}
          >
            motion designer
          </span>
        </div>
      </div>
    </div>
  );
};
```

---

## 3. Blueprint 3 : Simulateur Multi-Easing avec Spacing Chart & Ghosting

Utilisé pour l'expérience didactique majeure de la Scène 02 (Frames 226 à 337).

### 3.1. Formules Mathématiques des 6 Fonctions d'Interpolation
Toutes les fonctions sont normalisées sur l'intervalle $t \in [0, 1]$ et renvoient une progression $p(t) \in [0, 1]$ (ou avec dépassement pour `back` et `elastic`).
Durée de la course : exactement 56 frames ($0.94s$).
Point de départ : $A = 660px$. Point d'arrivée : $B = 1700px$. Course totale : $D = 1040px$.

1. `linear` :
   $$p(t) = t$$
2. `ease-in-out` :
   $$p(t) = \begin{cases} 4t^3 & \text{si } t < 0.5 \\ 1 - \frac{(-2t + 2)^3}{2} & \text{si } t \ge 0.5 \end{cases}$$
3. `expo-out` :
   $$p(t) = 1 - 2^{-10t}$$
4. `back-out` ($s = 1.70158$) :
   $$p(t) = 1 + (s + 1)(t - 1)^3 + s(t - 1)^2$$
5. `elastic-out` :
   $$p(t) = 2^{-10t} \cdot \sin\left(\frac{(10t - 0.75) \cdot 2\pi}{3}\right) + 1$$
6. `bounce-out` :
   $$p(t) = \begin{cases} 
   7.5625 t^2 & \text{si } t < \frac{1}{2.75} \\
   7.5625 (t - \frac{1.5}{2.75})^2 + 0.75 & \text{si } t < \frac{2.25}{2.75} \\
   7.5625 (t - \frac{2.625}{2.75})^2 + 0.9375 & \text{si } t < \frac{2.625}{2.75} \\
   7.5625 (t - \frac{2.75}{2.75})^2 + 0.984375 & \text{sinon}
   \end{cases}$$

### 3.2. Implémentation Complète (Moteur TypeScript / Canvas 2D)

```typescript
export interface EasingTrack {
  id: string;
  name: string;
  color: string;
  fn: (t: number) => number;
}

export const EASING_DEFINITIONS: EasingTrack[] = [
  { id: '01', name: 'linear', color: '#0F0F11', fn: (t) => t },
  {
    id: '02',
    name: 'ease-in-out',
    color: '#2B30FB',
    fn: (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2),
  },
  {
    id: '03',
    name: 'expo-out',
    color: '#F04B38',
    fn: (t) => (t === 1 ? 1 : 1 - Math.pow(2, -10 * t)),
  },
  {
    id: '04',
    name: 'back-out',
    color: '#0F0F11',
    fn: (t) => {
      const c1 = 1.70158;
      const c3 = c1 + 1;
      return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
    },
  },
  {
    id: '05',
    name: 'elastic',
    color: '#2B30FB',
    fn: (t) => {
      if (t === 0) return 0;
      if (t === 1) return 1;
      return Math.pow(2, -10 * t) * Math.sin(((t * 10 - 0.75) * (2 * Math.PI)) / 3) + 1;
    },
  },
  {
    id: '06',
    name: 'bounce',
    color: '#F04B38',
    fn: (t) => {
      const n1 = 7.5625;
      const d1 = 2.75;
      if (t < 1 / d1) return n1 * t * t;
      if (t < 2 / d1) return n1 * (t -= 1.5 / d1) * t + 0.75;
      if (t < 2.5 / d1) return n1 * (t -= 2.25 / d1) * t + 0.9375;
      return n1 * (t -= 2.625 / d1) * t + 0.984375;
    },
  },
];

export function renderEasingScene(
  ctx: CanvasRenderingContext2D,
  frame: number, // Frame locale dans la scène (0 à 112)
  width: number,
  height: number
) {
  const START_X = 660;
  const END_X = 1700;
  const DISTANCE = END_X - START_X;
  const DURATION_FRAMES = 56; // 0.94s exacts
  const BALL_RADIUS = 18;

  const t = Math.min(1, Math.max(0, frame / DURATION_FRAMES));

  // Effacer sur fond crème
  ctx.fillStyle = '#F2EFE6';
  ctx.fillRect(0, 0, width, height);

  EASING_DEFINITIONS.forEach((track, index) => {
    const y = 310 + index * 85;

    // 1. Tracé du rail de guidage
    ctx.strokeStyle = '#D1CDC2';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(START_X, y);
    ctx.lineTo(END_X, y);
    ctx.stroke();

    // Butées A et B
    ctx.beginPath();
    ctx.moveTo(START_X, y - 8);
    ctx.lineTo(START_X, y + 8);
    ctx.moveTo(END_X, y - 8);
    ctx.lineTo(END_X, y + 8);
    ctx.stroke();

    // 2. Ticks de Spacing (échantillonnage toutes les 4 frames jusqu'à la frame active)
    for (let f = 0; f <= Math.min(frame, DURATION_FRAMES); f += 4) {
      const sampleT = f / DURATION_FRAMES;
      const samplePos = START_X + track.fn(sampleT) * DISTANCE;
      ctx.strokeStyle = track.color;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(samplePos, y - 12);
      ctx.lineTo(samplePos, y - 4);
      ctx.stroke();
    }

    // 3. Calcul de la position et de la vitesse instantanée
    const currentProgress = track.fn(t);
    const posX = START_X + currentProgress * DISTANCE;

    // Vitesse instantanée (différence finie sur 1 frame)
    const prevT = Math.max(0, (frame - 1) / DURATION_FRAMES);
    const prevX = START_X + track.fn(prevT) * DISTANCE;
    const velocity = Math.abs(posX - prevX);

    // Déformation en Squash & Stretch sous vitesse
    const stretchX = 1 + Math.min(1.4, velocity * 0.05);
    const scaleY = 1 / stretchX;

    // 4. Traînées de Motion Ghosting (3 échos estompés)
    if (frame > 2 && frame <= DURATION_FRAMES) {
      [2, 4, 6].forEach((lagFrame, ghostIdx) => {
        const lagT = Math.max(0, (frame - lagFrame) / DURATION_FRAMES);
        const ghostX = START_X + track.fn(lagT) * DISTANCE;
        ctx.fillStyle = track.color;
        ctx.globalAlpha = 0.15 - ghostIdx * 0.04;
        ctx.beginPath();
        ctx.arc(ghostX, y, BALL_RADIUS, 0, Math.PI * 2);
        ctx.fill();
      });
      ctx.globalAlpha = 1.0;
    }

    // 5. Bille animée avec étirement elliptique
    ctx.save();
    ctx.translate(posX, y);
    ctx.scale(stretchX, scaleY);
    ctx.fillStyle = track.color;
    ctx.beginPath();
    ctx.arc(0, 0, BALL_RADIUS, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();

    // 6. Onde de choc d'impact après arrivée à B (Frames 56 à 84)
    if (frame >= DURATION_FRAMES) {
      const impactTime = frame - DURATION_FRAMES;
      if (impactTime < 24) {
        const shockRadius = BALL_RADIUS + impactTime * 2.2;
        const shockAlpha = Math.max(0, 1 - impactTime / 24);
        ctx.strokeStyle = track.color;
        ctx.lineWidth = 2;
        ctx.globalAlpha = shockAlpha;
        ctx.beginPath();
        ctx.arc(END_X, y, shockRadius, 0, Math.PI * 2);
        ctx.stroke();
        ctx.globalAlpha = 1.0;
      }
    }
  });
}
```

---

## 4. Blueprint 4 : Moteur de Morphing Géométrique Vectoriel & Dial Satellites

Utilisé pour les transformations topologiques de la Scène 03 (Frames 338 à 450).

### 4.1. Principe d'Échantillonnage Angulaire & Ressort
Pour morpher continûment entre le cercle, le triangle, l'étoile et le carré, une fonction polaire unifiée calcule le rayon $R(\theta)$ pour $N = 360$ points :
1. **Cercle** : $R_{circle}(\theta) = R_0$.
2. **Triangle** ($m=3$) : $R_{tri}(\theta) = \frac{R_0}{\cos(\theta \pmod{\frac{2\pi}{3}} - \frac{\pi}{3}) + 0.15}$.
3. **Étoile à 5 branches** : $R_{star}(\theta) = R_{mid} + R_{amp} \cdot \cos(5\theta)$.
4. **Carré (Superellipse)** : $R_{sq}(\theta) = \frac{R_0}{(|\cos\theta|^4 + |\sin\theta|^4)^{1/4}}$.

L'interpolation entre les géométries est asservie à un ressort harmonique sous-amorti ($F = 2.6 \text{ Hz}, \zeta = 0.30$) qui provoque un léger dépassement élastique (overshoot) lors de chaque transition de forme.
Des lignes filaires fantômes de couleur orange/rouge (`rgba(240, 75, 56, 0.25)`) sont conservées en mémoire tampon pour tracer les révolutions passées.

### 4.2. Implémentation Complète (Algorithme TypeScript Canvas)

```typescript
export function computeMorphedPolygon(
  shapeTypeA: 'circle' | 'triangle' | 'star' | 'square',
  shapeTypeB: 'circle' | 'triangle' | 'star' | 'square',
  morphProgress: number, // 0.0 à 1.0 (piloté par ressort)
  baseRadius: number,
  pointsCount: number = 180
): Array<[number, number]> {
  const getRadius = (type: string, theta: number): number => {
    switch (type) {
      case 'circle':
        return baseRadius;
      case 'triangle': {
        const sector = (2 * Math.PI) / 3;
        const modTheta = ((theta % sector) + sector) % sector - sector / 2;
        return baseRadius / (Math.cos(modTheta) + 0.2);
      }
      case 'star': {
        const k = 5;
        const modulation = 0.45 * Math.cos(k * theta);
        return baseRadius * (0.8 + modulation);
      }
      case 'square': {
        const n = 4;
        const cosT = Math.cos(theta);
        const sinT = Math.sin(theta);
        return baseRadius / Math.pow(Math.pow(Math.abs(cosT), n) + Math.pow(Math.abs(sinT), n), 1 / n);
      }
      default:
        return baseRadius;
    }
  };

  const vertices: Array<[number, number]> = [];
  for (let i = 0; i < pointsCount; i++) {
    const theta = (i * 2 * Math.PI) / pointsCount;
    const rA = getRadius(shapeTypeA, theta);
    const rB = getRadius(shapeTypeB, theta);
    const currentR = rA + (rB - rA) * morphProgress;
    vertices.push([Math.cos(theta) * currentR, Math.sin(theta) * currentR]);
  }
  return vertices;
}
```

---

## 5. Blueprint 5 : Labyrinthe Génératif de Pavage de Truchet Multi-Vagues

Utilisé pour les motifs en tuyauterie procédurale de la Scène 04 (Frames 451 à 562).

### 5.1. Principe Mathématique du Pavage de Truchet
La scène est découpée en **153 cellules carrées** ($17 \text{ colonnes} \times 9 \text{ rangées}$, pas de tuile $S = 112px$).
Chaque cellule contient deux arcs de cercle opposés de rayon $R = \frac{S}{2} = 56px$ et d'épaisseur $12px$.
Une cellule à la position $(col, row)$ possède une orientation binaire $\theta \in \{0^\circ, 90^\circ\}$.
Trois vagues de perturbation se superposent dans le temps :
1. **Vague 1 (Front vertical)** : Décalage d'angle $\Delta\theta_1(x) = 90^\circ \cdot \text{smoothstep}(v_1 t - x)$. Bascule de couleur du blanc-crème (`#F2EFE6`) vers le rouge vermillon (`#F04B38`).
2. **Vague 2 (Front de retour)** : Deuxième rotation de $90^\circ$ restaurant la couleur blanche.
3. **Vague 3 (Onde concentrique radiale)** : Perturbation angulaire proportionnelle à la distance euclidienne au centre :
   $$\Delta\theta_3(r) = 90^\circ \cdot \exp\left(-\frac{(r - v_3 t)^2}{2\sigma^2}\right)$$

### 5.2. Implémentation Complète (Composant Canvas Haute Performance)

```typescript
export interface TruchetTile {
  col: number;
  row: number;
  initialOrientation: 0 | 1; // 0: coins (NO, SE), 1: coins (NE, SO)
  rotationAngle: number; // Angle continu en radians
  color: string;
}

export function drawTruchetTile(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  size: number,
  angle: number,
  color: string
) {
  const r = size / 2;
  ctx.save();
  ctx.translate(x + r, y + r);
  ctx.rotate(angle);
  ctx.translate(-r, -r);

  ctx.strokeStyle = color;
  ctx.lineWidth = 12;
  ctx.lineCap = 'butt';

  // Arc 1 : Coin supérieur gauche (0, 0)
  ctx.beginPath();
  ctx.arc(0, 0, r, 0, Math.PI / 2);
  ctx.stroke();

  // Arc 2 : Coin inférieur droit (size, size)
  ctx.beginPath();
  ctx.arc(size, size, r, Math.PI, (3 * Math.PI) / 2);
  ctx.stroke();

  ctx.restore();
}

export function updateAndRenderTruchetBoard(
  ctx: CanvasRenderingContext2D,
  frame: number, // Frame locale scène 04 (0 à 112)
  width: number = 1920,
  height: number = 1080
) {
  const COLS = 17;
  const ROWS = 9;
  const SIZE = 112;
  const offsetX = (width - COLS * SIZE) / 2;
  const offsetY = (height - ROWS * SIZE) / 2;

  ctx.fillStyle = '#0F0F11';
  ctx.fillRect(0, 0, width, height);

  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      const tileX = offsetX + c * SIZE;
      const tileY = offsetY + r * SIZE;

      // Pseudo-random initial orientation (Seed 0x2A = 42)
      const isAlt = ((c * 73 + r * 37 + 42) % 100) > 50;
      let angle = isAlt ? Math.PI / 2 : 0;
      let tileColor = '#F2EFE6';

      // Vague 1 : Balayage horizontal de gauche à droite (Frames 20 à 60)
      if (frame >= 20) {
        const waveX = (frame - 20) * 48; // v = 48 px/frame
        const distFromFront = waveX - tileX;
        if (distFromFront > 0) {
          const progress = Math.min(1, distFromFront / 200);
          angle += progress * (Math.PI / 2);
          tileColor = progress > 0.5 ? '#F04B38' : '#F2EFE6';
        }
      }

      // Vague 3 : Onde circulaire radiale depuis le centre (Frames 75 à 110)
      if (frame >= 75) {
        const centerX = width / 2;
        const centerY = height / 2;
        const distCenter = Math.hypot(tileX + SIZE / 2 - centerX, tileY + SIZE / 2 - centerY);
        const ringRadius = (frame - 75) * 32;
        const ringDiff = Math.abs(distCenter - ringRadius);
        if (ringDiff < 180) {
          const bump = Math.cos((ringDiff / 180) * (Math.PI / 2));
          angle += bump * Math.PI;
        }
      }

      drawTruchetTile(ctx, tileX, tileY, SIZE, angle, tileColor);
    }
  }
}
```

---

## 6. Blueprint 6 : Moteur de Projection 3D & Nuage de Points (Sphere & Torus)

Utilisé pour les visualisations spatiales de la Scène 05 (Frames 563 à 675).

### 6.1. Projection Perspective & Formules Toroïdales
576 sommets ($N_u = 24, N_v = 24 \implies 24 \times 24 = 576$) sont projetés selon une caméra virtuelle :
- Matrice de coordonnées pour le tore ($R = 320px, r = 110px$) :
  $$X(u, v) = (R + r \cos v) \cos u$$
  $$Y(u, v) = (R + r \cos v) \sin u$$
  $$Z(u, v) = r \sin v$$
- Rotation sur l'axe Y :
  $$X' = X \cos\theta + Z \sin\theta, \quad Y' = Y, \quad Z' = -X \sin\theta + Z \cos\theta$$
- Projection en perspective (Focale $F = 1400$, distance caméra $d_0 = 1200$) :
  $$x_{screen} = x_c + \frac{X' \cdot F}{Z' + d_0}, \quad y_{screen} = y_c + \frac{Y' \cdot F}{Z' + d_0}$$
- Flou de profondeur de champ (DoF) :
  $$CoC(Z') = \left|\frac{Z' - Z_{focus}}{Z_{max}}\right| \cdot R_{blur}$$

### 6.2. Implémentation Complète (TypeScript Canvas 3D)

```typescript
export interface Vertex3D {
  x: number;
  y: number;
  z: number;
  isRed: boolean;
}

export function generateTorusVertices(R: number = 320, r: number = 110): Vertex3D[] {
  const vertices: Vertex3D[] = [];
  const U_SEGMENTS = 24;
  const V_SEGMENTS = 24;

  for (let u = 0; u < U_SEGMENTS; u++) {
    const theta = (u * 2 * Math.PI) / U_SEGMENTS;
    for (let v = 0; v < V_SEGMENTS; v++) {
      const phi = (v * 2 * Math.PI) / V_SEGMENTS;
      const x = (R + r * Math.cos(phi)) * Math.cos(theta);
      const z = (R + r * Math.cos(phi)) * Math.sin(theta);
      const y = r * Math.sin(phi);
      // Sélection pseudo-aléatoire de 15% de sommets rouges
      const isRed = ((u * 17 + v * 31) % 100) < 15;
      vertices.push({ x, y, z, isRed });
    }
  }
  return vertices;
}

export function render3DScene(
  ctx: CanvasRenderingContext2D,
  frame: number,
  vertices: Vertex3D[],
  width: number = 1920,
  height: number = 1080
) {
  const FOCAL = 1400;
  const CAM_DIST = 1100;
  const rotY = (frame * 0.024) + 0.4;
  const rotX = 0.45; // Plongée caméra fixe

  ctx.fillStyle = '#0F0F11';
  ctx.fillRect(0, 0, width, height);

  // Transformation et projection
  const projected = vertices.map((v) => {
    // Rotation Y
    const x1 = v.x * Math.cos(rotY) + v.z * Math.sin(rotY);
    const y1 = v.y;
    const z1 = -v.x * Math.sin(rotY) + v.z * Math.cos(rotY);

    // Rotation X
    const x2 = x1;
    const y2 = y1 * Math.cos(rotX) - z1 * Math.sin(rotX);
    const z2 = y1 * Math.sin(rotX) + z1 * Math.cos(rotX);

    const scale = FOCAL / (z2 + CAM_DIST);
    const sx = width / 2 + x2 * scale;
    const sy = height / 2 + y2 * scale;

    return { sx, sy, z: z2, scale, isRed: v.isRed };
  });

  // Tri par profondeur Z (Painter's algorithm)
  projected.sort((a, b) => b.z - a.z);

  // Rendu des sommets avec simulation de Depth of Field (DoF)
  projected.forEach((p) => {
    const dofBlur = Math.abs(p.z) * 0.006;
    const dotRadius = Math.max(1, (p.isRed ? 4.5 : 2.8) * p.scale);

    ctx.fillStyle = p.isRed ? '#F04B38' : '#F2EFE6';
    ctx.globalAlpha = Math.min(1, Math.max(0.15, p.scale * 0.8));

    ctx.beginPath();
    ctx.arc(p.sx, p.sy, dotRadius + dofBlur, 0, Math.PI * 2);
    ctx.fill();
  });

  ctx.globalAlpha = 1.0;
}
```

---

## 7. Blueprint 7 : Onde de Choc d'Iris Bloom & Dispersion de Confettis

Utilisé pour l'apothéose finale de la Scène 07 (Frames 788 à 845).

### 7.1. Principe de Diffraction Spectrale & Balistique de Particules
À la frame 788 (Bar 8 Beat 1), un sous-choc acoustique déclenche :
1. **L'Iris Bloom Shockwave** : Un tore circulaire 2D d'expansion exponentielle $R(t) = R_{max} \cdot (1 - e^{-k t})$ dont l'épaisseur s'affine. Le shader simule une dispersion chromatique avec bord externe rosé/cyan.
2. **La Déflagration Balistique** : 40 particules géométriques (carrés de $8 \times 8px$, disques de $R=5px$, triangles de $10px$) sont expulsées avec une vitesse initiale aléatoire $v_0 \in [18, 42] px/\text{frame}$, un angle radial $\theta_i \in [0, 2\pi]$ et une traînée aérodynamique visqueuse $v(t) = v_0 \cdot \gamma^t$ avec $\gamma = 0.92$.

### 7.2. Implémentation Complète (TypeScript / Remotion)

```typescript
export interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  rotation: number;
  vRot: number;
  shape: 'circle' | 'square' | 'triangle';
  color: string;
  size: number;
}

export function generateExplosionParticles(count: number = 40): Particle[] {
  const colors = ['#F2EFE6', '#302FF5', '#090806', '#FFFFFF'];
  const shapes: Array<'circle' | 'square' | 'triangle'> = ['circle', 'square', 'triangle'];
  const particles: Particle[] = [];

  for (let i = 0; i < count; i++) {
    const angle = Math.random() * Math.PI * 2;
    const speed = 12 + Math.random() * 26;
    particles.push({
      x: 960,
      y: 540,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      rotation: Math.random() * 360,
      vRot: (Math.random() - 0.5) * 15,
      shape: shapes[Math.floor(Math.random() * shapes.length)],
      color: colors[Math.floor(Math.random() * colors.length)],
      size: 6 + Math.random() * 6,
    });
  }
  return particles;
}

export function renderShockwaveAndParticles(
  ctx: CanvasRenderingContext2D,
  frame: number, // Frame locale scène 07 (0 à 60)
  particles: Particle[]
) {
  // 1. Fond rouge vermillon
  ctx.fillStyle = '#F04B38';
  ctx.fillRect(0, 0, 1920, 1080);

  // 2. Onde de choc d'iris bloom circulaire (Frames 0 à 25)
  if (frame < 25) {
    const progress = frame / 25;
    const radius = progress * 1100;
    const alpha = Math.max(0, 1 - progress);

    const gradient = ctx.createRadialGradient(960, 540, radius * 0.85, 960, 540, radius);
    gradient.addColorStop(0, 'rgba(255, 255, 255, 0)');
    gradient.addColorStop(0.7, `rgba(255, 240, 200, ${alpha * 0.8})`);
    gradient.addColorStop(0.9, `rgba(255, 120, 160, ${alpha * 0.9})`);
    gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');

    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(960, 540, radius, 0, Math.PI * 2);
    ctx.fill();
  }

  // 3. Mise à jour et rendu des particules balistiques
  particles.forEach((p) => {
    const decay = Math.pow(0.91, frame);
    const px = 960 + p.vx * ((1 - decay) / (1 - 0.91));
    const py = 540 + p.vy * ((1 - decay) / (1 - 0.91));
    const rot = p.rotation + p.vRot * frame;
    const alpha = Math.max(0, 1 - frame / 50);

    ctx.save();
    ctx.translate(px, py);
    ctx.rotate((rot * Math.PI) / 180);
    ctx.fillStyle = p.color;
    ctx.globalAlpha = alpha;

    if (p.shape === 'circle') {
      ctx.beginPath();
      ctx.arc(0, 0, p.size / 2, 0, Math.PI * 2);
      ctx.fill();
    } else if (p.shape === 'square') {
      ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
    } else {
      ctx.beginPath();
      ctx.moveTo(0, -p.size / 2);
      ctx.lineTo(p.size / 2, p.size / 2);
      ctx.lineTo(-p.size / 2, p.size / 2);
      ctx.closePath();
      ctx.fill();
    }

    ctx.restore();
  });
  ctx.globalAlpha = 1.0;
}
```
