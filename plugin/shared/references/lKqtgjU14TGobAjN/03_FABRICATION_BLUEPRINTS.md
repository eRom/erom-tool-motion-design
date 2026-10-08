# 03. Blueprints de Fabrication & Recettes de Code

Ce guide fournit aux agents développeurs (Remotion, Canvas 2D, SVG/GSAP, WebGL/Three.js) les algorithmes, formules mathématiques et architectures logicielles nécessaires pour ré-implémenter fidèlement les six briques visuelles maîtresses de la vidéo.

---

## 1. Moteur 1 : Simulateur Bouncing Ball avec Squash & Stretch Vectoriel

Utilisé pour la discipline `01 / SQUASH & STRETCH` (Frames 0 à 54).

### Principe Mathématique & Physique
1. **Trajectoire verticale & Gravité** :
   - Chute libre accélérée : $y(t) = y_0 + v_0 t + \frac{1}{2} g t^2$ avec $g \approx 3.2 \text{ px/frame}^2$.
   - Coefficient de restitution : Lors du premier rebond, $v_{rebound} = -e \cdot v_{impact}$ avec $e = 0.62$.
2. **Conservation Volumétrique & Déformation Elliptique** :
   - Pendant le vol, étirement proportionnel à la vélocité : $s_y = 1.0 + k_{stretch} \cdot |v|$, et par conservation de l'aire $s_x = \frac{1}{s_y}$.
   - Lors de l'impact contre le sol ($Y_{floor} = 740px$), écrasement harmonique :
     $$s_y(t) = 1.0 - (1.0 - s_{y,min}) \cdot \sin\left(\frac{\pi (t - t_{hit})}{\Delta t_{squash}}\right)$$
     avec $s_{y,min} = 0.38$ sur le premier impact ($\Delta t_{squash} = 4 \text{ frames}$) et $s_x = \frac{1}{s_y} \approx 2.63$.
3. **Ombre Portée Dynamique (Contact Shadow)** :
   - Largeur : $w_{shadow} = w_0 \cdot \left(1.0 - 0.7 \cdot \frac{Y_{floor} - y}{H_{max}}\right)$.
   - Opacité : $\alpha_{shadow} = \alpha_{max} \cdot \left(1.0 - \frac{Y_{floor} - y}{H_{max}}\right)^2$.
4. **Dilatation Exponentielle Finale (Frames 45 à 54)** :
   $$R(t) = R_{nominal} \cdot \exp\left(0.32 \cdot (t - t_{expand})\right)$$

### Implémentation Complète (TypeScript / Remotion + Canvas 2D)

```typescript
import React, { useRef, useEffect } from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';

interface BallPhysicsState {
  y: number;
  scaleX: number;
  scaleY: number;
  shadowWidth: number;
  shadowOpacity: number;
}

export function computeBallPhysics(frame: number): BallPhysicsState {
  const FLOOR_Y = 740;
  const REST_Y = 680;
  const RADIUS = 60; // Diamètre nominal 120px

  // Phase 1 : Chute 1 (Frames 12 à 18)
  if (frame < 18) {
    const t = Math.max(0, frame - 12);
    const progress = t / 6;
    const y = 120 + progress * progress * (FLOOR_Y - RADIUS - 120);
    const stretch = 1.0 + 0.52 * progress;
    return {
      y,
      scaleX: 1 / stretch,
      scaleY: stretch,
      shadowWidth: 60 + 60 * progress,
      shadowOpacity: 0.15 + 0.45 * progress,
    };
  }

  // Phase 2 : Impact 1 - Squash (Frames 18 à 21)
  if (frame <= 21) {
    const tSquash = (frame - 18) / 3;
    const squashFactor = Math.sin(tSquash * Math.PI);
    const sy = 1.0 - 0.62 * squashFactor; // Min 0.38
    return {
      y: FLOOR_Y - RADIUS * sy,
      scaleX: 1 / sy,
      scaleY: sy,
      shadowWidth: 120 + 60 * squashFactor,
      shadowOpacity: 0.65,
    };
  }

  // Phase 3 : Rebond 1 vers Apex (Frames 22 à 28)
  if (frame <= 28) {
    const t = (frame - 21) / 7;
    // Courbe décélérée vers apex Y = 380
    const easeOut = Math.sin(t * (Math.PI / 2));
    const y = FLOOR_Y - RADIUS - easeOut * (FLOOR_Y - RADIUS - 380);
    const sy = 1.0 + 0.41 * (1 - t);
    return {
      y,
      scaleX: 1 / sy,
      scaleY: sy,
      shadowWidth: 120 - 50 * t,
      shadowOpacity: 0.65 - 0.40 * t,
    };
  }

  // Phase 4 : Descente 2 vers Sol (Frames 29 à 37)
  if (frame <= 37) {
    const t = (frame - 28) / 9;
    const easeIn = t * t;
    const y = 380 + easeIn * (FLOOR_Y - RADIUS - 380);
    const sy = 1.0 + 0.23 * t;
    return {
      y,
      scaleX: 1 / sy,
      scaleY: sy,
      shadowWidth: 70 + 45 * t,
      shadowOpacity: 0.25 + 0.35 * t,
    };
  }

  // Phase 5 : Impact 2 - Squash amorti (Frames 38 à 41)
  if (frame <= 41) {
    const tSquash = (frame - 37) / 4;
    const squashFactor = Math.sin(tSquash * Math.PI);
    const sy = 1.0 - 0.41 * squashFactor; // Min 0.59
    return {
      y: FLOOR_Y - RADIUS * sy,
      scaleX: 1 / sy,
      scaleY: sy,
      shadowWidth: 115 + 35 * squashFactor,
      shadowOpacity: 0.60,
    };
  }

  // Phase 6 : Repos statique (Frames 42 à 44)
  if (frame <= 44) {
    return {
      y: REST_Y,
      scaleX: 1.0,
      scaleY: 1.0,
      shadowWidth: 120,
      shadowOpacity: 0.55,
    };
  }

  // Phase 7 : Dilatation exponentielle (Frames 45 à 54)
  const tExp = frame - 44;
  const expScale = Math.exp(tExp * 0.34);
  return {
    y: REST_Y,
    scaleX: expScale,
    scaleY: expScale,
    shadowWidth: 120 * expScale,
    shadowOpacity: Math.max(0, 0.55 - tExp * 0.1),
  };
}

export const SquashAndStretchCanvas: React.FC = () => {
  const frame = useCurrentFrame();
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.clearRect(0, 0, 1920, 1080);
    const phys = computeBallPhysics(frame);
    const CENTER_X = 960;
    const FLOOR_Y = 740;

    // 1. Tracé de la ligne de sol
    ctx.strokeStyle = '#1C1917';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(CENTER_X - 400, FLOOR_Y);
    ctx.lineTo(CENTER_X + 400, FLOOR_Y);
    ctx.stroke();

    // 2. Ombre de contact au sol
    if (phys.shadowOpacity > 0.01) {
      ctx.save();
      ctx.fillStyle = `rgba(28, 25, 23, ${phys.shadowOpacity})`;
      ctx.beginPath();
      ctx.ellipse(CENTER_X, FLOOR_Y, phys.shadowWidth / 2, 8, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }

    // 3. Balle Terracotta déformée
    ctx.save();
    ctx.translate(CENTER_X, phys.y);
    ctx.scale(phys.scaleX, phys.scaleY);
    ctx.fillStyle = '#C5593C';
    ctx.beginPath();
    ctx.arc(0, 0, 60, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }, [frame]);

  return <canvas ref={canvasRef} width={1920} height={1080} className="absolute inset-0" />;
};
```

---

## 2. Moteur 2 : Grille Nodale Réactive & Double Vague de Morphing

Utilisé pour la discipline `02 / SHAPE & RHYTHM` (Frames 100 à 180).

### Principe Mathématique
1. **Structure de la Matrice** : 91 nœuds ($N_x = 13$, $N_y = 7$) centrés sur $(960, 540)$ avec un pas de $80px \times 80px$.
2. **Onde Concentrique (Disques, Frames 100 à 120)** :
   $$r_i = r_{base} + A \cdot \cos\left(k \cdot d_i - \omega \cdot t\right)$$
   avec $d_i = \sqrt{(x_i - x_0)^2 + (y_i - y_0)^2}$, $r_{base} = 9.5px$, $A = 6.5px$, $k = 0.012$, $\omega = 0.35$.
3. **Première Vague de Morphing : Disques $\to$ Carrés (Frames 121 à 145)** :
   Front d'onde se déplaçant selon l'axe X :
   $$p_1(x, t) = \text{clamp}\left(\frac{(t - 120) \cdot v_1 - x}{W_{fade}}, 0, 1\right)$$
   - Forme : `border-radius` varie de $50\%$ à $4px$.
   - Dimension : $2 \cdot r_i \to 24px$.
   - Couleur : Interpolation RVB de `#1C1917` vers `#C5593C`.
   - Rotation : $\theta(t) = 90^\circ \cdot p_1(x, t)$.
4. **Seconde Vague de Morphing : Carrés $\to$ Bâtonnets Vectoriels (Frames 146 à 174)** :
   $$p_2(x, t) = \text{clamp}\left(\frac{(t - 145) \cdot v_2 - x}{W_{fade}}, 0, 1\right)$$
   - Forme : Largeur $24px \to 36px$, Hauteur $24px \to 6px$.
   - Orientation tangentielle d'un champ de tourbillon (Vortex) :
     $$\phi_i = \text{atan2}(y_i - 540, x_i - 960) + \frac{\pi}{2} + 0.05 \cdot (t - 145)$$
   - Teinte : 80% noir (`#1C1917`), 20% terracotta (`#C5593C`) selon un masque pseudo-aléatoire déterministe.

### Implémentation Complète (TypeScript / Remotion + SVG)

```typescript
import React from 'react';
import { useCurrentFrame } from 'remotion';

interface GridNode {
  col: number;
  row: number;
  x: number;
  y: number;
  distToCenter: number;
  isAccent: boolean;
}

const COLS = 13;
const ROWS = 7;
const PITCH = 80;
const ORIGIN_X = 960 - ((COLS - 1) * PITCH) / 2; // 480
const ORIGIN_Y = 540 - ((ROWS - 1) * PITCH) / 2; // 300

const NODES: GridNode[] = [];
for (let r = 0; r < ROWS; r++) {
  for (let c = 0; c < COLS; c++) {
    const x = ORIGIN_X + c * PITCH;
    const y = ORIGIN_Y + r * PITCH;
    const distToCenter = Math.hypot(x - 960, y - 540);
    // Accent terracotta déterministe sur 20% des nœuds
    const isAccent = (c * 7 + r * 13) % 5 === 0;
    NODES.push({ col: c, row: r, x, y, distToCenter, isAccent });
  }
}

export const ShapeAndRhythmGrid: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <svg width={1920} height={1080} className="absolute inset-0 pointer-events-none">
      {/* Filigrane d'arrière-plan RHYTHM */}
      <text
        x={960}
        y={580}
        textAnchor="middle"
        className="font-black select-none"
        style={{
          fontFamily: 'Inter Tight, system-ui, sans-serif',
          fontSize: '300px',
          fontWeight: 900,
          fill: '#DFD9CC',
          letterSpacing: '0.02em',
        }}
      >
        RHYTHM
      </text>

      {/* Matrice de 91 nœuds dynamiques */}
      {NODES.map((node, i) => {
        // Phase 1 : Ondulation concentrique (Frames 100 à 120)
        const ripplePhase = node.distToCenter * 0.012 - (frame - 100) * 0.35;
        const radius = 9.5 + 6.5 * Math.cos(ripplePhase);

        // Progression Vague 1 : Disques -> Carrés (Frames 121 à 145)
        const wave1Progress = Math.min(
          1,
          Math.max(0, ((frame - 120) * 60 - (node.x - ORIGIN_X)) / 160)
        );

        // Progression Vague 2 : Carrés -> Bâtonnets (Frames 146 à 175)
        const wave2Progress = Math.min(
          1,
          Math.max(0, ((frame - 145) * 60 - (node.x - ORIGIN_X)) / 160)
        );

        // Interpolation dimensions
        const sizeCircle = radius * 2;
        const sizeSquare = 24;
        const stickW = 36;
        const stickH = 6;

        let width = sizeCircle + (sizeSquare - sizeCircle) * wave1Progress;
        let height = width;
        let rx = (width / 2) * (1 - wave1Progress) + 4 * wave1Progress;
        let rotation = 90 * wave1Progress;

        if (wave2Progress > 0) {
          width = sizeSquare + (stickW - sizeSquare) * wave2Progress;
          height = sizeSquare + (stickH - sizeSquare) * wave2Progress;
          rx = 2; // Léger arrondi sur les bâtonnets
          // Champ vectoriel de vortex
          const vortexAngle =
            Math.atan2(node.y - 540, node.x - 960) * (180 / Math.PI) +
            90 +
            (frame - 145) * 2.5;
          rotation = 90 + (vortexAngle - 90) * wave2Progress;
        }

        // Interpolation couleur
        let fillColor = '#1C1917';
        if (wave1Progress > 0 && wave2Progress === 0) {
          fillColor = '#C5593C';
        } else if (wave2Progress > 0) {
          fillColor = node.isAccent ? '#C5593C' : '#1C1917';
        }

        return (
          <g
            key={i}
            transform={`translate(${node.x}, ${node.y}) rotate(${rotation})`}
          >
            <rect
              x={-width / 2}
              y={-height / 2}
              width={width}
              height={height}
              rx={rx}
              ry={rx}
              fill={fillColor}
            />
          </g>
        );
      })}
    </svg>
  );
};
```

---

## 3. Moteur 3 : Odomètre Numérique & Étalonnage Comparatif d'Easing

Utilisé pour la discipline `03 / DATA IN MOTION` (Frames 180 à 270).

### Principe Mathématique
1. **Odomètre de Frames** : Progression de `0` à `450` avec la fonction `expo.out` sur 45 frames (Frames 185 à 230) :
   $$\text{value}(t) = \text{round}\left(450 \cdot (1 - 2^{-10 \cdot \frac{t - 185}{45}})\right)$$
2. **Histogramme 15 Barres (1 bar / seconde)** :
   Chaque barre $i \in [0, 14]$ s'active séquentiellement lorsque l'odomètre franchit le palier $(i + 1) \times 30$ frames.
   Hauteur cible : profil logarithmique saturant $h_i = 160 \cdot (1 - e^{-(i + 1) / 3.8})$. La 15e barre est teintée en `#C5593C`.
3. **Course des Traceurs sur la Courbe d'Asservissement (Frames 220 à 260)** :
   - Coordonnées normalisées $u \in [0, 1]$ sur $\Delta t = 40 \text{ frames}$ (1.0 seconde) :
     - Bille Linéaire : $x_{lin}(u) = u$, $y_{lin}(u) = u$.
     - Bille Exponentielle : $x_{exp}(u) = u$, $y_{exp}(u) = 1 - 2^{-10 u}$.
   - Projection dans le repère graphique $W_{box} = 480px, H_{box} = 340px$ :
     $$X_{screen} = X_{origin} + x(u) \cdot W_{box}, \quad Y_{screen} = Y_{origin} + (1 - y(u)) \cdot H_{box}$$

### Implémentation Complète (TypeScript / Remotion)

```typescript
import React from 'react';
import { useCurrentFrame } from 'remotion';

export const DataInMotionScene: React.FC = () => {
  const frame = useCurrentFrame();

  // 1. Calcul du compteur de frames (Frames 185 à 230)
  const countProgress = Math.min(1, Math.max(0, (frame - 185) / 45));
  const easeExpo = countProgress === 1 ? 1 : 1 - Math.pow(2, -10 * countProgress);
  const frameCount = Math.round(450 * easeExpo);

  // 2. Barres de l'histogramme (15 secondes)
  const TOTAL_BARS = 15;
  const BAR_PITCH = 48;
  const BAR_WIDTH = 34;

  // 3. Course des traceurs (Frames 220 à 260 = 40 frames = 1.0s)
  const raceProgress = Math.min(1, Math.max(0, (frame - 220) / 40));
  const expoY = raceProgress === 1 ? 1 : 1 - Math.pow(2, -10 * raceProgress);
  const linearY = raceProgress;

  // Repère du graphique de droite
  const GRAPH_X = 1040;
  const GRAPH_Y = 240;
  const GRAPH_W = 460;
  const GRAPH_H = 340;

  return (
    <div className="absolute inset-0 bg-[#EBE7DB] p-10 font-mono select-none">
      {/* Panneau Gauche : Odomètre & Barres */}
      <div className="absolute left-[120px] top-[220px]">
        <div className="text-[180px] font-bold text-[#1C1917] leading-none tracking-tight">
          {frameCount}
        </div>
        <div className="text-[20px] font-medium text-[#1C1917] tracking-wider mt-4">
          FRAMES IN THIS REEL
        </div>

        {/* Histogramme de 15 barres */}
        <div className="flex items-end gap-[14px] h-[180px] mt-12">
          {Array.from({ length: TOTAL_BARS }).map((_, i) => {
            const isVisible = frameCount >= (i + 1) * 28;
            const targetHeight = Math.round(180 * (1 - Math.exp(-(i + 1) / 4.2)));
            const isLast = i === TOTAL_BARS - 1;
            return (
              <div
                key={i}
                style={{
                  width: `${BAR_WIDTH}px`,
                  height: isVisible ? `${targetHeight}px` : '0px',
                  backgroundColor: isLast ? '#C5593C' : '#1C1917',
                  transition: 'height 0.08s ease-out',
                }}
              />
            );
          })}
        </div>
        <div className="text-[16px] text-[#8A877E] mt-4 tracking-widest uppercase">
          15 SECONDS · 30 FPS · 1 TIMELINE
        </div>
      </div>

      {/* Panneau Droit : Graphique Comparatif */}
      <div className="absolute left-[980px] top-[180px] w-[580px] h-[480px] bg-[#FAF8F5] border-[3px] border-[#1C1917] p-6 shadow-sm">
        <div className="flex justify-between text-[16px] font-bold text-[#1C1917] mb-6">
          <span>VALUE / TIME</span>
          <span>SAME 1.0s</span>
        </div>

        <svg width={GRAPH_W} height={GRAPH_H} className="overflow-visible">
          {/* Grille interne */}
          <line x1={0} y1={GRAPH_H / 2} x2={GRAPH_W} y2={GRAPH_H / 2} stroke="#E5E0D5" strokeWidth={1} />
          <line x1={GRAPH_W / 2} y1={0} x2={GRAPH_W / 2} y2={GRAPH_H} stroke="#E5E0D5" strokeWidth={1} />

          {/* Axes X et Y */}
          <line x1={0} y1={0} x2={0} y2={GRAPH_H} stroke="#1C1917" strokeWidth={2} />
          <line x1={0} y1={GRAPH_H} x2={GRAPH_W} y2={GRAPH_H} stroke="#1C1917" strokeWidth={2} />

          {/* Diagonale linéaire (pointillée) */}
          <line
            x1={0}
            y1={GRAPH_H}
            x2={GRAPH_W}
            y2={0}
            stroke="#1C1917"
            strokeWidth={2}
            strokeDasharray="6 6"
          />

          {/* Courbe expo.out */}
          <path
            d={Array.from({ length: 50 })
              .map((_, idx) => {
                const u = idx / 49;
                const ey = 1 - Math.pow(2, -10 * u);
                const px = u * GRAPH_W;
                const py = GRAPH_H - ey * GRAPH_H;
                return `${idx === 0 ? 'M' : 'L'} ${px} ${py}`;
              })
              .join(' ')}
            fill="none"
            stroke="#C5593C"
            strokeWidth={4}
          />

          {/* Traceur Linéaire (Bille Blanche) */}
          <circle
            cx={raceProgress * GRAPH_W}
            cy={GRAPH_H - linearY * GRAPH_H}
            r={8}
            fill="#FAF8F5"
            stroke="#1C1917"
            strokeWidth={2}
          />

          {/* Traceur Exponentiel (Bille Terracotta) */}
          <circle
            cx={raceProgress * GRAPH_W}
            cy={GRAPH_H - expoY * GRAPH_H}
            r={8}
            fill="#C5593C"
            stroke="#1C1917"
            strokeWidth={2}
          />

          {/* Libellés de courbes */}
          <text x={GRAPH_W - 120} y={60} fill="#1C1917" fontSize={16}>
            expo.out
          </text>
          <text x={GRAPH_W - 100} y={GRAPH_H - 80} fill="#1C1917" fontSize={16}>
            linear
          </text>
        </svg>
      </div>
    </div>
  );
};
```

---

## 4. Moteur 4 : Carrousel 3D Cylindrique / Octogonal (CSS 3D / Remotion)

Utilisé pour la discipline `04 / DEPTH & EASE` (Frames 270 à 360).

### Principe Géométrique
1. **Octogone Régulier dans l'Espace** :
   - $N = 8$ fiches de dimensions $W = 375px, H = 500px$ (ratio 3:4).
   - Angle d'ouverture par fiche : $\alpha = \frac{360^\circ}{8} = 45^\circ$.
   - Rayon circonscrit du prisme :
     $$R = \frac{W / 2}{\tan(\alpha / 2)} = \frac{187.5}{\tan(22.5^\circ)} = \frac{187.5}{0.4142} \approx 452.7px$$
2. **Orientation des Faces** :
   Chaque fiche $k \in [0, 7]$ subit la transformation CSS :
   $$\text{transform} = \text{rotateY}(k \cdot 45^\circ) \; \text{translateZ}(453px)$$
3. **Révolution & Angle Caméra** :
   Le cylindre complet tourne autour de l'axe Y : $\Theta(t) = \Theta_0 + \omega \cdot t$ avec un léger tilt de caméra $\text{rotateX}(12^\circ)$ et une perspective de $1200px$.
4. **Faces Bifaces** :
   - Face avant : fond blanc crème `#FAF8F5`, bordure noire 3px, formule et courbe d'easing.
   - Face arrière : fond plein terracotta `#C5593C`, bordure noire 3px (`transform: rotateY(180deg)`).

### Implémentation Complète (TypeScript / Remotion)

```typescript
import React from 'react';
import { useCurrentFrame } from 'remotion';

const CARDS = [
  { id: '01 / 08', name: 'expo.out' },
  { id: '02 / 08', name: 'power4.inOut' },
  { id: '03 / 08', name: 'back.out(1.6)' },
  { id: '04 / 08', name: 'circ.inOut' },
  { id: '05 / 08', name: 'sine.inOut' },
  { id: '06 / 08', name: 'elastic.out' },
  { id: '07 / 08', name: 'steps(5)' },
  { id: '08 / 08', name: 'power2.in' },
];

export const Carousel3DScene: React.FC = () => {
  const frame = useCurrentFrame();

  // Rotation continue asservie au temps (Frames 270 à 360)
  const relFrame = Math.max(0, frame - 270);
  const rotY = relFrame * 2.2; // ~2.2 degrés par frame
  const RADIUS = 453; // Rayon théorique exact

  return (
    <div className="absolute inset-0 flex items-center justify-center overflow-hidden bg-[#EBE7DB]">
      {/* Filigrane d'arrière-plan DEPTH */}
      <div
        className="absolute top-[180px] text-[300px] font-black text-[#DFD9CC] tracking-widest select-none pointer-events-none"
        style={{ fontFamily: 'Inter Tight, system-ui, sans-serif' }}
      >
        DEPTH
      </div>

      {/* Conteneur de perspective 3D */}
      <div
        className="relative w-[375px] h-[500px]"
        style={{
          perspective: '1200px',
          perspectiveOrigin: '50% 45%',
        }}
      >
        {/* Cylindre rotatif */}
        <div
          className="w-full h-full relative"
          style={{
            transformStyle: 'preserve-3d',
            transform: `rotateX(-10deg) rotateY(${rotY}deg)`,
          }}
        >
          {CARDS.map((card, idx) => {
            const angle = idx * 45;
            return (
              <div
                key={idx}
                className="absolute inset-0"
                style={{
                  transformStyle: 'preserve-3d',
                  transform: `rotateY(${angle}deg) translateZ(${RADIUS}px)`,
                }}
              >
                {/* Face Avant (Blanche) */}
                <div
                  className="absolute inset-0 bg-[#FAF8F5] border-[3px] border-[#1C1917] rounded-sm p-6 flex flex-col justify-between font-mono"
                  style={{
                    backfaceVisibility: 'hidden',
                  }}
                >
                  <div className="text-[18px] font-bold text-[#1C1917]">{card.id}</div>
                  <div className="w-full h-[220px] border border-[#E5E0D5] relative flex items-center justify-center p-2">
                    {/* Schéma de courbe d'asservissement */}
                    <svg viewBox="0 0 100 100" className="w-full h-full overflow-visible">
                      <path
                        d="M 5 95 Q 20 20 95 10"
                        fill="none"
                        stroke="#C5593C"
                        strokeWidth={4}
                      />
                    </svg>
                  </div>
                  <div className="text-[22px] font-bold text-[#1C1917] tracking-tight">
                    {card.name}
                  </div>
                </div>

                {/* Face Arrière (Terracotta) */}
                <div
                  className="absolute inset-0 bg-[#C5593C] border-[3px] border-[#1C1917] rounded-sm"
                  style={{
                    backfaceVisibility: 'hidden',
                    transform: 'rotateY(180deg)',
                  }}
                />
              </div>
            );
          })}
        </div>
      </div>

      {/* Titre inférieur EASE IS EMOTION */}
      <div className="absolute bottom-[100px] text-[72px] font-black tracking-tight select-none">
        <span className="text-[#1C1917]">EASE IS </span>
        <span className="text-[#C5593C]">EMOTION.</span>
      </div>
    </div>
  );
};
```

---

## 5. Moteur 5 : Logo Assembler Claude & Moteur Dactylographique

Utilisé pour la discipline `05 / IDENTITY` (Frames 360 à 452).

### Principe Géométrique
1. **Géométrie de l'Astérisque Claude** :
   Composé de 6 branches à extrémités arrondies (`strokeLinecap: 'round'`) rayonnant depuis le centre $(0, 0)$ avec une épaisseur de trait $22px$ en couleur `#C5593C` :
   - Branche 1 (Horizontale gauche) : $0^\circ$, longueur $100px$.
   - Branche 2 (Supérieure gauche) : $135^\circ$, longueur $90px$.
   - Branche 3 (Verticale supérieure) : $90^\circ$, longueur $95px$.
   - Branche 4 (Supérieure droite) : $45^\circ$, longueur $75px$.
   - Branche 5 (Horizontale droite) : $0^\circ$, longueur $85px$.
   - Branche 6 (Inférieure) : $-90^\circ$, longueur $70px$.
2. **Animation d'Entrée & Translation** :
   - Frames 360 à 372 : Les 6 rayons convergent depuis un rayon initial $R = 300px$ vers le centre $(960, 430)$ avec `expo.out`.
   - Frames 373 à 388 : L'astérisque glisse horizontalement vers la gauche de $X = 960px$ à $X = 426px$ ($\Delta X = -534px$).
3. **Apparition Typographique "CLAUDE"** :
   - Révélation synchrone par masque rectangulaire horizontal de gauche à droite sur les frames 375 à 390.
4. **Machine à Écrire avec Curseur Clignotant** :
   - Chaîne cible : `"MOTION DESIGNER · REEL 2026"` (27 caractères).
   - Cadence : 1 caractère toutes les 2 frames sur les frames 395 à 422.
   - Curseur : Rectangle plein terracotta $20px \times 36px$, clignotant à 2 Hz (15 frames allumé, 15 frames éteint) après la saisie.

### Implémentation Complète (TypeScript / Remotion + SVG)

```typescript
import React from 'react';
import { useCurrentFrame } from 'remotion';

export const ClaudeIdentityScene: React.FC = () => {
  const frame = useCurrentFrame();

  // 1. Onde de choc circulaire radar (Frames 355 à 370)
  const waveProg = Math.min(1, Math.max(0, (frame - 355) / 20));
  const waveRadius = waveProg * 700;
  const waveOpacity = (1 - waveProg) * 0.45;

  // 2. Assemblage des branches de l'astérisque (Frames 360 à 372)
  const assembleProg = Math.min(1, Math.max(0, (frame - 360) / 12));
  const easeAssemble = assembleProg === 1 ? 1 : 1 - Math.pow(2, -10 * assembleProg);

  // 3. Glissement vers la gauche (Frames 373 à 390)
  const slideProg = Math.min(1, Math.max(0, (frame - 373) / 17));
  const easeSlide = slideProg === 1 ? 1 : 1 - Math.pow(2, -10 * slideProg);
  const asteriskX = 960 - 534 * easeSlide; // 960 -> 426

  // 4. Filet horizontal (Frames 390 à 405)
  const ruleProg = Math.min(1, Math.max(0, (frame - 390) / 15));

  // 5. Machine à écrire (Frames 395 à 422)
  const FULL_TEXT = 'MOTION DESIGNER · REEL 2026';
  const typeFrame = Math.max(0, frame - 395);
  const charsCount = Math.min(FULL_TEXT.length, Math.floor(typeFrame / 1.5));
  const visibleText = FULL_TEXT.slice(0, charsCount);
  const isTypingDone = charsCount === FULL_TEXT.length;
  const cursorBlink = isTypingDone ? Math.floor(frame / 15) % 2 === 0 : true;

  // 6. Tagline inférieure (Frames 420 à 440)
  const taglineOpacity = Math.min(1, Math.max(0, (frame - 420) / 20));

  return (
    <div className="absolute inset-0 bg-[#EBE7DB] select-none overflow-hidden">
      {/* Onde de choc circulaire */}
      {waveOpacity > 0.01 && (
        <svg className="absolute inset-0 w-full h-full pointer-events-none">
          <circle
            cx={960}
            cy={540}
            r={waveRadius}
            fill="none"
            stroke="#E0876E"
            strokeWidth={3}
            opacity={waveOpacity}
          />
        </svg>
      )}

      {/* Bloc Identité Central */}
      <div className="absolute inset-0 flex items-center justify-center">
        {/* Astérisque Claude Vectoriel */}
        <div
          className="absolute"
          style={{
            left: `${asteriskX}px`,
            top: '430px',
            transform: 'translate(-50%, -50%)',
          }}
        >
          <svg width={220} height={220} viewBox="-110 -110 220 220">
            {/* 6 Rayons vectoriels de l'astérisque Claude */}
            {[
              { angle: -90, len: 95 },
              { angle: -45, len: 80 },
              { angle: 0, len: 98 },
              { angle: 45, len: 75 },
              { angle: 90, len: 72 },
              { angle: 180, len: 95 },
            ].map((spoke, idx) => {
              const rad = (spoke.angle * Math.PI) / 180;
              const curLen = spoke.len * easeAssemble;
              const x2 = Math.cos(rad) * curLen;
              const y2 = Math.sin(rad) * curLen;
              return (
                <line
                  key={idx}
                  x1={0}
                  y1={0}
                  x2={x2}
                  y2={y2}
                  stroke="#C5593C"
                  strokeWidth={22}
                  strokeLinecap="round"
                />
              );
            })}
          </svg>
        </div>

        {/* Titre Monumental "CLAUDE" */}
        <div
          className="absolute left-[610px] top-[300px] overflow-hidden"
          style={{
            width: `${1007 * easeSlide}px`,
            height: '266px',
          }}
        >
          <div
            className="text-[266px] font-black text-[#1C1917] leading-none"
            style={{
              fontFamily: 'Inter Tight, system-ui, sans-serif',
              letterSpacing: '-0.03em',
            }}
          >
            CLAUDE
          </div>
        </div>

        {/* Filet horizontal terracotta */}
        <div
          className="absolute left-[610px] top-[580px] h-[6px] bg-[#C5593C]"
          style={{
            width: `${1007 * ruleProg}px`,
          }}
        />

        {/* Sous-titre Machine à Écrire */}
        <div className="absolute left-[610px] top-[610px] flex items-center font-mono">
          <span className="text-[36px] font-medium text-[#1C1917] tracking-[0.08em]">
            {visibleText}
          </span>
          {cursorBlink && (
            <span className="inline-block w-[20px] h-[36px] bg-[#C5593C] ml-2" />
          )}
        </div>
      </div>

      {/* Tagline Manifeste Inférieure */}
      <div
        className="absolute bottom-[160px] left-0 right-0 flex justify-center items-center gap-6 font-mono text-[22px] font-medium text-[#1C1917] tracking-[0.06em]"
        style={{ opacity: taglineOpacity }}
      >
        <span>450 FRAMES</span>
        <span className="text-[#C5593C] text-[18px]">◆</span>
        <span>5 DISCIPLINES</span>
        <span className="text-[#C5593C] text-[18px]">◆</span>
        <span>EVERY KEYFRAME WRITTEN IN CODE</span>
      </div>
    </div>
  );
};
```

---

## 6. Moteur 6 : Cadre HUD Viewfinder & Télémétrie Globale

Composant conteneur englobant toute la production (Niveau `Z-Index: 100`).

```typescript
import React from 'react';
import { useCurrentFrame } from 'remotion';

interface ViewfinderProps {
  disciplineNumber: string;
  disciplineTitle: string;
  disciplineProgress: number; // 0.0 à 1.0
}

export const ViewfinderOverlay: React.FC<ViewfinderProps> = ({
  disciplineNumber,
  disciplineTitle,
  disciplineProgress,
}) => {
  const frame = useCurrentFrame();

  // Formatage frame-accurate du Timecode (TC 00:00:SS:FF @ 30fps)
  const totalSeconds = Math.floor(frame / 30);
  const framesMod = frame % 30;
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  const pad = (n: number) => n.toString().padStart(2, '0');
  const timecodeString = `TC 00:${pad(minutes)}:${pad(seconds)}:${pad(framesMod)}`;

  // Position et dimensions des repères de cadrage
  const MARGIN = 40;
  const BRACKET_LEN = 20;
  const STROKE = 2;

  return (
    <div className="absolute inset-0 pointer-events-none font-mono select-none">
      {/* 1. Trame matricielle de points 48px */}
      <svg className="absolute inset-0 w-full h-full opacity-35">
        <defs>
          <pattern id="dotGrid" width={48} height={48} patternUnits="userSpaceOnUse">
            <circle cx={24} cy={24} r={1.5} fill="#C5C0B3" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#dotGrid)" />
      </svg>

      {/* 2. Cornières de visée HUD [ ] */}
      <svg className="absolute inset-0 w-full h-full">
        {/* Coin Supérieur Gauche ┌ */}
        <path
          d={`M ${MARGIN} ${MARGIN + BRACKET_LEN} L ${MARGIN} ${MARGIN} L ${MARGIN + BRACKET_LEN} ${MARGIN}`}
          fill="none"
          stroke="#1C1917"
          strokeWidth={STROKE}
        />
        {/* Coin Supérieur Droit ┐ */}
        <path
          d={`M ${1920 - MARGIN - BRACKET_LEN} ${MARGIN} L ${1920 - MARGIN} ${MARGIN} L ${1920 - MARGIN} ${MARGIN + BRACKET_LEN}`}
          fill="none"
          stroke="#1C1917"
          strokeWidth={STROKE}
        />
        {/* Coin Inférieur Gauche └ */}
        <path
          d={`M ${MARGIN} ${1080 - MARGIN - BRACKET_LEN} L ${MARGIN} ${1080 - MARGIN} L ${MARGIN + BRACKET_LEN} ${1080 - MARGIN}`}
          fill="none"
          stroke="#1C1917"
          strokeWidth={STROKE}
        />
        {/* Coin Inférieur Droit ┘ */}
        <path
          d={`M ${1920 - MARGIN - BRACKET_LEN} ${1080 - MARGIN} L ${1920 - MARGIN} ${1080 - MARGIN} L ${1920 - MARGIN} ${1080 - MARGIN - BRACKET_LEN}`}
          fill="none"
          stroke="#1C1917"
          strokeWidth={STROKE}
        />
      </svg>

      {/* 3. Bandeau Supérieur */}
      <div className="absolute top-[64px] left-[70px] flex items-center gap-2 text-[16px] font-medium text-[#1C1917] tracking-wider">
        <span className="w-2.5 h-2.5 rounded-full bg-[#1C1917] inline-block" />
        <span>CLAUDE / MOTION REEL '26</span>
      </div>
      <div className="absolute top-[64px] right-[70px] text-[16px] font-medium text-[#1C1917] tracking-wider">
        {timecodeString}
      </div>

      {/* 4. Bandeau Inférieur */}
      <div className="absolute bottom-[72px] left-[70px] text-[16px] font-medium text-[#1C1917] tracking-wider uppercase">
        {disciplineNumber} / {disciplineTitle}
      </div>
      <div className="absolute bottom-[72px] right-[70px] text-[16px] font-medium text-[#1C1917] tracking-wider">
        1920×1080 · 30 FPS
      </div>

      {/* 5. Ligne de Sol & Barre de Progression */}
      <div className="absolute bottom-[50px] left-[40px] right-[40px] h-[1px] bg-[rgba(28,25,23,0.20)]">
        <div
          className="h-[3px] bg-[#1C1917] -mt-[1px] transition-all duration-75"
          style={{
            width: `${Math.min(100, Math.max(0, disciplineProgress * 100))}%`,
          }}
        />
      </div>
    </div>
  );
};
```
